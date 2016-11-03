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

import logging

from elasticsearch_dsl.connections import connections

from ceda_opensearch.settings import ELASTIC_HOST


LOGGING = logging.getLogger(__name__)


class CedaOpensearchMiddleware(object):
    """
    This class holds the singletons used in this package.

    """
    __elasticsearch = None
    __osEngine = None

    @classmethod
    def __init_os_engine(cls):
        from ceda_opensearch.os_conf import setUp
        LOGGING.info("__init_os_engine - OpenSearch Engine created")
        CedaOpensearchMiddleware.__osEngine = setUp()

    @classmethod
    def get_osengine(cls, debug=False):
        """
        Get an instance of an osEngine, create one if necessary.

        """
        if debug or CedaOpensearchMiddleware.__osEngine is None:
            CedaOpensearchMiddleware.__init_os_engine()
        return CedaOpensearchMiddleware.__osEngine

    @classmethod
    def __init_elasticsearch(cls):
        LOGGING.info("__init_os_engine - Elastic Search connection created")
        CedaOpensearchMiddleware.__elasticsearch = (
            connections.create_connection(hosts=[ELASTIC_HOST], timeout=20))

    @classmethod
    def get_elasticsearch(cls, debug=False):
        """
        Get an elastic search connection, create one if necessary.

        """
        if debug or CedaOpensearchMiddleware.__elasticsearch is None:
            CedaOpensearchMiddleware.__init_elasticsearch()
        return CedaOpensearchMiddleware.__elasticsearch
