# -*- coding: utf-8 -*-
###Directories for data
working_dir = 'G:\DARBAS\MY DOCS\MY PROJECTS 2019\Nuoteku analize'
SWAT_setup_dir = 'G:/MODELLING/HELCOM_PLC/MODEL_NO_AGRO/Setup/Watersheds/'
SWAT_setup_folder = '/SWAT/results_no_tile_no_points'  #results_no_tile_no_points \
C_up_dlk = {"BOD7":3.3, "NH4":0.2, "NO3":2.3, "Ntot":3.0, "PO4":0.09, "Ptot":0.14} #Good water quality
Q_init = 5 #m3 per day. Minimal discharge for applyting new rules
GE_min = 50
Year_to_start = 2015 #Starting year for WWTP data usage in assessment
BOD7_concentration = 1.85175
###Selention list for WWTP types
wwtp_types = ['miestu, kaimo gyvenamuju vietoviu  NVI',
              #'pavirsiniu NVI',
              'pramones (gamybos ar kitu komerciniu) imoniu NVI, isskyrus tuos, kuriuose valomos ir miestu, kaimo gyvenamuju vietoviu nuotekos',
              'individualus, grupiniai buitiniu NVI',
              'kitokios paskirties (nurodyti)',
              'pramones (gamybos ar kitu komerciniu) imoniu NVI, kuriuose valomos ir miestu, kaimo gyvenamuju vietoviu nuotekos',
              'No info']
###Floor and ceilings constrains for the different PE
###Over 100000 PE
N_floor_100000 = 8
P_floor_100000 = 0.4
BOD_floor_100000 = 5
N_ceilings_100000 = 10
P_ceilings_100000 = 1
BOD_ceilings_100000 = 8
###10000-100000 PE
N_floor_10000 = 8
P_floor_10000 = 0.5
BOD_floor_10000 = 5
N_ceilings_10000 = 15
P_ceilings_10000 = 2
BOD_ceilings_10000 = 12
### <10000 PE
N_floor = 8
P_floor = 1.1
BOD_floor = 5
N_ceilings = 20
P_ceilings = 2
### 2000-10000 PE
BOD_ceilings_2000 = 20
### <2000 PE
BOD_ceilings = 25
###Limit for the flow in the river 30 most dry day flows
Discharge_quartile = 0.082
#### Modeling data extracting years
starting_date = "1997-01-01"
ending_date = "2016-12-30"
#####WWTP data tiding for LT letters removal
start_year = 2013
ending_year = 2017
