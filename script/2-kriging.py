import os
import arcpy
from arcpy import env

os.chdir('C:/workspace/data')
env.workspace = 'C:/workspace/output_shp'
out_path = 'C:/workspace/output_shp'
prj_path = 'C:/workspace/output_shp'

# set spacial reference
spRef = arcpy.SpatialReference('WGS84 ARC System Zone 18')

# prepare names and types fields
names = []
# Function: create name fields
def adf(fields):
    for field in fields:
        for i in range(24):
            names.append(field+str(i+1))
          
adf(['temp','pre','hum','wsp'])

for i in range(1,3):
    day_count = i
    in_table = os.path.join(out_path,'day%d.shp'%(day_count))
    arcpy.DefineProjection_management(in_table, spRef)
    out_lyr = 'pp_day%d'%(day_count)
    arcpy.MakeXYEventLayer_management(in_table, 'long', 'lat', out_lyr, spRef)
    

    inFeatures = out_lyr
    for name in names:
        field = name
        out_raster = "r1_day%d_%s"%(day_count,name)
        kModel = 'Spherical'
        cell_size = 0.003758
        search_radius = 0.006418
        out_var = "v1_day%d_%s"%(day_count,name)
        # Execute Kriging
        try:
            arcpy.Kriging_3d(inFeatures, field, out_raster, kModel, 
                             cell_size, search_radius, out_var)
            print("success:day %d -- field %s"%(day_count,name))
        except:
            print("failed:day %d -- field %s"%(day_count,name))