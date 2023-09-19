// C/C++ Includes
#include <iostream>

// ROOT Includes
#include "TTree.h"
#include "TFile.h"
#include "TCanvas.h"
#include "TH1D.h"

// mattak
#include "mattak/DAQStatus.h"

int main(int argc, char **argv)
{

    // this is a way of making sure we have enough arguments to proceed
    if(argc<2) {  // check for args
        std::cout << "Use like: " << basename(argv[0]) << " <input data file>" << std::endl;
        return -1;
    }

    // make a container for our output results
    TH1D *hist = new TH1D("events vs attenuation","events vs attenuation", 20, 1, 30);

    // open the file
    TFile *fIn = new TFile(argv[1], "OLD");
    fIn -> cd();
    
    // the top level in ROOT data storage is the "tree"
    TTree * daqstatusTree = (TTree*) fIn -> Get("daqstatus"); 
    mattak::DAQStatus * d = 0; 
    daqstatusTree->SetBranchAddress("daqstatus",&d);
    
    // get number of entries in the tree
    int n = daqstatusTree->GetEntries();

    // iterate over all entries in the tree
    for(int i=0; i<n; i++){
        daqstatusTree->GetEntry(i); // get the event

        // variables you have access to can be found online
        // https://github.com/RNO-G/mattak/blob/main/src/DAQStatus.cc

        auto time = d->readout_time_lt;

        std::cout<<"Time "<< time<<std::endl;

        float att = d->calinfo.attenuation; // get the attenuator setting
        
        // how many coincidence triggers (trig_coinc)
        // were recorded in the past second (lt_1Hz)
        // that happened when the "gate" (PPS) was high (gated_scalers)
        float gated_scalers = d->lt_1Hz_gated_scalers.trig_coinc; 
        
        // just to see
        printf("Att %f, Scaler %f \n", att, gated_scalers);
        
        // fill that bin in the histogram
        hist -> Fill(att, gated_scalers);
    }

	// save the plot
    TCanvas *c = new TCanvas("c","c",1100,850);
    hist -> Draw("hist");
    hist -> GetXaxis()->SetTitle("attenuation (dB)");
    hist -> GetYaxis()->SetTitle("events");
    c->SaveAs("events_vs_att.png");
    delete hist, c;

    // close the file for safety
    fIn->Close();

} //close the main program