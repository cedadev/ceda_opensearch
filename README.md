# CEDA Opensearch
This package provides an open search interface to CEDAs elastic search, which currently provides Sentinel 1A and 2A data.

## Search Parameters common to Sentinel 1 and 2

* [bbox](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Geo/1.0/Draft_2#The_.22box.22_parameter)
* dataFormat
* [endDate](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Time/1.0/Draft_1#The_.22start.22_and_.22end.22_parameters)
* [geometry](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Geo/1.0/Draft_2#The_.22geometry.22_parameter) (polygon)
* [instrument](http://portal.opengeospatial.org/files/65168)
* [maximumRecords](http://www.opensearch.org/Specifications/OpenSearch/1.1#The_.22count.22_parameter)
* mission
* name
* [orbitNumber](http://portal.opengeospatial.org/files/65168)
* [platform](http://portal.opengeospatial.org/files/65168)
* [sensorMode](http://portal.opengeospatial.org/files/65168)
* [startDate](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Time/1.0/Draft_1#The_.22start.22_and_.22end.22_parameters)
* [startPage](http://www.opensearch.org/Specifications/OpenSearch/1.1#The_.22startPage.22_parameter)
* [startRecord](http://www.opensearch.org/Specifications/OpenSearch/1.1#The_.22startIndex.22_parameter)
* [uid](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Geo/1.0/Draft_2#The_.22uid.22_parameter)

## Search parameters currently specific to Sentinel 1

* [orbitDirection](http://portal.opengeospatial.org/files/65168)
* [polarisationChannels](http://portal.opengeospatial.org/files/65168)
* [productType](http://portal.opengeospatial.org/files/65168)
* [resolution](http://portal.opengeospatial.org/files/65168)

## Search parameters specific to Sentinel 2

* [maxCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)
* [minCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)

## Search result format

Results may be obtained either as an atom feed or in json by specifying the format in the URL:

* http://opensearch-test.ceda.ac.uk/opensearch/atom
* http://opensearch-test.ceda.ac.uk/opensearch/json

## Resource format

Information about a specific resource can be obtained in gml or json by specifying the format in the URL:
* http://opensearch-test.ceda.ac.uk/resource/gml
* http://opensearch-test.ceda.ac.uk/resource/json


## Example searches

### Sentinel 1

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&dataFormat=safe

http://opensearch-test.ceda.ac.uk/opensearch/atom?instrument=SAR

http://opensearch-test.ceda.ac.uk/opensearch/atom?mission=sentinel-1

http://opensearch-test.ceda.ac.uk/opensearch/atom?name=S1A_EW_GRDM_1SSH_20160801T001924_20160801T002010_012399_013578_021D

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&productType=GRD

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&orbitDirection=ascending

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&orbitNumber=12399

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&resolution=M

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&sensorMode=EW

http://opensearch-test.ceda.ac.uk/opensearch/atom?uid=42a2a190104f75d8180ddf44d5cc28c4e675badc

#### date

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&endDate=2016-08-20T00:00:00.000Z

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-20T00:00:00.000Z

#### bbox

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&bbox=1,1,90,90

#### polygon

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&geometry=POLYGON((30%2010,40%2040,20%2040,10%2020,30%2010)(29%2011,29%2028,11%2021,29%2011))

#### polarisation

http://opensearch-test.ceda.ac.uk/opensearch/atom?polarisationChannels=VV

### Sentinel 2

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&dataFormat=safe

http://opensearch-test.ceda.ac.uk/opensearch/atom?instrument=MSI

http://opensearch-test.ceda.ac.uk/opensearch/atom?mission=sentinel-2

http://opensearch-test.ceda.ac.uk/opensearch/atom?name=S2A_OPER_PRD_MSIL1C_PDMC_20160801T072514_R073_V20160801T000734_20160801T000734

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&orbitNumber=005790

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&sensorMode=INS-NOBS

http://opensearch-test.ceda.ac.uk/opensearch/atom?uid=876f2e35b75d645723642b3ef95571d5ea23691d

#### date

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&endDate=2016-08-20T00:00:00.000Z

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-20T00:00:00.000Z

#### bbox

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&bbox=1,1,90,90

#### polygon

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&geometry=POLYGON((30%2010,40%2040,20%2040,10%2020,30%2010)(29%2011,29%2028,11%2021,29%2011))

#### cloud

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&minCloudCoverPercentage=40

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&maxCloudCoverPercentage=50

http://opensearch-test.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&minCloudCoverPercentage=40&maxCloudCoverPercentage=50

