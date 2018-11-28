import arcpy
from arcpy import env

# set spacial reference
spRef = arcpy.SpatialReference('WGS84 ARC System Zone 18')
env.workspace = 'C:/workspace/results'

out_station = 'station_point'
arcpy.MakeXYEventLayer_management(station_table, '经度（E）', '纬度（N）', out_station, spRef)

from arcpy.sa import *
raster_table = 'C:/workspace/output_shp/r1_day1_wsp5'
station_table = 'C:/workspace/3shps/污染物站点.shp'
ExtractValuesToPoints(station_table, raster_table ,
                      "result1","INTERPOLATE",
                      "VALUE_ONLY")