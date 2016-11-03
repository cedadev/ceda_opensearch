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

from ceda_markup.markup import createMarkup
from ceda_markup.opensearch import OS_PREFIX, OS_NAMESPACE, \
    OpenSearchDescription
from ceda_markup.opensearch.os_engine import OSEngine
from ceda_markup.opensearch.os_engine_helper import OSEngineHelper
from ceda_opensearch.constants import OS_PATH, OS_DESCRIPTION_FILE_NAME
from ceda_opensearch.os_impl import COSQuery, COSAtomResponse, COSJsonResponse


def setUp():
    query = COSQuery()
    responses = [COSAtomResponse(), COSJsonResponse()]
    # max 16 char
    os_short_name = "CEDA Search"
    # max 48 char
    os_long_name = "CEDA Search Service"
    # max 1024 char
    os_description = "Use CEDA search to search for Sentinel products"
    # max 256 char, single word and delimited by the space character (' ')
    os_tags = "Sentinal CEDA NERC"
    os_developer = "CEDA"
    os_attribution = "NERC"
    os_adult_content = "false"
    os_syndacation_right = "open"

    osd = OpenSearchDescription(os_short_name, os_description, OS_PATH,
                                file_name=OS_DESCRIPTION_FILE_NAME,
                                tags=os_tags, long_name=os_long_name,
                                developer=os_developer,
                                attribution=os_attribution,
                                syndacation_right=os_syndacation_right,
                                adult_content=os_adult_content)
    return OSEngine(query, responses, osd, os_engine_helper=helper())


class helper(OSEngineHelper):
    """
    An implementation of the OSEngineHelper class used to provide additional
    information for the description document.

    """

    def __init__(self):
        """
        Constructor
        """
        super(OSEngineHelper)

    def additional_description(self, req_doc):
        """
        Overriding the OSEngineHelper method to add further tags into req_doc.

        @param req_doc: a request OpenSource document

        """
        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("dataFormat", "SAFE")
        markup.set("instrument", "SAR")
        markup.set("mission", "sentinel-1")
        markup.set("orbitDirection", "ascending")
        markup.set("orbitNumber", "12399")
        markup.set("platform", "sentinel-1A")
        markup.set("productType", "GRD")
        markup.set("resolution", "M")
        markup.set("sensorMode", "EW")
        req_doc.append(markup)

        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("dataFormat", "SAFE")
        markup.set("instrument", "MSI")
        markup.set("mission", "sentinel-2")
#         markup.set("orbitDirection", "ascending")
        markup.set("orbitNumber", "005790")
        markup.set("platform", "sentinel-2A")
#         markup.set("productType", "")
#         markup.set("resolution", "10")
        markup.set("sensorMode", "INS-NOBS")
        req_doc.append(markup)

        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("uid", "876f2e35b75d645723642b3ef95571d5ea23691d")
        req_doc.append(markup)

        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("name", "S2A_OPER_PRD_MSIL1C_PDMC_20160801T072514_R073_"
                   "V20160801T000734_20160801T000734")
        req_doc.append(markup)

        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("startDate", "2016-08-01T00:00:00.000Z")
        markup.set("endDate", "2016-09-01T00:00:00.000Z")
        req_doc.append(markup)

        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("bbox", "144,-35,146,-36")
        req_doc.append(markup)

        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("geometry", "POLYGON ((30%2010,40%2040,20%2040,10%2020,"
                   "30%2010)(29%2011,29%2028,11%2021,29%2011))")
        req_doc.append(markup)
        # Sentinel 1 specific
        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("platform", "sentinel-1A")
        markup.set("polarisationChannels", "HH")
        req_doc.append(markup)

        # Sentinel 2 specific
        markup = createMarkup('Query', OS_PREFIX, OS_NAMESPACE, req_doc)
        markup.set("role", "example")
        markup.set("platform", "sentinel-2A")
        markup.set("minCloudCoverPercentage", "30")
        markup.set("maxCloudCoverPercentage", "40")
        req_doc.append(markup)

        return req_doc
