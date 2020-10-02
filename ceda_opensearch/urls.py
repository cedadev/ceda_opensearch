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


ceda_opensearch URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path, re_path
from django.contrib import admin

from ceda_opensearch.constants import OS_PATH
from ceda_opensearch.views import Description, OpenSearch, Index, Resource, Status

IFORMAT = ["atom", "json"]
IFORMATS_RE = '(' + '|'.join(IFORMAT) + ')'

IFORMAT2 = ["gml", "json", "xml"]
IFORMATS_RE2 = '(' + '|'.join(IFORMAT2) + ')'

urlpatterns = [
    path('admin/', admin.site.urls),

    # status
    path('status/', Status.as_view()),

    # Resource
    re_path(r'resource/{IFORMATS_RE2}'.format(IFORMATS_RE2=IFORMATS_RE2), Resource.as_view(), name='resource'),

    # Opensearch description
    path(f'{OS_PATH}/description.xml', Description.as_view(),
         name='os_description'),

    # Opensearch search
    re_path(r'{OS_PATH}/{IFORMATS_RE}'.format(OS_PATH=OS_PATH, IFORMATS_RE=IFORMATS_RE), OpenSearch.as_view(), name='os_search'),
    path(f'{OS_PATH}/atom', OpenSearch.as_view(), name='os_search_atom'),

    # Everything else
    path('', Index.as_view(), name='index'),
]
