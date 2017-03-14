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
import os

from ceda_markup.atom.atom import ATOM_NAMESPACE, ATOM_PREFIX, createID, \
    createUpdated, createPublished, createEntry, createLink
from ceda_markup.atom.info import createTitle, TEXT_TYPE
from ceda_markup.markup import createMarkup, createSimpleMarkup
from ceda_markup.opensearch import OSAtomResponse, OSJsonResponse, OSParam, \
    OSQuery, Result, OS_NAMESPACE, Person
from ceda_opensearch.constants import CEDA_NAMESPACE, EO_NAMESPACE, \
    GEO_NAMESPACE, DCT_NAMESPACE, CEDA_PREFIX, EO_PREFIX, \
    GEO_PREFIX, DCT_PREFIX, TIME_NAMESPACE, TIME_PREFIX, OS_PATH, \
    COUNT_DEFAULT, PARAM_PREFIX, PARAM_NAMESPACE
from ceda_opensearch.elastic_search import get_search_results
from ceda_opensearch.helper import get_index, get_mime_type, \
    import_count_and_page, urljoin_path
from ceda_opensearch.settings import ELASTIC_INDEX, FTP_SERVER, PYDAP_SERVER


LOGGING = logging.getLogger(__name__)


class COSAtomResponse(OSAtomResponse):
    """
    This class extends an OSAtomResponse class.

    It implements the two abstract methods generate_entries and generate_url
    from OSAtomResponse. It also implements the abstract method
    digest_search_results from OSEngineResponse.

    Work flow:
        digest_search_results
        generate_url
        generate_entries

    """

    def __init__(self):
        """
        Constructor.

        """
        super(COSAtomResponse, self).__init__()

    def digest_search_results(self, results, context):
        """
        Create a Result object.

        Overrides abstract method from OSEngineResponse.

        @param results (dict): a dict with keys:
                            'results': a list of json objects
                            'total_count': the total number of possible results
        @param context (dict): the query parameters from the users request plus
            defaults from the OSQuery. This only contains parameters for
            registered OSParams.

        @result an opensearch Result

        """
        LOGGING.debug(
            "COSAtomResponse:digest_search_results(results, context)")
        title = "Catalogue Search Feed for %s" % ELASTIC_INDEX
        count, start_index, start_page = import_count_and_page(context)
        index = get_index(count, start_index, start_page)
        subtitle = self._get_subtitle(
            index, len(results['results']), results['total_count'], context)
        authors = [Person("CEDA")]
        return Result(count, index, start_page, results['total_count'],
                      subresult=results['results'], title=title,
                      subtitle=subtitle, authors=authors)

    def generate_entries(self, atomroot, subresults, url):
        """
        Construct an XML element containing the subresults.

        This method overrides the abstract method from OSAtomResponse.

        @param atomroot (ElementTree.Element): the root tag of the document
                containing this element
        @param subresults (list): a list of json objects
        @param url (str): a URL including path

        @return an ElementTree.Element containing the atom entries

        """
        LOGGING.debug("COSAtomResponse:generate_entries(atomroot, subresults)")
        if subresults is None:
            return

        entries = []
        for subresult in subresults:
            _id = '%s?uid=%s' % (url, subresult.meta.id)
            atom_id = createID(_id, root=atomroot)

            try:
                title = subresult.misc.product_info[
                    'Product Class Description']
            except (AttributeError, KeyError):
                title = subresult.meta.id
            ititle = createTitle(root=atomroot, body=title, itype=TEXT_TYPE)
            atom_content = None
            time_doc = datetime.datetime.now().isoformat()
            atom_updated = createUpdated(time_doc,
                                         root=atomroot)
            atom_published = createPublished(time_doc,
                                             root=atomroot)
            entry = createEntry(atom_id, ititle, atom_updated,
                                published=atom_published,
                                content=atom_content, root=atomroot)
            entry.append(
                createSimpleMarkup(subresult.meta.id, atomroot, 'identifier',
                                   DCT_NAMESPACE, DCT_PREFIX))
            date_str = '{start}Z/{end}Z'.format(
                start=subresult.temporal.start_time,
                end=subresult.temporal.end_time)

            entry.append(createSimpleMarkup(date_str, atomroot, 'date',
                                            DCT_NAMESPACE, DCT_PREFIX))

            resource_url = url.replace('/{}/'.format(OS_PATH), '/resource/')

            gml_url = resource_url.replace('/atom', '/gml')
            gml_uri = '%s?uid=%s' % (gml_url, subresult.meta.id)
            entry.append(createLink(gml_uri, 'alternate',
                                    get_mime_type('gml'), atomroot))

            json_url = resource_url.replace('atom', 'json')
            json_uri = '%s?uid=%s' % (json_url, subresult.meta.id)
            entry.append(createLink(json_uri, 'alternate',
                                    get_mime_type('json'), atomroot))

            directory = subresult.file.directory

            # data files
            if subresult.file.location == "on_disk":
                self._add_data_files(subresult, directory, atomroot, entry)

            # metadata
            file_name = subresult.file.metadata_file
            self._add_file_links(file_name, directory, atomroot, entry, 'via')

            # add quick look
            try:
                file_name = subresult.file.quicklook_file
                if file_name != "":
                    self._add_file_links(file_name, directory, atomroot, entry,
                                         'icon')
            except AttributeError:
                # no quick look
                pass

            entries.append(entry)

        for entry in entries:
            atomroot.append(entry)

    def _add_data_files(self, subresult, directory, atomroot, entry):
        """
        Update the 'entry' with links to the data file(s).

        """
        try:
            # check for multiple data files
            file_names = subresult.file.data_files.split(',')
            for file_name in file_names:
                self._add_file_links(file_name, directory, atomroot, entry,
                                     'section')
        except AttributeError:
            # no multiple data files, so add data file, but
            file_name = subresult.file.data_file
            self._add_file_links(file_name, directory, atomroot, entry,
                                 'enclosure')

    def _add_file_links(self, file_name, directory, atomroot, entry,
                        atom_type):
        """
        Update the 'entry' with links to a file.

        """
        full_path = os.path.join(directory, file_name)
        file_type = file_name.split('.')[-1].lower()
        try:
            mime_type = get_mime_type(file_type)
        except KeyError:
            LOGGING.warn(
                'Unable to discover mime type for {}'.
                format(file_type))
            mime_type = None

        # add data links
        data_url = urljoin_path(FTP_SERVER, full_path)
        link = createLink(data_url, atom_type, mime_type, atomroot)
        link.set('title', 'ftp')
        entry.append(link)
        data_url = urljoin_path(PYDAP_SERVER, full_path)
        link = createLink(data_url, atom_type, mime_type, atomroot)
        link.set('title', 'pydap')
        entry.append(link)

    def generate_url(self, os_host_url, context):
        """
        Returns the URL used to assemble the OSResponse links.

        Overrides abstract method from OSAtomResponse.

        @param os_host_url (str): the URL of the opensearch host
        @param context (dict): the query parameters from the users request plus
            defaults from the OSQuery. This only contains parameters for
            registered OSParams.

        @return a URL including path

        """
        LOGGING.debug("COSAtomResponse:generate_url(%s, context)",
                      str(os_host_url))
        return "%s/%s" % (os_host_url, OS_PATH)

    def _get_subtitle(self, index, result_count, total_count, context):
        """
        Create the HTML containing a subtitle for the ATOM feed.

        @param index (int): the index of the first search result desired
        @param result_count (int): the number of results returned
        @param total_count (int): the total number of possible results
        @param context (dict): the query parameters from the users request plus
            defaults from the OSQuery. This only contains parameters for
            registered OSParams.

        @return a string containing the subtitle

        """
        subtitle = 'Found %s results.' % total_count
        if total_count > 0:
            if index < 2:
                if result_count == 1:
                    subtitle = '%s Showing the first %s result' % (
                        subtitle, result_count)
                else:
                    subtitle = '%s Showing the first %s results' % (
                        subtitle, result_count)
            else:
                subtitle = '%s Showing from %s to %s' % (
                    subtitle, (index), (result_count + index - 1))
        first = True
        params = ""
        for key in context.keys():
            if context[key] != None:
                if not first:
                    params = '%s,' % params
                else:
                    first = False
                params = '%s%s=%s' % (params, key, context[key])
        subtitle = '%s <br/>Query Parameters used %s <br/>' % (
            subtitle, params)
        return subtitle


class COSJsonResponse(OSJsonResponse):
    """
    This class extends an OSJsonResponse class.

    It implements the abstract method from OSJsonResponse, generate_rows. It
    also implements the abstract method digest_search_results from
    OSEngineResponse.

    """

    def __init__(self):
        """
        Constructor.

        """
        super(COSJsonResponse, self).__init__()

    def digest_search_results(self, results, context):
        """
        Create a Result object.

        Overrides abstract method from OSEngineResponse.

        @param results (dict): a dict with keys:
                            'results': a list of json objects
                            'total_count': the total number of possible results
        @param context (dict): the query parameters from the users request plus
            defaults from the OSQuery. This only contains parameters for
            registered OSParams.

        @result an opensearch Result

        """
        LOGGING.debug("COSJsonResponse:digest_search_results(results, "
                      "context)")
        title = "Catalogue Search Feed for %s" % ELASTIC_INDEX
        count, start_index, start_page = import_count_and_page(context)
        index = get_index(count, start_index, start_page)
        subresults = results['results']
        return Result(count, index, start_page, results['total_count'],
                      subresult=subresults, title=title)

    def generate_rows(self, subresults):
        """
        Construct a list containing json serializable objects from the
        subresults.

        Overrides abstract method from OSJsonResponse.

        @param subresults (list): a list of json objects

        @return a list containing the json results

        """

        subresult_list = []
        for subresult in subresults:
            subresult_list.append(subresult.to_dict())

        return subresult_list


class COSQuery(OSQuery):
    """
    This class extends the OSQuery class.

    It implements the abstract method do_search from OSQuery.

    """

    def __init__(self):
        """
        Constructor.

        """
        params = []
        params.append(OSParam("maximumRecords", "count",
                              namespace=OS_NAMESPACE,
                              default=str(COUNT_DEFAULT)))
        params.append(OSParam("startPage", "startPage", namespace=OS_NAMESPACE,
                              default=''))
        params.append(OSParam("startRecord", "startIndex",
                              namespace=OS_NAMESPACE, default=''))
        params.append(OSParam("q", "searchTerms", namespace=OS_NAMESPACE,
                              default=''))
        params.append(OSParam("uid", "uid", namespace=GEO_NAMESPACE,
                              namespace_prefix=GEO_PREFIX, default=''))
        params.append(OSParam("bbox", "box", namespace=GEO_NAMESPACE,
                              namespace_prefix=GEO_PREFIX, default=''))
        params.append(OSParam("geometry", "geometry", namespace=GEO_NAMESPACE,
                              namespace_prefix=GEO_PREFIX, default=''))
        params.append(OSParam("startDate", "start", namespace=TIME_NAMESPACE,
                              namespace_prefix=TIME_PREFIX, default=''))
        params.append(OSParam("endDate", "end",  namespace=TIME_NAMESPACE,
                              namespace_prefix=TIME_PREFIX, default=''))
        params.append(OSParam("dataFormat", "dataFormat",
                              namespace=CEDA_NAMESPACE,
                              namespace_prefix=CEDA_PREFIX, default=''))
        params.append(OSParam("dataOnline", "dataOnline",
                              namespace=CEDA_NAMESPACE,
                              namespace_prefix=CEDA_PREFIX, default=''))
        params.append(OSParam("instrument", "instrument",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX,
                              default=''))
        params.append(OSParam("minCloudCoverPercentage",
                              "cloudCover", namespace=EO_PREFIX,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("maxCloudCoverPercentage",
                              "cloudCover", namespace=EO_PREFIX,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("mission", "mission",
                              namespace=CEDA_NAMESPACE,
                              namespace_prefix=CEDA_PREFIX,
                              default=''))
        params.append(OSParam("name", "name",
                              namespace=CEDA_NAMESPACE,
                              namespace_prefix=CEDA_PREFIX,
                              default=''))
        params.append(OSParam("platform", "platform",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX,
                              default=''))
        params.append(OSParam("polarisationChannels", "polarisationChannels",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("productType", "productType",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("resolution", "resolution",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("orbitDirection", "orbitDirection",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("orbitNumber", "orbitNumber",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX, default=''))
        params.append(OSParam("sensorMode", "sensorMode",
                              namespace=EO_NAMESPACE,
                              namespace_prefix=EO_PREFIX, default=''))

        self._query_signature = self._get_query_signature(params)
        super(COSQuery, self).__init__(params)

    def do_search(self, query, context):
        """
        Search based on parameters in the context.

        Overrides abstract method from OSQuery.

        @param query: query in xml format
        @param context (dict): the query parameters from the users request plus
            defaults from the OSQuery. This only contains parameters for
            registered OSParams.
        @return a dict with keys:
                    'results': a list of json objects
                    'total_count': the total number of possible results

        """
        LOGGING.debug("do_search(query, context)")
        results, total_results = get_search_results(context)
        return {'results': results, 'total_count': total_results}

    def _get_query_signature(self, params_model):
        """
        Get the list of params.

        """
        _params = []
        for params in params_model:
            if params.par_name not in ['maximumRecords', 'startPage',
                                       'startRecord']:
                _params.append(params.par_name)
        return _params

    def add_parameter_markup(self, root):
        """
        Add the parameter markup.

        @param root: the root tag of the document containing this element

        """
        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "maximumRecords")
        markup.set("maxInclusive", "50")
        markup.set("minInclusive", "0")
        markup.set("pattern", "[0-9]+")
        markup.set("value", "{count}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "startRecord")
        markup.set("minInclusive", "1")
        markup.set("pattern", "[0-9]+")
        markup.set("value", "{startIndex}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "startPage")
        markup.set("minInclusive", "1")
        markup.set("pattern", "[0-9]+")
        markup.set("value", "{startPage}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "dataOnline")
        markup.set("value", "{ceda:dataOnline}")
        root.append(markup)
        dataOnline = ['true', 'false']
        for status in dataOnline:
            option = createMarkup(
                'Option', PARAM_PREFIX, PARAM_NAMESPACE, root)
            option.set("label", status)
            option.set("value", status)
            markup.append(option)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "geometry")
        markup.set("minimum", "0")
        markup.set("title", "inventory which has a spatial extent overlapping "
                   "this geometry")
        markup.set("value", "{geo:geometry}")
        root.append(markup)
        atom = createMarkup('link', ATOM_PREFIX, ATOM_NAMESPACE, root)
        atom.set("rel", "profile")
        atom.set("href", "http://www.opengis.net/wkt/POLYGON")
        atom.set("title", "This service accepts WKT Polygons")
        markup.append(atom)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "minCloudCoverPercentage")
        markup.set("maxInclusive", "100")
        markup.set("minInclusive", "0")
        markup.set("pattern", "[0-9]+")
        markup.set("value", "{opt:cloudCoverPercentage}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "maxCloudCoverPercentage")
        markup.set("maxInclusive", "100")
        markup.set("minInclusive", "0")
        markup.set("pattern", "[0-9]+")
        markup.set("value", "{opt:cloudCoverPercentage}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "startDate")
        markup.set("pattern", "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:"
                   "[0-9]{2}(\.[0-9]+)?(Z|[\+\-][0-9]{2}:[0-9]{2})$")
        markup.set("value", "{time:start}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "endDate")
        markup.set("pattern", "^[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:"
                   "[0-9]{2}(\.[0-9]+)?(Z|[\+\-][0-9]{2}:[0-9]{2})$")
        markup.set("value", "{time:end}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "mission")
        markup.set("value", "{eo:mission}")
        root.append(markup)
        missions = ['Landsat', 'Sentinel-1', 'Sentinel-2']
        for mission in missions:
            option = createMarkup(
                'Option', PARAM_PREFIX, PARAM_NAMESPACE, root)
            option.set("label", mission)
            option.set("value", mission)
            markup.append(option)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "platform")
        markup.set("value", "{eo:plarform}")
        root.append(markup)
        platforms = ['Landsat-5', 'Landsat-7', 'Landsat-8', 'Sentinel-1A',
                     'Sentinel-2A']
        for platform in platforms:
            option = createMarkup(
                'Option', PARAM_PREFIX, PARAM_NAMESPACE, root)
            option.set("label", platform)
            option.set("value", platform)
            markup.append(option)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "orbitDirection")
        markup.set("value", "{eo:orbitDirection}")
        root.append(markup)
        directions = ['ascending', 'descending']
        for direction in directions:
            option = createMarkup(
                'Option', PARAM_PREFIX, PARAM_NAMESPACE, root)
            option.set("label", direction)
            option.set("value", direction)
            markup.append(option)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "orbitNumber")
        markup.set("pattern", "(\[|\])[0-9]+,[0-9]+(\[|\])|(\[|\])?[0-9]+|[0-9"
                   "]+(\[|\])?|\{[0-9]+,[0-9]+\}")
        markup.set("value", "{eo:orbitNumber}")
        root.append(markup)

        markup = createMarkup(
            'Parameter', PARAM_PREFIX, PARAM_NAMESPACE, root)
        markup.set("name", "polarisationChannels")
        markup.set("value", "{eo:polarisationChannels}")
        root.append(markup)
        polarisations = ['HH', 'HV', 'VH', 'VV', 'HH,VV', 'HH,VH', 'HH,HV',
                         'VH,VV', 'VH,HV', 'VV,HV', 'VV,VH', 'HV,VH',
                         'UNDEFINED']
        for polar in polarisations:
            option = createMarkup(
                'Option', PARAM_PREFIX, PARAM_NAMESPACE, root)
            option.set("label", polar)
            option.set("value", polar)
            markup.append(option)
