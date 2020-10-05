""""
BSD Licence Copyright (c) 2016, Science & Technology Facilities Council (STFC)
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

    * Redistributions of source code must retain the above copyright notice,
    this list of conditions and the following disclaimer.

    * Redistributions in binary form must reproduce the above copyright notice,
    this list of conditions and the following disclaimer in the documentation
    and/or other materials provided with the distribution.

    * Neither the name of the Science & Technology Facilities Council (STFC)
    nor the names of its contributors may be used to endorse or promote
    products derived from this software without specific prior written
    permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON
ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""

import datetime
import logging

from elasticsearch.exceptions import ConnectionError, TransportError
from elasticsearch_dsl import Search

from ceda_opensearch.errors import Http400, Http503
from ceda_opensearch.helper import get_index, import_count_and_page
from ceda_opensearch.middleware import CedaOpensearchMiddleware
from ceda_opensearch.settings import ELASTIC_INDEX


LOGGING = logging.getLogger(__name__)

# N.B. bbox, geometry, minCloudCoverPercentage, maxCloudCoverPercentage,
# startDate and endDate have been left out on purpose, there are separate calls
# to get the bbox filter, geometry filter, cloud filter and temporal filter
SEARCH_TERMS = {
    'uid': 'misc.product_info.Name',
    'dataFormat': 'data_format.format',
    'dataOnline': 'file.location',
    'instrument': 'misc.platform.Instrument Abbreviation',
    'mission': 'misc.platform.Mission',
    'name': 'misc.product_info.Name',
    'platform': 'misc.platform.Satellite',
    'polarisationChannels': 'misc.product_info.Polarisation',
    'productType': 'misc.product_info.Product Type',
    'orbitDirection': 'misc.orbit_info.Pass Direction',
    'orbitNumber': 'misc.orbit_info.Start Orbit Number',
    'relativeOrbitNumber': 'misc.orbit_info.Start Relative Orbit Number',
    'resolution': 'misc.product_info.Resolution',
    'sensorMode': ['misc.product_info.Datatake Type',
                   'misc.platform.Instrument Mode'],
}


def get_search_results(context):
    """
    Get the search results based on the query_attr.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @return a tuple containing an attribute list, a count of total results, and results relation.
    The relation is needed because elasticsearch does not calculate the true count if there are
    > 10k results.

    """
    LOGGING.debug("get_search_results(context)")
    client = CedaOpensearchMiddleware.get_elasticsearch()
    elastic_search = Search(using=client)

    bool_query = {}
    must_list = _get_must_list(context)
    if must_list:
        bool_query['must'] = must_list

    should_list = _get_should_list(context)
    if should_list:
        for should in should_list:
            # N.B. This will only work when there is one attribute with a
            # should (sensorMode)
            bool_query['should'] = should
            bool_query["minimum_should_match"] = 1

    filter_list = _get_filter_list(context)
    if filter_list:
        bool_query['filter'] = filter_list

    query_dict = {'query': {'bool': bool_query}}
    elastic_search = elastic_search.from_dict(query_dict)
    elastic_search = elastic_search.sort(
        {'temporal.start_time': {'order': 'desc'}})

    count, start_index, start_page = import_count_and_page(context)
    first_result = _get_offset(count, start_index, start_page)
    last_result = first_result + count
    if last_result < 0:
        last_result = 0
    if first_result < 0:
        first_result = 0

    # Elastic search will only let you page through the first 10,000 results
    if last_result > 10000:
        raise Http400("This server is currently only able to page through the "
                      "first 10,000 results. You could try additional "
                      "constraints on the query.")

    elastic_search = elastic_search[first_result:last_result]
    elastic_search = elastic_search.extra(explain=True)
    elastic_search = elastic_search.index(ELASTIC_INDEX)

    try:
        response = elastic_search.execute()
    except ConnectionError:
        LOGGING.error("ConnectionError while connecting to the elastic search "
                      "service")
        raise Http503("Error while connecting to the elastic search service")
    except TransportError as ex:
        if 'invalid_shape_exception' in str(ex):
            msg = str(ex).split('invalid_shape_exception: ')[1].split("'")[0]
            raise Http400(msg)
        LOGGING.error("TransportError while connecting to the elastic search "
                      "service. {}".format(ex))
        raise (ex)

    LOGGING.debug("get_search_results returning %s hits out of %s (%s)",
                  len(response.hits), response.hits.total.value, response.hits.total.relation)

    return response.hits, response.hits.total.value, {'gte':'>=', 'lte': '<='}.get(response.hits.total.relation, '')


def _get_offset(count, index, page):
    """
    Get the offset of the first result to return.

    An offset of zero should return the first result.

    @param count (int): the number of search results per page desired
    @param index (int): the index of the first search result desired
    @param page (int): the page number of the set of search results desired

    @return an int containing the offset of the first result to return

    """
    return get_index(count, index, page) - 1


def _get_must_list(context):
    """
    Construct a list of queries based on the values in the context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a list of strings containing queries

    """
    query_list = []
    for key in SEARCH_TERMS.keys():
        attr = context.get(key)
        if attr:
            if key == 'dataOnline':
                if attr.upper() == 'TRUE':
                    attr = 'on_disk'
                elif attr.upper() == 'FALSE':
                    attr = 'on_tape'
            if type(SEARCH_TERMS[key]) == str:
                query_list.append({"match_phrase":
                                   {SEARCH_TERMS[key]: attr}
                                   })
    return query_list


def _get_should_list(context):
    """
    Construct a list of queries based on the values in the context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a list of strings containing queries

    """
    query_list = []
    for key in SEARCH_TERMS.keys():
        attr = context.get(key)
        if attr:
            if type(SEARCH_TERMS[key]) == list:
                should_list = []
                for term in SEARCH_TERMS[key]:
                    should_list.append({"match_phrase":
                                        {term: attr}
                                        })
                query_list.append(should_list)

    return query_list


def _get_filter_list(context):
    """
    Construct a list of filters based on the values in the context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a list of strings containing queries

    """
    filter_list = []
    bbox = _get_bbox_query(context)
    if bbox:
        filter_list.append(bbox)
    geometry = _get_geo_query(context)
    if geometry:
        filter_list.append(geometry)
    filter_list.extend(_temporal_query(context))
    filter_list.extend(_cloud_query(context))
    return filter_list


def _cloud_query(context):
    """
    Construct a query based on the minCloudCoverPercentage and
    maxCloudCoverPercentage values in the context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a string containing a cloud query

    """
    query_list = []
    min_cloud = context.get('minCloudCoverPercentage')
    max_cloud = context.get('maxCloudCoverPercentage')
    if min_cloud is not None and max_cloud is not None:
        query_list.append(
            {"range":
             {"misc.quality_info.Cloud Coverage Assessment":
              {"gte": float(min_cloud), "lte": float(max_cloud)}
              }})
    elif min_cloud is not None:
        query_list.append(
            {"range":
             {"misc.quality_info.Cloud Coverage Assessment":
              {"gte": float(min_cloud)}
              }})
    elif max_cloud is not None:
        query_list.append(
            {"range":
             {"misc.quality_info.Cloud Coverage Assessment":
              {"lte": float(max_cloud)}
              }})
    return query_list


def _get_bbox_query(context):
    """
    Construct a query for a bbox based on the values in the context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a string containing a query for a bbox

    """
    bbox = context.get('bbox')
    if bbox is None:
        return None
    try:
        west, south, east, north = bbox.split(',')
    except ValueError:
        LOGGING.debug("bbox values not west, south, east, north. {}".
                      format(bbox))
        return None
    query = {"geo_shape":
             {"spatial.geometries.search":
              {"shape":
               {"type": "envelope",
                "coordinates": [[int(west), int(south)],
                                [int(east), int(north)]]}
               }}}
    return query


def _get_geo_query(context):
    """
    Construct a query for a geometry based on the values in the context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a string containing a query for a geometry

    """
    geometry = context.get('geometry')
    if geometry is None:
        return None
    geometry = geometry.upper()
    if not geometry.startswith('POLYGON'):
        raise Http400("Invalid geometry, it must be a POLYGON")
    try:
        rings = (geometry.split('POLYGON')[1].strip().split('('))
        outer_ring = rings[2].split(')')[0]
        if len(rings) > 3:
            inner_ring = rings[3].split(')')[0]
        else:
            inner_ring = None
    except (ValueError, IndexError):
        raise Http400("Invalid polygon WKT format, {}".format(geometry))
    polygon = []
    polygon.append(get_coordinate_list(outer_ring))
    if inner_ring is not None:
        polygon.append(get_coordinate_list(inner_ring))
    query = {"geo_shape":
             {"spatial.geometries.search":
              {"shape":
               {"type": "polygon", "coordinates": polygon}
               }}}
    return query


def get_coordinate_list(coordinates):
    coordinate_list = []
    points = coordinates.split(',')
    if len(points) < 4:
        raise Http400("Invalid polygon WKT format, number of points in a ring "
                      "must be >= 4")
    for point in points:
        point = point.strip()
        try:
            long, lat = point.split(" ")
        except ValueError:
            raise Http400("Invalid polygon WKT format")
        coordinate_list.append([float(long), float(lat)])
    return coordinate_list


def _temporal_query(context):
    """
    Construct a temporal query based on the startDate and endDate values in the
    context.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns a string containing a temporal query

    """
    query_list = []
    start_date = context.get('startDate')
    if start_date is not None:
        query_list.append(
            {"range":
             {"temporal.end_time":
              {"gte": start_date}
              }})

    end_date = context.get('endDate')
    if end_date is not None:
        next_day = _validate_date(end_date)
        if next_day is not None:
            query_list.append(
                {"range":
                 {"temporal.start_time":
                  {"lt": next_day}
                  }})
        else:
            query_list.append(
                {"range":
                 {"temporal.start_time":
                  {"lte": end_date}
                  }})
    return query_list


def _validate_date(user_date):
    """
    Validate the date against RFC-3339.

    If the given date is of the format %Y-%m-%d then return the date of the
    next day. Otherwise return None.

    @param user_date(str)

    @return a str containing the next day in the format %Y-%m-%d or None

    """
    next_day = _get_next_day(user_date)
    if next_day is not None:
        return next_day

    # validate against other formats
    date_formats = [
        "%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%S.%f", "%Y-%m-%dT%H:%M:%SZ",
        "%Y-%m-%dT%H:%M:%S"]
    date_ok = False

    for date_format in date_formats:
        try:
            datetime.datetime.strptime(user_date, date_format)
            date_ok = True
            break
        except ValueError:
            pass

    if not date_ok:
        raise Http400("Invalid date format")
    return None


def _get_next_day(user_date):
    """
    If the given date is of the format %Y-%m-%d then return the date of the
    next day.

    @param user_date(str)

    @return a str containing the next day in the format %Y-%m-%d or None

    """
    try:
        date_ok = datetime.datetime.strptime(user_date, "%Y-%m-%d")
    except ValueError:
        return None

    day = datetime.timedelta(days=1)
    next_day = date_ok + day
    return datetime.datetime.strftime(next_day, "%Y-%m-%d")
