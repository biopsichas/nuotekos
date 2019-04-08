# coding=utf-8
#Script resamples monitoring results to data means and quartiles required for the assessment
import pandas as pd
import os, sys
import settings
working_dir = settings.working_dir
def prep_assessment_table():
    print ("Preparation of scenario assessment table script is started.")
    mod = pd.read_csv(working_dir + "/all_output_rch.csv", header = 0, index_col="CACHID")
    mod.sort_index(inplace=True)
    c = list(mod)
    c=c[1:-1]
    df = pd.DataFrame(index=mod.index, columns=c)
    c = c[:-1]
    for index, row in df.iterrows():
        df.set_value(index, "Q", mod.loc[index, "Q"])
        for i in c:
            if i != "BOD7":
                df.set_value(index, i, mod.loc[index, i])
            else:
                df.set_value(index, i, settings.BOD7_concentration)
    wwtp_ca_link = pd.read_csv(working_dir + "/wwtp_ca_link.csv", header = 0)
    wwtp_ca_link.sort_index(inplace=True)
    df.reset_index(inplace=True)
    df = pd.merge(wwtp_ca_link, df, on=['CACHID', 'CACHID'])
    filename = working_dir + "/q_wq_input_table.csv"
    if os.path.exists(filename):
        os.remove(filename)
    df.to_csv(filename, index=False, encoding='utf-8')
    del df
    print ("Preparation of scenario assessment table script is started. Results are saved q_wq_input_table.csv")
