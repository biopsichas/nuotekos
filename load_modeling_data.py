import os.path
import pandas as pd
import mod_to_results
pd.options.mode.chained_assignment = None
import settings
import sys
import gc
working_dir = settings.working_dir
def mod_data_prep():
    print ("Modeling data preparation script is started.")
    f = open("basin_file.txt", "r")
    columns = ["RCH","GIS","MON","AREAkm2","FLOW_INcms", "FLOW_OUTcms" ,"EVAPcms", "TLOSScms",  "SED_INtons",
               "SED_OUTtons", "SEDCONCmg/kg", "ORGN_INkg", "ORGN_OUTkg", "ORGP_INkg", "ORGP_OUTkg", "NO3_INkg",
               "NO3_OUTkg", "NH4_INkg", "NH4_OUTkg", "NO2_INkg", "NO2_OUTkg", "MINP_INkg", "MINP_OUTkg", "CHLA_INkg",
               "CHLA_OUTkg", "CBOD_INkg", "CBOD_OUTkg", "DISOX_INkg", "DISOX_OUTkg", "SOLPST_INmg", "SOLPST_OUTmg",
               "SORPST_INmg", "SORPST_OUTmg", "REACTPSTmg", "VOLPSTmg", "SETTLPSTmg", "RESUSP_PSTmg", "DIFFUSEPSTmg",
               "REACBEDPSTmg", "BURYPSTmg", "BED_PSTmg", "BACTP_OUTct", "BACTLP_OUTct", "CMETAL#1kg", "CMETAL#2kg",
               "CMETAL#3kg", "TOT Nkg","TOT Pkg", "NO3ConcMg/l", "WTMPdegc"]
    all_tables = pd.DataFrame()
    links = pd.read_csv(working_dir + "/link_mon_to_model_table.csv", index_col=["GRIDCODE"])
    links.index.names = ['RCH']
    for number, x in enumerate(f):
        file_path = settings.SWAT_setup_dir + x.rstrip() + settings.SWAT_setup_folder
        if os.path.exists(file_path+"/output.rch"):
            df = pd.read_csv(file_path+"/output.rch", sep = '\s+', header = 2, names=columns, usecols = range(1,51))
            ls = df.RCH.unique()
            dates = pd.date_range(start=settings.starting_date, end=settings.ending_date, name="Dates")
            df_recombined = pd.DataFrame()
            for i in ls:
                dfr = df[df["RCH"] == i]
                dfr = dfr.iloc[:dates.size]
                dfr["Dates"] = dates
                if i == 1:
                    df_recombined = dfr
                else:
                    df_recombined = df_recombined.append(dfr)
            df_recombined["Setup"] = x.rstrip()
            df_recombined = df_recombined.set_index(['RCH', 'Dates'])
        df_results = mod_to_results.mod_results(df_recombined)
        df_results["Setup"] = x.rstrip()
        links_extracted = links[links["Setup"] == x.rstrip()]
        df_results = pd.concat([df_results, links_extracted["CACHID"]], axis=1)
        if all_tables.empty:
            all_tables = df_results
        else:
            all_tables = all_tables.append(df_results)
        print (x.rstrip() + " done" + " number " + str(number+1) + " out of 106")
        gc.collect()
    filename = working_dir + "/all_output_rch.csv"
    if os.path.exists(filename):
        os.remove(filename)
    all_tables.to_csv(filename, encoding='utf-8')
    del all_tables, df_results, df_recombined, dfr
    print ("Modeling data preparation script is finished. Results are saved in all_output_rch.csv")
