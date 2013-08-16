#ifndef BRANCHDEFS_H
#define BRANCHDEFS_H
#include "TTree.h"
#include <vector>
//Define variables as extern below and declare them in the .cxx file to avoid multiple definitions
namespace IN {
 extern Int_t				nConv;
 extern Int_t				nLowPtJet;
 extern Int_t				nJet;
 extern Int_t				nPFPho;
 extern Int_t				nMu;
 extern Int_t				nPho;
 extern Int_t				nEle;
 extern Int_t				nPUInfo;
 extern Int_t				nMC;
 extern Int_t				nVtxBS;
 extern Int_t				nVtx;
 extern Int_t				nHLT;
 extern Int_t				run;
 extern Long64_t				event;
 extern Int_t				lumis;
 extern Bool_t				isData;
 extern Int_t				HLT[444];
 extern Int_t				HLTIndex[70];
 extern Float_t				bspotPos[3];
 extern Float_t				vtx[59][3];
 extern Int_t				IsVtxGood;
 extern Int_t				nGoodVtx;
 extern Float_t				vtxbs[59][3];
 extern Float_t				pdf[7];
 extern Float_t				pthat;
 extern Float_t				processID;
 extern Int_t				mcPID[118];
 extern Float_t				mcVtx[118][3];
 extern Float_t				mcPt[118];
 extern Float_t				mcMass[118];
 extern Float_t				mcEta[118];
 extern Float_t				mcPhi[118];
 extern Float_t				mcE[118];
 extern Float_t				mcEt[118];
 extern Int_t				mcGMomPID[118];
 extern Int_t				mcMomPID[118];
 extern Float_t				mcMomPt[118];
 extern Float_t				mcMomMass[118];
 extern Float_t				mcMomEta[118];
 extern Float_t				mcMomPhi[118];
 extern Int_t				mcIndex[118];
 extern Int_t				mcDecayType[118];
 extern Int_t				mcParentage[118];
 extern Int_t				mcStatus[118];
 extern Float_t				genMET;
 extern Float_t				genMETPhi;
 extern Int_t				nPU[4];
 extern Int_t				puBX[4];
 extern Float_t				puTrue[4];
 extern Float_t				pfMET;
 extern Float_t				pfMETPhi;
 extern Float_t				pfMETsumEt;
 extern Float_t				pfMETmEtSig;
 extern Float_t				pfMETSig;
 extern Float_t				recoPfMET;
 extern Float_t				recoPfMETPhi;
 extern Float_t				recoPfMETsumEt;
 extern Float_t				recoPfMETmEtSig;
 extern Float_t				recoPfMETSig;
 extern Float_t				trkMETxPV;
 extern Float_t				trkMETyPV;
 extern Float_t				trkMETPhiPV;
 extern Float_t				trkMETPV;
 extern Float_t				trkMETx[59];
 extern Float_t				trkMETy[59];
 extern Float_t				trkMETPhi[59];
 extern Float_t				trkMET[59];
 extern Int_t				metFilters[10];
 extern Int_t				eleTrg[10][16];
 extern Int_t				eleClass[10];
 extern Int_t				eleIsEcalDriven[10];
 extern Int_t				eleCharge[10];
 extern Float_t				eleEn[10];
 extern Float_t				eleEcalEn[10];
 extern Float_t				eleSCRawEn[10];
 extern Float_t				eleSCEn[10];
 extern Float_t				eleESEn[10];
 extern Float_t				elePt[10];
 extern Float_t				eleEta[10];
 extern Float_t				elePhi[10];
 extern Float_t				eleEtaVtx[10][100];
 extern Float_t				elePhiVtx[10][100];
 extern Float_t				eleEtVtx[10][100];
 extern Float_t				eleSCEta[10];
 extern Float_t				eleSCPhi[10];
 extern Float_t				eleSCEtaWidth[10];
 extern Float_t				eleSCPhiWidth[10];
 extern Float_t				eleVtx[10][3];
 extern Float_t				eleD0[10];
 extern Float_t				eleDz[10];
 extern Float_t				eleD0GV[10];
 extern Float_t				eleDzGV[10];
 extern Float_t				eleD0Vtx[10][100];
 extern Float_t				eleDzVtx[10][100];
 extern Float_t				eleHoverE[10];
 extern Float_t				eleHoverE12[10];
 extern Float_t				eleEoverP[10];
 extern Float_t				elePin[10];
 extern Float_t				elePout[10];
 extern Float_t				eleTrkMomErr[10];
 extern Float_t				eleBrem[10];
 extern Float_t				eledEtaAtVtx[10];
 extern Float_t				eledPhiAtVtx[10];
 extern Float_t				eleSigmaIEtaIEta[10];
 extern Float_t				eleSigmaIEtaIPhi[10];
 extern Float_t				eleSigmaIPhiIPhi[10];
 extern Float_t				eleEmax[10];
 extern Float_t				eleE1x5[10];
 extern Float_t				eleE3x3[10];
 extern Float_t				eleE5x5[10];
 extern Float_t				eleE2x5Max[10];
 extern Float_t				eleRegrE[10];
 extern Float_t				eleRegrEerr[10];
 extern Float_t				elePhoRegrE[10];
 extern Float_t				elePhoRegrEerr[10];
 extern Float_t				eleSeedTime[10];
 extern Int_t				eleRecoFlag[10];
 extern Int_t				elePos[10];
 extern Int_t				eleGenIndex[10];
 extern Int_t				eleGenGMomPID[10];
 extern Int_t				eleGenMomPID[10];
 extern Float_t				eleGenMomPt[10];
 extern Float_t				eleIsoTrkDR03[10];
 extern Float_t				eleIsoEcalDR03[10];
 extern Float_t				eleIsoHcalDR03[10];
 extern Float_t				eleIsoHcalDR0312[10];
 extern Float_t				eleIsoTrkDR04[10];
 extern Float_t				eleIsoEcalDR04[10];
 extern Float_t				eleIsoHcalDR04[10];
 extern Float_t				eleIsoHcalDR0412[10];
 extern Float_t				eleModIsoTrk[10];
 extern Float_t				eleModIsoEcal[10];
 extern Float_t				eleModIsoHcal[10];
 extern Int_t				eleMissHits[10];
 extern Float_t				eleConvDist[10];
 extern Float_t				eleConvDcot[10];
 extern Int_t				eleConvVtxFit[10];
 extern Float_t				eleIP3D[10];
 extern Float_t				eleIP3DErr[10];
 extern Float_t				eleIDMVANonTrig[10];
 extern Float_t				eleIDMVATrig[10];
 extern Float_t				eleIDMVATrigIDIso[10];
 extern Float_t				elePFChIso03[10];
 extern Float_t				elePFPhoIso03[10];
 extern Float_t				elePFNeuIso03[10];
 extern Float_t				elePFChIso04[10];
 extern Float_t				elePFPhoIso04[10];
 extern Float_t				elePFNeuIso04[10];
 extern Float_t				eleESEffSigmaRR[10][3];
 extern Int_t				phoTrg[12][8];
 extern Int_t				phoTrgFilter[12][50];
 extern Bool_t				phoIsPhoton[12];
 extern Float_t				phoSCPos[12][3];
 extern Float_t				phoCaloPos[12][3];
 extern Float_t				phoE[12];
 extern Float_t				phoEt[12];
 extern Float_t				phoEta[12];
 extern Float_t				phoVtx[12][3];
 extern Float_t				phoPhi[12];
 extern Float_t				phoEtVtx[12][100];
 extern Float_t				phoEtaVtx[12][100];
 extern Float_t				phoPhiVtx[12][100];
 extern Float_t				phoR9[12];
 extern Float_t				phoTrkIsoHollowDR03[12];
 extern Float_t				phoEcalIsoDR03[12];
 extern Float_t				phoHcalIsoDR03[12];
 extern Float_t				phoHcalIsoDR0312[12];
 extern Float_t				phoTrkIsoHollowDR04[12];
 extern Float_t				phoCiCTrkIsoDR03[12][100];
 extern Float_t				phoCiCTrkIsoDR04[12][100];
 extern Float_t				phoCiCdRtoTrk[12];
 extern Float_t				phoEcalIsoDR04[12];
 extern Float_t				phoHcalIsoDR04[12];
 extern Float_t				phoHcalIsoDR0412[12];
 extern Float_t				phoHoverE[12];
 extern Float_t				phoHoverE12[12];
 extern Int_t				phoEleVeto[12];
 extern Float_t				phoSigmaIEtaIEta[12];
 extern Float_t				phoSigmaIEtaIPhi[12];
 extern Float_t				phoSigmaIPhiIPhi[12];
 extern Float_t				phoCiCPF4phopfIso03[12];
 extern Float_t				phoCiCPF4phopfIso04[12];
 extern Float_t				phoCiCPF4chgpfIso02[12][100];
 extern Float_t				phoCiCPF4chgpfIso03[12][100];
 extern Float_t				phoCiCPF4chgpfIso04[12][100];
 extern Float_t				phoEmax[12];
 extern Float_t				phoE3x3[12];
 extern Float_t				phoE3x1[12];
 extern Float_t				phoE1x3[12];
 extern Float_t				phoE5x5[12];
 extern Float_t				phoE1x5[12];
 extern Float_t				phoE2x2[12];
 extern Float_t				phoE2x5Max[12];
 extern Float_t				phoPFChIso[12];
 extern Float_t				phoPFPhoIso[12];
 extern Float_t				phoPFNeuIso[12];
 extern Float_t				phoSCRChIso[12];
 extern Float_t				phoSCRPhoIso[12];
 extern Float_t				phoSCRNeuIso[12];
 extern Float_t				phoRegrE[12];
 extern Float_t				phoRegrEerr[12];
 extern Float_t				phoSeedTime[12];
 extern Int_t				phoSeedDetId1[12];
 extern Int_t				phoSeedDetId2[12];
 extern Float_t				phoLICTD[12];
 extern Int_t				phoRecoFlag[12];
 extern Int_t				phoPos[12];
 extern Int_t				phoGenIndex[12];
 extern Int_t				phoGenGMomPID[12];
 extern Int_t				phoGenMomPID[12];
 extern Float_t				phoGenMomPt[12];
 extern Float_t				phoSCE[12];
 extern Float_t				phoSCRawE[12];
 extern Float_t				phoESEn[12];
 extern Float_t				phoSCEt[12];
 extern Float_t				phoSCEta[12];
 extern Float_t				phoSCPhi[12];
 extern Float_t				phoSCEtaWidth[12];
 extern Float_t				phoSCPhiWidth[12];
 extern Float_t				phoSCBrem[12];
 extern Int_t				phoOverlap[12];
 extern Int_t				phohasPixelSeed[12];
 extern Int_t				pho_hasConvPf[12];
 extern Int_t				pho_hasSLConvPf[12];
 extern Float_t				pho_pfconvVtxZ[12];
 extern Float_t				pho_pfconvVtxZErr[12];
 extern Int_t				pho_nSLConv[12];
 extern Float_t				pho_pfSLConvPos[12][20][3];
 extern Float_t				pho_pfSLConvVtxZ[12][20];
 extern Int_t				phoIsConv[12];
 extern Int_t				phoNConv[12];
 extern Float_t				phoConvInvMass[12];
 extern Float_t				phoConvCotTheta[12];
 extern Float_t				phoConvEoverP[12];
 extern Float_t				phoConvZofPVfromTrks[12];
 extern Float_t				phoConvMinDist[12];
 extern Float_t				phoConvdPhiAtVtx[12];
 extern Float_t				phoConvdPhiAtCalo[12];
 extern Float_t				phoConvdEtaAtCalo[12];
 extern Float_t				phoConvTrkd0[12][2];
 extern Float_t				phoConvTrkPin[12][2];
 extern Float_t				phoConvTrkPout[12][2];
 extern Float_t				phoConvTrkdz[12][2];
 extern Float_t				phoConvTrkdzErr[12][2];
 extern Float_t				phoConvChi2[12];
 extern Float_t				phoConvChi2Prob[12];
 extern Int_t				phoConvNTrks[12];
 extern Float_t				phoConvCharge[12][2];
 extern Float_t				phoConvValidVtx[12];
 extern Float_t				phoConvLikeLihood[12];
 extern Float_t				phoConvP4[12][4];
 extern Float_t				phoConvVtx[12][3];
 extern Float_t				phoConvVtxErr[12][3];
 extern Float_t				phoConvPairMomentum[12][3];
 extern Float_t				phoConvRefittedMomentum[12][3];
 extern Int_t				SingleLegConv[12];
 extern Float_t				phoPFConvVtx[12][3];
 extern Float_t				phoPFConvMom[12][3];
 extern Float_t				phoESEffSigmaRR[12][3];
 extern Int_t				muTrg[15][10];
 extern Float_t				muEta[15];
 extern Float_t				muPhi[15];
 extern Int_t				muCharge[15];
 extern Float_t				muPt[15];
 extern Float_t				muPz[15];
 extern Float_t				muVtx[15][3];
 extern Float_t				muVtxGlb[15][3];
 extern Int_t				muGenIndex[15];
 extern Float_t				mucktPt[15];
 extern Float_t				mucktPtErr[15];
 extern Float_t				mucktEta[15];
 extern Float_t				mucktPhi[15];
 extern Float_t				mucktdxy[15];
 extern Float_t				mucktdz[15];
 extern Float_t				muIsoTrk[15];
 extern Float_t				muIsoCalo[15];
 extern Float_t				muIsoEcal[15];
 extern Float_t				muIsoHcal[15];
 extern Float_t				muChi2NDF[15];
 extern Float_t				muInnerChi2NDF[15];
 extern Float_t				muPFIsoR04_CH[15];
 extern Float_t				muPFIsoR04_NH[15];
 extern Float_t				muPFIsoR04_Pho[15];
 extern Float_t				muPFIsoR04_PU[15];
 extern Float_t				muPFIsoR04_CPart[15];
 extern Float_t				muPFIsoR04_NHHT[15];
 extern Float_t				muPFIsoR04_PhoHT[15];
 extern Float_t				muPFIsoR03_CH[15];
 extern Float_t				muPFIsoR03_NH[15];
 extern Float_t				muPFIsoR03_Pho[15];
 extern Float_t				muPFIsoR03_PU[15];
 extern Float_t				muPFIsoR03_CPart[15];
 extern Float_t				muPFIsoR03_NHHT[15];
 extern Float_t				muPFIsoR03_PhoHT[15];
 extern Int_t				muType[15];
 extern Float_t				muD0[15];
 extern Float_t				muDz[15];
 extern Float_t				muD0GV[15];
 extern Float_t				muDzGV[15];
 extern Float_t				muD0Vtx[15][100];
 extern Float_t				muDzVtx[15][100];
 extern Float_t				muInnerD0[15];
 extern Float_t				muInnerDz[15];
 extern Float_t				muInnerD0GV[15];
 extern Float_t				muInnerDzGV[15];
 extern Float_t				muInnerPt[15];
 extern Float_t				muInnerPtErr[15];
 extern Int_t				muNumberOfValidTrkLayers[15];
 extern Int_t				muNumberOfValidTrkHits[15];
 extern Int_t				muNumberOfValidPixelLayers[15];
 extern Int_t				muNumberOfValidPixelHits[15];
 extern Int_t				muNumberOfValidMuonHits[15];
 extern Int_t				muStations[15];
 extern Int_t				muChambers[15];
 extern Float_t				muIP3D[15];
 extern Float_t				muIP3DErr[15];
 extern Float_t				PFPhoEt[61];
 extern Float_t				PFPhoEta[61];
 extern Float_t				PFPhoPhi[61];
 extern Int_t				PFPhoType[61];
 extern Float_t				PFPhoIso[61];
 extern Float_t				rho25;
 extern Float_t				rho25_neu;
 extern Float_t				rho25_muPFiso;
 extern Float_t				rho25_elePFiso;
 extern Float_t				rho2011;
 extern Float_t				rho2012;
 extern Int_t				jetTrg[91][14];
 extern Float_t				jetEn[91];
 extern Float_t				jetPt[91];
 extern Float_t				jetEta[91];
 extern Float_t				jetPhi[91];
 extern Float_t				jetCharge[91];
 extern Float_t				jetEt[91];
 extern Float_t				jetRawPt[91];
 extern Float_t				jetRawEn[91];
 extern Float_t				jetArea[91];
 extern Float_t				jetCHF[91];
 extern Float_t				jetNHF[91];
 extern Float_t				jetCEF[91];
 extern Float_t				jetNEF[91];
 extern Int_t				jetNCH[91];
 extern Float_t				jetHFHAE[91];
 extern Float_t				jetHFEME[91];
 extern Int_t				jetNConstituents[91];
 extern Float_t				jetCombinedSecondaryVtxBJetTags[91];
 extern Float_t				jetCombinedSecondaryVtxMVABJetTags[91];
 extern Float_t				jetJetProbabilityBJetTags[91];
 extern Float_t				jetJetBProbabilityBJetTags[91];
 extern Float_t				jetTrackCountingHighPurBJetTags[91];
 extern Float_t				jetBetaStar[91][100];
 extern Bool_t				jetPFLooseId[91];
 extern Float_t				jetDRMean[91];
 extern Float_t				jetDR2Mean[91];
 extern Float_t				jetDZ[91];
 extern Float_t				jetFrac01[91];
 extern Float_t				jetFrac02[91];
 extern Float_t				jetFrac03[91];
 extern Float_t				jetFrac04[91];
 extern Float_t				jetFrac05[91];
 extern Float_t				jetFrac06[91];
 extern Float_t				jetFrac07[91];
 extern Float_t				jetBeta[91];
 extern Float_t				jetBetaStarCMG[91];
 extern Float_t				jetBetaStarClassic[91];
 extern Float_t				jetBetaExt[91][100];
 extern Float_t				jetBetaStarCMGExt[91][100];
 extern Float_t				jetBetaStarClassicExt[91][100];
 extern Float_t				jetNNeutrals[91];
 extern Float_t				jetNCharged[91];
 extern Float_t				jetMVAs[91][4];
 extern Int_t				jetWPLevels[91][4];
 extern Float_t				jetMVAsExt[91][4][100];
 extern Int_t				jetWPLevelsExt[91][4][100];
 extern Float_t				jetMt[91];
 extern Float_t				jetJECUnc[91];
 extern Float_t				jetLeadTrackPt[91];
 extern Float_t				jetVtxPt[91];
 extern Float_t				jetVtxMass[91];
 extern Float_t				jetVtx3dL[91];
 extern Float_t				jetVtx3deL[91];
 extern Float_t				jetSoftLeptPt[91];
 extern Float_t				jetSoftLeptPtRel[91];
 extern Float_t				jetSoftLeptdR[91];
 extern Float_t				jetSoftLeptIdlooseMu[91];
 extern Float_t				jetSoftLeptIdEle95[91];
 extern Float_t				jetDPhiMETJet[91];
 extern Float_t				jetPuJetIdL[91];
 extern Float_t				jetPuJetIdM[91];
 extern Float_t				jetPuJetIdT[91];
 extern Int_t				jetPartonID[91];
 extern Int_t				jetGenJetIndex[91];
 extern Float_t				jetGenJetEn[91];
 extern Float_t				jetGenJetPt[91];
 extern Float_t				jetGenJetEta[91];
 extern Float_t				jetGenJetPhi[91];
 extern Int_t				jetGenPartonID[91];
 extern Float_t				jetGenEn[91];
 extern Float_t				jetGenPt[91];
 extern Float_t				jetGenEta[91];
 extern Float_t				jetGenPhi[91];
 extern Float_t				jetLowPtEn[61];
 extern Float_t				jetLowPtPt[61];
 extern Float_t				jetLowPtEta[61];
 extern Float_t				jetLowPtPhi[61];
 extern Float_t				jetLowPtCharge[61];
 extern Float_t				jetLowPtEt[61];
 extern Float_t				jetLowPtRawPt[61];
 extern Float_t				jetLowPtRawEn[61];
 extern Float_t				jetLowPtArea[61];
 extern Int_t				jetLowPtPartonID[61];
 extern Float_t				jetLowPtGenJetEn[61];
 extern Float_t				jetLowPtGenJetPt[61];
 extern Float_t				jetLowPtGenJetEta[61];
 extern Float_t				jetLowPtGenJetPhi[61];
 extern Int_t				jetLowPtGenPartonID[61];
 extern Float_t				jetLowPtGenEn[61];
 extern Float_t				jetLowPtGenPt[61];
 extern Float_t				jetLowPtGenEta[61];
 extern Float_t				jetLowPtGenPhi[61];
 extern Float_t				convP4[238][4];
 extern Float_t				convVtx[238][3];
 extern Float_t				convVtxErr[238][3];
 extern Float_t				convPairMomentum[238][3];
 extern Float_t				convRefittedMomentum[238][3];
 extern Int_t				convNTracks[238];
 extern Float_t				convPairInvMass[238];
 extern Float_t				convPairCotThetaSep[238];
 extern Float_t				convEoverP[238];
 extern Float_t				convDistOfMinApproach[238];
 extern Float_t				convDPhiTrksAtVtx[238];
 extern Float_t				convDPhiTrksAtEcal[238];
 extern Float_t				convDEtaTrksAtEcal[238];
 extern Float_t				convDxy[238];
 extern Float_t				convDz[238];
 extern Float_t				convLxy[238];
 extern Float_t				convLz[238];
 extern Float_t				convZofPrimVtxFromTrks[238];
 extern Int_t				convNHitsBeforeVtx[238][2];
 extern Int_t				convNSharedHits[238];
 extern Int_t				convValidVtx[238];
 extern Float_t				convMVALikelihood[238];
 extern Float_t				convChi2[238];
 extern Float_t				convChi2Probability[238];
 extern Float_t				convTk1Dz[238];
 extern Float_t				convTk2Dz[238];
 extern Float_t				convTk1DzErr[238];
 extern Float_t				convTk2DzErr[238];
 extern Int_t				convCh1Ch2[238];
 extern Float_t				convTk1D0[238];
 extern Float_t				convTk1Pout[238];
 extern Float_t				convTk1Pin[238];
 extern Float_t				convTk2D0[238];
 extern Float_t				convTk2Pout[238];
 extern Float_t				convTk2Pin[238];
};
namespace OUT {
 extern Int_t				nConv;
 extern Int_t				nLowPtJet;
 extern Int_t				nJet;
 extern Int_t				nPFPho;
 extern Int_t				nMu;
 extern Int_t				nPho;
 extern Int_t				nEle;
 extern Int_t				nPUInfo;
 extern Int_t				nMC;
 extern Int_t				nVtxBS;
 extern Int_t				nVtx;
 extern Int_t				nHLT;
 extern Int_t				run;
 extern Long64_t				event;
 extern Int_t				lumis;
 extern Bool_t				isData;
 extern Int_t				HLT[444];
 extern Int_t				HLTIndex[70];
 extern Float_t				bspotPos[3];
 extern Float_t				vtx[59][3];
 extern Int_t				IsVtxGood;
 extern Int_t				nGoodVtx;
 extern Float_t				vtxbs[59][3];
 extern Float_t				pdf[7];
 extern Float_t				pthat;
 extern Float_t				processID;
 extern Int_t				mcPID[118];
 extern Float_t				mcVtx[118][3];
 extern Float_t				mcPt[118];
 extern Float_t				mcMass[118];
 extern Float_t				mcEta[118];
 extern Float_t				mcPhi[118];
 extern Float_t				mcE[118];
 extern Float_t				mcEt[118];
 extern Int_t				mcGMomPID[118];
 extern Int_t				mcMomPID[118];
 extern Float_t				mcMomPt[118];
 extern Float_t				mcMomMass[118];
 extern Float_t				mcMomEta[118];
 extern Float_t				mcMomPhi[118];
 extern Int_t				mcIndex[118];
 extern Int_t				mcDecayType[118];
 extern Int_t				mcParentage[118];
 extern Int_t				mcStatus[118];
 extern Float_t				genMET;
 extern Float_t				genMETPhi;
 extern Int_t				nPU[4];
 extern Int_t				puBX[4];
 extern Float_t				puTrue[4];
 extern Float_t				pfMET;
 extern Float_t				pfMETPhi;
 extern Float_t				pfMETsumEt;
 extern Float_t				pfMETmEtSig;
 extern Float_t				pfMETSig;
 extern Float_t				recoPfMET;
 extern Float_t				recoPfMETPhi;
 extern Float_t				recoPfMETsumEt;
 extern Float_t				recoPfMETmEtSig;
 extern Float_t				recoPfMETSig;
 extern Float_t				trkMETxPV;
 extern Float_t				trkMETyPV;
 extern Float_t				trkMETPhiPV;
 extern Float_t				trkMETPV;
 extern Float_t				trkMETx[59];
 extern Float_t				trkMETy[59];
 extern Float_t				trkMETPhi[59];
 extern Float_t				trkMET[59];
 extern Int_t				metFilters[10];
 extern Int_t				eleTrg[10][16];
 extern Int_t				eleClass[10];
 extern Int_t				eleIsEcalDriven[10];
 extern Int_t				eleCharge[10];
 extern Float_t				eleEn[10];
 extern Float_t				eleEcalEn[10];
 extern Float_t				eleSCRawEn[10];
 extern Float_t				eleSCEn[10];
 extern Float_t				eleESEn[10];
 extern Float_t				elePt[10];
 extern Float_t				eleEta[10];
 extern Float_t				elePhi[10];
 extern Float_t				eleEtaVtx[10][100];
 extern Float_t				elePhiVtx[10][100];
 extern Float_t				eleEtVtx[10][100];
 extern Float_t				eleSCEta[10];
 extern Float_t				eleSCPhi[10];
 extern Float_t				eleSCEtaWidth[10];
 extern Float_t				eleSCPhiWidth[10];
 extern Float_t				eleVtx[10][3];
 extern Float_t				eleD0[10];
 extern Float_t				eleDz[10];
 extern Float_t				eleD0GV[10];
 extern Float_t				eleDzGV[10];
 extern Float_t				eleD0Vtx[10][100];
 extern Float_t				eleDzVtx[10][100];
 extern Float_t				eleHoverE[10];
 extern Float_t				eleHoverE12[10];
 extern Float_t				eleEoverP[10];
 extern Float_t				elePin[10];
 extern Float_t				elePout[10];
 extern Float_t				eleTrkMomErr[10];
 extern Float_t				eleBrem[10];
 extern Float_t				eledEtaAtVtx[10];
 extern Float_t				eledPhiAtVtx[10];
 extern Float_t				eleSigmaIEtaIEta[10];
 extern Float_t				eleSigmaIEtaIPhi[10];
 extern Float_t				eleSigmaIPhiIPhi[10];
 extern Float_t				eleEmax[10];
 extern Float_t				eleE1x5[10];
 extern Float_t				eleE3x3[10];
 extern Float_t				eleE5x5[10];
 extern Float_t				eleE2x5Max[10];
 extern Float_t				eleRegrE[10];
 extern Float_t				eleRegrEerr[10];
 extern Float_t				elePhoRegrE[10];
 extern Float_t				elePhoRegrEerr[10];
 extern Float_t				eleSeedTime[10];
 extern Int_t				eleRecoFlag[10];
 extern Int_t				elePos[10];
 extern Int_t				eleGenIndex[10];
 extern Int_t				eleGenGMomPID[10];
 extern Int_t				eleGenMomPID[10];
 extern Float_t				eleGenMomPt[10];
 extern Float_t				eleIsoTrkDR03[10];
 extern Float_t				eleIsoEcalDR03[10];
 extern Float_t				eleIsoHcalDR03[10];
 extern Float_t				eleIsoHcalDR0312[10];
 extern Float_t				eleIsoTrkDR04[10];
 extern Float_t				eleIsoEcalDR04[10];
 extern Float_t				eleIsoHcalDR04[10];
 extern Float_t				eleIsoHcalDR0412[10];
 extern Float_t				eleModIsoTrk[10];
 extern Float_t				eleModIsoEcal[10];
 extern Float_t				eleModIsoHcal[10];
 extern Int_t				eleMissHits[10];
 extern Float_t				eleConvDist[10];
 extern Float_t				eleConvDcot[10];
 extern Int_t				eleConvVtxFit[10];
 extern Float_t				eleIP3D[10];
 extern Float_t				eleIP3DErr[10];
 extern Float_t				eleIDMVANonTrig[10];
 extern Float_t				eleIDMVATrig[10];
 extern Float_t				eleIDMVATrigIDIso[10];
 extern Float_t				elePFChIso03[10];
 extern Float_t				elePFPhoIso03[10];
 extern Float_t				elePFNeuIso03[10];
 extern Float_t				elePFChIso04[10];
 extern Float_t				elePFPhoIso04[10];
 extern Float_t				elePFNeuIso04[10];
 extern Float_t				eleESEffSigmaRR[10][3];
 extern Int_t				phoTrg[12][8];
 extern Int_t				phoTrgFilter[12][50];
 extern Bool_t				phoIsPhoton[12];
 extern Float_t				phoSCPos[12][3];
 extern Float_t				phoCaloPos[12][3];
 extern Float_t				phoE[12];
 extern Float_t				phoEt[12];
 extern Float_t				phoEta[12];
 extern Float_t				phoVtx[12][3];
 extern Float_t				phoPhi[12];
 extern Float_t				phoEtVtx[12][100];
 extern Float_t				phoEtaVtx[12][100];
 extern Float_t				phoPhiVtx[12][100];
 extern Float_t				phoR9[12];
 extern Float_t				phoTrkIsoHollowDR03[12];
 extern Float_t				phoEcalIsoDR03[12];
 extern Float_t				phoHcalIsoDR03[12];
 extern Float_t				phoHcalIsoDR0312[12];
 extern Float_t				phoTrkIsoHollowDR04[12];
 extern Float_t				phoCiCTrkIsoDR03[12][100];
 extern Float_t				phoCiCTrkIsoDR04[12][100];
 extern Float_t				phoCiCdRtoTrk[12];
 extern Float_t				phoEcalIsoDR04[12];
 extern Float_t				phoHcalIsoDR04[12];
 extern Float_t				phoHcalIsoDR0412[12];
 extern Float_t				phoHoverE[12];
 extern Float_t				phoHoverE12[12];
 extern Int_t				phoEleVeto[12];
 extern Float_t				phoSigmaIEtaIEta[12];
 extern Float_t				phoSigmaIEtaIPhi[12];
 extern Float_t				phoSigmaIPhiIPhi[12];
 extern Float_t				phoCiCPF4phopfIso03[12];
 extern Float_t				phoCiCPF4phopfIso04[12];
 extern Float_t				phoCiCPF4chgpfIso02[12][100];
 extern Float_t				phoCiCPF4chgpfIso03[12][100];
 extern Float_t				phoCiCPF4chgpfIso04[12][100];
 extern Float_t				phoEmax[12];
 extern Float_t				phoE3x3[12];
 extern Float_t				phoE3x1[12];
 extern Float_t				phoE1x3[12];
 extern Float_t				phoE5x5[12];
 extern Float_t				phoE1x5[12];
 extern Float_t				phoE2x2[12];
 extern Float_t				phoE2x5Max[12];
 extern Float_t				phoPFChIso[12];
 extern Float_t				phoPFPhoIso[12];
 extern Float_t				phoPFNeuIso[12];
 extern Float_t				phoSCRChIso[12];
 extern Float_t				phoSCRPhoIso[12];
 extern Float_t				phoSCRNeuIso[12];
 extern Float_t				phoRegrE[12];
 extern Float_t				phoRegrEerr[12];
 extern Float_t				phoSeedTime[12];
 extern Int_t				phoSeedDetId1[12];
 extern Int_t				phoSeedDetId2[12];
 extern Float_t				phoLICTD[12];
 extern Int_t				phoRecoFlag[12];
 extern Int_t				phoPos[12];
 extern Int_t				phoGenIndex[12];
 extern Int_t				phoGenGMomPID[12];
 extern Int_t				phoGenMomPID[12];
 extern Float_t				phoGenMomPt[12];
 extern Float_t				phoSCE[12];
 extern Float_t				phoSCRawE[12];
 extern Float_t				phoESEn[12];
 extern Float_t				phoSCEt[12];
 extern Float_t				phoSCEta[12];
 extern Float_t				phoSCPhi[12];
 extern Float_t				phoSCEtaWidth[12];
 extern Float_t				phoSCPhiWidth[12];
 extern Float_t				phoSCBrem[12];
 extern Int_t				phoOverlap[12];
 extern Int_t				phohasPixelSeed[12];
 extern Int_t				pho_hasConvPf[12];
 extern Int_t				pho_hasSLConvPf[12];
 extern Float_t				pho_pfconvVtxZ[12];
 extern Float_t				pho_pfconvVtxZErr[12];
 extern Int_t				pho_nSLConv[12];
 extern Float_t				pho_pfSLConvPos[12][20][3];
 extern Float_t				pho_pfSLConvVtxZ[12][20];
 extern Int_t				phoIsConv[12];
 extern Int_t				phoNConv[12];
 extern Float_t				phoConvInvMass[12];
 extern Float_t				phoConvCotTheta[12];
 extern Float_t				phoConvEoverP[12];
 extern Float_t				phoConvZofPVfromTrks[12];
 extern Float_t				phoConvMinDist[12];
 extern Float_t				phoConvdPhiAtVtx[12];
 extern Float_t				phoConvdPhiAtCalo[12];
 extern Float_t				phoConvdEtaAtCalo[12];
 extern Float_t				phoConvTrkd0[12][2];
 extern Float_t				phoConvTrkPin[12][2];
 extern Float_t				phoConvTrkPout[12][2];
 extern Float_t				phoConvTrkdz[12][2];
 extern Float_t				phoConvTrkdzErr[12][2];
 extern Float_t				phoConvChi2[12];
 extern Float_t				phoConvChi2Prob[12];
 extern Int_t				phoConvNTrks[12];
 extern Float_t				phoConvCharge[12][2];
 extern Float_t				phoConvValidVtx[12];
 extern Float_t				phoConvLikeLihood[12];
 extern Float_t				phoConvP4[12][4];
 extern Float_t				phoConvVtx[12][3];
 extern Float_t				phoConvVtxErr[12][3];
 extern Float_t				phoConvPairMomentum[12][3];
 extern Float_t				phoConvRefittedMomentum[12][3];
 extern Int_t				SingleLegConv[12];
 extern Float_t				phoPFConvVtx[12][3];
 extern Float_t				phoPFConvMom[12][3];
 extern Float_t				phoESEffSigmaRR[12][3];
 extern Int_t				muTrg[15][10];
 extern Float_t				muEta[15];
 extern Float_t				muPhi[15];
 extern Int_t				muCharge[15];
 extern Float_t				muPt[15];
 extern Float_t				muPz[15];
 extern Float_t				muVtx[15][3];
 extern Float_t				muVtxGlb[15][3];
 extern Int_t				muGenIndex[15];
 extern Float_t				mucktPt[15];
 extern Float_t				mucktPtErr[15];
 extern Float_t				mucktEta[15];
 extern Float_t				mucktPhi[15];
 extern Float_t				mucktdxy[15];
 extern Float_t				mucktdz[15];
 extern Float_t				muIsoTrk[15];
 extern Float_t				muIsoCalo[15];
 extern Float_t				muIsoEcal[15];
 extern Float_t				muIsoHcal[15];
 extern Float_t				muChi2NDF[15];
 extern Float_t				muInnerChi2NDF[15];
 extern Float_t				muPFIsoR04_CH[15];
 extern Float_t				muPFIsoR04_NH[15];
 extern Float_t				muPFIsoR04_Pho[15];
 extern Float_t				muPFIsoR04_PU[15];
 extern Float_t				muPFIsoR04_CPart[15];
 extern Float_t				muPFIsoR04_NHHT[15];
 extern Float_t				muPFIsoR04_PhoHT[15];
 extern Float_t				muPFIsoR03_CH[15];
 extern Float_t				muPFIsoR03_NH[15];
 extern Float_t				muPFIsoR03_Pho[15];
 extern Float_t				muPFIsoR03_PU[15];
 extern Float_t				muPFIsoR03_CPart[15];
 extern Float_t				muPFIsoR03_NHHT[15];
 extern Float_t				muPFIsoR03_PhoHT[15];
 extern Int_t				muType[15];
 extern Float_t				muD0[15];
 extern Float_t				muDz[15];
 extern Float_t				muD0GV[15];
 extern Float_t				muDzGV[15];
 extern Float_t				muD0Vtx[15][100];
 extern Float_t				muDzVtx[15][100];
 extern Float_t				muInnerD0[15];
 extern Float_t				muInnerDz[15];
 extern Float_t				muInnerD0GV[15];
 extern Float_t				muInnerDzGV[15];
 extern Float_t				muInnerPt[15];
 extern Float_t				muInnerPtErr[15];
 extern Int_t				muNumberOfValidTrkLayers[15];
 extern Int_t				muNumberOfValidTrkHits[15];
 extern Int_t				muNumberOfValidPixelLayers[15];
 extern Int_t				muNumberOfValidPixelHits[15];
 extern Int_t				muNumberOfValidMuonHits[15];
 extern Int_t				muStations[15];
 extern Int_t				muChambers[15];
 extern Float_t				muIP3D[15];
 extern Float_t				muIP3DErr[15];
 extern Float_t				PFPhoEt[61];
 extern Float_t				PFPhoEta[61];
 extern Float_t				PFPhoPhi[61];
 extern Int_t				PFPhoType[61];
 extern Float_t				PFPhoIso[61];
 extern Float_t				rho25;
 extern Float_t				rho25_neu;
 extern Float_t				rho25_muPFiso;
 extern Float_t				rho25_elePFiso;
 extern Float_t				rho2011;
 extern Float_t				rho2012;
 extern Int_t				jetTrg[91][14];
 extern Float_t				jetEn[91];
 extern Float_t				jetPt[91];
 extern Float_t				jetEta[91];
 extern Float_t				jetPhi[91];
 extern Float_t				jetCharge[91];
 extern Float_t				jetEt[91];
 extern Float_t				jetRawPt[91];
 extern Float_t				jetRawEn[91];
 extern Float_t				jetArea[91];
 extern Float_t				jetCHF[91];
 extern Float_t				jetNHF[91];
 extern Float_t				jetCEF[91];
 extern Float_t				jetNEF[91];
 extern Int_t				jetNCH[91];
 extern Float_t				jetHFHAE[91];
 extern Float_t				jetHFEME[91];
 extern Int_t				jetNConstituents[91];
 extern Float_t				jetCombinedSecondaryVtxBJetTags[91];
 extern Float_t				jetCombinedSecondaryVtxMVABJetTags[91];
 extern Float_t				jetJetProbabilityBJetTags[91];
 extern Float_t				jetJetBProbabilityBJetTags[91];
 extern Float_t				jetTrackCountingHighPurBJetTags[91];
 extern Bool_t				jetPFLooseId[91];
 extern Float_t				jetDRMean[91];
 extern Float_t				jetDR2Mean[91];
 extern Float_t				jetDZ[91];
 extern Float_t				jetFrac01[91];
 extern Float_t				jetFrac02[91];
 extern Float_t				jetFrac03[91];
 extern Float_t				jetFrac04[91];
 extern Float_t				jetFrac05[91];
 extern Float_t				jetFrac06[91];
 extern Float_t				jetFrac07[91];
 extern Float_t				jetNNeutrals[91];
 extern Float_t				jetNCharged[91];
 extern Int_t				jetWPLevels[91][4];
 extern Float_t				jetMt[91];
 extern Float_t				jetJECUnc[91];
 extern Float_t				jetLeadTrackPt[91];
 extern Float_t				jetVtxPt[91];
 extern Float_t				jetVtxMass[91];
 extern Float_t				jetVtx3dL[91];
 extern Float_t				jetVtx3deL[91];
 extern Float_t				jetSoftLeptPt[91];
 extern Float_t				jetSoftLeptPtRel[91];
 extern Float_t				jetSoftLeptdR[91];
 extern Float_t				jetSoftLeptIdlooseMu[91];
 extern Float_t				jetSoftLeptIdEle95[91];
 extern Float_t				jetDPhiMETJet[91];
 extern Float_t				jetPuJetIdL[91];
 extern Float_t				jetPuJetIdM[91];
 extern Float_t				jetPuJetIdT[91];
 extern Int_t				jetPartonID[91];
 extern Int_t				jetGenJetIndex[91];
 extern Float_t				jetGenJetEn[91];
 extern Float_t				jetGenJetPt[91];
 extern Float_t				jetGenJetEta[91];
 extern Float_t				jetGenJetPhi[91];
 extern Int_t				jetGenPartonID[91];
 extern Float_t				jetGenEn[91];
 extern Float_t				jetGenPt[91];
 extern Float_t				jetGenEta[91];
 extern Float_t				jetGenPhi[91];
 extern Float_t				convP4[238][4];
 extern Float_t				convVtx[238][3];
 extern Float_t				convVtxErr[238][3];
 extern Float_t				convPairMomentum[238][3];
 extern Float_t				convRefittedMomentum[238][3];
 extern Int_t				convNTracks[238];
 extern Float_t				convPairInvMass[238];
 extern Float_t				convPairCotThetaSep[238];
 extern Float_t				convEoverP[238];
 extern Float_t				convDistOfMinApproach[238];
 extern Float_t				convDPhiTrksAtVtx[238];
 extern Float_t				convDPhiTrksAtEcal[238];
 extern Float_t				convDEtaTrksAtEcal[238];
 extern Float_t				convDxy[238];
 extern Float_t				convDz[238];
 extern Float_t				convLxy[238];
 extern Float_t				convLz[238];
 extern Float_t				convZofPrimVtxFromTrks[238];
 extern Int_t				convNHitsBeforeVtx[238][2];
 extern Int_t				convNSharedHits[238];
 extern Int_t				convValidVtx[238];
 extern Float_t				convMVALikelihood[238];
 extern Float_t				convChi2[238];
 extern Float_t				convChi2Probability[238];
 extern Float_t				convTk1Dz[238];
 extern Float_t				convTk2Dz[238];
 extern Float_t				convTk1DzErr[238];
 extern Float_t				convTk2DzErr[238];
 extern Int_t				convCh1Ch2[238];
 extern Float_t				convTk1D0[238];
 extern Float_t				convTk1Pout[238];
 extern Float_t				convTk1Pin[238];
 extern Float_t				convTk2D0[238];
 extern Float_t				convTk2Pout[238];
 extern Float_t				convTk2Pin[238];
};
#endif