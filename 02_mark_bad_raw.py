# This script creates a Cycler object to loop over your raw data to mark bad segments
# Run this file from command line with '-i' for interactive mode
# Then use the cyc.go() command each time to pop the next file in the list for inspection and annotation - then use cyc.save() when done
# ...then cyc.go() again for the next file... until the list is empty

import mne
import matplotlib.pyplot as plt
import numpy as np

plt.ion() #this keeps plots interactive

# define file locations
proc_dir = "D:/XXX/proc/"
# pass subject and run lists
subjs = ["XXX_01","XXX_02",]
runs = ["1","3"]
# create new lists, if you want to try things on single subjects or runs

#dictionary with conditions/triggers for plotting
event_id = {'rest': 220,}

# collecting the files for annotation into a list
filelist = []
for sub in subjs:
    for run in runs:
        filelist.append('{dir}{sub}_{run}-raw.fif'.format(dir=proc_dir,sub=sub,run=run))

#definition of cycler object to go through the file list for annotation
class Cycler():

    def __init__(self,filelist):
        self.filelist = filelist    # when initializing the object, the filelist is collected

    def go(self):
        self.fn = self.filelist.pop(0)    # this pops the first raw file from the list
        self.raw = mne.io.Raw(self.fn)
        self.events = np.load(self.fn[:-8]+"_events.npy")   # and loads the events
        self.raw.plot(duration=15.0,n_channels=90,scalings=dict(mag=0.5e-12),events=self.events,event_id=event_id)    #  these parameters work well for inspection, but change to your liking (works also interactively during plotting)
        self.raw.plot_psd(fmax=95)    # we also plot the PSD, which is helpful to spot bad channels

    def plot(self,n_channels=90):
        self.raw.plot(duration=15.0,n_channels=90,scalings=dict(mag=0.5e-12),events=self.events,event_id=event_id)

    def show_file(self):
        print("Current Raw File: " + self.fn)    # use this to find out which subject/run we're looking at currently

    def save(self):
        self.raw.save(self.fn[:-8]+'_m-raw.fif')   # important: save the annotated file in the end !

cyc = Cycler(filelist)


# Tipps: click on bad channels to mark them (they're easily spotted from the PSD plot); press 'a' to switch in annotation mode and drag the mouse over 'BAD' segments to mark with that label
# important: close the plot to save the markings! - then do cyc.save() to save the file
