## Beispiel Script für Exploration von Sensor-level Daten
## ... in progress ...

import mne
import numpy as np
import matplotlib.pyplot as plt

plt.ioff()

# define file locations
proc_dir = "C:/Users/schmitae/Desktop/Anne/TSM_SOMA/TSM_Analyse/MEG_Data/proc/"
fig_dir = "C:/Users/schmitae/Desktop/Anne/TSM_SOMA/TSM_Analyse/MEG_Data/proc/plot/"
# pass subject and run lists
subjs = ["nc_TSM_01","nc_TSM_02","nc_TSM_03","nc_TSM_04"]
tension = ["nc_TSM_01","nc_TSM_02"]
relax = ["nc_TSM_03","nc_TSM_04"]
runs = ["2"]

# provide the dictionary with your conditions/triggers
event_id = {'Anspannung': 60, 'Entspannung': 80}
trig_id = {v: k for k,v in event_id.items()}
conds = ['Anspannung', 'Entspannung']

# for each subject
for sub in subjs:

    # read in epo file for CAT (run 2)
    epo = mne.read_epochs("{}{}_2-epo.fif".format(proc_dir,sub))
    # get data for different conditions
    for cond in conds:
        # plot PSD for each condition
        fig1 = epo[cond].plot_psd(fmax=45,bandwidth=1,show=False)
        fig1.savefig("{d}{s}_{c}_psd.png".format(d=fig_dir,s=sub,c=cond))
        # plot PSD topomap for alpha band for each condition
        fig2 = epo[cond].plot_psd_topomap(bands=[(7, 13, 'Alpha')],bandwidth=1,vlim=(None,None),show=False)
        fig2.savefig("{d}{s}_{c}_alpha_topo.png".format(d=fig_dir,s=sub,c=cond))
