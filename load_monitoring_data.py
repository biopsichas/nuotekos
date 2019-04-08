# coding=utf-8
#Script resamples monitoring results to data means and quartiles required for the assessment
import pandas as pd
import os
import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import Transform_txt_csv
import settings
working_dir = settings.working_dir
def mon_data_prep():
    print ("Monitoring data preparation script is started")
    # Transform_txt_csv.text_to_csv(working_dir+'/Data/QObs.txt')
    Q = pd.read_csv(working_dir + "/Data/QObs.csv", index_col=["STAT", "DATE"], parse_dates = True)
    WQ = pd.read_csv(working_dir + "/Data/WQObs.csv", index_col=["Station", "Date"], parse_dates = True)
    Q = Q.reindex(Q.index.dropna())
    WQ = WQ.reset_index().dropna().set_index(WQ.index.names)
    Q["Q"]=pd.to_numeric(Q["Q"], errors="coerce")
    for i in WQ.columns:
        WQ[i]=pd.to_numeric(WQ[i], errors="coerce")
    def resampler(x):
        return x.set_index('Date').resample('A').mean().mean()
    def resampler_q(x):
        return  x.set_index('DATE').resample('A').quantile(q=settings.Discharge_quartile, interpolation = "midpoint")
    WQ = WQ.reset_index(level=1).groupby(level=0).apply(resampler)
    Q = Q.reset_index(level=1).groupby(level=0).apply(resampler_q)
    files = {'Q': Q,'WQ': WQ}
    for key, value in files.iteritems():
        filename = working_dir + "/"+key+".csv"
        if os.path.exists(filename):
            os.remove(filename)
        value.to_csv(filename, index=True, encoding='utf-8')
    del WQ, Q
    print ("Monitoring data preparation script is finished. Results are saved in Q.csv and WQ.csv")

