from arcgis import GIS
from arcgis.features import FeatureLayer
import arcpy
from os.path import exists
import json
from configparser import ConfigParser


ini_file = r"H:\Profile\myfile.ini"
if exists(ini_file):
    config = ConfigParser()
    config.read(ini_file)
    oracle_username = config["credentials"]["bcgw_username"]
    oracle_password = config["credentials"]["bcgw_password"]
    agol_username = config["credentials"]["agol_username"]
    agol_password = config["credentials"]["agol_password"]

arcpy.SignInToPortal("https://governmentofbc.maps.arcgis.com", agol_username, agol_password)
gis = GIS("https://governmentofbc.maps.arcgis.com", agol_username, agol_password, verify_cert=False)
now = gis.content.get('09a77ae6a66947668159bdc4de778829')

pep = now.layers[0]
where_clause = "PUBLIC_COMMENT_START_DATE is NOT NULL And PUBLIC_COMMENT_END_DATE is NULL"
results = pep.query(
    where = where_clause,
    as_df = False,
    return_all_records = False,
    out_fields = "MINE_NAME"

)
print(results)
with open(r'\\spatialfiles.bcgov\work\em\vic\mtb\Local\Applications\web_mapping\public_engagement_portal\documents\App_Development\CHEFS\NoW_mines_for_PEP.json', 'w') as file:
    file.write(str(results))




with open(r'\\spatialfiles.bcgov\work\em\vic\mtb\Local\Applications\web_mapping\public_engagement_portal\documents\App_Development\CHEFS\NoW_mines_for_PEP.json', 'r') as f:
    data = json.load(f)
mine_names_json = [
    {
        'OBJECTID':feature["attributes"]["OBJECTID"],
        'MINE_NAME': feature["attributes"]["MINE_NAME"]
    
        } 
        for feature in data["features"]
    
    ]
with open(r'\\spatialfiles.bcgov\work\em\vic\mtb\Local\Applications\web_mapping\public_engagement_portal\documents\App_Development\CHEFS\public_engagement_portal\mine_name.json', 'w') as outfile:
    json.dump(mine_names_json, outfile, indent=2)
