import arcpy
from arcpy import env
import xlrd
import os
from collections import defaultdict
import glob

# make path
os.chdir('C:/workspace/data')
env.workspace = 'C:/workspace/output_shp'
out_path = env.workspace

# read files
files = glob.glob("*.xls")


# prepare names and types fields
names = ['no','long','lat']
types = ['FLOAT','FLOAT','FLOAT']
# Function: create name fields
def adf(fields):
    for field in fields:
        for i in range(24):
            names.append(field+str(i+1))
            types.append('FLOAT')
            
adf(['temp','pre','hum','wsp'])
day_count = 0
for file in files:
    day_count += 1
    # prepare data
    excel = xlrd.open_workbook(file)
    table = excel.sheets()[0]
    nrows = table.nrows
    ncols = table.ncols
    data = defaultdict(list)
    # add data to dictionary
    for name_id in range(len(names)):
        for value_id in range(1,nrows):
            value = table.cell(value_id,name_id).value
            if value == '':
                value = None
            data[names[name_id]].append(value)
    # Execute CreateFeatureclass
    arcpy.CreateFeatureclass_management(out_path,'day%d.shp'%(day_count))
    in_table = os.path.join(out_path,'day%d.shp'%(day_count))
    for i in range(len(names)):
        arcpy.AddField_management(in_table,names[i],types[i])
    rows = arcpy.InsertCursor(in_table)
    for i in range(nrows-1):
        stat = rows.newRow()
        print("generating no.%d record:"%(i+1))
        for name in names:
            stat.setValue(name,data[name][i])
            print("-------generating field:",name)
        rows.insertRow(stat)
        print("@@  sucessed for no.%d record !"%(i+1))
    print('********************** finish day%d.shp ***************************'%(day_count))