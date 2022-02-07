import re
from pprint import pprint

import pandas as pd
from collections import Counter
from polyleven import levenshtein
from osgeo.osr import SpatialReference, CoordinateTransformation
import time
pd.options.display.max_columns = None
pd.options.display.max_rows = None


# Read the county and town land csv files and store it in df_counties and df_town Data frame.
col = ['OBJECTID', 'County', 'Contae', 'English_Name', 'Irish_Name', 'ITM_E', 'ITM_N']
df_counties = pd.read_csv("Dataset/Counties_-_OSi_National_Placenames_Gazetteer.csv", usecols=col)
df_town = pd.read_csv("Dataset/Townlands_-_OSi_National_Placenames_Gazetteer.csv", usecols=col)


# Data Preprocessing. Convert all strings to lower case.
for column in ['County', 'Contae', 'English_Name', 'Irish_Name']:
    df_counties[column] = df_counties[column].str.lower()
    df_town[column] = df_town[column].str.lower()


# New dataframe containing no special character names.
df_town['english_name_'] = df_town['English_Name'].replace(r'\W+', ' ', regex=True)


# Figure out top 50 common words like east, west, north, demense, etc. and store in common.
common = []
for names in df_town['english_name_'].str.split():
    if len(names) > 1:
        common.extend(names[1:])
dictionary = Counter(common)
common = list(list(zip(*dictionary.most_common(50)))[0])


# Take a input from user and parse it, the same way townlands in dataFrame are parsed.
input_address = 'East Rath  Road, Fermoy, cork'.lower()
input_address_list = re.findall(r"[\w']+", input_address)
input_address = ' '.join(input_address_list)

print(input_address)
# Store matched string in this dictionary.


address_dict = {"objectid": [],
                "townland": [],
                "county": [],
                "irish_county": [],
                "itm_e": [],
                "itm_n": []}


# Searching for County.
for word in input_address_list:
    # The county Louth matches with South, More with Cork. So take care.
    if word in common:
        continue
    leven = df_counties.apply(lambda x: levenshtein(x['County'], word) < 2, axis=1)
    county_df = df_counties[leven.values]
    # county_df = df_counties[(df_counties['County'] == word) | (df_counties['Contae'] == word)]
    if not county_df.empty:
        break


def populate_dict():
    address_dict['county'].append(county_df.values[0][1])
    address_dict['irish_county'].append(county_df.values[0][2])
    address_dict['itm_e'].append(county_df.values[0][5])
    address_dict['itm_n'].append(county_df.values[0][6])


# Town DataFrame where county = 'X. Used to narrow search.
if not county_df.empty:

    town = df_town[(df_town['County'] == county_df.values[0][1])
                   | (df_town['Contae'] == county_df.values[0][2])]
else:
    town = df_town


for word in input_address_list:
    # if word is a common word, don't search it.
    if word in common:
        continue

    # Search for county X and it's variants(x south, x beg, etc).
    town_df = town[town["english_name_"].str.contains(fr'\b{word}\b', regex=True, case=False)]

    if not town_df.empty:
        max_len = 0
        # We know County x exists. Check for a much closer match.
        for item in town_df.values:
            if (item[7] in input_address or ' '.join(reversed(item[7].split(' '))) in input_address)\
                    and len(item[7]) > max_len:

                max_len = len(item[7])
                townland = item
        if 'townland' in locals():
            if townland[0] not in address_dict['objectid']:
                address_dict['objectid'].append(townland[0])
                address_dict['county'].append(townland[1])
                address_dict['townland'].append(townland[3])
                address_dict['itm_e'].append(townland[5])
                address_dict['itm_n'].append(townland[6])

# Check for an empty value.
if not address_dict["townland"]:
    populate_dict()


# gdal Convert ITM to Lat. Long
def convert_coordinates():

    epsg2157 = SpatialReference()
    epsg2157.ImportFromEPSG(2157)

    epsg4326 = SpatialReference()
    epsg4326.ImportFromEPSG(4326)

    itm2lat_lon = CoordinateTransformation(epsg2157, epsg4326)
    lat_lon2rd = CoordinateTransformation(epsg4326, epsg2157)
    return itm2lat_lon.TransformPoint(address_dict['itm_e'][0], address_dict['itm_n'][0])


pprint(address_dict)
print(convert_coordinates())
