# coding=utf-8
#Script transforms point source cleaned table
import pandas as pd
import sys, os
import numpy as np
import warnings, time
import settings
import math
warnings.filterwarnings("ignore", category=RuntimeWarning)
#####Importing data
working_dir = settings.working_dir
def eval_for_new_rules(file_name):
    print ("Evaluation WWTPs for new rules script is started")
    wwtp = pd.read_csv(working_dir + "/000_table.csv", header=0, low_memory=False)
    q_wq_data = pd.read_csv(working_dir + "/q_wq_input_table.csv", header=0, low_memory=False)
    q_wq_data.rename(columns={'NNO3': 'NO3', 'NTOT': 'Ntot', 'PPO4': 'PO4', 'PTOT': 'Ptot', 'NNH4': 'NH4'}, inplace=True)
    ##Setting parameters
    C_up_dlk = settings.C_up_dlk
    Q_init = settings.Q_init
    Year_to_start = settings.Year_to_start
    #####################################################
    ###Methodology
    ###1. Filtering point sources
    print ("Totally there are " + str(len(wwtp.PS_CODE.unique())) + " point sources,")
    wwtp = wwtp[((wwtp["Discharge"]>((365.25*Q_init)/1000))|(wwtp["GE"]>settings.GE_min))&(wwtp["PTYPE"].isin(settings.wwtp_types))]
    # wwtp = wwtp[(wwtp["Discharge"] > ((365.25 * Q_init) / 1000)) & (wwtp["PTYPE"].isin(settings.wwtp_types))]
    wwtp_codes = wwtp.PS_CODE.unique()
    print ("of them " + str(len(wwtp_codes)) + " were selected."+ "\n")
    final_p = pd.DataFrame()
    wwtp["NO3_Ntot"] = wwtp["NO3"] / wwtp["Ntot"]
    NO3_Ntot = wwtp[(wwtp["NO3_Ntot"]>0)&(wwtp["NO3_Ntot"]<=1)]["NO3_Ntot"].mean()
    wwtp["NH4_Ntot"] = wwtp["NH4"] / wwtp["Ntot"]
    NH4_Ntot = wwtp[(wwtp["NH4_Ntot"]>0) & (wwtp["NH4_Ntot"]<=1)]["NH4_Ntot"].mean()
    wwtp["PO4_Ptot"] = wwtp["PO4"] / wwtp["Ptot"]
    PO4_Ptot = wwtp[(wwtp["PO4_Ptot"]>0) & (wwtp["PO4_Ptot"]<=1)]["PO4_Ptot"].mean()
    wwtp.drop(["NO3_Ntot", "NH4_Ntot", "PO4_Ptot"], axis=1, inplace=True)
    ###2. Loop for each point sources
    for c, i in enumerate(wwtp_codes):
        ### Output precantage counter
        if c%((len(wwtp_codes)-1)/100) == 0:
            sys.stdout.write("\r" + (str(np.round(float(c)/float(len(wwtp_codes)-1)*100,1)) + " % evaluated" + " " + ">"*int(c/(len(wwtp_codes)/10))))
            sys.stdout.flush()
            time.sleep(0.2)
        if c==len(wwtp_codes)-1:
            sys.stdout.write("\r"+ "100 % evaluated" + " " + ">"*int(c/(len(wwtp_codes)/10)))
            sys.stdout.flush()
            time.sleep(0.2)
        ### 3. Select last years for each point sources and aggregate on last years
        wwtp_1 = wwtp[(wwtp["PS_CODE"] == i)]
        wwtp_1 = wwtp[(wwtp["PS_CODE"] == i) & (wwtp["Year"] > Year_to_start-1)]
        wwtp_1 = wwtp_1.groupby('Year').agg({'PS_CODE': 'first','X': 'first','Y': 'first',
                                             'River': 'first', 'Discharge': 'sum', 'BOD7': 'mean','NH4':
                                                 'mean','NO3': 'mean','Ntot': 'mean','PO4': 'mean','Ptot': 'mean', 'GE':'mean', 'GE_class':'last'})
        wwtp_1c = wwtp_1.groupby('PS_CODE').agg({'BOD7': 'mean', 'NH4': 'mean', 'NO3': 'mean', 'Ntot': 'mean', 'PO4': 'mean',
                                                'Ptot': 'mean', 'Discharge': 'mean', 'GE':'mean', 'GE_class':'median'})
        if wwtp_1c.empty:
            continue
        wwtp_1 =wwtp_1c.to_dict(orient = "list")
        ### 4. Extracting data of river water quality for each point source
        q_wq_data_1c = q_wq_data[(q_wq_data["PS_CODE"] == i)]
        q_wq_data_1 = q_wq_data_1c.drop(['PS_CODE', 'CACHID'], axis=1)
        q_wq_data_1c.set_index("PS_CODE", inplace=True)
        if q_wq_data_1.empty:
            continue
        C_up = q_wq_data_1.to_dict(orient="list")
        ### 5. Setting dataframes
        p_final = pd.DataFrame(columns=list(C_up_dlk.keys()))
        pv_final = pd.DataFrame(columns=list(C_up_dlk.keys()))
        wwtp_q = (wwtp_1['Discharge'][0] * 1000) / (365.25 * 24 * 60 * 60)
        GE = wwtp_1["GE"][0]
        if GE > 100000:
            N_floor = settings.N_floor_100000
            P_floor = settings.P_floor_100000
            BOD_floor = settings.BOD_floor_100000
            N_ceilings = settings.N_ceilings_100000
            P_ceilings = settings.P_ceilings_100000
            BOD_ceilings = settings.BOD_ceilings_100000
        elif 10000 < GE <=100000:
            N_floor = settings.N_floor_10000
            P_floor = settings.P_floor_10000
            BOD_floor = settings.BOD_floor_10000
            N_ceilings = settings.N_ceilings_10000
            P_ceilings = settings.P_ceilings_10000
            BOD_ceilings = settings.BOD_ceilings_10000
        else:
            N_floor = settings.N_floor
            P_floor = settings.P_floor
            BOD_floor = settings.BOD_floor
            N_ceilings = settings.N_ceilings
            P_ceilings = settings.P_ceilings
            if GE < 2000:
                BOD_ceilings = settings.BOD_ceilings
            else:
                BOD_ceilings = settings.BOD_ceilings_2000
        NO3_floor = NO3_Ntot * N_floor
        NH4_floor = NH4_Ntot * N_floor
        PO4_floor = PO4_Ptot * P_floor
        NO3_ceilings = NO3_Ntot * N_ceilings
        NH4_ceilings = NH4_Ntot * N_ceilings
        PO4_ceilings = PO4_Ptot * P_ceilings
        for key in C_up_dlk:
            if C_up_dlk[key]> C_up[key][0]:
                C_nuot = (((C_up_dlk[key] + C_up[key][0]) / 2) * (C_up['Q'][0] + wwtp_q) - C_up[key][0] * C_up['Q'][0]) / wwtp_q
            else:
                C_nuot = C_up_dlk[key]
            if key == "BOD7":
                if C_nuot < BOD_floor:
                    C_nuot = BOD_floor
                if C_nuot > BOD_ceilings:
                    C_nuot = BOD_ceilings
            if key == "Ntot":
                if C_nuot < N_floor:
                    C_nuot = N_floor
                if C_nuot > N_ceilings:
                    C_nuot = N_ceilings
            if key == "Ptot":
                if C_nuot < P_floor:
                    C_nuot = P_floor
                if C_nuot > P_ceilings:
                    C_nuot = P_ceilings
            if key == "NO3":
                if C_nuot < NO3_floor:
                    C_nuot = NO3_floor
                if C_nuot > NO3_ceilings:
                    C_nuot = NO3_ceilings
            if key == "NH4":
                if C_nuot < NH4_floor:
                    C_nuot = NH4_floor
                if C_nuot > NH4_ceilings:
                    C_nuot = NH4_ceilings
            if key == "PO4":
                if C_nuot < PO4_floor:
                    C_nuot = PO4_floor
                if C_nuot > PO4_ceilings:
                    C_nuot = PO4_ceilings
            if C_nuot <= wwtp_1[key][0]:
                value = 1
            elif  math.isnan(wwtp_1[key][0]):
                value = np.nan
            else:
                value = 0
            p_final.set_value(i, key, value)
            pv_final.set_value(i, key, C_nuot)
        p_final["count"] = p_final.sum(axis=1, skipna= True)
        p_final["PS_CODE"] = i
        l1 = [c1 + "_OUT" for c1 in list(wwtp_1c)]
        l2 = [c2 + "_PERMIT" for c2 in list(pv_final)]
        l3 = [c3 + "_WQ_RI" for c3 in list(q_wq_data_1c)]
        l4 = [c4 + "_EVAL" for c4 in list(p_final)]
        cols = list(pv_final)
        pv_final[cols] = pv_final[cols].apply(pd.to_numeric, errors='coerce', axis=1)
        p_final = pd.concat([np.round(wwtp_1c, 2), np.round(pv_final, 2), np.round(q_wq_data_1c, 2), p_final], axis = 1)
        p_final.columns = l1+l2+l3+l4
        cols2 = list(p_final)
        cols2.insert(0, cols2.pop(cols2.index('PS_CODE_EVAL')))
        cols2.insert(1, cols2.pop(cols2.index('CACHID_WQ_RI')))
        cols2.insert(2, cols2.pop(cols2.index('GE_OUT')))
        cols2.insert(3, cols2.pop(cols2.index('GE_class_OUT')))
        p_final = p_final.ix[:, cols2]
        final_p = final_p.append(p_final)
    c = float(final_p["count_EVAL"].count())
    print ("\n"+ "\n" + str(np.round(float(final_p[final_p["count_EVAL"]>0]["count_EVAL"].count())/c,3)*100) +
           " % bent vienas")
    print ("\n"+ str(np.round(float(final_p[final_p["PO4_EVAL"] > 0]["PO4_EVAL"].count()) / final_p["PO4_EVAL"].dropna().count(), 3) * 100) +
           " % PO4")
    print (str(np.round(float(final_p[final_p["Ptot_EVAL"] > 0]["Ptot_EVAL"].count()) / final_p["Ptot_EVAL"].dropna().count(), 3) * 100) +
           " % Ptot")
    print (str(np.round(float(final_p[final_p["NH4_EVAL"] > 0]["NH4_EVAL"].count()) / final_p["NH4_EVAL"].dropna().count(), 3) * 100) +
           " % NH4")
    print (str(np.round(float(final_p[final_p["NO3_EVAL"] > 0]["NO3_EVAL"].count()) / final_p["NO3_EVAL"].dropna().count(), 3) * 100) +
           " % NO3")
    print (str(np.round(float(final_p[final_p["Ntot_EVAL"] > 0]["Ntot_EVAL"].count()) / final_p["Ntot_EVAL"].dropna().count(), 3) * 100) +
           " % Ntot")
    print (str(np.round(float(final_p[final_p["BOD7_EVAL"] > 0]["BOD7_EVAL"].count()) / final_p["BOD7_EVAL"].dropna().count(), 3) * 100) +
           " % BOD7")
    filename = working_dir + "/" + file_name + ".csv"
    if os.path.exists(filename):
        os.remove(filename)
    final_p.to_csv(filename, index=False, encoding='utf-8')
    del final_p, p_final, pv_final
    print ("\n"+ "Script is finished")
    print ("Evaluation WWTPs for new rules script is finished. Results are saved in " + file_name + ".csv")
