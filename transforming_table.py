# coding=utf-8
#Script transforms point source cleaned table
import pandas as pd
import os
import numpy as np
import settings
working_dir = settings.working_dir
def transform_table():
    print ("Transforming table script is started.")
    df0 = pd.read_csv(working_dir + "/000_PointSources_ins.csv", header=0, low_memory=False)
    df0['UNIPSCODE'] = df0.apply(lambda row: str(row['Year'])[:4] +"_"+ str(row['PS_CODE'])[:7], axis=1)
    df = df0.pivot_table(index=['UNIPSCODE','PS_CODE','Name', 'Year', 'Y','X', 'River', 'PTYPE', "Discharge"], columns="Nutrient",
                        values="Concentration", aggfunc=np.mean)
    wwtp = df0.pivot_table(index=['UNIPSCODE','PS_CODE','Name', 'Year', 'Y','X', 'River', 'PTYPE', "Discharge"], columns="Nutrient",
                        values="Concentration_in", aggfunc=np.mean)
    df = df.reset_index()
    wwtp = wwtp.reset_index()
    wwtp_q = (wwtp['Discharge'] * 1000) / (365.25 * 24 * 60 * 60)
    ###Calculation of GE
    wwtp_q_day = wwtp_q * 24 * 60 * 60
    BOD7GE = (wwtp["BOD7"] * wwtp_q_day / 70)  # .item()
    NtotGE = (wwtp["Ntot"] * wwtp_q_day / 12)  # .item()
    PtotGE = (wwtp["Ptot"] * wwtp_q_day / 2.7)  # .item()
    GE = pd.concat([BOD7GE, NtotGE, PtotGE], axis=1)
    GE = GE.max(axis=1)
    wwtp["GE"] = GE.round(decimals=0)
    wwtp["GE_class"] = 1
    wwtp.loc[wwtp["GE"] >= 100000, "GE_class"] = 3
    wwtp.loc[(wwtp["GE"] >= 10000) & (wwtp["GE"] < 100000), "GE_class"] = 2
    df["GE"] = wwtp["GE"]
    df["GE_class"] = wwtp["GE_class"]
    filename = working_dir + "/000_table.csv"
    if os.path.exists(filename):
        os.remove(filename)
    df.to_csv(filename, encoding='utf-8')
    del df, df0, wwtp
    print ("Transforming table script is finished. Results is saved in 000_table.csv")