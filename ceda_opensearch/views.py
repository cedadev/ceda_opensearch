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

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template.context_processors import csrf
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import View
from django.views.generic.base import TemplateView
from elasticsearch.exceptions import RequestError

from ceda_opensearch import elastic_search
from ceda_opensearch.constants import OS_DESCRIPTION_TYPE
from ceda_opensearch.errors import Http400, Http503, ServiceUnavailable
from ceda_opensearch.example_queries import EXAMPLE_PARAMETERS, BASE_CONTEXT
from ceda_opensearch.helper import build_host_url, update_context, \
    get_mime_type
from ceda_opensearch.middleware import CedaOpensearchMiddleware
from ceda_opensearch.resource import get_resource
from ceda_opensearch.settings import ELASTIC_INDEX


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
            if 'text/html' in request.META.get('HTTP_ACCEPT'):
                context = {'message': ex.message}
                return render_to_response('400.html', context, status=400)
            else:
                return HttpResponseBadRequest(reason=ex.message)
        except Http503 as ex:
            return ServiceUnavailable(reason=ex.message)

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


class Status(TemplateView):
    """
    Perform a number of queries based on the list in example_queries.

    """

    def get(self, request, *args, **kwargs):
        """
        Present the results of the example queries on a test page.

        """
        results = []
        for example_parameters in EXAMPLE_PARAMETERS:
            params = example_parameters.split('&')
            context = dict(BASE_CONTEXT)
            for param in params:
                key, value = param.split('=')
                context[key] = value
            try:
                _, total_hits = (elastic_search.get_search_results(context))
            except (RequestError) as ex:
                results.append({'test': example_parameters, 'status': 'ERROR',
                                'message': ex})
                continue
            except Http400 as ex:
                LOGGING.error(ex.message)
                context = {'message': ex.message}
                return render_to_response('400.html', context, status=400)
            except Http503 as ex:
                return ServiceUnavailable(reason=ex.message)
            if total_hits > 0:
                results.append({'test': example_parameters, 'status': 'OK',
                                'message': '{} results found'.
                                format(total_hits)})
            else:
                results.append({'test': example_parameters,
                                'status': 'WARNING',
                                'message': ' No results returned'})

        context = {'status': results, 'es_index': ELASTIC_INDEX}
        return render_to_response('status.html', context,
                                  content_type='text/html')
