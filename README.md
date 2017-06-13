# CEDA Opensearch
This package provides an open search interface to CEDAs elastic search, which currently provides Landsat 5, 7 and 8 data (all limited in geographic scope) and Sentinel 1, 2 and 3 data. The dataOnline flag is used to indicate if the data is online (spinning disk) or offline (tape).

## Open search description document

The [open search description document](http://opensearch.ceda.ac.uk/opensearch/description.xml) contains details about the supported parameters and their values. Below is a more human readable form of the search parameters.

## Search Parameters common to Landsat and Sentinel

* [bbox](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Geo/1.0/Draft_2#The_.22box.22_parameter)
* dataFormat
* dataOnline
* [endDate](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Time/1.0/Draft_1#The_.22start.22_and_.22end.22_parameters)
* [geometry](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Geo/1.0/Draft_2#The_.22geometry.22_parameter) (polygon)
* [instrument](http://portal.opengeospatial.org/files/65168)
* [maximumRecords](http://www.opensearch.org/Specifications/OpenSearch/1.1#The_.22count.22_parameter)
* mission
* name
* [platform](http://portal.opengeospatial.org/files/65168)
* [startDate](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Time/1.0/Draft_1#The_.22start.22_and_.22end.22_parameters)
* [startPage](http://www.opensearch.org/Specifications/OpenSearch/1.1#The_.22startPage.22_parameter)
* [startRecord](http://www.opensearch.org/Specifications/OpenSearch/1.1#The_.22startIndex.22_parameter)
* [uid](http://www.opensearch.org/Specifications/OpenSearch/Extensions/Geo/1.0/Draft_2#The_.22uid.22_parameter)

## Additional search parameters for Landsat 5 and 7

* [maxCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)
* [minCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)
* [sensorMode](http://portal.opengeospatial.org/files/65168)

## Additional search parameters for Landsat 8

* [maxCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)
* [minCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)

## Additional search parameters for Sentinel 1

* [orbitDirection](http://portal.opengeospatial.org/files/65168)
* [orbitNumber](http://portal.opengeospatial.org/files/65168)
* [polarisationChannels](http://portal.opengeospatial.org/files/65168)
* [productType](http://portal.opengeospatial.org/files/65168)
* [relativeOrbitNumber](http://www.esa.int/safe/sentinel/1.1)
* [resolution](http://portal.opengeospatial.org/files/65168)
* [sensorMode](http://portal.opengeospatial.org/files/65168)

## Additional search parameters for Sentinel 2

* [maxCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)
* [minCloudCoverPercentage](http://portal.opengeospatial.org/files/65168)
* [orbitNumber](http://portal.opengeospatial.org/files/65168)
* [relativeOrbitNumber](http://www.esa.int/safe/sentinel/1.1)
* [sensorMode](http://portal.opengeospatial.org/files/65168)

## Additional search parameters for Sentinel 3

* [orbitNumber](http://portal.opengeospatial.org/files/65168)
* [relativeOrbitNumber](http://www.esa.int/safe/sentinel/1.1)
* [sensorMode](http://portal.opengeospatial.org/files/65168)

## Search result format

Results may be obtained either as an atom feed or in json by specifying the format in the URL:

* http://opensearch.ceda.ac.uk/opensearch/atom
* http://opensearch.ceda.ac.uk/opensearch/json

## Resource format

Information about a specific resource can be obtained in gml or json by specifying the format in the URL:
* http://opensearch.ceda.ac.uk/resource/gml
* http://opensearch.ceda.ac.uk/resource/json


## Example searches

### Landsat

http://opensearch.ceda.ac.uk/opensearch/atom?mission=landsat

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-5

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-5&dataFormat=geotiff

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-5&instrument=TM

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-7&instrument=ETM

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-8&instrument=OLI_TIRS

http://opensearch.ceda.ac.uk/opensearch/atom?name=LT50210501990010CPE00

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-5&sensorMode=SAM

http://opensearch.ceda.ac.uk/opensearch/atom?platform=landsat-7&sensorMode=SAM

http://opensearch.ceda.ac.uk/opensearch/atom?uid=42a2a190104f75d8180ddf44d5cc28c4e675badc

#### date

http://opensearch.ceda.ac.uk/opensearch/atom?mission=landsat&startDate=2016-08-10T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?mission=landsat&endDate=2016-08-20T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?mission=landsat&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-20T00:00:00.000Z

#### bbox

http://opensearch.ceda.ac.uk/opensearch/atom?mission=landsat&bbox=1,1,90,90

#### polygon

http://opensearch.ceda.ac.uk/opensearch/atom?mission=landsat&geometry=POLYGON((-90%2016,-95%2012,-95%2010,-90%2010,-90%2016))

#### cloud

http://opensearch.ceda.ac.uk/opensearch/atom?platform=mission=landsat&minCloudCoverPercentage=40

http://opensearch.ceda.ac.uk/opensearch/atom?platform=mission=landsat&maxCloudCoverPercentage=50

http://opensearch.ceda.ac.uk/opensearch/atom?platform=mission=landsat&minCloudCoverPercentage=40&maxCloudCoverPercentage=50

### Sentinel 1

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&dataFormat=safe

http://opensearch.ceda.ac.uk/opensearch/atom?instrument=SAR

http://opensearch.ceda.ac.uk/opensearch/atom?mission=sentinel-1

http://opensearch.ceda.ac.uk/opensearch/atom?name=S1A_EW_GRDM_1SSH_20160801T001924_20160801T002010_012399_013578_021D

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&productType=GRD

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&orbitDirection=ascending

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&orbitNumber=12399

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&relativeOrbitNumber=77

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&resolution=M

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&sensorMode=EW

http://opensearch.ceda.ac.uk/opensearch/atom?uid=42a2a190104f75d8180ddf44d5cc28c4e675badc

#### date

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&endDate=2016-08-20T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-20T00:00:00.000Z

#### bbox

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&bbox=1,1,90,90

#### polygon

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-1A&geometry=POLYGON((30%2010,40%2040,20%2040,10%2020,30%2010)(29%2011,29%2028,11%2021,29%2011))

#### polarisation

http://opensearch.ceda.ac.uk/opensearch/atom?polarisationChannels=VV

### Sentinel 2

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&dataFormat=safe

http://opensearch.ceda.ac.uk/opensearch/atom?instrument=MSI

http://opensearch.ceda.ac.uk/opensearch/atom?mission=sentinel-2

http://opensearch.ceda.ac.uk/opensearch/atom?name=S2A_OPER_PRD_MSIL1C_PDMC_20160801T072514_R073_V20160801T000734_20160801T000734

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&orbitNumber=005790

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&orbitNumber=073

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&sensorMode=INS-NOBS

http://opensearch.ceda.ac.uk/opensearch/atom?uid=876f2e35b75d645723642b3ef95571d5ea23691d

#### date

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&endDate=2016-08-20T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&startDate=2016-08-10T00:00:00.000Z&endDate=2016-08-20T00:00:00.000Z

#### bbox

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&bbox=1,1,90,90

#### polygon

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&geometry=POLYGON((30%2010,40%2040,20%2040,10%2020,30%2010)(29%2011,29%2028,11%2021,29%2011))

#### cloud

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&minCloudCoverPercentage=40

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&maxCloudCoverPercentage=50

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-2A&minCloudCoverPercentage=40&maxCloudCoverPercentage=50

### Sentinel 3

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&dataFormat=safe

http://opensearch.ceda.ac.uk/opensearch/atom?instrument=SLSTR

http://opensearch.ceda.ac.uk/opensearch/atom?mission=sentinel-3

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&orbitNumber=3905

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&orbitNumber=82

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&sensorMode=Earth Observation

#### date

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&startDate=2016-11-10T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&endDate=2016-11-20T00:00:00.000Z

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&startDate=2016-11-10T00:00:00.000Z&endDate=2016-11-20T00:00:00.000Z

#### bbox

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&bbox=1,1,90,90

#### polygon

http://opensearch.ceda.ac.uk/opensearch/atom?platform=sentinel-3A&geometry=POLYGON((30%2010,40%2040,20%2040,10%2020,30%2010)(29%2011,29%2028,11%2021,29%2011))

## Limitations

### Pagination

It is only possible to page through the first 10,000 results. This is due to limitations in the underlying elastic search. See [Deep Paging in Distributed Systems](https://www.elastic.co/guide/en/elasticsearch/guide/current/pagination.html) for an explanation.
