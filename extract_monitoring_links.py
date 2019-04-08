# coding=utf-8
import pandas as pd
import os
import arcpy
import re
import settings
working_dir = settings.working_dir
def extract_m_links():
    print ("Extracting monitoring links script is started.")
    workspace = working_dir + "/GIS/PSDATA.gdb"
    arcpy.env.workspace = workspace
    arcpy.env.outputCoordinateSystem = arcpy.SpatialReference(3346)
    ### Extracting dataframe table of modeling system configuration of basins and reaches
    y = list()
    cur = arcpy.UpdateCursor('bc')
    for row in cur:
        x1 = row.getValue('Subbasin')
        x2 = row.getValue('Setup_name')
        x3 = row.getValue('GRIDCODE')
        x4 = row.getValue('cach_id')
        y.append([x1, x2, x3, x4])
    df = pd.DataFrame(y, columns=["Subbasin", "Setup_name","GRIDCODE", "CACHID"])
    df = df.reindex(columns = ["Subbasin", "Setup_name","GRIDCODE", "CACHID", "Q_ST_ID", "WQ_ST_ID", "Q_MULT", "WQ_MULT"])
    df=df.set_index(["Subbasin", "Setup_name","GRIDCODE"]).sort_index()
    ###Reading links between monitoring data and model from prepared paicswat.ini file
    with open(working_dir + '\Scripts\paicswat.ini', 'r') as f:
        x = f.readlines()
        ###Writing patterns to find different values in text file
        p_Subbasin =r'(?<=name = ).[^_]*'
        p_Setup_name = r'(?<=_).*'
        p_GRIDCODE_q = r'(?<=qreachnr = ).*'
        p_stID_q = r'(?<=qstationid = ).*'
        p_qstationmult = r'(?<=qstationmult = ).*'
        p_GRIDCODE_wq = r'(?<=wqreachnr = ).*'
        p_stID_wq = r'(?<=wqstationid = ).*'
        p_wqstationmult=r'(?<=wqstationmult = ).*'
        p_values = '\d+'
        p_decimals = '\d+\.\d+'
        p_end_point = r'(?<=wqvalid = ).*'
        ###Finding and extracting values from text file
        for i in x:
            Subbasin = re.search(p_Subbasin, i)
            GRIDCODE_q = re.search(p_GRIDCODE_q, i)
            stID_q = re.search(p_stID_q, i)
            qstationmult = re.search(p_qstationmult, i)
            end_point = re.search(p_end_point, i)
            if Subbasin:
                Setup_name = re.search(p_Setup_name, i)
                Subbasin_v = Subbasin.group()
                Setup_name_v = Setup_name.group()
            elif GRIDCODE_q:
                GRIDCODE_wq = re.search(p_GRIDCODE_wq, i)
                if GRIDCODE_wq:
                    GRIDCODE_wq_v = re.findall(p_values, GRIDCODE_wq.group())
                else:
                    GRIDCODE_q_v = re.findall(p_values, GRIDCODE_q.group())
            elif stID_q:
                stID_wq = re.search(p_stID_wq, i)
                if stID_wq:
                    stID_wq_v = re.findall(p_values, stID_wq.group())
                else:
                    stID_q_v = re.findall(p_values, stID_q.group())
            elif qstationmult:
                wqstationmult = re.search(p_wqstationmult, i)
                if wqstationmult:
                    wqstationmult_v = re.findall(p_decimals, wqstationmult.group())
                else:
                    qstationmult_v = re.findall(p_decimals, qstationmult.group())
            elif end_point:
                for cg, g_v in enumerate(GRIDCODE_q_v):
                    df.set_value((Subbasin_v, Setup_name_v, int(g_v)), "Q_ST_ID", int(stID_q_v[cg]))
                    df.set_value((Subbasin_v, Setup_name_v, int(g_v)), "Q_MULT", float(qstationmult_v[cg]))
                for cwg, wq_v in enumerate(GRIDCODE_wq_v):
                    df.set_value((Subbasin_v, Setup_name_v, int(wq_v)), "WQ_ST_ID", int(stID_wq_v[cwg]))
                    df.set_value((Subbasin_v, Setup_name_v, int(wq_v)), "WQ_MULT", float(wqstationmult_v[cwg]))
    df=df.reset_index(level=[0,1], drop=False)
    df["Setup"] = df["Subbasin"]+'/'+ df["Setup_name"]
    filename = working_dir + "/link_mon_to_model_table.csv"
    if os.path.exists(filename):
        os.remove(filename)
    df.to_csv(filename, encoding='utf-8')
    del df
    print ("Extracting monitoring links script is finished. Results are saved in link_mon_to_model_table.csv")
