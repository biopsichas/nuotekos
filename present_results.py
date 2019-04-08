# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib
import pandas as pd
import warnings, os, sys
import settings
import numpy as np
from Transform_txt_csv import frange
warnings.filterwarnings("ignore", category=RuntimeWarning)
working_dir = settings.working_dir
matplotlib.rc('font', family='Arial')
plt.gcf().set_facecolor('white')
def wwtp_conc (GE_class, parameter, ceilings, step = 0.2, max_v = 0):
    wwtp = pd.read_csv(working_dir + "/" + "000_table" + ".csv", header=0, low_memory=False)
    parameter = parameter
    GE_class = GE_class
    step = step
    if GE_class == 3:
        GE_title = "GE > 100k"
    elif GE_class == 2:
        GE_title = "GE 10k-100k"
    else:
        GE_title = "GE < 10k"
    max = wwtp.loc[wwtp["GE_class"]==GE_class, parameter].max()
    min = wwtp.loc[wwtp["GE_class"]==GE_class, parameter].min()
    print ("Minimum is " + str(min))
    print ("Maximum is " + str(max))
    ceilings_check = wwtp.loc[wwtp["GE_class"] == GE_class, parameter].dropna()
    c1 = np.asarray(ceilings_check)
    c2 = (c1 > ceilings).sum()
    text = str(np.round((float(c2)/float(c1.size)*100), 2))+"% above ceilings"
    print (text)
    if max_v != 0:
        max = max_v
    bins = frange(0, max+step, step)
    plt.xlim(0, max+step)
    wwtp.loc[wwtp["GE_class"]==GE_class, parameter].dropna().hist(bins = bins, facecolor='blue', alpha=0.5)
    plt.xlabel(u"Metinės teršalų koncentracijos mg/l")
    plt.ylabel(u"Nuotekų išleistuvų skaičius (2013-2017)")
    plt.axvline(x=ceilings, linewidth=3, color='r')
    plt.xticks(bins)
    plt.title(u"Nuotėkų išleidimų pasiskirstymas pagal" + " " + parameter + " valyklose kur " + GE_title)
    plt.show()
###
def comparison_fig(filename):
    wwtp0 = pd.read_csv(working_dir + "/" + filename + ".csv", header=0, low_memory=False)
    GE_list = sorted(wwtp0["GE_class_OUT"].unique())
    ls0 = ["BOD7",  "NH4", "NO3", "Ntot", "PO4", "Ptot", "count"]
    ls = [i + "_EVAL" for i in ls0]
    fig, axs = plt.subplots(nrows=3, ncols=2)
    c1 = 0
    c2 = 0
    for GE_class in GE_list:
        wwtp = wwtp0[wwtp0["GE_class_OUT"]==GE_class]
        ls_values = []
        ls1 = []
        ls2 = []
        if GE_class == 3:
            GE_title = "GE > 100k"
        elif GE_class == 2:
            GE_title = "GE 10k-100k"
        else:
            GE_title = "GE < 10k"
        for i in ls:
           ls_values.append(float(wwtp.loc[wwtp[i]>0, i].count())/float(wwtp[i].dropna().count())*100)
           ls1.append(wwtp.loc[wwtp[i]>0, i].count())
           ls2.append(wwtp[i].dropna().count())
        ls0[6] = "Bendras"
        ls_values = np.round(ls_values, 2)
        index = np.arange(len(ls))
        ax = axs[c1, c2]
        ax.bar(index, ls_values, align='center', alpha=0.5)
        ax.set_xticks(index, minor=False)
        ax.set_xticklabels(ls0, fontdict=None, minor=False)
        ax.set_ylim(top=100)
        ax.set_ylabel(u"% problematiškų")
        ax.text(0.1, 0.8, GE_title, transform=ax.transAxes, fontsize =18)
        ax = axs[c1, c2+1]
        ax.bar(index, ls2, align='center', alpha=0.75, color = 'g', width=0.8, label = u"Pasiekta")
        ax.bar(index, ls1, align='center', alpha=0.75, color = 'r', width=0.8, label = u"Nepasiekta")
        ax.set_xticks(index, minor=False)
        ax.set_xticklabels(ls0, fontdict=None, minor=False)
        ax.set_ylabel(u"Valyklų skaičius")
        ax.legend(loc = 4)
        c1+=1
    plt.gcf().set_facecolor('white')
    plt.rcParams.update({'font.size': 18})
    fig.tight_layout(pad=0, w_pad=-1, h_pad=-1)
    plt.show()
###
def river_changes(filename):
    wwtp = pd.read_csv(working_dir + "/" + filename + ".csv", header=0, low_memory=False)
    fig = plt.figure()
    i = 1
    for key, value in settings.C_up_dlk.iteritems():
        ax = fig.add_subplot(2, 3, i)
        ax.set_title(key)
        if key == "PO4":
            ax.set_xlim(right=1)
            bins = frange(0, 1, 0.02)
        if key == "BOD7":
            ax.set_xlim(right=8)
            bins = frange(0, 8, 0.5)
        if key == "Ntot":
            ax.set_xlim(right=10)
            bins = frange(0, 10, 0.5)
        if key == "Ptot":
            ax.set_xlim(right=1)
            bins = frange(0, 1, 0.02)
        if key == "NH4":
            ax.set_xlim(right=1)
            bins = frange(0, 1, 0.05)
        if key == "NO3":
            ax.set_xlim(right=6)
            bins = frange(0, 6, 0.2)
        key = key + "_WQ_RI"
        ax.hist(wwtp[key],bins=bins, facecolor='blue', alpha=0.5)
        ax.axvline(x=value, linewidth=3, color='r')
        i+=1
    fig.tight_layout()
    plt.gcf().set_facecolor('white')
    plt.rcParams.update({'font.size': 18})
    fig.tight_layout(pad=0, w_pad=-1, h_pad=-1)
    plt.show()
def flow_compare(list_of_2files):
    data = pd.DataFrame()
    title = []
    for filename in list_of_2files:
        wwtp = pd.read_csv(working_dir + "/" + filename + ".csv", header=0, index_col="PS_CODE_EVAL", low_memory=False)
        if data.empty:
            data = wwtp["Q_WQ_RI"]
            title = filename
        else:
            title = title.upper() + " vs " + filename.upper()
            data = pd.concat([data, wwtp["Q_WQ_RI"]], axis = 1)
    data["pr"] = (data.iloc[:,1]/data.iloc[:,0]-1)
    data["pr"].hist(bins=20, facecolor='blue', alpha=0.5)
    plt.ylabel(u"Skaičius atkarpų surištų su valyklomis")
    plt.xlabel(u"Skirtumas kartais")
    plt.tight_layout()
    plt.gcf().set_facecolor('white')
    plt.rcParams.update({'font.size': 18})
    plt.title(title)
    plt.show()
def concentrations():
    wq = pd.read_csv(working_dir + "/Data/WQObs.csv", index_col=["Station","Date"], parse_dates = True)
    wq = wq.reset_index().dropna().set_index(wq.index.names)
    wq=wq[wq.index.get_level_values('Date').year > 2015]
    for i in wq.columns:
       wq[i] = pd.to_numeric(wq[i], errors="coerce")
    def resampler(x):
        return x.set_index('Date').resample('A').mean().mean()
    wq = wq.reset_index(level=1).groupby(level=0).apply(resampler)
    fig = plt.figure()
    i = 1
    for key, value in sorted(settings.C_up_dlk.iteritems()):
        ax = fig.add_subplot(2, 3, i)
        ax.set_title(key)
        if key == "PO4":
            ax.set_xlim(right=0.4)
            bins = frange(0, 0.4, 0.01)
            key = "PO4-P"
        if key == "BOD7":
            ax.set_xlim(right=8)
            bins = frange(0, 8, 0.25)
            key = "BOD7"
        if key == "Ntot":
            ax.set_xlim(right=15)
            bins = frange(0, 15, 0.5)
            key = "N total"
        if key == "Ptot":
            ax.set_xlim(right=0.4)
            bins = frange(0, 0.4, 0.01)
            key = "P total"
        if key == "NH4":
            ax.set_xlim(right=0.4)
            bins = frange(0, 0.4, 0.01)
            key = "NH4-N"
        if key == "NO3":
            ax.set_xlim(right=15)
            bins = frange(0, 15, 0.5)
            key = "NO3-N"
        data = wq[key].dropna()
        data=data.reset_index()
        data.drop("Station", axis=1, inplace=True)
        data = data.values
        ax.hist(data, bins=bins, facecolor='blue', alpha=0.5)
        ax.axvline(x=value, linewidth=3, color='r')
        ax.text(0.42, 0.7, str(np.round(float(data[data>value].shape[0])/float(data.shape[0])*100, 1))+
                u"% žemiau geros būklės", transform=ax.transAxes, fontsize=18, color ="#B22222")
        i+=1
    fig.tight_layout()
    plt.gcf().set_facecolor('white')
    plt.rcParams.update({'font.size': 18})
    fig.tight_layout(pad=0, w_pad=-1, h_pad=-1)
    plt.show()
def concentrations_reaches():
    wq = pd.read_csv(working_dir + "/all_output_rch_no_agro_no_wwtp.csv", low_memory=False)
    fig = plt.figure()
    i = 1
    for key, value in sorted(settings.C_up_dlk.iteritems()):
        if key !="BOD7":
            ax = fig.add_subplot(2, 3, i)
            ax.set_title(key)
            if key == "PO4":
                ax.set_xlim(right=0.4)
                bins = frange(0, 0.4, 0.01)
                key = "PPO4"
            if key == "Ntot":
                ax.set_xlim(right=15)
                bins = frange(0, 15, 0.5)
                key = "NTOT"
            if key == "Ptot":
                ax.set_xlim(right=0.4)
                bins = frange(0, 0.4, 0.01)
                key = "PTOT"
            if key == "NH4":
                ax.set_xlim(right=0.4)
                bins = frange(0, 0.4, 0.01)
                key = "NNH4"
            if key == "NO3":
                ax.set_xlim(right=15)
                bins = frange(0, 15, 0.5)
                key = "NNO3"
            data = wq[key].dropna()
            data = data.values
            ax.hist(data, bins=bins, facecolor='blue', alpha=0.5)
            ax.axvline(x=value, linewidth=3, color='r')
            ax.text(0.42, 0.7, str(np.round(float(data[data > value].shape[0]) / float(data.shape[0]) * 100, 1)) +
                    u"% žemiau geros būklės", transform=ax.transAxes, fontsize=18, color="#B22222")
            i += 1
    fig.tight_layout()
    plt.gcf().set_facecolor('white')
    plt.rcParams.update({'font.size': 18})
    fig.tight_layout(pad=0, w_pad=-1, h_pad=-1)
    plt.show()
