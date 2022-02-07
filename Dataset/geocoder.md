# Geocoder

## Summary

This task is to design and build a geocoder for Irish addresses.

What a geocoder does is takes an address, such as

    Johnstown, Bennekerry, Co Carlow
    
and turns it into GPS co-ordinates like

    52.82089152866102,-6.868629101436554

As Ireland has only recently adopted postal codes, this is quite a hard problem, but also quite a common one.

## Background

Addresses in Ireland are generally formatted as such:

```
    Resident Name,
    Road or Local Area Name,
    Townland,
    Town/City,
    County
```
So in reverse order of magnitude:

'counties' are provinces in Ireland, spanning potentially several hundred kilometres square. 

'town/cities' are centers of population, that may contain several townlands. 

'townlands' are much smaller areas, usually named after the nearest town or city to a location, approximately dozens of kilometres squared.

'road' is the typically the road the location is on.

'local area name' may be a colloquial name for a location, usually very small.

'resident name' is the name of the resident of the location. This will not be included in the addresses we need to code.

You'll notice a lack of postcodes. Ireland is unique in the fact that it has not adopted postcodes until very recently. The only place in Ireland that has had postcodes previous to this is Dublin City, which has 25 postcodes, [listed here](https://en.wikipedia.org/wiki/List_of_Dublin_postal_districts).

Not all addresses will have all the fields. Generally, at least 1 of Road/Local area name, Townland, or Town/City are required, but reall addresses may have all of them.  None of the addresses in our test set have postcodes, and we've excluded Dublin addresses from our test set due to the added complexity.

Addresses in the test set are mostly separated by commas, but it's not guaranteed.  Addresses may be spelled correctly, but it's not guaranteed. 

## Datasets

There are several datasets licensed under CC-BY from Ordnance Survey Ireland, called the Placenames Gazetteer, that are useful for this problem. They're listed below. These datasets are lists of placenames and their centroid (ie, their co-ordinates).

Each dataset has a slightly different resolution - that is, the 'counties' dataset has the centroid for each county, while the 'townlands' dataset has centroids for towns and surrounding areas. 
* https://data.gov.ie/dataset/townlands-osi-national-placenames-gazetteer3
* https://data.gov.ie/dataset/counties-osi-national-placenames-gazetteer2

These two above are the most useful. The following are here for completion but are less likely to be useful for this specific task.
The population dataset has some larger towns and cities that contain multiple townlands which will appear in real addresses, where the barionies, electoral district and local authorities are not likely to show up in an address.
* https://data.gov.ie/dataset/centres-of-population-osi-national-placenames-gazetteer1
* https://data.gov.ie/dataset/baronies-osi-national-placenames-gazetteer2
* https://data.gov.ie/dataset/electoral-districts-osi-national-placenames-gazetteer3
* https://data.gov.ie/dataset/local-authorities-osi-national-placenames-gazetteer2

These are available as GeoJson, CSV, and KML. You may use any format, depending on your solution. You may want to examine all of the formats before choosing.

Within the datasets, the field named `English_Name` is the most likely to be useful for matching your address. As Ireland is a bilingual country, there is also an `Irish_Name` field, as well as an `Alternative Name` field for some locations that have multiple accepted spellings of English names. The CSV contains coordinates in a projection called Irish Transverse Mercator (EPSG:2157), labeled `ITM_E` and `ITM_N`.  Those coordinates can be converted to the usual GPS coordinates (EPSG:4326) using gdal (https://gdal.org/programs/ogr2ogr.html), proj, or other open source software. The GeoJson and KML formats contain all of the attributes from the CSV, in addition to the EPSG:4326 Lat/Lon coordinates.

We will supply you with a list of addresses to test against, in a file called `addresses_for_task.csv`.

## Objective

We're not expecting a fully-functional, high-performance, super-accurate geocoder from you :)

What we would like to see is a document explaining _how_ you would build this, and a proof-of-concept. As this is a coding challenge, we would like your solution to have more than a hundred lines of your own code, so balance your document and your proof-of-concept. Your document should include an exploration of advantages and disadvantages of your approach.

Ideally, your proof-of-concept would have a HTTP API, but command-line solutions or libraries are acceptable as well.

Ideally, your proof-of-concept would be able to at least code an address to the county level.

## Requirements

Please use either Python or Javascript for your proof-of-concept.

You may use whatever libraries or tools you like, _except_ if they do the geocoding for you. For instance, using a library to parse addresses into a more usable format is fine, but using OpenStreetMaps' geocoder is not.
