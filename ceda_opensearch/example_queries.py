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

BASE_CONTEXT = {'maximumRecords': '1',
                'startRecord': '1',
                'polarisationChannels': None,
                'maxCloudCoverPercentage': None,
                'endDate': None,
                'dataOnline': None,
                'geometry': None,
                'uid': None,
                'orbitNumber': None,
                'sensorMode': None,
                'name': None,
                'resolution': None,
                'minCloudCoverPercentage': None,
                'mission': None,
                'productType': None,
                'dataFormat': None,
                'startDate': None,
                'q': None,
                'startPage': None,
                'platform': None,
                'bbox': None,
                'instrument': None,
                'orbitDirection': None}

EXAMPLE_PARAMETERS = [
    # General
    'maximumRecords=2',
    'startPage=3',
    'startRecord=21',

    # Landsat 5
    'platform=landsat-5',
    'platform=landsat-5&dataFormat=geoTIFF',
    'platform=landsat-5&dataOnline=true',
    'platform=landsat-5&instrument=TM',
    'platform=landsat-5&maxCloudCoverPercentage=40',
    'platform=landsat-5&minCloudCoverPercentage=30',
    'platform=landsat-5&mission=landsat',
    'platform=landsat-5&sensorMode=SAM',
    # Date
    'platform=landsat-5&startDate=2006-08-10T00:00:00.000Z',
    'platform=landsat-5&endDate=2006-08-20T00:00:00.000Z',
    'platform=landsat-5&startDate=2006-08-10T00:00:00.000Z&endDate=2006-08-2'
    '0T00:00:00.000Z',
    # bbox
    'platform=landsat-5&bbox=1,1,90,-90',
    # poloygon
    'platform=landsat-5&geometry=POLYGON((-95 30,-80 30,-80 10,-95 10,-95 30)'
    ')',
    # multiple ranges
    'platform=landsat-5&startDate=2006-08-10T00:00:00.000Z&endDate=2006-08-20T'
    '00:00:00.000Z&minCloudCoverPercentage=40&maxCloudCoverPercentage=60&bbox='
    '1,1,90,-90',

    # Landsat 7
    'platform=landsat-7',
    'platform=landsat-7&dataFormat=geoTIFF',
    'platform=landsat-7&dataOnline=true',
    'platform=landsat-7&instrument=ETM',
    'platform=landsat-7&maxCloudCoverPercentage=40',
    'platform=landsat-7&minCloudCoverPercentage=30',
    'platform=landsat-7&mission=landsat',
    'platform=landsat-7&sensorMode=SAM',
    # Date
    'platform=landsat-7&startDate=2006-08-10T00:00:00.000Z',
    'platform=landsat-7&endDate=2006-08-20T00:00:00.000Z',
    'platform=landsat-7&startDate=2006-08-10T00:00:00.000Z&endDate=2006-08-2'
    '0T00:00:00.000Z',
    # bbox
    'platform=landsat-7&bbox=1,1,90,-90',
    # poloygon
    'platform=landsat-7&geometry=POLYGON((-95 30,-80 30,-80 10,-95 10,-95 30)'
    ')',
    # multiple ranges
    'platform=landsat-7&startDate=2006-08-10T00:00:00.000Z&endDate=2006-08-20T'
    '00:00:00.000Z&minCloudCoverPercentage=40&maxCloudCoverPercentage=50&bbox='
    '1,1,90,-90',

    # Landsat 8
    'platform=landsat-8',
    'platform=landsat-8&dataFormat=geoTIFF',
    'platform=landsat-8&dataOnline=true',
    'platform=landsat-8&instrument=OLI_TIRS',
    'platform=landsat-8&maxCloudCoverPercentage=40',
    'platform=landsat-8&minCloudCoverPercentage=30',
    'platform=landsat-8&mission=landsat',
    # Date
    'platform=landsat-8&startDate=2016-08-10T00:00:00.000Z',
    'platform=landsat-8&endDate=2016-08-20T00:00:00.000Z',
    'platform=landsat-8&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-2'
    '0T00:00:00.000Z',
    # bbox
    'platform=landsat-8&bbox=1,1,90,-90',
    # poloygon
    'platform=landsat-8&geometry=POLYGON((-95 30,-80 30,-80 10,-95 10,-95 30)'
    ')',
    # multiple ranges
    'platform=landsat-8&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-20T'
    '00:00:00.000Z&minCloudCoverPercentage=40&maxCloudCoverPercentage=50&bbox='
    '1,1,90,-90',

    # Sentinel 1
    'platform=sentinel-1A',
    'platform=sentinel-1A&dataFormat=safe',
    'platform=sentinel-1A&dataOnline=true',
    'instrument=SAR',
    'mission=sentinel-1',
    'name=S1A_EW_GRDM_1SSH_20160801T001924_20160801T002010_012399_013578_021D',
    'platform=sentinel-1A&productType=GRD',
    'platform=sentinel-1A&orbitNumber=12399',
    'platform=sentinel-1A&relativeOrbitNumber=77',
    'platform=sentinel-1A&orbitDirection=ascending',
    'platform=sentinel-1A&resolution=M',
    'platform=sentinel-1A&sensorMode=EW',
    'uid=S1A_IW_SLC__1SDV_20141003T054301_20141003T054328_002661_002F66_75CD',
    # Date
    'platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z',
    'platform=sentinel-1A&endDate=2016-08-20T00:00:00.000Z',
    'platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-2'
    '0T00:00:00.000Z',
    # bbox
    'platform=sentinel-1A&bbox=1,1,90,-90',
    # poloygon
    'platform=sentinel-1A&geometry=POLYGON((30 10,40 40,20 40,10 20,30 10)(29 '
    '11,29 28,11 21,29 11))',
    # multiple ranges
    'platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-2'
    '0T00:00:00.000Z&bbox=1,1,90,-90',
    # Sentinel 1 specific
    # polarisation
    'polarisationChannels=VV',

    # Sentinel 2
    'platform=sentinel-2A',
    'platform=sentinel-2A&dataFormat=safe',
    'platform=sentinel-2A&dataOnline=true',
    'instrument=MSI',
    'mission=sentinel-2',
    'name=S2A_OPER_PRD_MSIL1C_PDMC_20160801T072514_R073_V20160801T000734_20160'
    '801T000734',
    # 'platform=sentinel-2A&productType=S2MSI1C',
    'platform=sentinel-2A&orbitNumber=005790',
    'platform=sentinel-2A&relativeOrbitNumber=073',
    # 'platform=sentinel-2A&orbitDirection=ascending',
    # 'platform=sentinel-2A&resolution=20',
    'platform=sentinel-2A&sensorMode=INS-NOBS',
    'uid=S2A_OPER_PRD_MSIL1C_PDMC_20160607T155132_R062_V20150627T102531_20150627T102531',
    # Date
    'platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z',
    'platform=sentinel-2A&endDate=2016-08-20T00:00:00.000Z',
    'platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-2'
    '0T00:00:00.000Z',
    # bbox
    'platform=sentinel-2A&bbox=1,1,90,-90',
    # poloygon
    'platform=sentinel-2A&geometry=POLYGON((30 10,40 40,20 40,10 20,30 10)(29 '
    '11,29 28,11 21,29 11))',
    # multiple ranges
    'platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-2'
    '0T00:00:00.000Z&minCloudCoverPercentage=40&maxCloudCoverPercentage=50&bbo'
    'x=1,1,90,-90',
    # Sentinel 2 specific
    # Cloud
    'platform=sentinel-2A&minCloudCoverPercentage=40',
    'platform=sentinel-2A&maxCloudCoverPercentage=50',
    'platform=sentinel-2A&minCloudCoverPercentage=40&maxCloudCoverPercentage=5'
    '0',

    # Sentinel 3
    'platform=sentinel-3A',
    'platform=sentinel-3A&dataFormat=safe',
    'platform=sentinel-3A&dataOnline=true',
    'instrument=SLSTR',
    'mission=sentinel-3',
    # 'name=S1A_EW_GRDM_1SSH_20160801T001924_20160801T002010_012399_013578_021D',
    # 'platform=sentinel-3A&productType=SL_1_RBT',
    'platform=sentinel-3A&orbitNumber=3905',
    'platform=sentinel-3A&relativeOrbitNumber=82',
    #     'platform=sentinel-3A&orbitDirection=ascending',
    #     'platform=sentinel-3A&resolution=M',
    'platform=sentinel-3A&sensorMode=Earth Observation',
    'uid=S3A_SL_1_RBT____20161116T142921_20161116T143221_20161116T171144_0179_011_082_0719_SVL_O_NR_002',
    # Date
    'platform=sentinel-3A&startDate=2016-11-10T00:00:00.000Z',
    'platform=sentinel-3A&endDate=2016-11-20T00:00:00.000Z',
    'platform=sentinel-3A&startDate=2016-11-10T00:00:00.000Z&endDate=2016-11-2'
    '0T00:00:00.000Z',
    # bbox
    'platform=sentinel-3A&bbox=1,1,90,-90',
    # poloygon
    'platform=sentinel-3A&geometry=POLYGON((30 10,40 40,20 40,10 20,30 10)(29 '
    '11,29 28,11 21,29 11))',
    # multiple ranges
    'platform=sentinel-3A&startDate=2016-11-10T00:00:00.000Z&endDate=2016-11-2'
    '0T00:00:00.000Z&bbox=1,1,90,-90',
]
