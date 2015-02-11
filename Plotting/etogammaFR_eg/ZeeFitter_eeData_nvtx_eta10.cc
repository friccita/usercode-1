/** \macro H2GGFitter.cc
 *
 * $Id$
 *
 * Software developed for the CMS Detector at LHC
 *
 *
 *  \author Serguei Ganjour - CEA/IRFU/SPP, Saclay
 * 
 *
 * Macro is implementing the unbinned maximum-likelihood model for 
 * the Higgs to gamma gamma analysis. PDF model and RooDataSets 
 * are stored in the workspace which is feeded to  HiggsAnalysis/CombinedLimit tools:
 * 
 * http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit
 * http://cmssw.cvs.cern.ch/cgi-bin/cmssw.cgi/CMSSW/HiggsAnalysis/CombinedLimit/data/lhc-hcg/cms-hgg-1fb/
 * 
 * The analysis root trees produced in a simple format 
 *
 *     TFile file(filename,"RECREATE", "H->gg input tree for unbinned maximum-likelihood fit");
 *     TTree* outTree  = new TTree("HToGG","H->gg input tree for unbinned maximum-likelihood fit");
 *     Float_t mass, pt, pt1, pt2;
 *     Int_t CAT4, CATJET;
 *     Float_t weight;
 *
 *     outTree->Branch("mass",&mass,"mass/F");
 *     outTree->Branch("pt",&pt,"pt/F");
 *     outTree->Branch("pt1",&pt1,"pt1/F");
 *     outTree->Branch("pt2",&pt2,"pt2/F");
 *     outTree->Branch("CAT4",&CAT4,"CAT4/I");
 *     outTree->Branch("CATJET",&CATJET,"CATJET/I");
 *     {
 *       .............
 *       outTree->Fill();
 *     }
 *
 *     file.Write();
 *     file.Close();
 *     delete outTree;
 *
 * are used as input files. They have to be produced for 
 * data and Monte Carlo signal and background data sets 
 * after all analysis selections to be applied. It is recommended to put   
 * loose kinematical cuts on pt1 and pt2 (20 GeV) since further selections 
 * are possible based on RooDataSets. 
 * It is recommended to use Root 5.28/00 (CMSSW_4_1_3).
 *
 *
 */
// Loading:  .L H2GGFitter.cc
// Running:  runfits("hgg120-shapes-combined-Unbinned.root")  
//                


#include <cstring>
#include <cerrno>
#include <iostream>
#include <cstdlib>
#include <cmath>
#include <vector>
#include <string>
#include <stdexcept>
#include <algorithm>
#include <unistd.h>
#include <errno.h>

// ROOT headers
#include "TCanvas.h"
#include "TF1.h"
#include "TFile.h"
#include "TTree.h"
#include "TIterator.h"
//#include 
//#include#includeTChain.h
#include "TROOT.h" 

// RooFit headers
#include "RooAbsPdf.h"
#include "RooDataHist.h"
#include "RooDataSet.h"
#include "RooHistPdf.h"
#include "RooMsgService.h"
#include "RooNLLVar.h"
#include "RooPlot.h"
#include "RooRandom.h"
#include "RooRealVar.h"
#include "RooWorkspace.h"
#include "TStyle.h"
// RooStats headers
#include "RooStats/HLFactory.h"
#include "RooAbsPdf.h"
#include "RooAddPdf.h"
#include "RooProdPdf.h"
#include "RooAbsData.h"
#include "RooPlot.h"
#include "RooGaussian.h"
#include "RooProduct.h"
#include "RooExtendPdf.h"
#include "RooStats/ModelConfig.h"
#include "RooStats/HybridCalculator.h"
#include "RooStats/ToyMCSampler.h"
#include "RooStats/HypoTestResult.h"
#include "RooStats/HypoTestPlot.h"
#include "RooStats/SimpleLikelihoodRatioTestStat.h"
#include "RooStats/BayesianCalculator.h"
#include "RooStats/SimpleInterval.h"
#include "RooUniform.h"
#include "RooStats/MCMCCalculator.h"
#include "RooStats/MCMCInterval.h"
#include "RooStats/MCMCIntervalPlot.h"



//#include "zee_models.rs"
//#include "RooCMSShape.cc"
//#include "RooCMSShape.h"
//#include ""

using namespace RooFit;
using namespace RooStats ;

void AddData(RooWorkspace*,Int_t, Int_t ,Int_t);
void ModelFit(RooWorkspace*,Int_t, Int_t ,Int_t);
void MakePlots(RooWorkspace*,Int_t, Int_t ,Int_t);
void SetParamNames(RooWorkspace*,Int_t, Int_t ,Int_t);

RooArgSet* defineVariables()
{
  // define variables of the input ntuple
  // RooRealVar* mass  = new RooRealVar("mass","M(#gamma#gamma)",50,200,"GeV/c^{2}");


  RooRealVar* GamGamMass  = new RooRealVar("GamGamMass","M(#gamma#gamma)",50,200,"GeV/c^{2}");
  RooRealVar* pt    = new RooRealVar("pt","p_{T}(#gamma#gamma)",0,200,"GeV/c");
  RooRealVar* pt1   = new RooRealVar("pt1","p_{T}^{1}",0,200,"GeV/c");
  RooRealVar* pt2   = new RooRealVar("pt2","p_{T}^{2}",0,200,"GeV/c");
  RooRealVar* eta1   = new RooRealVar("eta1","#eta^{1}",-2.5,2.5,"");
  RooRealVar* eta2   = new RooRealVar("eta2","#eta^{2}",-2.5,2.5,"");
  RooRealVar* nVtx   = new RooRealVar("nVtx","nVtx",0,999,"");

  RooCategory* cat  = new RooCategory("eta2CAT","event category") ;
  cat->defineType("cat4_eta0",0);
  cat->defineType("cat4_eta1",1);
  cat->defineType("cat4_eta2",2);
  cat->defineType("cat4_eta3",3);
  cat->defineType("cat4_eta4",4);

  // RooArgSet* ntplVars = new RooArgSet(*mass,*pt,*pt1, *pt2, *eta1, *eta2, *cat);
  RooArgSet* ntplVars = new RooArgSet(*GamGamMass,*pt,*pt1, *pt2, *eta1, *eta2, *nVtx);
 

 
  return ntplVars;
}



void runfits(Int_t etabin=0, Int_t ptbin=0, Int_t nvtxbin)
{
  //gROOT->LoadMacro("RooCMSShape.cc+");
  TString wsDir   = "workspace/";
  TString outFile = wsDir+"hee.root";
  TString card_name("zee_models.rs");
  HLFactory hlf("HLFactory", card_name, false);
  RooWorkspace* w = hlf.GetWs();

// Add data to the workspace
  AddData(w,etabin, ptbin, nvtxbin);
  cout <<"data added  "  <<endl;
// Add the signal and background models to the workspace.
// Inside this function you will find a discription our model.
// Fit data with models
  ModelFit(w,etabin, ptbin, nvtxbin);
  cout <<"model  fit ok  "  <<endl;
// Make plots for data and fit results
  MakePlots(w,etabin, ptbin, nvtxbin);
  cout <<"plot made  "  <<endl;
// Write workspace into root file
  w->writeToFile(outFile);
  cout <<"file wrote "  <<endl;


  

}

void loop_runfits(){
  void runfits(Int_t etabin, Int_t ptbin, Int_t nvtxbin);
  //  TFile fres("fitresult.root","") ;

  // int mode=1;


  //  cout <<"ieta "<< ie << "  ipt " << ip <<"  iv "<< iv  <<endl;
  // runfits(0,0,0);    

 
  for(int iv=1; iv<3; iv++){
    for(int ie=3; ie<10; ie++){
      for(int ip=1; ip<3; ip++){
	cout <<"ieta "<< ie << "  ipt " << ip <<"  iv "<< iv  <<endl;
	runfits(ie,ip,iv);    
      }// loop over pt range
    }// loop over eta range
  } // loop over nvtx range
  


  
}

void AddData(RooWorkspace* w, Int_t etabin, Int_t ptbin, Int_t nvtxbin) {

  //  TString inDir   = "/data2/volpe/hgg/GG/CMSSW_4_2_3/src/ggAnalysis/analysis/exclusiveAna/eletree_ee/";
  // TString inDir   = "/data2/volpe/hgg/GG/CMSSW_4_2_3/src/ggAnalysis/analysis/exclusiveAna/eletree_eg/";

  // TString inDir = "/data2/volpe/hgg/GG/CMSSW_4_2_3/src/ggAnalysis/analysis/exclusiveAna/mvaVtx/data_eg/";
 //TString inDir   = "/data2/volpe/hgg/GG/CMSSW_4_2_3/src/ggAnalysis/analysis/exclusiveAna/nov6/bkgStudies/";
//****************************//
// Signal Data Set
//****************************//

  cout << "Begin: AddData() ....." << endl; 

  // Variables
  RooArgSet* ntplVars = defineVariables();
  RooRealVar weightVar("weightVar","",1,0,1000);

// add weight var into the list of ntuple variables
  weightVar.setVal(1.);
  ntplVars->add(RooArgList(weightVar));

  // common preselection cut
  // TString mainCut("pt1>45 && pt2>25");

  TString mainCut("pt1>15 ");  //!!!!!!
  //cout <<" pt1>45 && pt2>25"    <<endl;
  //****************************//
// CMS Data Set
//****************************//
// retrieve the data tree;
// no common preselection cut applied yet; 

  // TFile dataFile(inDir+"red_data_eg_L2908.root");  

  // TFile dataFile(inDir+"red_eg_L4309.root");  
  //TFile dataFile(inDir+"red_data_eg_runArunB.root");
  //TFile dataFile("/data2/volpe/hgg/GG/CMSSW_4_2_3/src/ggAnalysis/analysis/exclusiveAna/mvaVtx/data_eg_2525/red_eg_runArunB.root");
  //  TFile dataFile("/data2/volpe/hgg/GG/CMSSW_4_2_3/src/ggAnalysis/analysis/exclusiveAna/baselineLepTag/dr07_defvtx_egamma/data_egamma_jan16rereco.root");


  // TFile dataFile("/data2/volpe/hgg/GG/CMSSW_5_2_5_patch1/src/testBtag/minitrees/sept13_elegamma/data_2012NOrunB.root");

  // TFile dataFile("/data2/volpe/hgg/GG/CMSSW_5_2_5_patch1/src/may6_hgglep/minitrees/pt2538_cic4pf_eg_nvtx/dataAll2012_eg.root");
  //TFile dataFile("/data2/volpe/hgg/GG/CMSSW_5_2_5_patch1/src/EleToGamFR/minitrees/pt2538_cic4pf_ee_data_1M/dataAll2012_ee.root");


  TFile dataFile("/data2/volpe/hgg/GG/CMSSW_5_3_10_patch1/src/Waa/newNtuple_feb21/minitrees/Wgg_data_ele_1M_ee/dataEle_ee.root");
  //  TFile dataFile("/data2/volpe/hgg/GG/CMSSW_5_3_10_patch1/src/Waa/newNtuple_feb21/minitrees/Wgg_data_ele_1M_ee/dataRunAEle_ee.root");

  TTree* dataTree     = (TTree*) dataFile.Get("mtree_1lep2pho");
  weightVar.setVal(1.);
  RooDataSet Data("Data","dataset",dataTree,*ntplVars,"","weightVar");

// apply a common preselection cut;



  mainCut = "pt1>15 && pt2>15";
  
  if(nvtxbin==0){
    mainCut = "pt1>15 && pt2>15 && nVtx<=10";
  }else if(nvtxbin==1){
    mainCut = "pt1>15 && pt2>15 && nVtx>10 && nVtx<=20";
  }else if(nvtxbin==2){
    mainCut = "pt1>15 && pt2>15 && nVtx>20";
  }
  //  mainCut = "nVtx>20 && nVtx<=40";
  // }else if(nvtxbin==3){
  //  mainCut = "nVtx>40";
  // }




  //  RooDataSet* dataToFit_test   ;

  TString str_pt[3];
  TString str_eta[10];
  

  str_pt[0] = "&& pt2 > 15 && pt2< 30";
  str_pt[1] = "&& pt2 > 30 && pt2< 50";
  str_pt[2] = "&& pt2 > 50 ";
  
  str_eta[0] ="&&  fabs(eta2)<0.25";
  str_eta[1] ="&& fabs(eta2)>0.25 && fabs(eta2)<0.5";
  str_eta[2] ="&& fabs(eta2)>0.50 && fabs(eta2)<0.75";
  str_eta[3] ="&& fabs(eta2)>0.75 && fabs(eta2)<1";
  str_eta[4] ="&& fabs(eta2)>1. && fabs(eta2)<1.25";
  str_eta[5] ="&& fabs(eta2)>1.25 && fabs(eta2)<1.5";
  str_eta[6] ="&& fabs(eta2)>1.50 && fabs(eta2)<1.75";
  str_eta[7] ="&& fabs(eta2)>1.75 && fabs(eta2)<2";
  str_eta[8] ="&& fabs(eta2)>2. && fabs(eta2)<2.25";
  str_eta[9] ="&& fabs(eta2)>2.25 && fabs(eta2)<2.5";
  

  TString etacut = str_eta[etabin];
  TString ptcut = str_pt[ptbin];
  
  RooDataSet* dataToFit_test   = (RooDataSet*) Data.reduce(*w->var("GamGamMass"),mainCut+etacut+ptcut);


  //cout <<" mainCut  "<<mainCut <<endl;
  // RooDataSet* dataToFit_test   = (RooDataSet*) Data.reduce(*w->var("GamGamMass"),mainCut);
  cout << "  dataToFit_test->sumEntries(): " << dataToFit_test->sumEntries()  << endl; 
  w->import(*dataToFit_test, Rename("Data"));
  
  cout << "End: AddData() ....." << endl; 

  
  //  delete ntplVars;
  // delete dataTree;
}


void ModelFit(RooWorkspace* w, Int_t etabin, Int_t ptbin, Int_t nvtxbin) {
  //gROOT->Reset();
  // gROOT->LoadMacro("CMSstyle.C");
  // CMSstyle();
  //  gSystem->Load("libRooFit");
  gROOT->LoadMacro("RooCMSShape.cc+");
  
//******************************************//
// Fit signal and background with model pdfs
//******************************************//

  cout << "Begin: ModelFit() ....." << endl; 
// retrieve datasets from workspace to fit with pdf models
// data
  RooDataSet* data         = (RooDataSet*) w->data("Data");
  Float_t Ntot=data->sumEntries();

  cout <<"=========    Ntot   "<< Ntot  <<"===================="<<endl;
  RooRealVar* mgg_sig_m0     = w->var("mgg_sig_m0");  
  RooRealVar* mgg_sig_sigma  = w->var("mgg_sig_sigma");
  RooRealVar* mgg_sig_alpha  = w->var("mgg_sig_alpha"); 
  RooRealVar* mgg_sig_n      = w->var("mgg_sig_n"); 
  RooRealVar* mgg_sig_gsigma = w->var("mgg_sig_gsigma");
  RooRealVar* mgg_sig_frac   = w->var("mgg_sig_frac");

  //  RooRealVar  nsig("N_{S}", "#signal events", 5000,1000.,1000000.);
  // RooRealVar  nbkg("N_{B}", "#background events", 0,0,10000.);

  RooRealVar* mgg_bkg_slope  = w->var("mgg_bkg_slope");

  RooRealVar* GamGamMass     = w->var("GamGamMass");  

  //RooRealVar  GamGamMass("GamGamMass", "M_{ee}", 50, 200, "GeV/c^{2}");

  //RooRealVar  GamGamMass     = w->var("GamGamMass");  
  ////  Parameters for Crystal Ball Lineshape

  cout <<" GamGamMass "<<GamGamMass <<endl;

  RooRealVar  m0("#Delta m_{0}", "Bias", 0.874, -2.0, 2.0,"GeV/c^{2}");

  //  RooRealVar  m0("#Delta m_{0}", "Bias", 10, -1.0, 1.0,"GeV/c^{2}");
  RooRealVar  sigma("#sigma_{CB}","Width", 1.968,0.5,4,"GeV/c^{2}");
  RooRealVar  cut("#alpha","Cut", -1.13,-4.0,0.);
  //RooRealVar  power("#gamma","Power", 100, 50, 200.0);
  RooRealVar  power("#gamma","Power",7,5,30);
  //  m0.setConstant();
  //sigma.setConstant();
  // cut.setConstant();

//  Parameters for Breit-Wigner Distribution
  RooRealVar  mRes("M_{Z^{0}}", "Z0 Resonance  Mass", 91.188, 88.0, 94.0,"GeV/c^{2}");
  RooRealVar  Gamma("#Gamma", "#Gamma", 2.495, 1,4.0,"GeV/c^{2}");
  mRes.setConstant();
  Gamma.setConstant();
  cout <<"parameters ok  "  <<endl;

/// /  Parameters for Crystal Ball Lineshape
//   //RooRealVar  m0("#Delta m_{0}", "Bias", 0.0, -10.0, 10.0,"GeV/c^{2}");
//   RooRealVar  m0("#Delta m_{0}", "GamGamMass", 1.0, -2.0, 2.0,"GeV/c^{2}");
//   //m0.setConstant();

//   RooRealVar  sigma("#sigma_{CB}","Width", 1.8,0.,5.0,"GeV/c^{2}");
//   RooRealVar  cut("#alpha,"Cut", 1.775,0.5,20.0);
//   RooRealVar  power("#gamma","Power", 1.214, 1.0, 20.0);

// //  Parameters for Breit-Wigner Distribution
//   RooRealVar  mRes("M_{Z^{0}}", "Z0 Resonance  GamGamMass", 91.188, 85.0, 95.0,"GeV/c^{2}");
//   RooRealVar  Gamma("#Gamma", "#Gamma", 2.495, 2.0,3.0,"GeV/c^{2}");
//   mRes.setConstant();
//   // Gamma.setConstant();

  RooRealVar  bgtau("a_{BG}", "Backgroung Shape", -0.15, -1.0, 0.0, "1/GeV/c^{2}");
  RooRealVar  frac("frac", "Signal Fraction", 0.5,0,1.0);

  RooRealVar  fracBkg("fracBkg", "Bkg Fraction",0.2,0.4,0.6);
  fracBkg.setConstant();
 
  RooRealVar  nsig("N_{S}", "#signal events", 5000 ,0,1000000.);
  RooRealVar  nbkg("N_{B}", "#background events", 1800,0,1000000.);


  cout <<"nsig nbkg  ok  "  <<endl;
//  nbkg.setConstant();
//  frac.setConstant();
//  bgtau.setConstant();

//  Introduce a resolution model
  RooCBShape     res("res", "A  Crystal Ball Lineshape", *GamGamMass, m0,sigma, cut, power);
  cout <<"res ok  "  <<endl;
//  Breit-Wigner Lineshape
  RooBreitWigner bw("bw","A Breit-Wigner Distribution",*GamGamMass,mRes,Gamma);
  cout <<"bw ok  "  <<endl;
//  Convolution p.d.f. using numeric convolution operator
//  RooNumConvPdf bw_res("bw_res","Convolution", GamGamMass, bw, res);
//  bw_res.setConvolutionWindow(m0,sigma,10);
//  Convolution p.d.f. using numeric convolution operator based on Fourier Transforms
  RooFFTConvPdf bw_res("bw_res","Convolution", *GamGamMass, bw, res);

 cout <<"bw_res ok  "  <<endl;
// Background  p.d.f.
//  RooExponential bg("bg", "Backgroung Distribution", *GamGamMass, bgtau);
  

  RooRealVar  bgtau("a_{BG}", "Backgroung Shape", -0.15, -1.0, 1.0, "1/GeV/c^{2}");
  cout <<"bgtau ok  "  <<endl;


  RooRealVar  bg_slope0("a0_{BG}", "Backgroung Shape 0", 0.01, 0, 0.2, "");
 cout <<"bg_slope0 ok  "  <<endl;

  //bg_slope0.setConstant();

  RooRealVar  bg_slope1("a1_{BG}", "Backgroung Shape 1", 0.05, 0., 0.2, "");
  RooRealVar  bg_slope2("a2_{BG}", "Backgroung Shape 2", 0.9, 0.7, 1., "");
 // RooRealVar  bg_slo2("a2_{BG}", "Backgroung Shape 2",2, 0., 10., "");
  RooRealVar  bg_slope3("a3_{BG}", "Backgroung Shape 3",0.05, 0., 0.2, "");

  cout <<"bg_slope123 ok  "  <<endl;

  // bg_slope3.setConstant();
  //bg_slope2.setConstant();
  // RooBernstein bg("bg", "polynom", *GamGamMass, RooArgList(RooConst(1.0), bg_slope1 , bg_slope2));

  // RooBernstein bg("bg", "Bern", *GamGamMass, RooArgList(RooConst(0.1),bg_slope1,bg_slope2,RooConst(0.1)));

  //  RooBernstein bg("bg", "Bern", *GamGamMass, RooArgList(bg_slope0,bg_slope1,bg_slope2,bg_slope3));
						  //  RooBernstein bg("bg", "Bern", *GamGamMass, RooArgList(bg_slope0,bg_slope1,bg_slope2,bg_slope3));
  //  RooBernstein bg("bg", "Bern", *GamGamMass, RooArgList(RooConst(0.0), RooConst(0.0), bg_slope2,bg_slope3));
  
  //  RooExponential bg("bg", "Backgroung Distribution", *GamGamMass, bgtau);
  
  

  //  RooRealVar  GamGamMass("GamGamMass", "M_{ee}", M_min, M_max, "GeV/c^{2}");
  // GamGamMass.setBins(nBins) ;
  // RooRealVar cms_alpha("cms_alpha", "cms_alpha", 67.3, 50, 200,"");
  // RooRealVar cms_beta("cms_beta", "cms_beta", 0.11, 0., 1,"");
  // RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.05, 0, 0.3,"");
  // RooRealVar cms_peak("cms_peak", "cms_peak", 91.2, 85, 95,"");
  
  if(etabin==0 && ptbin==0){
    RooRealVar cms_alpha("cms_alpha", "cms_alpha", 67.3, 50, 200,"");
    RooRealVar cms_beta("cms_beta", "cms_beta", 0.11, 0., 1,"");
    RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.05, 0, 0.3,"");
    RooRealVar cms_peak("cms_peak", "cms_peak", 91.2, 85, 95,"");
  }else if(etabin==0 && ptbin==1){    
    RooRealVar cms_alpha("cms_alpha", "cms_alpha", 96.4, 50, 200,"");
    RooRealVar cms_beta("cms_beta", "cms_beta", 0.2, 0., 1,"");
    RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.0, -0.01, 0.3,"");
    RooRealVar cms_peak("cms_peak", "cms_peak", 89, 85, 95,"");
 }else if(etabin==0 && ptbin==2){    
    RooRealVar cms_alpha("cms_alpha", "cms_alpha", 100 , 50, 200,"");
    RooRealVar cms_beta("cms_beta", "cms_beta", 0.04, 0., 1,"");
    RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.005, -0.01, 0.3,"");
    RooRealVar cms_peak("cms_peak", "cms_peak", 92, 85, 95,"");
  }
   
  if( ptbin==0){
    RooRealVar cms_alpha("cms_alpha", "cms_alpha", 67.3, 50, 200,"");
    RooRealVar cms_beta("cms_beta", "cms_beta", 0.11, 0., 1,"");
    RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.05, 0, 0.3,"");
    RooRealVar cms_peak("cms_peak", "cms_peak", 91.2, 85, 95,"");
  }else if(ptbin==1){    
    RooRealVar cms_alpha("cms_alpha", "cms_alpha", 96.4, 50, 200,"");
    RooRealVar cms_beta("cms_beta", "cms_beta", 0.2, 0., 1,"");
    RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.0, -0.01, 0.3,"");
    RooRealVar cms_peak("cms_peak", "cms_peak", 89, 85, 95,"");
  }else if(ptbin==2){    
    RooRealVar cms_alpha("cms_alpha", "cms_alpha", 100 , 50, 200,"");
    RooRealVar cms_beta("cms_beta", "cms_beta", 0.04, 0., 1,"");
    RooRealVar cms_gamma("cms_gamma", "cms_gamma", 0.005, -0.01, 0.3,"");
    RooRealVar cms_peak("cms_peak", "cms_peak", 92, 85, 95,"");
  }
  
  cout <<"cms-shape parameters  ok  "  <<endl;


  //  cms_peak.setConstant();
  //  cms_alpha.setConstant();
  // cms_beta.setConstant();
  //cms_gamma.setConstant();
  //cout <<" alphaPass "<< alphaPass <<endl;
  // cout <<"  before CMSshape "<<  endl;
  //cout <<"  GamGamMass  "<<   GamGamMass << "  *GamGamMass  "<<   *GamGamMass << "  &GamGamMass  "<<   &GamGamMass << endl;


  //  RooRealVar &GamGamMass_ = GamGamMass;
  // RooRealVar GamGamMass_a = *GamGamMass;

  //cout <<" &GamGamMass_  "<<  &GamGamMass_   << " GamGamMass_a "<< GamGamMass_a   <<endl;


  // RooRealVar testGamGamMass("testGamGamMass", "testGamGamMass", 90 , 0, 300,"");

  RooCMSShape bg("bg", "bg", *GamGamMass, cms_alpha, cms_beta, cms_gamma, cms_peak);




  //  RooCMSShape bg("bg", "bgPass", *GamGamMass, alphaPass, betaPass, gammaPass, peakPass);

  //------------------------
  cout <<" after CMSshape "<<  endl;
  RooRealVar  bg_pol0("a0_{BG}", "Backgroung Shape 0", 0.0,0., 100000., "");
  RooRealVar  bg_pol1("a1_{BG}", "Backgroung Shape 1", 0., -1., 1.0, "");
  //------------------------

  //  RooRealVar  bg_pol2("a2_{BG}", "Backgroung Shape 2", 0.9, 0., 10.0, "");
  //RooPolynomial bg("bg", "Poly", *GamGamMass, RooArgList(bg_pol0, bg_pol1),2);

// Fit Model
//  RooAddPdf      model("model", "Di-photon GamGamMass model", RooArgList(bw_res, bg), RooArgList(nsig, nbkg));
  //RooAddPdf      model("model", "Di-photon GamGamMass model", RooArgList(bw, bg), RooArgList(nsig, nbkg));
  //  RooAddPdf      model("model", "Di-photon GamGamMass model", RooArgList(bw_res , bg), RooArgList(nsig, nbkg));


  // RooAddPdf      model("model", "Di-photon GamGamMass model", bw_res , bg, frac);

  RooAddPdf      model("model", "Di-photon Mass model", RooArgList(bw_res, bg), RooArgList(nsig, nbkg));



  //  RooAddPdf      model("model", "Di-photon GamGamMass model", RooArgList(bw_res,bg), RooArgList(frac,fracBkg));
  // RooAddPdf      model("model", "Di-photon GamGamMass model", RooArgList(bw_res,bg), RooArgList(frac));

  Float_t minMassFit(70),maxMassFit(130); 

  // model.fitTo(*data, Range(minMassFit,maxMassFit),SumW2Error(kTRUE));
  RooFitResult* fitRes = model.fitTo(*data,Range(minMassFit,maxMassFit),SumW2Error(kTRUE),Save()) ;
  // RooRealIntegral *integ = bw_res-> 
  
 
  w->import(model); 
  cout << "End: Model() ....." << endl; 
  cout << "final value of floating parameters" << endl ;
  fitRes->floatParsFinal().Print("s"); 
  fitRes->Print("v"); 

  //  TString outdir = "fitresults/";
  char binning[150];
  
  sprintf(binning,"eta%d_pt%d_nvtx%d",etabin,ptbin,nvtxbin);
  cout <<"binning  "<<  binning <<  endl;
  TFile fres("fitRes_ee_dataABCD_10etabins/fitresult.root","UPDATE") ;
  //fitRes->floatParsFinal().Write("res3_test") ;
  
  fitRes->Write(binning) ;
  fres.Close();


  
//   delete mgg_sig_m0;
//   delete mgg_sig_sigma;
//   delete mgg_sig_alpha;
//   delete mgg_sig_n;
//   delete mgg_sig_gsigma;
//   delete mgg_sig_frac;
//   delete data;

//   delete mgg_bkg_slope;
//   //  delete GamGamMass;

}

void MakePlots(RooWorkspace* w, Int_t etabin, Int_t ptbin, Int_t nvtxbin) {


// retrieve data sets from the workspace
  RooDataSet* data         = (RooDataSet*) w->data("Data");
// retrieve GamGamMass observable from the workspace
  RooRealVar* GamGamMass     = w->var("GamGamMass");  
  GamGamMass->setUnit("GeV/c^{2}");

// retrieve pdfs after the fits
// Signal Model

  RooAbsPdf* ModelPdf  = w->pdf("model");



//****************************//
// Plot Mgg Fit results
//****************************//
// Set P.D.F. parameter names
//  SetParamNames(w);

  // Float_t minGamGamMassFit(50),maxGamGamMassFit(200); 

  gStyle->SetCanvasColor(0);
//   gStyle->SetCanvasBorderMode(0);
  gStyle->SetPadColor(0);
  Float_t minMassFit(70),maxMassFit(130); 
  Int_t nBinsMass(60);
  
  



  RooPlot* plotMgg = GamGamMass->frame(Range(minMassFit,maxMassFit),Bins(nBinsMass));

  cout <<"  plotMgg   ok"<<endl;
  data->plotOn(plotMgg);
  cout <<"  data->plotOn(plotMgg);  ok"<<endl;

  gStyle->SetCanvasColor(0);
//   gStyle->SetCanvasBorderMode(0);
     gStyle->SetPadColor(0);

  gStyle->SetOptTitle(0);

  gStyle->SetOptFit(0);
  ModelPdf->plotOn(plotMgg);
//  ModelPdf->paramOn(plot, Format(plotOpt,AutoPrecision(2)), Parameters(RooArgSet(m0, sigma, nsig, nbkg, cut, power, Gamma, mRes)), ShowConstants(kTRUE) );
  ModelPdf->plotOn(plotMgg, Components("bg"), LineStyle(kDashed), LineColor(kRed));
//  ModelPdf->plotOn(plotMgg,Components("MggGaussSig"),LineStyle(kDashed),LineColor(kGreen));
//  ModelPdf->plotOn(plotMgg,Components("MggCBSig"),LineStyle(kDashed),LineColor(kRed));
  Double_t parxmin(0.65);
  Double_t parxmax(0.99);
  Double_t parymax(0.95);
  // ModelPdf->paramOn(plotMgg, ShowConstants(true), Layout(0.15,0.55,0.9), Format("NEU",AutoPrecision(2)),parxmin,parxmax,parymax);

  ModelPdf->paramOn(plotMgg, ShowConstants(true), Layout(0.15,0.55,0.9), Format("NEU",AutoPrecision(2)));
  plotMgg->getAttText()->SetTextSize(0.03);



  //TPaveText *textfit  = new TPaveText(0.7,0.5,0.98,0.98);
  // TPaveText *textfit
  //TPaveText* dataPave = (TPaveText*) frame->findObject("model_paramBox");

  TPaveText *textfit = (TPaveText*)plotMgg->findObject("model_paramBox"); 
  textfit->SetX1(.6);
  textfit->SetX2(.98);
  textfit->SetY1(.4);
  textfit->SetY2(.98);
  //textfit->SetX1NDC(1);
  //textfit->SetX2NDC(0.8);
  
  TCanvas* c1 = new TCanvas("c1","Mgg",0,0,1000,800);
  c1->cd(1);
  TString plotDir = "plots_ee_dataABCD_10etabins/"; 
  

  TString vtxBinDir;

  if(nvtxbin==0)  vtxBinDir="nvtx0/"; 
  if(nvtxbin==1)  vtxBinDir="nvtx1/"; 
  if(nvtxbin==2)  vtxBinDir="nvtx2/"; 
  if(nvtxbin==3)  vtxBinDir="nvtx3/"; 
  TString outplotdir = plotDir + vtxBinDir;

  plotMgg->Draw();  
  // textfit->Draw();
  if(etabin==-1){
    // c1->SaveAs("plots2525/ee_alleta.pdf");
  }
  if(ptbin==0){
    if(etabin==0){
      c1->SaveAs(outplotdir+"DATAee_eta0_pt0.pdf");
    }else if(etabin==1){
      c1->SaveAs(outplotdir+"DATAee_eta1_pt0.pdf");
    }else  if(etabin==2){
      c1->SaveAs(outplotdir+"DATAee_eta2_pt0.pdf");
    }else if(etabin==3){
      c1->SaveAs(outplotdir+"DATAee_eta3_pt0.pdf");
    }else if(etabin==4){
      c1->SaveAs(outplotdir+"DATAee_eta4_pt0.pdf");
    }else if(etabin==5){
      c1->SaveAs(outplotdir+"DATAee_eta5_pt0.pdf");
    }else if(etabin==6){
      c1->SaveAs(outplotdir+"DATAee_eta6_pt0.pdf");
    }else if(etabin==7){
      c1->SaveAs(outplotdir+"DATAee_eta7_pt0.pdf");
    }else if(etabin==8){
      c1->SaveAs(outplotdir+"DATAee_eta8_pt0.pdf");
    }else if(etabin==9){
      c1->SaveAs(outplotdir+"DATAee_eta9_pt0.pdf");
    }
    

  }else if(ptbin==1){
    if(etabin==0){
      c1->SaveAs(outplotdir+"DATAee_eta0_pt1.pdf");
    }else if(etabin==1){
      c1->SaveAs(outplotdir+"DATAee_eta1_pt1.pdf");
    }else  if(etabin==2){
      c1->SaveAs(outplotdir+"DATAee_eta2_pt1.pdf");
    }else if(etabin==3){
      c1->SaveAs(outplotdir+"DATAee_eta3_pt1.pdf");
    }else if(etabin==4){
      c1->SaveAs(outplotdir+"DATAee_eta4_pt1.pdf");
    }else if(etabin==5){
      c1->SaveAs(outplotdir+"DATAee_eta5_pt1.pdf");
    }else if(etabin==6){
      c1->SaveAs(outplotdir+"DATAee_eta6_pt1.pdf");
    }else if(etabin==7){
      c1->SaveAs(outplotdir+"DATAee_eta7_pt1.pdf");
    }else if(etabin==8){
      c1->SaveAs(outplotdir+"DATAee_eta8_pt1.pdf");
    }else if(etabin==9){
      c1->SaveAs(outplotdir+"DATAee_eta9_pt1.pdf");
    }
    
  }else if(ptbin==2){
    if(etabin==0){
      c1->SaveAs(outplotdir+"DATAee_eta0_pt2.pdf");
    }else if(etabin==1){
      c1->SaveAs(outplotdir+"DATAee_eta1_pt2.pdf");
    }else  if(etabin==2){
      c1->SaveAs(outplotdir+"DATAee_eta2_pt2.pdf");
    }else if(etabin==3){
      c1->SaveAs(outplotdir+"DATAee_eta3_pt2.pdf");
    }else if(etabin==4){
      c1->SaveAs(outplotdir+"DATAee_eta4_pt2.pdf");
    }else if(etabin==5){
      c1->SaveAs(outplotdir+"DATAee_eta5_pt2.pdf");
    }else if(etabin==6){
      c1->SaveAs(outplotdir+"DATAee_eta6_pt2.pdf");
    }else if(etabin==7){
      c1->SaveAs(outplotdir+"DATAee_eta7_pt2.pdf");
    }else if(etabin==8){
      c1->SaveAs(outplotdir+"DATAee_eta8_pt2.pdf");
    }else if(etabin==9){
      c1->SaveAs(outplotdir+"DATAee_eta9_pt2.pdf");
    }    
  }

  //  delete ModelPdf;
  // delete GamGamMass;

}


void SetParamNames(RooWorkspace* w) {


//****************************//
// Mgg All categories
//****************************//

  RooRealVar* mgg_sig_m0     = w->var("mgg_sig_m0");  
  RooRealVar* mgg_sig_sigma  = w->var("mgg_sig_sigma");
  RooRealVar* mgg_sig_alpha  = w->var("mgg_sig_alpha"); 
  RooRealVar* mgg_sig_n      = w->var("mgg_sig_n"); 
  RooRealVar* mgg_sig_gsigma = w->var("mgg_sig_gsigma");
  RooRealVar* mgg_sig_frac   = w->var("mgg_sig_frac");

  mgg_sig_m0    ->SetName("m_{0}");
  mgg_sig_sigma ->SetName("#sigma_{CB}");
  mgg_sig_alpha ->SetName("#alpha");
  mgg_sig_n     ->SetName("n");
  mgg_sig_gsigma->SetName("#sigma_G");  
  mgg_sig_frac  ->SetName("f_G");  

  mgg_sig_m0    ->setUnit("GeV/c^{2}");
  mgg_sig_sigma ->setUnit("GeV/c^{2}");
  mgg_sig_gsigma->setUnit("GeV/c^{2}"); 


//****************************//
// Mgg category 0 
//****************************//


  RooRealVar* mgg_sig_m0_cat0     = w->var("mgg_sig_m0_cat0");  
  RooRealVar* mgg_sig_sigma_cat0  = w->var("mgg_sig_sigma_cat0");
  RooRealVar* mgg_sig_alpha_cat0  = w->var("mgg_sig_alpha_cat0"); 
  RooRealVar* mgg_sig_n_cat0      = w->var("mgg_sig_n_cat0"); 
  RooRealVar* mgg_sig_gsigma_cat0 = w->var("mgg_sig_gsigma_cat0");
  RooRealVar* mgg_sig_frac_cat0   = w->var("mgg_sig_frac_cat0");

  mgg_sig_m0_cat0    ->SetName("m_{0}");
  mgg_sig_sigma_cat0 ->SetName("#sigma_{CB}");
  mgg_sig_alpha_cat0 ->SetName("#alpha");
  mgg_sig_n_cat0     ->SetName("n");
  mgg_sig_gsigma_cat0->SetName("#sigma_{G}");  
  mgg_sig_frac_cat0  ->SetName("f_{G}");  

  mgg_sig_m0_cat0    ->setUnit("GeV/c^{2}");
  mgg_sig_sigma_cat0 ->setUnit("GeV/c^{2}");
  mgg_sig_gsigma_cat0->setUnit("GeV/c^{2}"); 

//****************************//
// Mgg category 1 
//****************************//


  RooRealVar* mgg_sig_m0_cat1     = w->var("mgg_sig_m0_cat1");  
  RooRealVar* mgg_sig_sigma_cat1  = w->var("mgg_sig_sigma_cat1");
  RooRealVar* mgg_sig_alpha_cat1  = w->var("mgg_sig_alpha_cat1"); 
  RooRealVar* mgg_sig_n_cat1      = w->var("mgg_sig_n_cat1"); 
  RooRealVar* mgg_sig_gsigma_cat1 = w->var("mgg_sig_gsigma_cat1");
  RooRealVar* mgg_sig_frac_cat1   = w->var("mgg_sig_frac_cat1");

  mgg_sig_m0_cat1    ->SetName("m_{0}");
  mgg_sig_sigma_cat1 ->SetName("#sigma_{CB}");
  mgg_sig_alpha_cat1 ->SetName("#alpha");
  mgg_sig_n_cat1     ->SetName("n");
  mgg_sig_gsigma_cat1->SetName("#sigma_{G}");  
  mgg_sig_frac_cat1  ->SetName("f_{G}");  

  mgg_sig_m0_cat1    ->setUnit("GeV/c^{2}");
  mgg_sig_sigma_cat1 ->setUnit("GeV/c^{2}");
  mgg_sig_gsigma_cat1->setUnit("GeV/c^{2}"); 

//****************************//
// Mgg category 2 
//****************************//


  RooRealVar* mgg_sig_m0_cat2     = w->var("mgg_sig_m0_cat2");  
  RooRealVar* mgg_sig_sigma_cat2  = w->var("mgg_sig_sigma_cat2");
  RooRealVar* mgg_sig_alpha_cat2  = w->var("mgg_sig_alpha_cat2"); 
  RooRealVar* mgg_sig_n_cat2      = w->var("mgg_sig_n_cat2"); 
  RooRealVar* mgg_sig_gsigma_cat2 = w->var("mgg_sig_gsigma_cat2");
  RooRealVar* mgg_sig_frac_cat2   = w->var("mgg_sig_frac_cat2");

  mgg_sig_m0_cat2    ->SetName("m_{0}");
  mgg_sig_sigma_cat2 ->SetName("#sigma_{CB}");
  mgg_sig_alpha_cat2 ->SetName("#alpha");
  mgg_sig_n_cat2     ->SetName("n");
  mgg_sig_gsigma_cat2->SetName("#sigma_{G}");  
  mgg_sig_frac_cat2  ->SetName("f_{G}");  

  mgg_sig_m0_cat2    ->setUnit("GeV/c^{2}");
  mgg_sig_sigma_cat2 ->setUnit("GeV/c^{2}");
  mgg_sig_gsigma_cat2->setUnit("GeV/c^{2}"); 


//****************************//
// Mgg category 3 
//****************************//


  RooRealVar* mgg_sig_m0_cat3     = w->var("mgg_sig_m0_cat3");  
  RooRealVar* mgg_sig_sigma_cat3  = w->var("mgg_sig_sigma_cat3");
  RooRealVar* mgg_sig_alpha_cat3  = w->var("mgg_sig_alpha_cat3"); 
  RooRealVar* mgg_sig_n_cat3      = w->var("mgg_sig_n_cat3"); 
  RooRealVar* mgg_sig_gsigma_cat3 = w->var("mgg_sig_gsigma_cat3");
  RooRealVar* mgg_sig_frac_cat3   = w->var("mgg_sig_frac_cat3");

  mgg_sig_m0_cat3    ->SetName("m_{0}");
  mgg_sig_sigma_cat3 ->SetName("#sigma_{CB}");
  mgg_sig_alpha_cat3 ->SetName("#alpha");
  mgg_sig_n_cat3     ->SetName("n");
  mgg_sig_gsigma_cat3->SetName("#sigma_{G}");  
  mgg_sig_frac_cat3  ->SetName("f_{G}");  

  mgg_sig_m0_cat3    ->setUnit("GeV/c^{2}");
  mgg_sig_sigma_cat3 ->setUnit("GeV/c^{2}");
  mgg_sig_gsigma_cat3->setUnit("GeV/c^{2}"); 


//****************************//
// Mgg category 3 
//****************************//


  RooRealVar* mgg_sig_m0_cat4     = w->var("mgg_sig_m0_cat4");  
  RooRealVar* mgg_sig_sigma_cat4  = w->var("mgg_sig_sigma_cat4");
  RooRealVar* mgg_sig_alpha_cat4  = w->var("mgg_sig_alpha_cat4"); 
  RooRealVar* mgg_sig_n_cat4      = w->var("mgg_sig_n_cat4"); 
  RooRealVar* mgg_sig_gsigma_cat4 = w->var("mgg_sig_gsigma_cat4");
  RooRealVar* mgg_sig_frac_cat4   = w->var("mgg_sig_frac_cat4");

  mgg_sig_m0_cat4    ->SetName("m_{0}");
  mgg_sig_sigma_cat4 ->SetName("#sigma_{CB}");
  mgg_sig_alpha_cat4 ->SetName("#alpha");
  mgg_sig_n_cat4     ->SetName("n");
  mgg_sig_gsigma_cat4->SetName("#sigma_{G}");  
  mgg_sig_frac_cat4  ->SetName("f_{G}");  

  mgg_sig_m0_cat4    ->setUnit("GeV/c^{2}");
  mgg_sig_sigma_cat4 ->setUnit("GeV/c^{2}");
  mgg_sig_gsigma_cat4->setUnit("GeV/c^{2}"); 



//****************************//
// Mgg background  
//****************************//

  RooRealVar* mgg_bkg_slope          = w->var("mgg_bkg_slope");
  RooRealVar* mgg_bkg_slope_cat0     = w->var("mgg_bkg_slope_cat0");
  RooRealVar* mgg_bkg_slope_cat1     = w->var("mgg_bkg_slope_cat1");
  RooRealVar* mgg_bkg_slope_cat2     = w->var("mgg_bkg_slope_cat2");
  RooRealVar* mgg_bkg_slope_cat3     = w->var("mgg_bkg_slope_cat3");
  RooRealVar* mgg_bkg_slope_cat4     = w->var("mgg_bkg_slope_cat4");
  mgg_bkg_slope         ->SetName("a_{B}");
  mgg_bkg_slope_cat0    ->SetName("a_{B}");
  mgg_bkg_slope_cat1    ->SetName("a_{B}");
  mgg_bkg_slope_cat2    ->SetName("a_{B}");
  mgg_bkg_slope_cat3    ->SetName("a_{B}");

  mgg_bkg_slope         ->setUnit("1/GeV/c^{2}");
  mgg_bkg_slope_cat0    ->setUnit("1/GeV/c^{2}");
  mgg_bkg_slope_cat1    ->setUnit("1/GeV/c^{2}");
  mgg_bkg_slope_cat2    ->setUnit("1/GeV/c^{2}");
  mgg_bkg_slope_cat3    ->setUnit("1/GeV/c^{2}");


}

