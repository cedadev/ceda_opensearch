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

import json
import logging
import os
from xml.dom import minidom
from xml.etree.ElementTree import tostring

from ceda_markup.markup import createMarkup, createSimpleMarkup
from ceda_opensearch.constants import EOP_PREFIX, EOP_NAMESPACE, OM_PREFIX,\
    OM_NAMESPACE, XLINK_PREFIX, XLINK_NAMESPACE, OWS_PREFIX, OWS_NAMESPACE,\
    XSI_PREFIX, SCHEMA_LOCATION, XSI_NAMESPACE, GML_PREFIX, GML_NAMESPACE,\
    SAR_NAMESPACE, SAR_PREFIX
from ceda_opensearch.elastic_search import get_search_results
from ceda_opensearch.helper import urljoin_path
from ceda_opensearch.settings import FTP_SERVER, PYDAP_SERVER


LOGGING = logging.getLogger(__name__)

next_id = 0
poly_count = 10000


def get_resource(request, iformat):
    """
    Get the resource formated according to the value of iformat.

    @param request: a HTTP request
    @param iformat: the requested format of data

    """
    if iformat == 'json':
        return _get_json(request)
    return _get_xml(request)


def _get_json(request):
    """
    Get the results as json.

    @param request: a HTTP request

    """
    results, _ = get_search_results({'uid': request.GET.get('uid')})
    jsondoc = results.pop().to_dict()
    return json.dumps(jsondoc, indent=4, separators=(',', ': '))


def _get_xml(request):
    """
    Get the results as xml.

    @param request: a HTTP request

    """
    global next_id, poly_count
    next_id = 0
    poly_count = 10000
    results, _ = get_search_results({'uid': request.GET.get('uid')})
    result = results[0]
    root = createMarkup('EarthObservation', EOP_PREFIX, EOP_NAMESPACE, None)
    root.set('xmlns:{}'.format(XSI_PREFIX), XSI_NAMESPACE)
    root.set('{}:schemaLocation'.format(XSI_PREFIX), SCHEMA_LOCATION)
    root.set('{}:id'.format(GML_PREFIX), _get_id())

    _add_phenomenonTime(root, result)
    _add_resultTime(root, result)
    _add_procedure(root, result)
    _add_observedProperty(root, result)
    _add_featureOfInterest(root, result)
    _add_result(root, result)
    _add_metaDataProperty(root, result)
    xml = ('<?xml version="1.0" encoding="utf-8"?>%s' %
           tostring(root, encoding='unicode'))

    reparsed = minidom.parseString(xml)
    return reparsed.toprettyxml()


def _add_phenomenonTime(root, result):
    start_time = None
    end_time = None
    try:
        start_time = str(result.temporal.start_time)
    except AttributeError:
        LOGGING.debug('start_time not found')
    try:
        end_time = str(result.temporal.end_time)
    except AttributeError:
        LOGGING.debug('end_time not found')
    if start_time is None and end_time is None:
        return

    phenomenonTime = createMarkup(
        'phenomenonTime', OM_PREFIX, OM_NAMESPACE, root)
    root.append(phenomenonTime)

    TimePeriod = createMarkup('TimePeriod', GML_PREFIX, GML_NAMESPACE, root)
    TimePeriod.set('{}:id'.format(GML_PREFIX), _get_id())
    phenomenonTime.append(TimePeriod)

    if start_time is not None:
        beginPosition = createSimpleMarkup(
            start_time, root, 'beginPosition', GML_NAMESPACE, GML_PREFIX)
        TimePeriod.append(beginPosition)

    if end_time is not None:
        endPosition = createSimpleMarkup(
            end_time, root, 'endPosition', GML_NAMESPACE, GML_PREFIX)
        TimePeriod.append(endPosition)


def _add_resultTime(root, result):
    resultTime = createMarkup(
        'resultTime', OM_PREFIX, OM_NAMESPACE, root)
    root.append(resultTime)


def _add_observedProperty(root, result):
    observedProperty = createMarkup(
        'observedProperty', OM_PREFIX, OM_NAMESPACE, root)
    observedProperty.set('nilReason', 'inapplicable')
    root.append(observedProperty)


def _add_featureOfInterest(root, result):
    try:
        search = result.spatial.geometries.display
    except AttributeError:
        LOGGING.debug('spatial.geometries.display not found')
        return
    featureOfInterest = createMarkup(
        'featureOfInterest', OM_PREFIX, OM_NAMESPACE, root)
    root.append(featureOfInterest)

    Footprint = createMarkup(
        'Footprint', EOP_PREFIX, EOP_NAMESPACE, root)
    Footprint.set('{}:id'.format(GML_PREFIX), _get_id())
    featureOfInterest.append(Footprint)

    multiExtentOf = createMarkup(
        'multiExtentOf', EOP_PREFIX, EOP_NAMESPACE, root)
    Footprint.append(multiExtentOf)

    MultiSurface = createMarkup(
        'MultiSurface', GML_PREFIX, GML_NAMESPACE, root)
    MultiSurface.set('{}:id'.format(GML_PREFIX), _get_id())
#     MultiSurface.set('{}:srsName'.format(GML_PREFIX), 'EPSG:4326')
    multiExtentOf.append(MultiSurface)

    surfaceMembers = createMarkup(
        'surfaceMembers', GML_PREFIX, GML_NAMESPACE, root)
    MultiSurface.append(surfaceMembers)

    if search.type == 'polygon':
        _add_polygon(root, surfaceMembers, search.coordinates)
    elif search.type == 'MultiPolygon':
        _add_multi_polygon(root, surfaceMembers, search.coordinates)
    elif search.type == 'LineString':
        _add_line_string(root, surfaceMembers, search.coordinates)
    else:
        LOGGING.error('geometry type {}, found in result, is not currently '
                      'supported'.format(search.type))


def _add_polygon(root, parent, result):
    global poly_count
    for polygon in result:
        exterior_pos_list = _get_pos_list(polygon)
        poly_count = poly_count + 1
        poly_id = 'POLN{}'.format(poly_count)
        Polygon = createMarkup(
            'Polygon', GML_PREFIX, GML_NAMESPACE, root)
        Polygon.set('{}:id'.format(GML_PREFIX), poly_id)
        parent.append(Polygon)

        exterior = createMarkup(
            'exterior', GML_PREFIX, GML_NAMESPACE, root)
        Polygon.append(exterior)

        LinearRing = createMarkup(
            'LinearRing', GML_PREFIX, GML_NAMESPACE, root)
        exterior.append(LinearRing)

        Polygon = createMarkup(
            'Polygon', GML_PREFIX, GML_NAMESPACE, root)
        posList = createSimpleMarkup(
            exterior_pos_list, root, 'posList', GML_NAMESPACE, GML_PREFIX)
        LinearRing.append(posList)


def _add_multi_polygon(root, parent, result):
    global poly_count
    for polygon in result:
        poly_count = poly_count + 1
        poly_id = 'POLN{}'.format(poly_count)
        Polygon = createMarkup(
            'Polygon', GML_PREFIX, GML_NAMESPACE, root)
        Polygon.set('{}:id'.format(GML_PREFIX), poly_id)
        parent.append(Polygon)

        exterior = createMarkup(
            'exterior', GML_PREFIX, GML_NAMESPACE, root)
        Polygon.append(exterior)

        LinearRing = createMarkup(
            'LinearRing', GML_PREFIX, GML_NAMESPACE, root)
        exterior.append(LinearRing)

        exterior_pos_list = _get_pos_list(polygon[0])
        Polygon = createMarkup(
            'Polygon', GML_PREFIX, GML_NAMESPACE, root)
        posList = createSimpleMarkup(
            exterior_pos_list, root, 'posList', GML_NAMESPACE, GML_PREFIX)
        LinearRing.append(posList)

        if len(polygon) > 1:
            interior_pos_list = _get_pos_list(polygon[1])
            if interior_pos_list != "":
                # add the hole
                interior = createMarkup(
                    'interior', GML_PREFIX, GML_NAMESPACE, root)
                Polygon.append(interior)

                LinearRing = createMarkup(
                    'LinearRing', GML_PREFIX, GML_NAMESPACE, root)
                interior.append(LinearRing)

                Polygon = createMarkup(
                    'Polygon', GML_PREFIX, GML_NAMESPACE, root)
                posList = createSimpleMarkup(
                    interior_pos_list, root, 'posList', GML_NAMESPACE,
                    GML_PREFIX)
                LinearRing.append(posList)


def _get_pos_list(polygon):
    pos_list = ""
    for coordinates in polygon:
        pos_list = '{pos_list} {coord0} {coord1}'.format(
            pos_list=pos_list, coord0=coordinates[0],
            coord1=coordinates[1])

    return pos_list


def _add_line_string(root, parent, result):
    # TODO
    pass


def _add_procedure(root, result):
    procedure = createMarkup('procedure', OM_PREFIX, OM_NAMESPACE, root)
    root.append(procedure)
    EarthObservationEquipment = createMarkup(
        'EarthObservationEquipment', EOP_PREFIX, EOP_NAMESPACE, root)
    EarthObservationEquipment.set('{}:id'.format(GML_PREFIX), _get_id())
    procedure.append(EarthObservationEquipment)
    _add_platform(root, EarthObservationEquipment, result)
    _add_instrument(root, EarthObservationEquipment, result)
    _add_acquisitionParameters(root, EarthObservationEquipment, result)


def _add_platform(root, parent, result):
    try:
        platform_name = result.misc.platform['Satellite']
    except (AttributeError, KeyError):
        LOGGING.debug('Satellite not found')
        return
    platform = createMarkup('platform', EOP_PREFIX, EOP_NAMESPACE, root)
    parent.append(platform)
    Platform = createMarkup('Platform', EOP_PREFIX, EOP_NAMESPACE, root)
    platform.append(Platform)
    shortName = createSimpleMarkup(
        platform_name, root, 'shortName', EOP_NAMESPACE, EOP_PREFIX)
    Platform.append(shortName)


def _add_instrument(root, parent, result):
    try:
        instrument_name = result.misc.platform['Instrument Abbreviation']
    except (AttributeError, KeyError):
        LOGGING.debug('Instrument Abbreviation not found')
        return
    instrument = createMarkup('instrument', EOP_PREFIX, EOP_NAMESPACE, root)
    parent.append(instrument)
    Instrument = createMarkup('Instrument', EOP_PREFIX, EOP_NAMESPACE, root)
    instrument.append(Instrument)
    shortName = createSimpleMarkup(
        instrument_name, root, 'shortName', EOP_NAMESPACE, EOP_PREFIX)
    Instrument.append(shortName)


def _add_acquisitionParameters(root, parent, result):
    orbit_number = None
    last_orbit_number = None
    orbit_direction = None
    polarisation = None
    try:
        orbit_number = result.misc.orbit_info['Start Orbit Number']
    except (AttributeError, KeyError):
        LOGGING.debug('Start Orbit Number not found')
    try:
        last_orbit_number = result.misc.orbit_info['Stop Orbit Number']
    except (AttributeError, KeyError):
        LOGGING.debug('Last Orbit Number not found')
    try:
        orbit_direction = result.misc.orbit_info['Pass Direction']
    except (AttributeError, KeyError):
        LOGGING.debug('Orbit Direction not found')
    try:
        polarisation = result.misc.product_info.Polarisation
    except AttributeError:
        LOGGING.debug('Polarisation not found')
    if orbit_number is None and polarisation is None:
        return

    acquisitionParameters = createMarkup(
        'acquisitionParameters', EOP_PREFIX, EOP_NAMESPACE, root)
    parent.append(acquisitionParameters)
    if orbit_number is not None:
        Acquisition = createMarkup(
            'Acquisition', EOP_PREFIX, EOP_NAMESPACE, root)
        acquisitionParameters.append(Acquisition)
        orbitNumber = createSimpleMarkup(
            orbit_number, root, 'orbitNumber', EOP_NAMESPACE, EOP_PREFIX)
        Acquisition.append(orbitNumber)
        if last_orbit_number is not None:
            lastOrbitNumber = createSimpleMarkup(
                last_orbit_number, root, 'lastOrbitNumber', EOP_NAMESPACE,
                EOP_PREFIX)
            Acquisition.append(lastOrbitNumber)
        if orbit_direction is not None:
            orbitDirection = createSimpleMarkup(
                orbit_direction, root, 'orbitDirection', EOP_NAMESPACE,
                EOP_PREFIX)
            Acquisition.append(orbitDirection)

    if polarisation is not None:
        Acquisition = createMarkup(
            'Acquisition', SAR_PREFIX, SAR_NAMESPACE, root)
        acquisitionParameters.append(Acquisition)
        orbitNumber = createSimpleMarkup(
            orbit_number, root, 'polarisationChannels', SAR_NAMESPACE,
            SAR_PREFIX)
        Acquisition.append(orbitNumber)


def _add_result(root, result):
    if result.file.location == "on_tape":
        LOGGING.debug('data is on tape')
        return
    try:
        file_names = result.file.data_files.split(',')
        sizes = result.file.data_file_sizes.split(',')
        earthObservationResult = _add_eo_result(root, result)

        for i in range(0, len(file_names) - 1):
            file_name = os.path.join(result.file.directory, file_names[i])
            _add_file(root, earthObservationResult, file_name, sizes[i])
    except AttributeError:
        # not multiple files, add single file
        try:
            file_name = os.path.join(result.file.directory,
                                     result.file.data_file)
            file_size = str(result.file.data_file_size)
            earthObservationResult = _add_eo_result(root, result)
            _add_file(root, earthObservationResult, file_name, file_size)
        except AttributeError:
            LOGGING.debug('file.directory or file.data_file not found')
            return


def _add_eo_result(root, result):

    result_ = createMarkup('result', OM_PREFIX, OM_NAMESPACE, root)
    root.append(result_)

    EarthObservationResult = createMarkup(
        'EarthObservationResult', EOP_PREFIX, EOP_NAMESPACE, root)
    EarthObservationResult.set('{}:id'.format(GML_PREFIX), _get_id())
    result_.append(EarthObservationResult)
    return EarthObservationResult


def _add_file(root, earthObservationResult, file_name, file_size):
    _add_product(root, earthObservationResult, file_name, 'ftp', file_size)
    _add_product(root, earthObservationResult, file_name, 'pydap', file_size)


def _add_product(root, parent, file_name, link_type, file_size):

    product = createMarkup('product', EOP_PREFIX, EOP_NAMESPACE, root)
    parent.append(product)

    ProductInformation = createMarkup(
        'ProductInformation', EOP_PREFIX, EOP_NAMESPACE, root)
    product.append(ProductInformation)

    fileName = createMarkup('fileName', EOP_PREFIX, EOP_NAMESPACE, root)
    ProductInformation.append(fileName)

    root.set("xmlns:%s" % (XLINK_PREFIX), XLINK_NAMESPACE)
    ServiceReference = createMarkup(
        'ServiceReference', OWS_PREFIX, OWS_NAMESPACE, root)

    if link_type == 'ftp':
        data_url = urljoin_path(FTP_SERVER, file_name)
        ServiceReference.set('{}:href'.format(XLINK_PREFIX), data_url)
    else:
        data_url = urljoin_path(PYDAP_SERVER, file_name)
        ServiceReference.set('{}:href'.format(XLINK_PREFIX), data_url)

    ServiceReference.set('{}:title'.format(XLINK_PREFIX), link_type)
    fileName.append(ServiceReference)

    RequestMessage = createMarkup(
        'RequestMessage', OWS_PREFIX, OWS_NAMESPACE, root)
    ServiceReference.append(RequestMessage)

    size = createSimpleMarkup(
        file_size, root, 'size', EOP_NAMESPACE, EOP_PREFIX)
    size.set('uom', 'byte')
    ProductInformation.append(size)


def _add_metaDataProperty(root, result):
    try:
        file_name = result.file.filename
    except AttributeError:
        LOGGING.debug('file.filename not found')
        return
    metaDataProperty = createMarkup(
        'metaDataProperty', EOP_PREFIX, EOP_NAMESPACE, root)
    root.append(metaDataProperty)

    EarthObservationMetaData = createMarkup(
        'EarthObservationMetaData', EOP_PREFIX, EOP_NAMESPACE, root)
    metaDataProperty.append(EarthObservationMetaData)

    identifier = createSimpleMarkup(
        file_name, root, 'identifier', EOP_NAMESPACE, EOP_PREFIX)
    EarthObservationMetaData.append(identifier)

    identifier = createSimpleMarkup(
        'NOMINAL', root, 'acquisitionType', EOP_NAMESPACE, EOP_PREFIX)
    EarthObservationMetaData.append(identifier)

    identifier = createSimpleMarkup(
        'ARCHIVED', root, 'status', EOP_NAMESPACE, EOP_PREFIX)
    EarthObservationMetaData.append(identifier)


def _get_id():
    global next_id
    next_id = next_id + 1
    if next_id < 10:
        return 'ID0{}N10001'.format(next_id)
    return 'ID{}N10001'.format(next_id)
