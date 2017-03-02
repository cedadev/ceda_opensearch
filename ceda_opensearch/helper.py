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

import mimetypes
from posixpath import join as path_urljoin
import socket
from urllib.parse import urljoin, urlparse
from urllib.parse import urlsplit, urlunsplit

from ceda_opensearch.constants import COUNT_DEFAULT, COUNT_MAX, \
    START_PAGE_DEFAULT, OS_DESCRIPTION, OS_DESCRIPTION_TYPE, \
    START_INDEX_DEFAULT, GML_PREFIX, GML_TYPE
from ceda_opensearch.middleware import CedaOpensearchMiddleware


if not mimetypes.inited:
    mimetypes.init()
if ('.%s' % OS_DESCRIPTION) not in getattr(mimetypes, 'types_map').keys():
    mimetypes.add_type(OS_DESCRIPTION_TYPE, '.%s' % OS_DESCRIPTION)
if ('.%s' % GML_PREFIX) not in getattr(mimetypes, 'types_map').keys():
    mimetypes.add_type(GML_TYPE, '.%s' % GML_PREFIX)


def build_host_url(request):
    hostname = socket.getfqdn()
    if (request.META['SERVER_PORT'] != str(80) and
            request.META['SERVER_PORT'] != str(443)):
        hostname = "%s:%s" % (hostname, request.META['SERVER_PORT'])
    if request.is_secure():
        return 'https://%s' % (hostname)
    else:
        return 'http://%s' % (hostname)


def update_context(request):
    """
    Add the parameters from the request GET dictionary to the default
    parameters.

    Only know parameters are added.

    @param request: the http request

    @return a dict containing the context

    """
    context = CedaOpensearchMiddleware.get_osengine().create_query_dictionary()
    if request.GET is not None:
        for key in context.keys():
            if key in request.GET.keys():
                context[key] = request.GET.get(key)
    if context.get('startPage') is None and context.get('startRecord') is None:
        context['startRecord'] = str(START_INDEX_DEFAULT)
    if int(context['maximumRecords']) > COUNT_MAX:
        context['maximumRecords'] = str(COUNT_MAX)
    return context


def get_mime_type(iformat):
    return getattr(mimetypes, 'types_map')[(('.%s') % iformat)]


def get_index(count, index, page):
    """
    Get the index of the first result to return.

    An index of one should return the first result.

    @param count (int): the number of search results per page desired
    @param index (int): the index of the first search result desired
    @param page (int): the page number of the set of search results desired

    @return an int containing the index of the first result to return

    """
    if index is not None:
        return int(index)

    if page is not None:
        return ((int(page) - 1) * int(count)) + 1
    return 1


def import_count_and_page(context):
    """
    Get the number of search results per page desired, the index of the first
    search result desired, the page number of the set of search results
    desired.

    @param context (dict): the query parameters from the users request plus
    defaults from the OSQuery. This only contains parameters for registered
    OSParams.

    @returns tuple(int, int, int). The number of search results per page
        desired, the index of the first search result desired, the page number
        of the set of search results desired.

    """
    ret = []
    try:
        ret.append(int(context.get('maximumRecords')))
    except (ValueError, TypeError):
        ret.append(COUNT_DEFAULT)

    try:
        ret.append(int(context.get('startRecord')))
    except (ValueError, TypeError):
        ret.append(None)

    try:
        ret.append(int(context.get('startPage')))
    except (ValueError, TypeError):
        ret.append(START_PAGE_DEFAULT)

    return tuple(ret)


def urljoin_path(site, path):
    segments = [s for s in path.split('/') if s]
    return urljoin(site, path_urljoin(urlparse(site).path, *segments))
