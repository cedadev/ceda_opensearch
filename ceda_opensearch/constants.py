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


# Namespaces
CEDA_NAMESPACE = 'http://localhost/ceda/opensearch'
CEDA_PREFIX = 'ceda'

DCT_NAMESPACE = 'http://purl.org/dc/terms/'
DCT_PREFIX = 'dc'

EO_NAMESPACE = 'http://a9.com/-/opensearch/extensions/eo/1.0/'
EO_PREFIX = 'eo'

EOP_NAMESPACE = 'http://www.opengis.net/eop/2.0'
EOP_PREFIX = 'eop'

GML_NAMESPACE = 'http://www.opengis.net/gml/3.2'
GML_PREFIX = 'gml'
GML_TYPE = 'application/gml+xml'

GEO_NAMESPACE = 'http://a9.com/-/opensearch/extensions/geo/1.0/'
GEO_PREFIX = 'geo'

OM_NAMESPACE = 'http://www.opengis.net/om/2.0'
OM_PREFIX = 'om'

OWS_NAMESPACE = 'http://www.opengis.net/ows/2.0'
OWS_PREFIX = 'ows'

PARAM_NAMESPACE = 'http://a9.com/-/spec/opensearch/extensions/parameters/1.0/'
PARAM_PREFIX = 'param'

SAFE_NAMESPACE = 'http://www.esa.int/safe/sentinel/1.1'
SAFE_PREFIX = 'safe'

SAR_NAMESPACE = 'http://www.opengis.net/sar/2.1'
SAR_PREFIX = 'sar'

TIME_NAMESPACE = 'http://a9.com/-/opensearch/extensions/time/1.0/'
TIME_PREFIX = 'time'

XLINK_NAMESPACE = 'http://www.w3.org/1999/xlink'
XLINK_PREFIX = 'xlink'

XSI_NAMESPACE = 'http://www.w3.org/2001/XMLSchema-instance'
XSI_PREFIX = 'xsi'

SCHEMA_LOCATION = ('http://www.opengis.net/eop/2.0 https://svn.opengeospatial.'
                   'org/ogc-projects/cite/scripts/wcseo/1.0/tags/r1/resources/'
                   'omeo/eop.xsd')


# Open search
OS_PATH = 'opensearch'
OS_DESCRIPTION = 'opensearchdescription'
OS_DESCRIPTION_FILE_NAME = 'description.xml'
OS_DESCRIPTION_TYPE = 'application/opensearchdescription+xml'


# Search defaults
COUNT_DEFAULT = 10
COUNT_MAX = 50
START_INDEX_DEFAULT = 1
START_PAGE_DEFAULT = 1
