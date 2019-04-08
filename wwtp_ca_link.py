# coding=utf-8
#Script links WWTP codes to catchment IDs
import arcpy
import pandas as pd
import os
import settings
working_dir = settings.working_dir
workspace = working_dir + "/GIS/PSDATA.gdb"
arcpy.env.workspace = workspace
arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3346)
featureclasses = arcpy.ListFeatureClasses()
def wwtp_catchid_link():
    print ("WWTP to CATCHID script is started.")
    print ("Cleaning database")
    for i in featureclasses:
        if i == "ca" or i == "ri" or i == "bc":
            print (i + " layer transferred")
        else:
            arcpy.Delete_management(i)
    print ("Reading point source data and making into GIS layer")
    df = pd.read_csv(working_dir + "/000_table.csv", header=0, low_memory=False)
    arcpy.MakeXYEventLayer_management(working_dir + "/000_table.csv","X","Y", "psources")
    arcpy.CopyFeatures_management("psources", "ps")
    print ("Overlaying point source data  and catchment data")
    arcpy.SpatialJoin_analysis("ps", "ca", "ps_ca")
    y = list()
    cur = arcpy.UpdateCursor("ps_ca")
    for row in cur:
        x1 = row.getValue('PS_CODE')
        x2 = row.getValue('catchmentID')
        y.append([x1, x2])
    df = pd.DataFrame(y, columns=["PS_CODE", "CACHID"])
    df.drop_duplicates("PS_CODE", keep='first', inplace=True)
    filename = working_dir + "/wwtp_ca_link.csv"
    if os.path.exists(filename):
        os.remove(filename)
    df.to_csv(filename, index=False, encoding='utf-8')
    del df
    print ("WWTP to CATCHID script is finished. Results are saved in wwtp_ca_link.csv")
