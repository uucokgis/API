import os.path

import geopandas as gpd
import arcpy

arcpy.MakeFeatureLayer_management

shp_folder = r"C:\Users\l4712\PycharmProjects\iettProject\RaporOrnekleri"

ba_raporu_gdf = gpd.read_file(os.path.join(shp_folder, "BARaporu.shp"))
ba_raporu_gdf.to_wkt().to_excel(os.path.join(shp_folder, "BARaporu.xlsx"))

durak_coord_gdf = gpd.read_file(os.path.join(shp_folder, "DurakCoord.shp"))
durak_coord_gdf.to_wkt().to_excel(os.path.join(shp_folder, "DurakCoord.xlsx"))

durakhb_garaj_gdf = gpd.read_file(os.path.join(shp_folder, "DurakHBGarajRota.shp"))
durak_coord_gdf.to_wkt().to_excel(os.path.join(shp_folder, "DurakHBGarajRota.xlsx"))

durakhb_gar_gdf = gpd.read_file(os.path.join(shp_folder, "DurakHBGarRota.shp"))
durak_coord_gdf.to_wkt().to_excel(os.path.join(shp_folder, "DurakHBGarRota.xlsx"))

