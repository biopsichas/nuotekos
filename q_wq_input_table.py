# coding=utf-8
#Script resamples monitoring results to data means and quartiles required for the assessment
import pandas as pd
import os, sys
import settings
working_dir = settings.working_dir
def prep_assessment_table():
    print ("Preparation of assessment table script is started.")
    link_table = pd.read_csv(working_dir + "/link_mon_to_model_table.csv", header = 0, usecols = ["CACHID","Q_ST_ID", "WQ_ST_ID"])
    link_table=link_table.set_index("CACHID")
    link_table.sort_index(inplace=True)
    mod = pd.read_csv(working_dir + "/all_output_rch.csv", header = 0, index_col="CACHID")
    mod.sort_index(inplace=True)
    mon_wq = pd.read_csv(working_dir + "/WQ.csv", header = 0, index_col="Station")
    mon_wq = mon_wq.rename(columns={'NO3-N': 'NNO3', 'N total': 'NTOT', 'PO4-P': 'PPO4', 'P total': 'PTOT', 'NH4-N': 'NNH4'})
    mon_wq.sort_index(inplace=True)
    mon_q = pd.read_csv(working_dir + "/Q.csv", header = 0, index_col="STAT")
    mon_q.sort_index(inplace=True)
    c = list(mod)
    c=c[1:-1]
    df = pd.DataFrame(index=mod.index, columns=c)
    c = c[:-1]
    for index, row in df.iterrows():
        if pd.isnull(link_table.loc[index, "Q_ST_ID"]):
            df.set_value(index, "Q", mod.loc[index, "Q"])
        else:
            df.set_value(index, "Q", mon_q.loc[link_table.loc[index, "Q_ST_ID"], "Q"])
        for i in c:
            if i != "BOD7":
                df.set_value(index, i, mod.loc[index, i])
            else:
                df.set_value(index, i, mon_wq["BOD7"].median())
        if pd.notnull(link_table.loc[index, "WQ_ST_ID"]):
            for i in c:
                if link_table.loc[index, "WQ_ST_ID"] in mon_wq.index:
                    if pd.notnull(mon_wq.loc[link_table.loc[index, "WQ_ST_ID"], i]):
                        df.set_value(index, i, mon_wq.loc[link_table.loc[index, "WQ_ST_ID"], i])
    wwtp_ca_link = pd.read_csv(working_dir + "/wwtp_ca_link.csv", header = 0)
    wwtp_ca_link.sort_index(inplace=True)
    df.reset_index(inplace=True)
    df = pd.merge(wwtp_ca_link, df, on=['CACHID', 'CACHID'])
    filename = working_dir + "/q_wq_input_table.csv"
    if os.path.exists(filename):
        os.remove(filename)
    df.to_csv(filename, index=False, encoding='utf-8')
    del df
    print ("Preparation of assessment table script is started. Results are saved q_wq_input_table.csv")
