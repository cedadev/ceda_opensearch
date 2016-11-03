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

from django.core.context_processors import csrf
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View

from ceda_opensearch.constants import OS_DESCRIPTION_TYPE
from ceda_opensearch.errors import Http400, Http503, ServiceUnavailable
from ceda_opensearch.helper import build_host_url, update_context, \
    get_mime_type
from ceda_opensearch.middleware import CedaOpensearchMiddleware
from ceda_opensearch.resource import get_resource


LOGGING = logging.getLogger(__name__)


class OpenSearch(View):
    """
    Handle search requests.

    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Override View.dspatch in order to use decorator.

        """
        return super(OpenSearch, self).dispatch(*args, **kwargs)

    def get(self, request, iformat):
        """
        Search.

        @param request: a HTTP request
        @param iformat: the requested format of data

        """
        host_url = build_host_url(request)
        context = update_context(request)
        try:
            response = (CedaOpensearchMiddleware.get_osengine()
                        .do_search(host_url, iformat, context))
            return HttpResponse(response, content_type=get_mime_type(iformat))
        except Http400 as ex:
            LOGGING.debug(ex.message)
            return HttpResponseBadRequest(ex.message)
        except Http503 as ex:
            return ServiceUnavailable(ex.message)

    def options(self, request, iformat):
        """
        Handles responding to requests for the OPTIONS HTTP verb.


        @param request: a HTTP request
        @param iformat: the requested format of data

        """
        response = super(OpenSearch, self).options(request)
        response['Content-Type'] = get_mime_type(iformat)
        return response


class Description(View):
    """
    Handle requests for the description document.

    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Override View.dspatch in order to use decorator.

        """
        return super(Description, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
        Get the description document.

        @param request: a HTTP request

        """
        host_url = build_host_url(request)
        response = (CedaOpensearchMiddleware.get_osengine()
                    .get_description(host_url))
        context = {}
        context['response'] = mark_safe(response)
        context.update(csrf(request))
        return render_to_response('responseTemplate.html', context,
                                  content_type=OS_DESCRIPTION_TYPE)

    def options(self, request):
        """
        Handles responding to requests for the OPTIONS HTTP verb.

        @param request: a HTTP request

        """
        response = super(Description, self).options(request)
        response['Content-Type'] = OS_DESCRIPTION_TYPE
        return response


class Resource(View):
    """
    Handle resource requests.

    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Override View.dspatch in order to use decorator.

        """
        return super(Resource, self).dispatch(*args, **kwargs)

    def get(self, request, iformat):
        """
        Search.

        @param request: a HTTP request
        @param iformat: the requested format of data

        """
        response = get_resource(request, iformat)
        return HttpResponse(response, content_type=get_mime_type(iformat))

    def options(self, request, iformat):
        """
        Handles responding to requests for the OPTIONS HTTP verb.


        @param request: a HTTP request
        @param iformat: the requested format of data

        """
        response = super(Resource, self).options(request)
        response['Content-Type'] = get_mime_type(iformat)
        return response


class Index(View):
    """
    Handle requests for the index page.

    """
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        """
        Override View.dspatch in order to use decorator.

        """
        return super(Index, self).dispatch(*args, **kwargs)

    def get(self, request):
        """
        Get the index page.

        @param request: a HTTP request

        """
        return render_to_response('index.html', {},
                                  content_type=get_mime_type('html'))
