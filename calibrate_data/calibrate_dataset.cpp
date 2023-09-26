// C/C++ Includes
#include <iostream>
#include <stdio.h>

// ROOT Includes
#include "TTree.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1D.h"

// mattak
#include "mattak/VoltageCalibration.h"
#include "mattak/Dataset.h"

int main(int argc, char **argv)
{

    std::string bias_scan = "/data/condor_builds/users/avijai/RNO/tutorials-rnog/get_daqstatus/s13_r1794_scan.dat.gz";
    std::string data_dir = "/data/i3store/users/rnog";

    mattak::VoltageCalibration vc = mattak::VoltageCalibration(bias_scan.c_str());
    mattak::Dataset d = mattak::Dataset(13, 1796, &vc, data_dir.c_str());
    auto cd = d.calibrated();

}
