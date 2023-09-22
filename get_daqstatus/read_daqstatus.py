import os
import argparse

import ROOT
from ROOT import gStyle, gPad, kRed

# load the RNO-G library
ROOT.gSystem.Load(os.environ.get('RNO_G_INSTALL_DIR')+"/lib/libmattak.so")

# make sure we have enough arguments to proceed
parser = argparse.ArgumentParser(description='daqstatus example')
parser.add_argument('--file', dest='file', required=True)
args = parser.parse_args()
filename = args.file

# histogram holder
h = ROOT.TH1D("events vs attenuation","events vs attenuation", 20, 1, 30)

# open the file
fIn = ROOT.TFile.Open(filename)

# top level in ROOT data storage is the tree
daqstatusTree = fIn.Get("daqstatus")

d = ROOT.mattak.DAQStatus()
daqstatusTree.SetBranchAddress("daqstatus", ROOT.AddressOf(d))

num_events = daqstatusTree.GetEntries()

for event in range(num_events):
    
    daqstatusTree.GetEntry(event)
    
    time = d.readout_time_lt
    att = d.calinfo.attenuation
    gated_scalers = d.lt_1Hz_gated_scalers.trig_coinc
    
    h.Fill(att, gated_scalers)

fIn.Close()
del fIn

c = ROOT.TCanvas("c", "c", 1100, 850)
h.Draw("hist")
h.GetXaxis().SetTitle("attenuation (dB)")
h.GetYaxis().SetTitle("events")
c.SaveAs("events_vs_att.png")
del c, h