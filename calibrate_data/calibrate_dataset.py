import os
import argparse
import math
import numpy as np
import ROOT
import matplotlib.pyplot as plt
from ROOT import gStyle, gPad, kRed

# load the RNO-G library
ROOT.gSystem.Load(os.environ.get('RNO_G_INSTALL_DIR')+"/lib/libmattak.so")

#voltage calibration 
bias_scan = "/data/condor_builds/users/avijai/RNO/tutorials-rnog/get_daqstatus/s13_r1794_scan.dat.gz"
data = "/data/i3store/users/rnog"

voltage_calib = ROOT.mattak.VoltageCalibration(bias_scan)
dataSet = ROOT.mattak.Dataset(13, 1796, voltage_calib, data)
dataSet_calib = dataSet.calibrated()