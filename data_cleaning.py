# coding=utf-8
#Script takes yierly raw reported data and writes Small_point_sources.mdb info and yierly.txt info to be copied into
# actual files avoiding dublication and preparing into excact format needed
from unidecode import unidecode
import pandas as pd
import os, sys
import numpy as np
import settings
import warnings
warnings.filterwarnings("ignore", category=RuntimeWarning)
working_dir = settings.working_dir
# ##Getting data tables and combining them
def clean_lt_letters():
    print ("Cleaning of LT letters script is started")
    result = None
    for x in range (settings.start_year, settings.ending_year+1):
        tb = pd.read_csv(working_dir + "/Data/" + str(x) + ".csv", header=0, sep=';', encoding='ISO 8859-13', engine='python')
        if result is None:
            result = tb
        else:
            result = pd.concat([result, tb], ignore_index=True)
    ##Getting rid of Lithuanian letters
    ri = list()
    for i in list(result.columns.values):
        ri.append(unidecode(i))
    index_list=result.index.tolist()
    result1 = pd.DataFrame(index=index_list,columns = ri)
    for c in range (result.shape[1]):
        for i in range (result.shape[0]):
            r=result.iloc[i][c]
            if isinstance(r, float):
                r=str(r)
            elif isinstance(r, np.int64):
                r=r.astype('str')
            elif isinstance(r, np.string_):
                r=r.astype('str')
            result1.iloc[i][c] = unidecode(r)
        print ("column nb: " + str(c) + " processed out of " + str(result.shape[1]))
    filename = working_dir + "/000_Summary.csv"
    if os.path.exists(filename):
        os.remove(filename)
    result1.to_csv(filename, encoding='utf-8')
    del result1, result
    print ("Cleaning of LT letters script is finished. Results are saved in 000_Summary.csv")
##+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
##From here less computationlly difficult part after getting rid off Lithuanian letters
def data_clean():
    print ("Data cleaning script is started")
    dfi = pd.read_csv(working_dir + "/000_Summary.csv", header=0, low_memory=False)
    ##Writing values to new table
    dfi['Ukio subjekto kodas'] = dfi['Ukio subjekto kodas'].astype(str)
    dfi['Ukio subjekto kodas'] = dfi['Ukio subjekto kodas'].str[:9]
    df=pd.DataFrame(columns=['ID', 'Year', 'Name', 'Type', 'Nutrient', 'Concentration','Concentration_in', 'Unit', 'Discharge', 'Y','X',
                             'WWTP_CODE','OLD_WWTP_CODE', 'TID','River', 'PS_CODE', 'PTYPE'])
    df['Year']= dfi['Metai']
    df['Name']= dfi['Ukio subjekto kodas'] +" "+ dfi['Ukio subjekto pavadinimas']
    dfi["Isleistuvo koordinates (LKS'94)"] = dfi["Isleistuvo koordinates (LKS'94)"].str.replace(" ","")
    df['X']= dfi["Isleistuvo koordinates (LKS'94)"].str[:6]
    df['Y']= dfi["Isleistuvo koordinates (LKS'94)"].str[6:]
    df['WWTP_CODE']= dfi['NVI kodas']
    df['Discharge']=dfi['Nuoteku kiekis']
    df['Nutrient']=dfi['Tersalo pavadinimas']
    df['Concentration']=dfi['Vid. metine (laikotarpio)  koncentracija isleidziamose NT']
    df['Concentration_in'] = dfi['Vid. metine (laikotarpio) koncentracija pries valyma']
    df['Unit']=dfi['Koncentracijos matavimo vnt.']
    df['River']=dfi['Pavirsinio vandens telkinio pavadinimas']
    df['PS_CODE']=dfi['Isleistuvo kodas']
    df['PTYPE']=dfi['NVI Paskirtis']
    df.PTYPE.fillna('No info', inplace=True)
    # df['Discharge']= df['Discharge'].str.replace(",",".")
    # df['Concentration']= df['Concentration'].str.replace(",",".")
    ##Selecting only needed parameters and renaming them
    df = df[(df['Nutrient'] == 'Amonio azotas (NH4-N)') |
            (df['Nutrient'] == 'Amonis (NH4)') |
            (df['Nutrient'] == 'BDS5') |
            (df['Nutrient'] == 'BDS7') |
            (df['Nutrient'] == 'Bendrasis azotas') |
            (df['Nutrient'] == 'Bendrasis fosforas') |
            (df['Nutrient'] == 'Fosfatai (PO4)') |
            (df['Nutrient'] == 'Fosfatinis fosforas (PO4-P)') |
            (df['Nutrient'] == 'NH4 ir amonio druskos') |
            (df['Nutrient'] == 'Nitratai (NO3)') |
            (df['Nutrient'] == 'Nitratinis azotas (NO3-N)') |
            (df['Nutrient'] == 'Nitritai (NO2)') |
            (df['Nutrient'] == 'Nitritinis azotas (NO2-N)') |
            (df['Nutrient'] == 'Skendinciosios medziagos')]
    df.loc[(df['Nutrient']=='Amonio azotas (NH4-N)') |
       (df['Nutrient']=='Amonis (NH4)') |
       (df['Nutrient']=='NH4 ir amonio druskos'), 'Nutrient'] = 'NH4'
    df.loc[(df['Nutrient']=='Fosfatai (PO4)') |
       (df['Nutrient']=='Fosfatinis fosforas (PO4-P)'), 'Nutrient' ] = 'PO4'
    df.loc[(df['Nutrient']=='Nitritinis azotas (NO2-N)') |
       (df['Nutrient']=='Nitritai (NO2)'), 'Nutrient' ] = 'NO2'
    df.loc[(df['Nutrient']=='Nitratai (NO3)') |
       (df['Nutrient']=='Nitratinis azotas (NO3-N)'), 'Nutrient' ] = 'NO3'
    df.Concentration = df.Concentration.astype(float)
    df.loc[(df['Nutrient']=='BDS5'),'Concentration'] *= 1.15
    df.loc[(df['Nutrient']=='BDS5') |
       (df['Nutrient']=='BDS7') , 'Nutrient'] = 'BOD7'
    df.loc[(df['Nutrient']=='Bendrasis azotas'), 'Nutrient'] = 'Ntot'
    df.loc[(df['Nutrient']=='Bendrasis fosforas'), 'Nutrient'] = 'Ptot'
    df.loc[(df['Nutrient']=='Skendinciosios medziagos'), 'Nutrient'] = 'SS'
    df.loc[(df['Nutrient']=='NH4') |
            (df['Nutrient'] == 'NO2') |
            (df['Nutrient'] == 'NO3') |
            (df['Nutrient'] == 'Ntot') , 'Unit'] = "mgN/l"
    df.loc[(df['Nutrient']=='PO4') |
            (df['Nutrient'] == 'Ptot') , 'Unit'] = "mgP/l"
    df.loc[(df['Nutrient']=='BOD7'), 'Unit'] = "mgO2/l"
    df.loc[(df['Nutrient']=='SS'), 'Unit'] = "mg/l"
    df['Type']= dfi['Nuoteku valymo budai'] +" "+ dfi['Papildomo valymo budai']
    df.loc[(df['Type']=='mechaninis kitas (nurodyti)')|(df['Type']=='mechaninis filtravimas per smeli'),'Type'] = "100"
    df.loc[(df['Type']=='mechaninis, cheminis kitas (nurodyti)'),'Type'] = "200"
    df.loc[(df['Type'].isnull()),'Type'] = "0"
    df.loc[(df['Type']!="100")&(df['Type']!="200")&(df['Type']!="0"),'Type'] = "300"
    ##Cleaning coordinates
    WWTP = pd.read_csv(working_dir + '/Data/WWTP_Stations.sta', header=0, sep='\t')
    df['Y'] = pd.to_numeric(df.Y, errors='coerce', downcast='integer')
    df['X'] = pd.to_numeric(df.X, errors='coerce', downcast='integer')
    df.loc[(df['Y']<5983980) |
            (df['Y'] > 6260984) , 'Y'] = np.nan
    df.loc[(df['X']<172764) |
            (df['X'] > 673836) , 'X'] = np.nan
    df = df[(df['X'] > 0) & (df['Y'] > 0)]
    filename = working_dir + "/000_PointSources_ins.csv"
    if os.path.exists(filename):
        os.remove(filename)
    df.to_csv(filename, index=False, encoding='utf-8')
    del df
    print ("Data cleaning script is finished. Results are saved in 000_PointSources_ins.csv")