# coding=utf-8
#Script transforms modeling results to data required for the assessment (concentration, Q)
import pandas as pd
import settings
def mod_results (df):
    df2 = pd.DataFrame(index=df.index, columns=["NNO3", "NTOT", "PPO4", "PTOT", "NNH4", "BOD7", "Q"])
    df2["NNO3"] = (df["NO3_INkg"]/df["FLOW_INcms"])/86.4
    df2["NTOT"] = ((df["NO3_INkg"]+df["ORGN_INkg"]+df["NH4_INkg"]+df["NO2_INkg"])/df["FLOW_INcms"])/86.4
    df2["PPO4"] = (df["MINP_INkg"]/df["FLOW_INcms"])/86.4
    df2["PTOT"] = ((df["MINP_INkg"]+df["ORGP_INkg"])/df["FLOW_INcms"])/86.4
    df2["NNH4"] = (df["NH4_INkg"]/df["FLOW_INcms"])/86.4
    df2["BOD7"] = (df["CBOD_INkg"] / df["FLOW_INcms"]) / 86.4
    df2 ["Q"] = df["FLOW_INcms"]
    def resampler(x):
        return x.set_index('Dates').resample('A')["NNO3", "NTOT", "PPO4", "PTOT", "NNH4", "BOD7"].mean().mean()
    def resampler_q(x):
        return x.set_index('Dates').resample('A')["Q"].quantile(settings.Discharge_quartile).mean()
    df_wq = df2.reset_index(level=1).groupby(level=0).apply(resampler)
    df_q = df2.reset_index(level=1).groupby(level=0).apply(resampler_q)
    df = pd.concat([df_wq, df_q], axis=1)
    df.rename(columns={0 : 'Q'}, inplace=True)
    return df

