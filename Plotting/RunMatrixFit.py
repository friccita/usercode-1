"""
Plot 
"""
import sys
import os
import re
import math
import uuid
import copy
import imp
import ROOT
from array import array
import random
import collections
import pickle
import time
from uncertainties import ufloat
from uncertainties import unumpy

from SampleManager import SampleManager
from SampleManager import Sample
from SampleManager import DrawConfig

# Parse command-line options
from argparse import ArgumentParser
p = ArgumentParser()
p.add_argument('--fileName',     default='ntuple.root',  dest='fileName',        help='( Default ntuple.root ) Name of files')
p.add_argument('--treeName',     default='events'     ,  dest='treeName',        help='( Default events ) Name tree in root file')
p.add_argument('--samplesConf',  default=None,           dest='samplesConf',     help=('Use alternate sample configuration. '
                                                                                       'Must be a python file that implements the configuration '
                                                                                       'in the same manner as in the main() of this script.  If only '
                                                                                       'the file name is given it is assumed to be in the same directory '
                                                                                       'as this script, if a path is given, use that path' ) )

                                                                                       
p.add_argument('--xsFile',     default=None,  type=str ,        dest='xsFile',         help='path to cross section file.  When calling AddSample in the configuration module, set useXSFile=True to get weights from the provided file')
p.add_argument('--lumi',     default=None,  type=float ,        dest='lumi',         help='Integrated luminosity (to use with xsFile)')
p.add_argument('--outputDir',     default=None,  type=str ,        dest='outputDir',         help='output directory for histograms')
p.add_argument('--readHists',     default=False,action='store_true',   dest='readHists',         help='read histograms from root files instead of trees')
p.add_argument('--quiet',     default=False,action='store_true',   dest='quiet',         help='disable information messages')
p.add_argument('--syst_file',     default=None,  type=str ,        dest='syst_file',         help='Location of systematics file')
p.add_argument('--ptbins',     default=None,  type=str ,        dest='ptbins',         help='Comma separated list of pt bins')

p.add_argument('--nom', default=False, action='store_true', dest='nom', help='run nom' )
p.add_argument('--loose', default=False, action='store_true', dest='loose', help='run loose' )
#p.add_argument('--asym533', default=False, action='store_true', dest='asym533', help='run asym533' )
#p.add_argument('--asym855', default=False, action='store_true', dest='asym855', help='run asym855' )
#p.add_argument('--asym1077', default=False, action='store_true', dest='asym1077', help='run asym1077' )
#p.add_argument('--asym1299', default=False, action='store_true', dest='asym1299', help='run asym1299' )
#p.add_argument('--asym151111', default=False, action='store_true', dest='asym151111', help='run asym151111' )
#p.add_argument('--asym201616', default=False, action='store_true', dest='asym201616', help='run asym201616' )
p.add_argument('--asymcorr533', default=False, action='store_true', dest='asymcorr533', help='run asymcorr533' )
p.add_argument('--asymcorr855', default=False, action='store_true', dest='asymcorr855', help='run asymcorr855' )
p.add_argument('--asymcorr1077', default=False, action='store_true', dest='asymcorr1077', help='run asymcorr1077' )
p.add_argument('--asymcorr1299', default=False, action='store_true', dest='asymcorr1299', help='run asymcorr1299' )
p.add_argument('--asymcorr151111', default=False, action='store_true', dest='asymcorr151111', help='run asymcorr151111' )
p.add_argument('--asymcorr201616', default=False, action='store_true', dest='asymcorr201616', help='run asymcorr201616' )
p.add_argument('--channel', default='mu',  dest='channel', help='run this channel' )

options = p.parse_args()


if options.outputDir is not None :
    ROOT.gROOT.SetBatch(True)
else :
    ROOT.gROOT.SetBatch(False)

sampMan = None
sampManData = None

common_ptbins = [15, 25, 40, 70, 1000000 ]
if options.ptbins is not None :
    common_ptbins = [int(x) for x in options.ptbins.split(',')]

def get_default_draw_commands(ch='mu' ) :

    real_fake_cmds = {
                      'real' :'mu_passtrig25_n>0 && mu_n==1 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && leadPhot_leadLepDR>0.3 && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 ' , 
                      'fake' :'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 ',
                      'fakewin' :'mu_passtrig25_n>0 && mu_n==2 && ph_n==1 && ph_hasPixSeed[0]==0 && ph_HoverE12[0] < 0.05 && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 5 && ph_chIsoCorr[0] < 10 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] ',

    }
    if ch=='mu' :
        #gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 ' }
        gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 ' }
    if ch=='muZgg' :
        #gg_cmds = {'gg' : ' mu_passtrig25_n>0 && mu_n==1 && ph_n==2 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && leadPhot_leadLepDR>0.4 && sublPhot_leadLepDR>0.4 && ph_hasPixSeed[0]==0 && ph_hasPixSeed[1]==0 && ph_HoverE12[0] < 0.05 && ph_HoverE12[1] < 0.05 ' }
        gg_cmds = {'gg' : ' mu_n==2 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4  && dr_ph1_sublLep>0.4 && dr_ph2_sublLep>0.4 && m_leplepphph > 105 ' }
               
    elif ch == 'elzcr' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && (fabs(m_leadLep_ph1_ph2-91.2) < 5) ',}
    elif ch == 'elfull' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5)',}
    elif ch == 'elinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 ',}
    elif ch == 'elinvpixsubl' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 ',}
    elif ch == 'elfullinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5)',}
    elif ch == 'elfullinvpixsubl' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && !(fabs(m_leadLep_ph1_ph2-91.2) < 5) && !(fabs(m_leadLep_ph1-91.2) < 5)  && !(fabs(m_leadLep_ph2-91.2) < 5)',}
    elif ch == 'elzcrinvpixlead' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && (fabs(m_leadLep_ph1_ph2-91.2) < 5) ',}
    elif ch == 'elzcrinvpixsubl' :
        gg_cmds = {'gg' : ' el_passtrig_n>0 && el_n==1 && dr_ph1_ph2 > 0.4 && m_ph1_ph2>15 && dr_ph1_leadLep>0.4 && dr_ph2_leadLep>0.4 && (fabs(m_leadLep_ph1_ph2-91.2) < 5) ',}

    real_fake_cmds.update(gg_cmds)

    return real_fake_cmds

def get_default_samples(ch='mu' ) :

    if ch.count('mu') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Muon' }
    elif ch.count('el') :
        return { 'real' : {'Data' : 'Wgamma'}, 'fake' : {'Data' : 'Muon', 'Background' : 'RealPhotonsZg'}, 'target' : 'Electron' }

def get_default_binning(var='sigmaIEIE') :

    if var == 'sigmaIEIE' :
        return { 'EB' : (30, 0, 0.03), 'EE' : (200, 0, 0.1) }
    elif var == 'chIsoCorr' :
        return { 'EB' : (30, 0, 45), 'EE' : (35, 0, 42) }
    elif var == 'neuIsoCorr' :
        return { 'EB' : (40, -2, 38), 'EE' : (30, -2, 43) }

def get_default_cuts(var='sigmaIEIE') :

    if var == 'sigmaIEIE' :

        return { 'EB' : { 'tight' : ( 0, 0.011-0.0001  ), 'loose' : ( 0.01101, 0.0299 ) },
                 'EE' : { 'tight' : ( 0, 0.033-0.0001 ), 'loose' : ( 0.033, 0.099 ) } 
               }
    elif var == 'chIsoCorr' :
        return { 'EB' : { 'tight' : ( 0, 1.5-0.01  ), 'loose' : ( 1.5001, 45 ) },
                 'EE' : { 'tight' : ( 0, 1.2-0.01 ), 'loose' : ( 1.2001, 42 ) } 
               }
    elif var == 'neuIsoCorr' :
        return { 'EB' : { 'tight' : ( -2, 1.0-0.01  ), 'loose' : ( 1.0001, 40 ) },
                 'EE' : { 'tight' : ( -2, 1.5-0.01 ), 'loose' : ( 1.5001, 45 ) } 
               }

syst_uncertainties={}
def get_syst_uncertainty( type, reg, ptrange, real_fake, tight_loose ) :

    # Put these in by hand, may be necessary to load later
    if type.count( 'Background' ) :
        #use a flat 15% uncertainty for now
        return 0.15

    if not syst_uncertainties :
        print 'Systematics not loaded!  Use --syst_file to provide systematics file'
        return 0.0

    type_data = syst_uncertainties.get( type, None )
    if type_data is None :
        print 'no systematics available for %s' %type
        raw_input('con')
        return 0.0

    reg_data = type_data.get( reg, None )

    if reg_data is None :
        print 'No systematics available for region %s' %reg
        raw_input('con')
        return 0.0

    syst_ptrange = ( str(ptrange[0]), str(ptrange[1]) )
    if ptrange[0] is None :
        syst_ptrange = (None,None)
    elif ptrange[1] is None :
        syst_ptrange = (str(ptrange[0]), 'max')

    pt_data = reg_data.get(syst_ptrange, None)
    if pt_data is None :
        print 'No systematics available for pt range ', syst_ptrange
        raw_input('con')
        return 0.0

    return reg_data[syst_ptrange]

             
def main() :

    global sampManLLG
    global sampManLG
    global sampManData
    global sampManDataInvL
    global sampManDataInvS

    #base_dir_data      = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDVetoPixSeedBoth_2014_12_08'
    base_dir_data      = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaGammaNoPhIDDiMuonTrig_2014_11_28'
    base_dir_data_invl = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvPixSeedLead_2014_12_08'
    base_dir_data_invs = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaGammaNoPhIDInvPixSeedSubl_2014_12_08'
    base_dir_llg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepLepGammaNoPhID_2014_12_08'
    base_dir_lg = '/afs/cern.ch/work/j/jkunkle/private/CMS/Wgamgam/Output/LepGammaNoPhID_2014_12_08'

    sampManLLG      = SampleManager(base_dir_llg, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManLG       = SampleManager(base_dir_lg, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManData     = SampleManager(base_dir_data, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManDataInvL = SampleManager(base_dir_data_invl, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)
    sampManDataInvS = SampleManager(base_dir_data_invs, options.treeName,filename=options.fileName, xsFile=options.xsFile, lumi=options.lumi, quiet=options.quiet)

    if options.samplesConf is not None :

        sampManLLG.ReadSamples( options.samplesConf )
        sampManLG.ReadSamples( options.samplesConf )
        #sampManData.ReadSamples( options.samplesConf )
        sampManData.ReadSamples( 'Modules/JetFakeFitZgg.py' )
        sampManDataInvL.ReadSamples( options.samplesConf )
        sampManDataInvS.ReadSamples( options.samplesConf )

    if options.outputDir is not None :
        if not os.path.isdir( options.outputDir ) :
            os.makedirs( options.outputDir )

    #RunClosureFitting( outputDir = None )

    if options.syst_file is not None :
        load_syst_file( options.syst_file )

    if options.nom :
        RunNomFitting( outputDir = options.outputDir, ch=options.channel)
        #RunNomFitting( outputDir = options.outputDir, ch='el' )
        #RunNomFitting( outputDir = options.outputDir, ch='elfull' )
        #RunNomFitting( outputDir = options.outputDir, ch='elinvpixsubl' )
        #RunNomFitting( outputDir = options.outputDir, ch='elinvpixlead' )
        #RunNomFitting( outputDir = options.outputDir, ch='elfullinvpixlead' )
        #RunNomFitting( outputDir = options.outputDir, ch='elfullinvpixsubl' )
    if options.loose :
        #RunLooseFitting( outputDir = options.outputDir, ch='mu' )
        #RunLooseFitting( outputDir = options.outputDir, ch='el' )
        RunLooseFitting( outputDir = options.outputDir, ch=options.channel )
    #if options.asym533 :
    #    #RunAsymFittingLoose(vals=( 5,3,3  ), outputDir = options.outputDir , ch='mu' )
    #    #RunAsymFittingLoose(vals=( 5,3,3  ), outputDir = options.outputDir , ch='el' )
    #    RunAsymFittingLoose(vals=( 5,3,3  ), outputDir = options.outputDir , ch=options.channel )
    #if options.asym855 :
    #    #RunAsymFittingLoose(vals=( 8,5,5  ), outputDir = options.outputDir , ch='mu' )
    #    #RunAsymFittingLoose(vals=( 8,5,5  ), outputDir = options.outputDir , ch='el' )
    #    RunAsymFittingLoose(vals=( 8,5,5  ), outputDir = options.outputDir , ch=options.channel )
    #if options.asym1077 :
    #    #RunAsymFittingLoose( vals=( 10,7,7 ), outputDir = options.outputDir, ch='mu' )
    #    #RunAsymFittingLoose( vals=( 10,7,7 ), outputDir = options.outputDir, ch='el' )
    #    RunAsymFittingLoose( vals=( 10,7,7 ), outputDir = options.outputDir, ch=options.channel )
    #if options.asym1299 :
    #    #RunAsymFittingLoose( vals=( 12,9,9 ), outputDir = options.outputDir, ch='mu' )
    #    #RunAsymFittingLoose( vals=( 12,9,9 ), outputDir = options.outputDir, ch='el' )
    #    RunAsymFittingLoose( vals=( 12,9,9 ), outputDir = options.outputDir, ch=options.channel )
    #if options.asym151111 :
    #    #RunAsymFittingLoose( vals=( 15,11,11 ), outputDir = options.outputDir, ch='mu' )
    #    #RunAsymFittingLoose( vals=( 15,11,11 ), outputDir = options.outputDir, ch='el' )
    #    RunAsymFittingLoose( vals=( 15,11,11 ), outputDir = options.outputDir, ch=options.channel )
    #if options.asym201616 :
    #    #RunAsymFittingLoose( vals=( 20,16,16 ), outputDir = options.outputDir, ch='mu' )
    #    #RunAsymFittingLoose( vals=( 20,16,16 ), outputDir = options.outputDir, ch='el' )
    #    RunAsymFittingLoose( vals=( 20,16,16 ), outputDir = options.outputDir, ch=options.channel )

    if options.asymcorr533 :
        #RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch='mu' )
        #RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch='el' )
        #RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch='elfull' )
        #RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch='elinvpixsubl' )
        #RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch='elinvpixlead' )
        #RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch='elfullinvpixsubl' )
        RunCorrectedAsymFitting(vals=( 5,3,3  ), outputDir = options.outputDir , ch=options.channel )
    if options.asymcorr855 :
        #RunCorrectedAsymFitting(vals=( 8,5,5  ), outputDir = options.outputDir , ch='mu' )
        #RunCorrectedAsymFitting(vals=( 8,5,5  ), outputDir = options.outputDir , ch='el' )
        RunCorrectedAsymFitting(vals=( 8,5,5  ), outputDir = options.outputDir , ch=options.channel )
    if options.asymcorr1077 :
        #RunCorrectedAsymFitting( vals=( 10,7,7 ), outputDir = options.outputDir, ch='mu' )
        #RunCorrectedAsymFitting( vals=( 10,7,7 ), outputDir = options.outputDir, ch='el' )
        RunCorrectedAsymFitting( vals=( 10,7,7 ), outputDir = options.outputDir, ch=options.channel )
    if options.asymcorr1299 :
        #RunCorrectedAsymFitting( vals=( 12,9,9 ), outputDir = options.outputDir, ch='mu' )
        #RunCorrectedAsymFitting( vals=( 12,9,9 ), outputDir = options.outputDir, ch='el' )
        RunCorrectedAsymFitting( vals=( 12,9,9 ), outputDir = options.outputDir, ch=options.channel)
    if options.asymcorr151111 :
        #RunCorrectedAsymFitting( vals=( 15,11,11 ), outputDir = options.outputDir, ch='mu' )
        #RunCorrectedAsymFitting( vals=( 15,11,11 ), outputDir = options.outputDir, ch='el' )
        RunCorrectedAsymFitting( vals=( 15,11,11 ), outputDir = options.outputDir, ch=options.channel )
    if options.asymcorr201616 :
        #RunCorrectedAsymFitting( vals=( 20,16,16 ), outputDir = options.outputDir, ch='mu' )
        #RunCorrectedAsymFitting( vals=( 20,16,16 ), outputDir = options.outputDir, ch='el' )
        RunCorrectedAsymFitting( vals=( 20,16,16 ), outputDir = options.outputDir, ch=options.channel )

def load_syst_file( file ) :

    global syst_uncertainties

    ofile = open( file ) 
    syst_uncertainties = pickle.load(ofile)

    ofile.close()

def RunNomFitting( outputDir = None, ch='mu') :

    outputDirNom = None
    if outputDir is not None :
        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsNomIso'

    var = 'sigmaIEIE'
    #var = 'chIsoCorr'
    #var = 'neuIsoCorr'

    iso_cuts_lead = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    iso_cuts_subl = 'ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #iso_cuts_lead = 'ph_passSIEIEMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #iso_cuts_subl = 'ph_passSIEIEMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #iso_cuts_lead = 'ph_passSIEIEMedium[0] && ph_passChIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    #iso_cuts_subl = 'ph_passSIEIEMedium[1] && ph_passChIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    #iso_cuts_lead = 'ph_chIsoCorr[0] < 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3 '
    #iso_cuts_subl = 'ph_chIsoCorr[1] < 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3 '
    #iso_cuts_lead = 'ph_chIsoCorr[0] < 15 && ph_neuIsoCorr[0] < 11 && ph_phoIsoCorr[0] < 11 '
    #iso_cuts_subl = 'ph_chIsoCorr[1] < 15 && ph_neuIsoCorr[1] < 11 && ph_phoIsoCorr[1] < 11 '
    #iso_cuts_lead = 'ph_chIsoCorr[0] < 8 && ph_neuIsoCorr[0] < 5 && ph_phoIsoCorr[0] < 5 '
    #iso_cuts_subl = 'ph_chIsoCorr[1] < 8 && ph_neuIsoCorr[1] < 5 && ph_phoIsoCorr[1] < 5 '
    #iso_cuts_lead = 'ph_chIsoCorr[0] < 3 && ph_neuIsoCorr[0] < 2 && ph_phoIsoCorr[0] < 2 '
    #iso_cuts_subl = 'ph_chIsoCorr[1] < 3 && ph_neuIsoCorr[1] < 2 && ph_phoIsoCorr[1] < 2 '
    #iso_cuts_lead = 'ph_neuIsoCorr[0] < 5 && ph_phoIsoCorr[0] < 5 '
    #iso_cuts_subl = 'ph_neuIsoCorr[1] < 5 && ph_phoIsoCorr[1] < 5 '

    do_nominal_fit( iso_cuts_lead, iso_cuts_subl, ptbins=common_ptbins, fitvar=var, ch=ch, outputDir = outputDirNom, systematics='Nom')

    # use last leading pt bin
    subl_pt_lead_bins = [ common_ptbins[-2],  common_ptbins[-1] ]
    #do_nominal_fit( iso_cuts_lead, iso_cuts_subl, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[0], common_ptbins[1]), ch=ch, outputDir = outputDirNom, systematics='Nom')
    #do_nominal_fit( iso_cuts_lead, iso_cuts_subl, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[1], None), ch=ch, outputDir = outputDirNom, systematics='Nom')

    #do_nominal_fit( iso_cuts_lead, iso_cuts_subl, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[0], common_ptbins[2]), ch=ch, outputDir = outputDirNom, systematics='Nom')
    #do_nominal_fit( iso_cuts_lead, iso_cuts_subl, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[2], None), ch=ch, outputDir = outputDirNom, systematics='Nom')

def RunClosureFitting( outputDir = None, ch='mu' ) :

    outputDirNom = None
    if outputDir is not None :
        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsNomIso'

    iso_cuts_lead = 'ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    iso_cuts_subl = 'ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] '
    do_closure_fit( iso_cuts_lead, iso_cuts_subl, ptbins=common_ptbins, ch=ch, corr_factor=-0.05, outputDir = outputDirNom )

def RunLooseFitting( outputDir = None, ch='mu' ) :

    outputDirNom = None
    if outputDir is not None :
        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsLooseIso'

    iso_cuts_lead = ' ph_chIsoCorr[0] < 5 && ph_neuIsoCorr[0] < 3 && ph_phoIsoCorr[0] < 3'
    iso_cuts_subl = ' ph_chIsoCorr[1] < 5 && ph_neuIsoCorr[1] < 3 && ph_phoIsoCorr[1] < 3'

    do_nominal_fit( iso_cuts_lead, iso_cuts_subl, ptbins=common_ptbins, ch=ch, outputDir = outputDirNom )

def RunAsymFittingLoose(vals, outputDir = None, ch='mu') :

    outputDirNom = None
    if outputDir is not None :
        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsLoose%d-%d-%dAsymIso'%(vals[0], vals[1], vals[2] )

    iso_cuts_iso = ' ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    iso_cuts_noiso = ' ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d' %(vals[0], vals[1], vals[2] )

    do_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=common_ptbins, ch=ch, outputDir=outputDirNom )

def RunCorrectedAsymFitting(vals, outputDir = None, ch='mu') :

    fitvar = 'sigmaIEIE'

    outputDirNom = None
    if outputDir is not None :
        outputDirNom = outputDir + '/JetFakeTemplateFitPlotsCorr%d-%d-%dAsymIso'%(vals[0], vals[1], vals[2] )

    iso_cuts_iso = ' ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] '
    iso_cuts_noiso = ' ph_chIsoCorr[0] < %d && ph_neuIsoCorr[0] < %d && ph_phoIsoCorr[0] < %d' %(vals[0], vals[1], vals[2] )
    loose_iso_cuts = vals

    do_corrected_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, loose_iso_cuts, ptbins=common_ptbins, fitvar=fitvar, ch=ch, outputDir=outputDirNom, systematics=('-'.join([str(v) for v in vals])) )
    # subleading binning
    #subl_pt_lead_bins = [ common_ptbins[-2],  common_ptbins[-1] ]
    #do_corrected_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[0], common_ptbins[1]), ch=ch, outputDir = outputDirNom, systematics='Nom')
    #do_corrected_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[1], None), ch=ch, outputDir = outputDirNom, systematics='Nom')

    #do_corrected_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[0], common_ptbins[2]), ch=ch, outputDir = outputDirNom, systematics='Nom')
    #do_corrected_asymiso_fit( iso_cuts_iso, iso_cuts_noiso, ptbins=subl_pt_lead_bins, subl_ptrange=(common_ptbins[2], None), ch=ch, outputDir = outputDirNom, systematics='Nom')

def do_nominal_fit( iso_cuts_lead=None, iso_cuts_subl=None, ptbins=[], subl_ptrange=(None,None), fitvar='sigmaIEIE', ch='mu', outputDir=None, systematics=None ) :

    binning = get_default_binning(fitvar)
    samples = get_default_samples(ch)

    # generate templates for both EB and EE
    real_template_str = get_default_draw_commands(ch )['real'] + ' && %s' %iso_cuts_lead
    #fake_template_str = get_default_draw_commands(ch )['fakewin']
    fake_template_str = get_default_draw_commands(ch )['fake'] + ' && %s' %iso_cuts_lead

    templates_reg = {}
    templates_reg['EB'] = {}
    templates_reg['EE'] = {}
    templates_reg['EB']['real'] = get_single_photon_template(real_template_str, binning['EB'], samples['real'], 'EB', fitvar=fitvar, sampMan=sampManLG)
    templates_reg['EE']['real'] = get_single_photon_template(real_template_str, binning['EE'], samples['real'], 'EE', fitvar=fitvar, sampMan=sampManLG)
    templates_reg['EB']['fake'] = get_single_photon_template(fake_template_str, binning['EB'], samples['fake'], 'EB', fitvar=fitvar, sampMan=sampManLLG)
    templates_reg['EE']['fake'] = get_single_photon_template(fake_template_str, binning['EE'], samples['fake'], 'EE', fitvar=fitvar, sampMan=sampManLLG)

    regions = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB')]
    for reg in regions :

        # convert from regions to lead/subl
        templates = {}
        templates['lead'] = {}
        templates['subl'] = {}
        templates['lead']['real'] = templates_reg[reg[0]]['real']
        templates['subl']['real'] = templates_reg[reg[1]]['real']
        templates['lead']['fake'] = templates_reg[reg[0]]['fake']
        templates['subl']['fake'] = templates_reg[reg[1]]['fake']

        count_var = None
        if fitvar == 'sigmaIEIE' :
            if ch.count('invpix') :
                count_var = 'ph_mediumNoSIEIENoEleVeto_n'
            else :
                count_var = 'ph_mediumNoSIEIE_n'
        if fitvar == 'chIsoCorr' :
            count_var = 'ph_mediumNoChIso_n'
        if fitvar == 'neuIsoCorr' :
            count_var = 'ph_mediumNoNeuIso_n'

        # add regions onto the selection
        #gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_mediumNoSIEIE_n > 1 && is%s_leadph12 && is%s_sublph12 ' %( reg[0], reg[1])
        gg_selection = get_default_draw_commands(ch)['gg'] + ' && %s >1 &&  is%s_leadph12 && is%s_sublph12 ' %( count_var, reg[0], reg[1] )
        #gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_iso151111_n > 1 && is%s_leadph12 && is%s_sublph12 ' %( reg[0], reg[1])
        #gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_iso533_n > 1 && is%s_leadph12 && is%s_sublph12 && chIsoCorr_leadph12 < 3 && neuIsoCorr_leadph12 < 2 && phoIsoCorr_leadph12 < 2 && chIsoCorr_sublph12 < 3 && neuIsoCorr_sublph12 < 2 && phoIsoCorr_sublph12 < 2  ' %( reg[0], reg[1])
        #gg_selection = get_default_draw_commands(ch)['gg'] + ' && ph_iso533_n > 1 && chIsoCorr_leadph12 < 3 && neuIsoCorr_leadph12 < 2 && phoIsoCorr_leadph12 < 2 && chIsoCorr_sublph12 < 3 && neuIsoCorr_sublph12 < 2 && phoIsoCorr_sublph12 < 2 && ( ( ph_pt[0] > ph_pt[1] && is%s_leadph12 && is%s_sublph12 ) || ( ph_pt[0] <= ph_pt[1] && is%s_sublph12 && is%s_leadph12) ) ' %( reg[0], reg[1], reg[0], reg[1])
        #if iso_cuts_lead is not None :
        #    gg_selection = gg_selection + ' && %s ' %( iso_cuts_lead )
        #if iso_cuts_subl is not None :
        #    gg_selection = gg_selection + ' && %s ' %( iso_cuts_subl )

        # add subl pt cuts onto the selection
        if subl_ptrange[0] is not None :
            if subl_ptrange[1] is None :
                gg_selection = gg_selection + ' && pt_sublph12 > %d' %subl_ptrange[0]
            else :
                gg_selection = gg_selection + ' && pt_sublph12 > %d && ph_sublph12 < %d' %(subl_ptrange[0], subl_ptrange[1] )

        # parse out the x and y binning
        ybinn = binning[reg[1]]
        xbinn = binning[reg[0]]

        # variable given to TTree.Draw
        if fitvar == 'sigmaIEIE' :
            var = 'pt_leadph12:sieie_sublph12:sieie_leadph12' #z:y:x
        elif fitvar == 'chIsoCorr' :
            var = 'pt_leadph12:chIsoCorr_sublph12:chIsoCorr_leadph12' #z:y:x
        elif fitvar == 'neuIsoCorr' :
            var = 'pt_leadph12:neuIsoCorr_sublph12:neuIsoCorr_leadph12' #z:y:x

        print 'USE var ', var
        # get sample
        if ch.count('invpixlead' ) :
            print 'USE sampManDataInvL'
            target_samp = sampManDataInvL.get_samples(name=samples['target'])

            # draw and get back the hist
            gg_hist = clone_sample_and_draw( target_samp[0], var, gg_selection, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500),useSampMan=sampManDataInvL )
        elif ch.count('invpixsubl' ) :
            print 'USE sampManDataInvS'
            target_samp = sampManDataInvS.get_samples(name=samples['target'])

            # draw and get back the hist
            gg_hist = clone_sample_and_draw( target_samp[0], var, gg_selection, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500),useSampMan=sampManDataInvS )

        else :
            print 'USE sampManData'
            target_samp = sampManData.get_samples(name=samples['target'])

            # draw and get back the hist
            gg_hist = clone_sample_and_draw( target_samp[0], var, gg_selection, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500),useSampMan=sampManData )

        # -----------------------
        # inclusive result
        # -----------------------

        # project data hist
        gg_hist_inclusive = gg_hist.Project3D( 'yx' )

        templates_inclusive = get_projected_templates( templates, lead_ptrange =(None,None), subl_ptrange=subl_ptrange )

        ndim = 3
        if ch == 'muZgg' :
            ndim = 4

        (results_inclusive_stat, results_inclusive_syst) = run_diphoton_fit(templates_inclusive, gg_hist_inclusive, reg[0], reg[1], lead_ptrange=(None,None), subl_ptrange=subl_ptrange, outputDir=outputDir, outputPrefix='__%s'%ch, systematics=systematics, fitvar=fitvar, ndim=ndim )

        namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
        save_templates( templates_inclusive, outputDir, lead_ptrange=(None,None), subl_ptrange=(None,None), namePostfix=namePostfix )
        save_results( results_inclusive_stat, outputDir, namePostfix )

        namePostfix_syst = '__syst%s' %namePostfix
        save_results( results_inclusive_syst, outputDir, namePostfix_syst )

        # -----------------------
        # pt binned results
        # -----------------------
        for idx, ptmin in enumerate(ptbins[:-1] ) :
            ptmax = ptbins[idx+1]

            # put lead range together (expected by following code)
            if ptmax == ptbins[-1] : 
                lead_ptrange = ( ptmin, None )
            else :
                lead_ptrange = ( ptmin, ptmax )

            print 'ptmin = %d, ptmax = %d, Min Z bin = %d, max Z bin = %d' %( ptmin, ptmax, gg_hist.GetZaxis().FindBin( ptmin), gg_hist.GetZaxis().FindBin( ptmax )-1 )

            # project data hist
            gg_hist.GetZaxis().SetRange( gg_hist.GetZaxis().FindBin( ptmin), gg_hist.GetZaxis().FindBin( ptmax )-1 )
            gg_hist_pt = gg_hist.Project3D( 'yx' )

            print 'Correlation'
            print gg_hist_pt.GetCorrelationFactor()
                
            # determine the proper
            # sublead range given
            # the input lead and
            # sublead 
            if subl_ptrange[0] is not None :
                subl_min = subl_ptrange[0]
            else :
                subl_min = 15
            if subl_ptrange[1] is not None :
                if lead_ptrange[1] is None :
                    subl_max = subl_ptrange[1]
                elif lead_ptrange[1] < subl_ptrange[1] :
                    subl_max = lead_ptrange[1]
                else :
                    subl_max = subl_ptrange[1]
            else :
                subl_max = lead_ptrange[1]


            # get templates
            templates_pt = get_projected_templates( templates, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max ) )

            ndim = 3
            if ptmax <= 40 :
                ndim = 4

            # get results
            (results_pt_stat, results_pt_syst) = run_diphoton_fit(templates_pt, gg_hist_pt, reg[0], reg[1], lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max ), outputDir=outputDir, outputPrefix='__%s' %ch, systematics=systematics, ndim=ndim, fitvar=fitvar )

            namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
            if lead_ptrange[0] is not None :
                if lead_ptrange[1] is None :
                    namePostfix += '__pt_%d-max' %lead_ptrange[0]
                else :
                    namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )

            if subl_ptrange[0] is not None :
                if subl_ptrange[1] is None :
                    namePostfix += '__subpt_%d-max' %subl_ptrange[0]
                else :
                    namePostfix += '__subpt_%d-%d' %(subl_ptrange[0], subl_ptrange[1] )

            save_templates( templates_pt, outputDir, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max), namePostfix=namePostfix )
            save_results( results_pt_stat, outputDir, namePostfix )

            namePostfix_syst = '__syst%s' %namePostfix

            save_results( results_pt_syst, outputDir, namePostfix_syst )

#def do_asymiso_fit( iso_cuts_iso=None, iso_cuts_noiso=None, ptbins=[], subl_ptrange=(None,None), ch='mu', outputDir=None ) :
#
#    binning = get_default_binning()
#    samples = get_default_samples(ch)
#
#    real_template_str_iso = get_default_draw_commands(ch )['real']
#    fake_template_str_iso = get_default_draw_commands(ch )['fake']
#    if iso_cuts_iso is not None :
#        real_template_str_iso = real_template_str_iso + ' && ' + iso_cuts_iso
#        fake_template_str_iso = fake_template_str_iso + ' && ' + iso_cuts_iso
#
#    real_template_str_noiso = get_default_draw_commands(ch )['real']
#    fake_template_str_noiso = get_default_draw_commands(ch )['fake']
#    if iso_cuts_noiso is not None :
#        real_template_str_noiso = real_template_str_noiso + ' && ' + iso_cuts_noiso
#        fake_template_str_noiso = fake_template_str_noiso + ' && ' + iso_cuts_noiso
#
#    templates_iso_reg = {}
#    templates_iso_reg['EB'] = {}
#    templates_iso_reg['EE'] = {}
#    templates_iso_reg['EB']['real'] = get_single_photon_template(real_template_str_iso, binning['EB'], samples['real'], 'EB' )
#    templates_iso_reg['EE']['real'] = get_single_photon_template(real_template_str_iso, binning['EE'], samples['real'], 'EE' )
#    templates_iso_reg['EB']['fake'] = get_single_photon_template(fake_template_str_iso, binning['EB'], samples['fake'], 'EB' )
#    templates_iso_reg['EE']['fake'] = get_single_photon_template(fake_template_str_iso, binning['EE'], samples['fake'], 'EE' )
#
#    templates_noiso_reg = {}
#    templates_noiso_reg['EB'] = {}
#    templates_noiso_reg['EE'] = {}
#    templates_noiso_reg['EB']['real'] = get_single_photon_template(real_template_str_noiso, binning['EB'], samples['real'], 'EB' )
#    templates_noiso_reg['EE']['real'] = get_single_photon_template(real_template_str_noiso, binning['EE'], samples['real'], 'EE' )
#    templates_noiso_reg['EB']['fake'] = get_single_photon_template(fake_template_str_noiso, binning['EB'], samples['fake'], 'EB' )
#    templates_noiso_reg['EE']['fake'] = get_single_photon_template(fake_template_str_noiso, binning['EE'], samples['fake'], 'EE' )
#
#    lead_iso_cuts   = None
#    subl_iso_cuts   = None
#    lead_noiso_cuts = None
#    subl_noiso_cuts = None
#
#    if iso_cuts_iso is not None :
#        lead_iso_cuts = iso_cuts_iso.replace('[1]', '[0]')
#        subl_iso_cuts = iso_cuts_iso.replace('[0]', '[1]')
#    if iso_cuts_noiso is not None :
#        lead_noiso_cuts = iso_cuts_noiso.replace('[1]', '[0]')
#        subl_noiso_cuts = iso_cuts_noiso.replace('[0]', '[1]')
#
#    regions = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB'), ('EE', 'EE') ]
#
#    for reg in regions :
#
#        templates_leadiso = {}
#        templates_leadiso['lead'] = {}
#        templates_leadiso['subl'] = {}
#        templates_leadiso['lead']['real'] = templates_iso_reg[reg[0]]['real']
#        templates_leadiso['subl']['real'] = templates_noiso_reg[reg[1]]['real']
#        templates_leadiso['lead']['fake'] = templates_iso_reg[reg[0]]['fake']
#        templates_leadiso['subl']['fake'] = templates_noiso_reg[reg[1]]['fake']
#
#        templates_subliso = {}
#        templates_subliso['lead'] = {}
#        templates_subliso['subl'] = {}
#        templates_subliso['lead']['real'] = templates_noiso_reg[reg[0]]['real']
#        templates_subliso['subl']['real'] = templates_iso_reg[reg[1]]['real']
#        templates_subliso['lead']['fake'] = templates_noiso_reg[reg[0]]['fake']
#        templates_subliso['subl']['fake'] = templates_iso_reg[reg[1]]['fake']
#
#        # add regions onto the selection
#        gg_selection_leadiso = get_default_draw_commands(ch)['gg'] + ' && ph_Is%s[0] && ph_Is%s[1] ' %( reg[0], reg[1] )
#        gg_selection_subliso = get_default_draw_commands(ch)['gg'] + ' && ph_Is%s[0] && ph_Is%s[1] ' %( reg[0], reg[1] )
#
#        # add object cuts to the selection
#        if lead_iso_cuts is not None :
#            gg_selection_leadiso = gg_selection_leadiso + ' && %s ' %(lead_iso_cuts)
#        if subl_noiso_cuts is not None :
#            gg_selection_leadiso = gg_selection_leadiso + ' && %s ' %(subl_noiso_cuts )
#
#        if subl_iso_cuts is not None :
#            gg_selection_subliso = gg_selection_subliso + ' && %s ' %(subl_iso_cuts)
#        if lead_noiso_cuts is not None :
#            gg_selection_subliso = gg_selection_subliso + ' && %s ' %(lead_noiso_cuts)
#
#        # add subl pt cuts onto the selection
#        if subl_ptrange[0] is not None :
#            if subl_ptrange[1] is None :
#                gg_selection_leadiso = gg_selection_leadiso + ' && ph_pt[1] > %d' %subl_ptrange[0]
#                gg_selection_subliso = gg_selection_subliso + ' && ph_pt[1] > %d' %subl_ptrange[0]
#            else :
#                gg_selection_leadiso = gg_selection_leadiso + ' && ph_pt[1] > %d && ph_pt[1] < %d' %(subl_ptrange[0], subl_ptrange[1] )
#                gg_selection_subliso = gg_selection_subliso + ' && ph_pt[1] > %d && ph_pt[1] < %d' %(subl_ptrange[0], subl_ptrange[1] )
#
#        # parse out the x and y binning
#        ybinn = binning[reg[1]]
#        xbinn = binning[reg[0]]
#
#        # variable given to TTree.Draw
#        var = 'ph_pt[0]:ph_sigmaIEIE[1]:ph_sigmaIEIE[0]' #z:y:x
#
#        # get sample
#        target_samp = sampMan.get_samples(name=samples['target'])
#
#        # draw and get back the hist
#        gg_hist_leadiso = clone_sample_and_draw( target_samp[0], var, gg_selection_leadiso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ) )
#        gg_hist_subliso = clone_sample_and_draw( target_samp[0], var, gg_selection_subliso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ) )
#
#        # -----------------------
#        # inclusive result
#        # -----------------------
#        # project data hist
#        gg_hist_leadiso_inclusive = gg_hist_leadiso.Project3D( 'yx' )
#        gg_hist_subliso_inclusive = gg_hist_subliso.Project3D( 'yx' )
#
#        templates_leadiso_inclusive = get_projected_templates( templates_leadiso, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )
#        templates_subliso_inclusive = get_projected_templates( templates_subliso, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )
#
#        results_leadiso = run_diphoton_fit(templates_leadiso_inclusive, gg_hist_leadiso_inclusive, reg[0], reg[1], lead_ptrange=(None,None), subl_ptrange=subl_ptrange, outputDir=outputDir, outputPrefix='__%s__leadiso'%ch )
#
#        results_subliso = run_diphoton_fit(templates_subliso_inclusive, gg_hist_subliso_inclusive,  reg[0], reg[1], lead_ptrange=(None,None), subl_ptrange=subl_ptrange, outputDir=outputDir, outputPrefix='__%s__subliso'%ch )
#
#        update_asym_results( results_leadiso, results_subliso )
#        
#        namePostfix = '__%s__%s-%s' %( reg[0], reg[1], ch )
#
#        namePostfix_leadiso = '__leadiso'+namePostfix
#        namePostfix_subliso = '__subliso'+namePostfix
#
#        save_templates( templates_leadiso_inclusive, outputDir, lead_ptrange=(None,None), subl_ptrange=(None,None), namePostfix=namePostfix_leadiso )
#        save_results( results_leadiso, outputDir, namePostfix_leadiso )
#
#        save_templates( templates_subliso_inclusive, outputDir, lead_ptrange=(None,None), subl_ptrange=(None,None), namePostfix=namePostfix_subliso )
#        save_results( results_subliso, outputDir, namePostfix_subliso )
#
#        # -----------------------
#        # pt binned results
#        # -----------------------
#        for idx, ptmin in enumerate(ptbins[:-1] ) :
#
#            ptmax = ptbins[idx+1]
#
#            # put lead range together (expected by following code)
#            if ptmax == ptbins[-1] : 
#                lead_ptrange = ( ptmin, None )
#            else :
#                lead_ptrange = ( ptmin, ptmax )
#
#            print 'ptmin = %d, ptmax = %d, Min Z bin = %d, max Z bin = %d' %( ptmin, ptmax, gg_hist_leadiso.GetZaxis().FindBin( ptmin), gg_hist_leadiso.GetZaxis().FindBin( ptmax )-1 )
#            # project data hist
#            gg_hist_leadiso.GetZaxis().SetRange( gg_hist_leadiso.GetZaxis().FindBin( ptmin), gg_hist_leadiso.GetZaxis().FindBin( ptmax )-1 )
#            gg_hist_leadiso_pt = gg_hist_leadiso.Project3D( 'yx' )
#
#            gg_hist_subliso.GetZaxis().SetRange( gg_hist_subliso.GetZaxis().FindBin( ptmin), gg_hist_subliso.GetZaxis().FindBin( ptmax )-1 )
#            gg_hist_subliso_pt = gg_hist_subliso.Project3D( 'yx' )
#                
#            # determine the proper
#            # sublead range given
#            # the input lead and
#            # sublead 
#            if subl_ptrange[0] is not None :
#                subl_min = subl_ptrange[0]
#            else :
#                subl_min = 15
#            if subl_ptrange[1] is not None :
#                if lead_ptrange[1] is None :
#                    subl_max = subl_ptrange[1]
#                elif lead_ptrange[1] < subl_ptrange[1] :
#                    subl_max = lead_ptrange[1]
#                else :
#                    subl_max = subl_ptrange[1]
#            else :
#                subl_max = lead_ptrange[1]
#
#            # get templates
#            templates_leadiso_pt = get_projected_templates( templates_leadiso, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max) )
#            templates_subliso_pt = get_projected_templates( templates_subliso, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max) )
#
#            # get results
#            results_leadiso_pt = run_diphoton_fit(templates_leadiso_pt, gg_hist_leadiso_pt, reg[0], reg[1], lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max), outputDir=outputDir, outputPrefix='__%s__leadiso'%ch )
#            results_subliso_pt = run_diphoton_fit(templates_subliso_pt, gg_hist_subliso_pt, reg[0], reg[1], lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max), outputDir=outputDir, outputPrefix='__%s__subliso'%ch )
#
#            update_asym_results( results_leadiso_pt, results_subliso_pt )
#
#            namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
#
#            if lead_ptrange[0] is not None :
#                if lead_ptrange[1] is None :
#                    namePostfix += '__pt_%d-max' %lead_ptrange[0]
#                else :
#                    namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )
#
#            if subl_ptrange[0] is not None :
#                if subl_ptrange[1] is None :
#                    namePostfix += '__subpt_%d-max' %subl_ptrange[0]
#                else :
#                    namePostfix += '__subpt_%d-%d' %(subl_ptrange[0], subl_ptrange[1] )
#
#            namePostfix_leadiso = '__leadiso'+namePostfix
#            namePostfix_subliso = '__subliso'+namePostfix
#
#            save_templates( templates_leadiso_pt, outputDir, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max), namePostfix=namePostfix_leadiso )
#            save_results( results_leadiso_pt, outputDir, namePostfix_leadiso )
#
#            save_templates( templates_subliso_pt, outputDir, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max), namePostfix=namePostfix_subliso )
#            save_results( results_subliso_pt, outputDir, namePostfix_subliso )

def do_corrected_asymiso_fit( iso_cuts_iso=None, iso_cuts_noiso=None, loose_iso_cuts = None, ptbins=[], subl_ptrange=(None,None), fitvar='sigmaIEIE', ch='mu', outputDir=None, systematics=None ) :

    binning = get_default_binning(fitvar)
    samples = get_default_samples(ch)

    real_template_str_iso = get_default_draw_commands(ch )['real']
    fake_template_str_iso = get_default_draw_commands(ch )['fake']
    if iso_cuts_iso is not None :
        real_template_str_iso = real_template_str_iso + ' && ' + iso_cuts_iso
        fake_template_str_iso = fake_template_str_iso + ' && ' + iso_cuts_iso

    real_template_str_noiso = get_default_draw_commands(ch )['real']
    fake_template_str_noiso = get_default_draw_commands(ch )['fake']
    if iso_cuts_noiso is not None :
        real_template_str_noiso = real_template_str_noiso + ' && ' + iso_cuts_noiso
        fake_template_str_noiso = fake_template_str_noiso + ' && ' + iso_cuts_noiso

    templates_iso_reg = {}
    templates_iso_reg['EB'] = {}
    templates_iso_reg['EE'] = {}
    templates_iso_reg['EB']['real'] = get_single_photon_template(real_template_str_iso, binning['EB'], samples['real'], 'EB', fitvar=fitvar, sampMan=sampManLG )
    templates_iso_reg['EE']['real'] = get_single_photon_template(real_template_str_iso, binning['EE'], samples['real'], 'EE', fitvar=fitvar, sampMan=sampManLG )
    templates_iso_reg['EB']['fake'] = get_single_photon_template(fake_template_str_iso, binning['EB'], samples['fake'], 'EB', fitvar=fitvar, sampMan=sampManLLG )
    templates_iso_reg['EE']['fake'] = get_single_photon_template(fake_template_str_iso, binning['EE'], samples['fake'], 'EE', fitvar=fitvar, sampMan=sampManLLG )

    templates_noiso_reg = {}
    templates_noiso_reg['EB'] = {}
    templates_noiso_reg['EE'] = {}
    templates_noiso_reg['EB']['real'] = get_single_photon_template(real_template_str_noiso, binning['EB'], samples['real'], 'EB', fitvar=fitvar, sampMan=sampManLG  )
    templates_noiso_reg['EE']['real'] = get_single_photon_template(real_template_str_noiso, binning['EE'], samples['real'], 'EE', fitvar=fitvar, sampMan=sampManLG  )
    templates_noiso_reg['EB']['fake'] = get_single_photon_template(fake_template_str_noiso, binning['EB'], samples['fake'], 'EB', fitvar=fitvar, sampMan=sampManLLG )
    templates_noiso_reg['EE']['fake'] = get_single_photon_template(fake_template_str_noiso, binning['EE'], samples['fake'], 'EE', fitvar=fitvar, sampMan=sampManLLG )

    lead_iso_cuts   = None
    subl_iso_cuts   = None
    lead_noiso_cuts = None
    subl_noiso_cuts = None

    if iso_cuts_iso is not None :
        lead_iso_cuts = iso_cuts_iso.replace('[1]', '[0]')
        subl_iso_cuts = iso_cuts_iso.replace('[0]', '[1]')
    if iso_cuts_noiso is not None :
        lead_noiso_cuts = iso_cuts_noiso.replace('[1]', '[0]')
        subl_noiso_cuts = iso_cuts_noiso.replace('[0]', '[1]')

    regions = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB') ]

    for reg in regions :

        templates_leadiso = {}
        templates_leadiso['lead'] = {}
        templates_leadiso['subl'] = {}
        templates_leadiso['lead']['real'] = templates_iso_reg[reg[0]]['real']
        templates_leadiso['subl']['real'] = templates_noiso_reg[reg[1]]['real']
        templates_leadiso['lead']['fake'] = templates_iso_reg[reg[0]]['fake']
        templates_leadiso['subl']['fake'] = templates_noiso_reg[reg[1]]['fake']

        templates_subliso = {}
        templates_subliso['lead'] = {}
        templates_subliso['subl'] = {}
        templates_subliso['lead']['real'] = templates_noiso_reg[reg[0]]['real']
        templates_subliso['subl']['real'] = templates_iso_reg[reg[1]]['real']
        templates_subliso['lead']['fake'] = templates_noiso_reg[reg[0]]['fake']
        templates_subliso['subl']['fake'] = templates_iso_reg[reg[1]]['fake']

        templates_nom = {}
        templates_nom['lead'] = {}
        templates_nom['subl'] = {}
        templates_nom['subl']['real'] = templates_subliso['subl']['real']
        templates_nom['subl']['fake'] = templates_subliso['subl']['fake']
        templates_nom['lead']['real'] = templates_leadiso['lead']['real']
        templates_nom['lead']['fake'] = templates_leadiso['lead']['fake']

        
        # add regions onto the selection
        gg_selection_leadiso = get_default_draw_commands(ch)['gg'] + ' && is%s_leadph12 && is%s_sublph12 ' %( reg[0], reg[1] )
        gg_selection_subliso = get_default_draw_commands(ch)['gg'] + ' && is%s_leadph12 && is%s_sublph12 ' %( reg[0], reg[1] )

        # add object cuts to the selection
        if reg[0] == 'EB' :
            nom_iso_cuts_lead = 'chIsoCorr_leadph12 < 1.5 && neuIsoCorr_leadph12 < 1.0 && phoIsoCorr_leadph12 < 0.7 '
        if reg[0] == 'EE' :
            nom_iso_cuts_lead = 'chIsoCorr_leadph12 < 1.2 && neuIsoCorr_leadph12 < 1.5 && phoIsoCorr_leadph12 < 1.0 '

        if reg[1] == 'EB' :
            nom_iso_cuts_subl = 'chIsoCorr_sublph12 < 1.5 && neuIsoCorr_sublph12 < 1.0 && phoIsoCorr_sublph12 < 0.7 '
        if reg[1] == 'EE' :
            nom_iso_cuts_subl = 'chIsoCorr_sublph12 < 1.2 && neuIsoCorr_sublph12 < 1.5 && phoIsoCorr_sublph12 < 1.0 '


        if loose_iso_cuts is not None :
            gg_selection_leadiso = gg_selection_leadiso + ' && ph_iso%d%d%d_n > 1 && %s ' %(loose_iso_cuts[0], loose_iso_cuts[1], loose_iso_cuts[2], nom_iso_cuts_lead)
        if subl_noiso_cuts is not None :
            gg_selection_leadiso = gg_selection_leadiso + ' && chIsoCorr_sublph12 < %d && neuIsoCorr_sublph12 < %d && phoIsoCorr_sublph12 < %d ' %( loose_iso_cuts )

        if subl_iso_cuts is not None :
            gg_selection_subliso = gg_selection_subliso + ' && ph_iso%d%d%d_n > 1 && %s ' %(loose_iso_cuts[0], loose_iso_cuts[1], loose_iso_cuts[2], nom_iso_cuts_subl )
        if lead_noiso_cuts is not None :
            gg_selection_subliso = gg_selection_subliso + ' && chIsoCorr_leadph12 < %d && neuIsoCorr_leadph12 < %d && phoIsoCorr_leadph12 < %d ' %( loose_iso_cuts )

        # add subl pt cuts onto the selection
        if subl_ptrange[0] is not None :
            if subl_ptrange[1] is None :
                gg_selection_leadiso = gg_selection_leadiso + ' && pt_sublph12 > %d' %subl_ptrange[0]
                gg_selection_subliso = gg_selection_subliso + ' && pt_sublph12 > %d' %subl_ptrange[0]
            else :
                gg_selection_leadiso = gg_selection_leadiso + ' && pt_sublph12 > %d && pt_sublph12 < %d' %(subl_ptrange[0], subl_ptrange[1] )
                gg_selection_subliso = gg_selection_subliso + ' && pt_sublph12 > %d && pt_sublph12 < %d' %(subl_ptrange[0], subl_ptrange[1] )

        # parse out the x and y binning
        ybinn = binning[reg[1]]
        xbinn = binning[reg[0]]

        # variable given to TTree.Draw
        #var = 'ph_pt[0]:ph_sigmaIEIE[1]:ph_sigmaIEIE[0]' #z:y:x
        var = 'pt_leadph12:sieie_sublph12:sieie_leadph12' #z:y:x

        # get sample

        # for certain channels, use a different SampleManager
        if ch.count('invpixlead' ) :
            print 'USE sampManDataInvL'
            target_samp = sampManDataInvL.get_samples(name=samples['target'])

            # draw and get back the hist
            gg_hist_leadiso = clone_sample_and_draw( target_samp[0], var, gg_selection_leadiso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ),useSampMan=sampManDataInvL )
            gg_hist_subliso = clone_sample_and_draw( target_samp[0], var, gg_selection_subliso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ),useSampMan=sampManDataInvL )

        elif ch.count('invpixsubl' ) :
            print 'USE sampManDataInvS'
            target_samp = sampManDataInvS.get_samples(name=samples['target'])

            # draw and get back the hist
            gg_hist_leadiso = clone_sample_and_draw( target_samp[0], var, gg_selection_leadiso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ),useSampMan=sampManDataInvS )
            gg_hist_subliso = clone_sample_and_draw( target_samp[0], var, gg_selection_subliso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ),useSampMan=sampManDataInvS )

        else :
            print 'USE sampManData'

            target_samp = sampManData.get_samples(name=samples['target'])

            # draw and get back the hist
            gg_hist_leadiso = clone_sample_and_draw( target_samp[0], var, gg_selection_leadiso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ),useSampMan=sampManData )
            gg_hist_subliso = clone_sample_and_draw( target_samp[0], var, gg_selection_subliso, ( xbinn[0], xbinn[1], xbinn[2], ybinn[0], ybinn[1], ybinn[2], 100, 0, 500 ),useSampMan=sampManData )

        # -----------------------
        # inclusive result
        # -----------------------
        # project data hist
        gg_hist_leadiso_inclusive = gg_hist_leadiso.Project3D( 'yx' )
        gg_hist_subliso_inclusive = gg_hist_subliso.Project3D( 'yx' )

        templates_leadiso_inclusive = get_projected_templates( templates_leadiso, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )
        templates_subliso_inclusive = get_projected_templates( templates_subliso, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )
        templates_nom_inclusive = get_projected_templates( templates_nom, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )

        (results_corr_stat, results_corr_syst)  = run_corrected_diphoton_fit(templates_leadiso_inclusive, templates_subliso_inclusive, gg_hist_leadiso_inclusive, gg_hist_subliso_inclusive, reg[0], reg[1], lead_ptrange=(None,None), subl_ptrange=subl_ptrange, outputDir=outputDir, outputPrefix='__%s' %ch, systematics=systematics)

        namePostfix = '__%s__%s-%s' %( ch,reg[0], reg[1] )

        save_templates( templates_nom_inclusive, outputDir, lead_ptrange=(None,None), subl_ptrange=(None,None),namePostfix=namePostfix )
        save_results( results_corr_stat, outputDir, namePostfix)

        namePostfix_syst = '__syst%s' %namePostfix
        save_results( results_corr_syst, outputDir, namePostfix_syst)

        # -----------------------
        # pt binned results
        # -----------------------
        for idx, ptmin in enumerate(ptbins[:-1] ) :

            ptmax = ptbins[idx+1]

            # put lead range together (expected by following code)
            if ptmax == ptbins[-1] : 
                lead_ptrange = ( ptmin, None )
            else :
                lead_ptrange = ( ptmin, ptmax )

            print 'ptmin = %d, ptmax = %d, Min Z bin = %d, max Z bin = %d' %( ptmin, ptmax, gg_hist_leadiso.GetZaxis().FindBin( ptmin), gg_hist_leadiso.GetZaxis().FindBin( ptmax )-1 )
            # project data hist
            gg_hist_leadiso.GetZaxis().SetRange( gg_hist_leadiso.GetZaxis().FindBin( ptmin), gg_hist_leadiso.GetZaxis().FindBin( ptmax )-1 )
            gg_hist_leadiso_pt = gg_hist_leadiso.Project3D( 'yx' )

            gg_hist_subliso.GetZaxis().SetRange( gg_hist_subliso.GetZaxis().FindBin( ptmin), gg_hist_subliso.GetZaxis().FindBin( ptmax )-1 )
            gg_hist_subliso_pt = gg_hist_subliso.Project3D( 'yx' )

            # determine the proper
            # sublead range given
            # the input lead and
            # sublead 
            if subl_ptrange[0] is not None :
                subl_min = subl_ptrange[0]
            else :
                subl_min = 15
            if subl_ptrange[1] is not None :
                if lead_ptrange[1] is None :
                    subl_max = subl_ptrange[1]
                elif lead_ptrange[1] < subl_ptrange[1] :
                    subl_max = lead_ptrange[1]
                else :
                    subl_max = subl_ptrange[1]
            else :
                subl_max = lead_ptrange[1]

                
            # get templates
            templates_leadiso_pt = get_projected_templates( templates_leadiso, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max) )
            templates_subliso_pt = get_projected_templates( templates_subliso, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max) )
            templates_nom_pt = get_projected_templates( templates_nom, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max) )

            # get results
            (results_corr_pt_stat, results_corr_pt_syst) = run_corrected_diphoton_fit(templates_leadiso_pt, templates_subliso_pt, gg_hist_leadiso_pt, gg_hist_subliso_pt, reg[0], reg[1], lead_ptrange=lead_ptrange, subl_ptrange=(subl_min, subl_max), outputDir=outputDir, outputPrefix='__%s'%ch, systematics=systematics)

            namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )

            if lead_ptrange[0] is not None :
                if lead_ptrange[1] is None :
                    namePostfix += '__pt_%d-max' %lead_ptrange[0]
                else :
                    namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )

            if subl_ptrange[0] is not None :
                if subl_ptrange[1] is None :
                    namePostfix += '__subpt_%d-max' %subl_ptrange[0]
                else :
                    namePostfix += '__subpt_%d-%d' %(subl_ptrange[0], subl_ptrange[1] )

            save_templates( templates_nom_pt, outputDir, lead_ptrange=lead_ptrange, subl_ptrange=(subl_min,subl_max), namePostfix=namePostfix)
            save_results( results_corr_pt_stat, outputDir, namePostfix)

            namePostfix_syst = '__syst%s' %namePostfix
            save_results( results_corr_pt_syst, outputDir, namePostfix_syst)

def do_closure_fit( iso_cuts_lead=None, iso_cuts_subl=None, ptbins=[], subl_ptrange=None, ch='mu', ngen=None, corr_factor=0.0, outputDir=None ) :

    if ngen is None :
        ngen = { 'RF' : 10000, 'FR' : 10000, 'FF' : 10000 }

    binning = get_default_binning()
    samples = get_default_samples(ch)

    # generate templates for both EB and EE
    real_template_str = get_default_draw_commands(ch )['real'] + ' && %s' %iso_cuts_lead
    fake_template_str = get_default_draw_commands(ch )['fake'] + ' && %s' %iso_cuts_lead

    templates_reg = {}
    templates_reg['EB'] = {}
    templates_reg['EE'] = {}
    templates_reg['EB']['real'] = get_single_photon_template(real_template_str, binning['EB'], samples['real'], 'EB', sampMan=sampManLG )
    templates_reg['EE']['real'] = get_single_photon_template(real_template_str, binning['EE'], samples['real'], 'EE', sampMan=sampManLG )
    templates_reg['EB']['fake'] = get_single_photon_template(fake_template_str, binning['EB'], samples['fake'], 'EB', sampMan=sampManLLG)
    templates_reg['EE']['fake'] = get_single_photon_template(fake_template_str, binning['EE'], samples['fake'], 'EE', sampMan=sampManLLG)

    regions = [ ('EB', 'EB'), ('EB', 'EE'), ('EE', 'EB'), ('EE', 'EE') ]
    for reg in regions :

        # convert from regions to lead/subl
        templates = {}
        templates['lead'] = {}
        templates['subl'] = {}
        templates['lead']['real'] = templates_reg[reg[0]]['real']
        templates['subl']['real'] = templates_reg[reg[1]]['real']
        templates['lead']['fake'] = templates_reg[reg[0]]['fake']
        templates['subl']['fake'] = templates_reg[reg[1]]['fake']

        templates_inclusive = get_projected_templates( templates, lead_ptrange = (None,None), subl_ptrange=subl_ptrange )

        results_inclusive = run_generated_diphoton_fit(templates_inclusive, reg[0], reg[1], ngen, corr_factor=corr_factor, outputDir=outputDir, outputPrefix='__%s'%ch )

        print results_inclusive

        #namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
        #save_templates( templates_inclusive, outputDir, lead_ptrange=(None,None), subl_ptrange=(None,None), namePostfix=namePostfix )
        #save_results( results_inclusive, outputDir, namePostfix )

        # -----------------------
        # pt binned results
        # -----------------------
        for idx, ptmin in enumerate(ptbins[:-1] ) :
            ptmax = ptbins[idx+1]

            # put lead range together (expected by following code)
            if ptmax == ptbins[-1] : 
                lead_ptrange = ( ptmin, None )
            else :
                lead_ptrange = ( ptmin, ptmax )

            # get templates
            templates_pt = get_projected_templates( templates, lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1] ) )

            # get results
            results_pt = run_generated_diphoton_fit(templates_pt, reg[0], reg[1],ngen, corr_factor=corr_factor, outputDir=outputDir, outputPrefix='__%s' %ch )

            print results_pt

            #namePostfix = '__%s__%s-%s' %( ch, reg[0], reg[1] )
            #if lead_ptrange[0] is not None :
            #    if lead_ptrange[1] is None :
            #        namePostfix += '__pt_%d-max' %lead_ptrange[0]
            #    else :
            #        namePostfix += '__pt_%d-%d' %(lead_ptrange[0], lead_ptrange[1] )

            #if subl_ptrange[0] is not None :
            #    if subl_ptrange[1] is None :
            #        namePostfix += '__subpt_%d-max' %subl_ptrange[0]
            #    else :
            #        namePostfix += '__subpt_%d-%d' %(subl_ptrange[0], subl_ptrange[1] )

            #save_templates( templates_pt, outputDir, lead_ptrange=lead_ptrange, subl_ptrange=(15, lead_ptrange[1]), namePostfix=namePostfix )
            #save_results( results_pt, outputDir, namePostfix )


def update_asym_results( results_leadiso, results_subliso ) :
        
    iso_eff_subl = (results_subliso['template_int_subl_fake_tight']+results_subliso['template_int_subl_fake_loose'])/(results_leadiso['template_int_subl_fake_tight']+results_leadiso['template_int_subl_fake_loose'])
    iso_eff_lead = (results_leadiso['template_int_lead_fake_tight']+results_leadiso['template_int_lead_fake_loose'])/(results_subliso['template_int_lead_fake_tight']+results_subliso['template_int_lead_fake_loose'])

    results_leadiso['iso_eff_subl'] = iso_eff_subl
    results_subliso['iso_eff_lead'] = iso_eff_lead

    results_leadiso['Npred_RF_TT_scaled'] = results_leadiso['Npred_RF_TT']*iso_eff_subl
    results_leadiso['Npred_FR_TT_scaled'] = results_leadiso['Npred_FR_TT']*iso_eff_subl
    results_leadiso['Npred_FF_TT_scaled'] = results_leadiso['Npred_FF_TT']*iso_eff_subl

    results_leadiso['Npred_RF_TL_scaled'] = results_leadiso['Npred_RF_TL']*iso_eff_subl
    results_leadiso['Npred_FR_TL_scaled'] = results_leadiso['Npred_FR_TL']*iso_eff_subl
    results_leadiso['Npred_FF_TL_scaled'] = results_leadiso['Npred_FF_TL']*iso_eff_subl

    results_leadiso['Npred_RF_LT_scaled'] = results_leadiso['Npred_RF_LT']*iso_eff_subl
    results_leadiso['Npred_FR_LT_scaled'] = results_leadiso['Npred_FR_LT']*iso_eff_subl
    results_leadiso['Npred_FF_LT_scaled'] = results_leadiso['Npred_FF_LT']*iso_eff_subl

    results_leadiso['Npred_RF_LL_scaled'] = results_leadiso['Npred_RF_LL']*iso_eff_subl
    results_leadiso['Npred_FR_LL_scaled'] = results_leadiso['Npred_FR_LL']*iso_eff_subl
    results_leadiso['Npred_FF_LL_scaled'] = results_leadiso['Npred_FF_LL']*iso_eff_subl

    results_subliso['Npred_RF_TT_scaled'] = results_subliso['Npred_RF_TT']*iso_eff_lead
    results_subliso['Npred_FR_TT_scaled'] = results_subliso['Npred_FR_TT']*iso_eff_lead
    results_subliso['Npred_FF_TT_scaled'] = results_subliso['Npred_FF_TT']*iso_eff_lead

    results_subliso['Npred_RF_TL_scaled'] = results_subliso['Npred_RF_TL']*iso_eff_lead
    results_subliso['Npred_FR_TL_scaled'] = results_subliso['Npred_FR_TL']*iso_eff_lead
    results_subliso['Npred_FF_TL_scaled'] = results_subliso['Npred_FF_TL']*iso_eff_lead

    results_subliso['Npred_RF_LT_scaled'] = results_subliso['Npred_RF_LT']*iso_eff_lead
    results_subliso['Npred_FR_LT_scaled'] = results_subliso['Npred_FR_LT']*iso_eff_lead
    results_subliso['Npred_FF_LT_scaled'] = results_subliso['Npred_FF_LT']*iso_eff_lead

    results_subliso['Npred_RF_LL_scaled'] = results_subliso['Npred_RF_LL']*iso_eff_lead
    results_subliso['Npred_FR_LL_scaled'] = results_subliso['Npred_FR_LL']*iso_eff_lead
    results_subliso['Npred_FF_LL_scaled'] = results_subliso['Npred_FF_LL']*iso_eff_lead

def get_projected_templates( templates, lead_ptrange=(None,None), subl_ptrange=(None,None) ) :

    templates_proj = {}
    templates_proj['lead'] = {}
    templates_proj['subl'] = {}

    # project in a range
    if lead_ptrange[0] is not None :
        for rf, hist_entries in templates['lead'].iteritems() :
            templates_proj['lead'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is None :
                    templates_proj['lead'][rf][hist_type] = None
                else :
                    if lead_ptrange[1] is None :
                        templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-max' %( lead_ptrange[0] ), hist.GetYaxis().FindBin( lead_ptrange[0] ) )
                    else :
                        templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-%d' %( lead_ptrange[0], lead_ptrange[1] ), hist.GetYaxis().FindBin( lead_ptrange[0] ), hist.GetYaxis().FindBin( lead_ptrange[1] )-1 )

    else : # project inclusive
        for rf, hist_entries in templates['lead'].iteritems() :
            templates_proj['lead'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is not None :
                    templates_proj['lead'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_inclusive' )
                else :
                    templates_proj['lead'][rf][hist_type] = None


    if subl_ptrange[0] is not None : # project in a range
        for rf, hist_entries in templates['subl'].iteritems() :
            templates_proj['subl'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is None :
                    templates_proj['subl'][rf][hist_type] = None
                else :
                    if subl_ptrange[1] is None :
                        templates_proj['subl'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-max' %subl_ptrange[0], hist.GetYaxis().FindBin( subl_ptrange[0] ) )
                    else :
                        templates_proj['subl'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_%d-%d' %(subl_ptrange[0],subl_ptrange[1]), hist.GetYaxis().FindBin( subl_ptrange[0] ) , hist.GetYaxis().FindBin( subl_ptrange[1] )-1 )
    else : # project inclusive
        for rf, hist_entries in templates['subl'].iteritems() :
            templates_proj['subl'][rf] = {}
            for hist_type, hist in hist_entries.iteritems() : 
                if hist is None :
                    templates_proj['subl'][rf][hist_type] = None
                else :
                    templates_proj['subl'][rf][hist_type] = hist.ProjectionX( hist.GetName()+'_px_inclusive' )

    return templates_proj


def run_corrected_diphoton_fit( templates_leadiso, templates_subliso, gg_hist_leadiso, gg_hist_subliso, lead_reg, subl_reg, lead_ptrange=(None,None), subl_ptrange=(None,None), ndim=3, outputDir=None, outputPrefix='', systematics=None ) :

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return
    if subl_reg not in accept_reg :
        print 'Subl region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    # Find the bins corresponding to the cuts
    # lead photon on X axis, subl on Y axis
    bins_lead_tight = ( gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['tight'][0] ), gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['tight'][1] ) )
    bins_lead_loose = ( gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['loose'][0] ), gg_hist_leadiso.GetXaxis().FindBin( cuts[lead_reg]['loose'][1] ) )
    bins_subl_tight = ( gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['tight'][0] ), gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['tight'][1] ) )
    bins_subl_loose = ( gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['loose'][0] ), gg_hist_leadiso.GetYaxis().FindBin( cuts[subl_reg]['loose'][1] ) )

    print 'cuts, bins lead, tight = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['tight'][0], cuts[lead_reg]['tight'][1], bins_lead_tight[0], bins_lead_tight[1] )
    print 'cuts, bins lead, loose = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['loose'][0], cuts[lead_reg]['loose'][1], bins_lead_loose[0], bins_lead_loose[1] )
    print 'cuts, bins subl, tight = %f-%f ( %d - %d ) ' %( cuts[subl_reg]['tight'][0], cuts[subl_reg]['tight'][1], bins_subl_tight[0], bins_subl_tight[1] )
    print 'cuts, bins subl, loose = %f-%f ( %d - %d ) ' %( cuts[subl_reg]['loose'][0], cuts[subl_reg]['loose'][1], bins_subl_loose[0], bins_subl_loose[1] )

    # arragnge the cuts by region
    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['subl'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']
    eff_cuts['subl']['tight'] = cuts[subl_reg]['tight']
    eff_cuts['subl']['loose'] = cuts[subl_reg]['loose']

    # get template integrals
    #int_leadiso = get_template_integrals( templates_leadiso, eff_cuts )
    #int_subliso = get_template_integrals( templates_subliso, eff_cuts )
    (stat_int_leadiso, syst_int_leadiso) = get_template_integrals( templates_leadiso, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )
    (stat_int_subliso, syst_int_subliso) = get_template_integrals( templates_subliso, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    iso_eff_subl_tight = stat_int_subliso['subl']['fake']['tight'] / stat_int_leadiso['subl']['fake']['tight']
    iso_eff_subl_loose = stat_int_subliso['subl']['fake']['loose'] / stat_int_leadiso['subl']['fake']['loose']

    iso_eff_lead_tight = stat_int_leadiso['lead']['fake']['tight'] / stat_int_subliso['lead']['fake']['tight']
    iso_eff_lead_loose = stat_int_leadiso['lead']['fake']['loose'] / stat_int_subliso['lead']['fake']['loose']

    # Integrate to the the data in the four regions
    Ndata_TT_leadiso = gg_hist_leadiso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_TL_leadiso = gg_hist_leadiso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_loose[0], bins_subl_loose[1] )
    Ndata_LT_leadiso = gg_hist_leadiso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_LL_leadiso = gg_hist_leadiso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_loose[0], bins_subl_loose[1] )

    Ndata_TT_subliso = gg_hist_subliso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_TL_subliso = gg_hist_subliso.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_loose[0], bins_subl_loose[1] )
    Ndata_LT_subliso = gg_hist_subliso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_LL_subliso = gg_hist_subliso.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_loose[0], bins_subl_loose[1] )

    #-----------------------------------------
    # Use data with loosened iso on the Loose photon
    # Multiply by the efficiency of the loosened iso
    #-----------------------------------------
     
    # lead has loosened iso
    # Correct data in LT region by loosening isolation on the lead photon 
    # and correct by the efficiency of the loosened selection
    Ncorr_LT         = Ndata_LT_subliso * iso_eff_lead_loose
    Ncorr_LL_subliso = Ndata_LL_subliso * iso_eff_lead_loose
    Ncorr_TT_subliso = Ndata_TT_subliso * iso_eff_lead_loose

    # subl has loosened iso
    # correct data in TL region by loosening isolation on the subl photon
    # and correct by the efficiency of the loosened selection
    Ncorr_TL         = Ndata_TL_leadiso * iso_eff_subl_loose
    Ncorr_LL_leadiso = Ndata_LL_leadiso * iso_eff_subl_loose
    Ncorr_TT_leadiso = Ndata_TT_leadiso * iso_eff_subl_loose

    # use the average of the two
    Ncorr_LL = ( Ncorr_LL_leadiso + Ncorr_LL_subliso )/2.
    Ncorr_TT = ( Ncorr_TT_leadiso + Ncorr_TT_subliso )/2.

    print 'NData orig leadiso , TT = %d, TL = %d, LT = %d, LL = %d' %( Ndata_TT_leadiso, Ndata_TL_leadiso, Ndata_LT_leadiso, Ndata_LL_leadiso )
    print 'NData orig subliso , TT = %d, TL = %d, LT = %d, LL = %d' %( Ndata_TT_subliso, Ndata_TL_subliso, Ndata_LT_subliso, Ndata_LL_subliso )
    print 'iso_eff_subl_tight = %s, iso_eff_subl_loose = %s, iso_eff_lead_tight = %s, iso_eff_lead_loose= %s' %( iso_eff_subl_tight, iso_eff_subl_loose, iso_eff_lead_tight, iso_eff_subl_loose )
    print 'NData corr, TL = %s, LT = %s, LLlead = %s, LLsubl = %s, LL = %s, TTlead = %s, TTsubl = %s, TT = %s ' %( Ncorr_TL, Ncorr_LT, Ncorr_LL_leadiso, Ncorr_LL_subliso, Ncorr_LL, Ncorr_TT_leadiso, Ncorr_TT_subliso, Ncorr_TT )

    templates_corr = {}
    templates_corr['lead'] = {}
    templates_corr['subl'] = {}
    templates_corr['lead']['real'] = templates_leadiso['lead']['real']
    templates_corr['lead']['fake'] = templates_leadiso['lead']['fake']
    templates_corr['subl']['real'] = templates_subliso['subl']['real']
    templates_corr['subl']['fake'] = templates_subliso['subl']['fake']

    # get 2-d efficiencies from 1-d inputs
    (eff_2d_stat, eff_2d_syst) = generate_2d_efficiencies( templates_corr, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )
    print eff_2d_stat

    if ndim == 3 :
        datacorr = {}
        datacorr['TL'] = Ncorr_TL
        datacorr['LT'] = Ncorr_LT
        datacorr['LL'] = Ncorr_LL
        results_stat = run_fit( datacorr, eff_2d_stat )
        results_syst= run_fit( datacorr, eff_2d_syst )

        datacorr['TT'] = ufloat(0, 0)

        text_results_stat = collect_results( results_stat, datacorr, eff_2d_stat, templates_corr, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim)
        text_results_syst = collect_results( results_syst, datacorr, eff_2d_syst, templates_corr, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim)

        
        print 'text_results_stat'
        print text_results_stat
        print 'text_results_syst'
        print text_results_syst

        print 'Npred_RF_TT = ', text_results_stat['Npred_RF_TT']
        print 'Npred_FR_TT = ', text_results_stat['Npred_FR_TT']
        print 'Npred_FF_TT = ', text_results_stat['Npred_FF_TT']
        print 'Sum = ', (text_results_stat['Npred_RF_TT']+text_results_stat['Npred_FR_TT']+text_results_stat['Npred_FF_TT'])


        return text_results_stat, text_results_syst
    else :
        print 'IMPLEMENT DIM4'
        return




def run_generated_diphoton_fit( templates, lead_reg, subl_reg, n_data_gen, ndim=3, corr_factor=0.0, outputDir=None, outputPrefix='' ) :

    rand = ROOT.TRandom3()
    rand.SetSeed( int(time.mktime(time.localtime()) ) )

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return
    if subl_reg not in accept_reg :
        print 'Subl region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning()
    cuts = get_default_cuts()

    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['subl'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']
    eff_cuts['subl']['tight'] = cuts[subl_reg]['tight']
    eff_cuts['subl']['loose'] = cuts[subl_reg]['loose']

    # get 2-d efficiencies from 1-d inputs
    (eff_2d, eff_2d_syst) = generate_2d_efficiencies( templates, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange )
    print eff_2d

    Ndata = {}
    Ndata['TT'] = 0
    Ndata['TL'] = 0
    Ndata['LT'] = 0
    Ndata['LL'] = 0
    
    eff_1d_lead_base = {}
    eff_1d_subl_base = {}
    eff_1d_lead_base['eff_F_T'] = eff_2d['eff_FF_TT'] + eff_2d['eff_FF_TL']
    eff_1d_lead_base['eff_F_L'] = eff_2d['eff_FF_LL'] + eff_2d['eff_FF_LT']
    eff_1d_subl_base['eff_F_T'] = eff_2d['eff_FF_TT'] + eff_2d['eff_FF_LT']
    eff_1d_subl_base['eff_F_L'] = eff_2d['eff_FF_LL'] + eff_2d['eff_FF_TL']

    print 'eff_1d_lead'
    print eff_1d_lead_base
    print 'eff_1d_subl'
    print eff_1d_subl_base

    # do FR
    #for tag in ['FR', 'RF', 'FF'] :
    for tag in ['FR', 'RF'] :
        for i in xrange( 0, n_data_gen[tag] ) :

            rndmval = rand.Rndm()

            lead_tight = None
            subl_tight = None

            # 2d efficiencies are normalized to unity...just linearize the efficiencies to determine
            # where the photons landed
            if rndmval < (eff_2d['eff_%s_TT'%tag]) :
                Ndata['TT'] = Ndata['TT']+1
            elif rndmval < (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag]) :
                Ndata['TL'] = Ndata['TL']+1
            elif rndmval < (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag] + eff_2d['eff_%s_LT'%tag]) :
                Ndata['LT'] = Ndata['LT']+1
            elif rndmval < (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag] + eff_2d['eff_%s_LT'%tag] + eff_2d['eff_%s_LL'%tag]) :
                Ndata['LL'] = Ndata['LL']+1
            else :
                print 'SHOULD NOT GET HERE -- templates not normalized to unity, it is ', (eff_2d['eff_%s_TT'%tag] + eff_2d['eff_%s_TL'%tag] + eff_2d['eff_%s_LT'%tag] + eff_2d['eff_%s_LL'%tag])

    # do FF, allow for a correlation 
    for i in xrange( 0, n_data_gen['FF'] ) :
        # decide which photon to select first
        lead_first = (rand.Rndm() < 0.5)
        # generate random numbers for lead and subl
        lead_rndm = rand.Rndm()
        subl_rndm = rand.Rndm()

        lead_tight = None
        subl_tight = None
        eff_1d_lead = {}
        eff_1d_subl = {}
        if lead_first :

            #make sure efficiencies are normalized to unity
            lead_norm = 1.0/(eff_1d_lead_base['eff_F_T']+eff_1d_lead_base['eff_F_L'])

            eff_1d_lead['eff_F_T'] = lead_norm*eff_1d_lead_base['eff_F_T']
            eff_1d_lead['eff_F_L'] = lead_norm*eff_1d_lead_base['eff_F_L']


            # determine if the lead photon is loose or tight
            # modify the subl efficiency based on the given correction factor
            if lead_rndm < eff_1d_lead['eff_F_T'] : 
                lead_tight = True
                eff_1d_subl['eff_F_L'] = eff_1d_subl_base['eff_F_L']*(1-corr_factor)
                eff_1d_subl['eff_F_T'] = eff_1d_subl_base['eff_F_T']
            else :
                lead_tight = False
                eff_1d_subl['eff_F_L'] = eff_1d_subl_base['eff_F_L']*(1+corr_factor)
                eff_1d_subl['eff_F_T'] = eff_1d_subl_base['eff_F_T']

            # normalize the modified subl efficiencies
            subl_norm = 1.0/(eff_1d_subl['eff_F_T']+eff_1d_subl['eff_F_L'])
            eff_1d_subl['eff_F_T'] = subl_norm*eff_1d_subl['eff_F_T']
            eff_1d_subl['eff_F_L'] = subl_norm*eff_1d_subl['eff_F_L']

            # check if subl is loose or tight
            if subl_rndm < eff_1d_subl['eff_F_T'] : 
                subl_tight = True
            else :
                subl_tight = False

        else :

            #make sure efficiencies are normalized to unity
            subl_norm = 1.0/(eff_1d_subl_base['eff_F_T']+eff_1d_subl_base['eff_F_L'])
            eff_1d_subl['eff_F_T'] = subl_norm*eff_1d_subl_base['eff_F_T']
            eff_1d_subl['eff_F_L'] = subl_norm*eff_1d_subl_base['eff_F_L']


            # determine if the subl photon is loose or tight
            # modify the lead efficiency based on the given correction factor
            if subl_rndm < eff_1d_subl['eff_F_T'] : 
                subl_tight = True
                eff_1d_lead['eff_F_L'] = eff_1d_lead_base['eff_F_L']*(1-corr_factor)
                eff_1d_lead['eff_F_T'] = eff_1d_lead_base['eff_F_T']
            else :
                subl_tight = False
                eff_1d_lead['eff_F_L'] = eff_1d_lead_base['eff_F_L']*(1+corr_factor)
                eff_1d_lead['eff_F_T'] = eff_1d_lead_base['eff_F_T']

            # normalize the modified lead efficiencies
            lead_norm = 1.0/(eff_1d_lead['eff_F_T']+eff_1d_lead['eff_F_L'])
            eff_1d_lead['eff_F_T'] = lead_norm*eff_1d_lead['eff_F_T']
            eff_1d_lead['eff_F_L'] = lead_norm*eff_1d_lead['eff_F_L']

            # check if lead is loose or tight
            if lead_rndm < eff_1d_lead['eff_F_T'] : 
                lead_tight = True
            else :
                lead_tight = False

        # make sure they were set
        if lead_tight is None or subl_tight is None :
            print 'Something went wrong!'
            return

        # fill the data
        if lead_tight and subl_tight :
            Ndata['TT'] = Ndata['TT']+1
        elif lead_tight and not subl_tight :
            Ndata['TL'] = Ndata['TL']+1
        elif not lead_tight and subl_tight :
            Ndata['LT'] = Ndata['LT']+1
        else  :
            Ndata['LL'] = Ndata['LL']+1

    Ndata['TT'] = ufloat( Ndata['TT'], math.sqrt( Ndata['TT'] ) )
    Ndata['TL'] = ufloat( Ndata['TL'], math.sqrt( Ndata['TL'] ) )
    Ndata['LT'] = ufloat( Ndata['LT'], math.sqrt( Ndata['LT'] ) )
    Ndata['LL'] = ufloat( Ndata['LL'], math.sqrt( Ndata['LL'] ) )

    print Ndata

    if ndim == 3 :
        results = run_fit( {'TL': Ndata['TL'], 'LT' : Ndata['LT'], 'LL' : Ndata['LL']}, eff_2d )
    if ndim == 4 :
        results = run_fit( Ndata, eff_2d )


    text_results=collections.OrderedDict()

    for key, val in eff_2d.iteritems() :
        text_results[key] = val

    if ndim == 4 :

        text_results['Ndata_TT'] = Ndata['TT']
        text_results['Ndata_TL'] = Ndata['TL']
        text_results['Ndata_LT'] = Ndata['LT']
        text_results['Ndata_LL'] = Ndata['LL']

        text_results['alpha_RR'] = results.item(0)
        text_results['alpha_RF'] = results.item(1)
        text_results['alpha_FR'] = results.item(2)
        text_results['alpha_FF'] = results.item(3)

        text_results['Npred_RR_TT'] = text_results['alpha_RR']*text_results['eff_RR_TT']
        text_results['Npred_RR_TL'] = text_results['alpha_RR']*text_results['eff_RR_TL']
        text_results['Npred_RR_LT'] = text_results['alpha_RR']*text_results['eff_RR_LT']
        text_results['Npred_RR_LL'] = text_results['alpha_RR']*text_results['eff_RR_LL']

    else :
        text_results['Ndata_TT'] = ufloat(0, 0)
        text_results['Ndata_TL'] = Ndata['TL']
        text_results['Ndata_LT'] = Ndata['LT']
        text_results['Ndata_LL'] = Ndata['LL']

        text_results['alpha_RF'] = results.item(0)
        text_results['alpha_FR'] = results.item(1)
        text_results['alpha_FF'] = results.item(2)


    text_results['Npred_RF_TT'] = text_results['alpha_RF']*text_results['eff_RF_TT']
    text_results['Npred_RF_TL'] = text_results['alpha_RF']*text_results['eff_RF_TL']
    text_results['Npred_RF_LT'] = text_results['alpha_RF']*text_results['eff_RF_LT']
    text_results['Npred_RF_LL'] = text_results['alpha_RF']*text_results['eff_RF_LL']

    text_results['Npred_FR_TT'] = text_results['alpha_FR']*text_results['eff_FR_TT']
    text_results['Npred_FR_TL'] = text_results['alpha_FR']*text_results['eff_FR_TL']
    text_results['Npred_FR_LT'] = text_results['alpha_FR']*text_results['eff_FR_LT']
    text_results['Npred_FR_LL'] = text_results['alpha_FR']*text_results['eff_FR_LL']

    text_results['Npred_FF_TT'] = text_results['alpha_FF']*text_results['eff_FF_TT']
    text_results['Npred_FF_TL'] = text_results['alpha_FF']*text_results['eff_FF_TL']
    text_results['Npred_FF_LT'] = text_results['alpha_FF']*text_results['eff_FF_LT']
    text_results['Npred_FF_LL'] = text_results['alpha_FF']*text_results['eff_FF_LL']

    text_results['Closure_TT'] = ( (text_results['Npred_RF_TT'] +text_results['Npred_FR_TT'] +text_results['Npred_FF_TT'] ) - Ndata['TT'] ) / Ndata['TT']
    text_results['Closure_TL'] = ( (text_results['Npred_RF_TL'] +text_results['Npred_FR_TL'] +text_results['Npred_FF_TL'] ) - Ndata['TL'] ) / Ndata['TL']
    text_results['Closure_LT'] = ( (text_results['Npred_RF_LT'] +text_results['Npred_FR_LT'] +text_results['Npred_FF_LT'] ) - Ndata['LT'] ) / Ndata['LT']
    text_results['Closure_LL'] = ( (text_results['Npred_RF_LL'] +text_results['Npred_FR_LL'] +text_results['Npred_FF_LL'] ) - Ndata['LL'] ) / Ndata['LL']

    print text_results


def run_diphoton_fit( templates, gg_hist, lead_reg, subl_reg, lead_ptrange=(None,None), subl_ptrange=(None,None), ndim=3, outputDir=None, outputPrefix='', systematics=None, fitvar='sigmaIEIE' ) :

    accept_reg = ['EB', 'EE']
    if lead_reg not in accept_reg :
        print 'Lead region does not make sense'
        return
    if subl_reg not in accept_reg :
        print 'Subl region does not make sense'
        return

    # get the defaults
    samples = get_default_samples()
    plotbinning = get_default_binning(fitvar)
    cuts = get_default_cuts(fitvar)

    # Find the bins corresponding to the cuts
    # lead photon on X axis, subl on Y axis
    bins_lead_tight = ( gg_hist.GetXaxis().FindBin( cuts[lead_reg]['tight'][0] ), gg_hist.GetXaxis().FindBin( cuts[lead_reg]['tight'][1] ) )
    bins_lead_loose = ( gg_hist.GetXaxis().FindBin( cuts[lead_reg]['loose'][0] ), gg_hist.GetXaxis().FindBin( cuts[lead_reg]['loose'][1] ) )
    bins_subl_tight = ( gg_hist.GetYaxis().FindBin( cuts[subl_reg]['tight'][0] ), gg_hist.GetYaxis().FindBin( cuts[subl_reg]['tight'][1] ) )
    bins_subl_loose = ( gg_hist.GetYaxis().FindBin( cuts[subl_reg]['loose'][0] ), gg_hist.GetYaxis().FindBin( cuts[subl_reg]['loose'][1] ) )

    print 'cuts, bins lead, tight = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['tight'][0], cuts[lead_reg]['tight'][1], bins_lead_tight[0], bins_lead_tight[1] )
    print 'cuts, bins lead, loose = %f-%f ( %d - %d ) ' %( cuts[lead_reg]['loose'][0], cuts[lead_reg]['loose'][1], bins_lead_loose[0], bins_lead_loose[1] )
    print 'cuts, bins subl, tight = %f-%f ( %d - %d ) ' %( cuts[subl_reg]['tight'][0], cuts[subl_reg]['tight'][1], bins_subl_tight[0], bins_subl_tight[1] )
    print 'cuts, bins subl, loose = %f-%f ( %d - %d ) ' %( cuts[subl_reg]['loose'][0], cuts[subl_reg]['loose'][1], bins_subl_loose[0], bins_subl_loose[1] )

    # Integrate to the the data in the four regions
    Ndata_TT = gg_hist.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_TL = gg_hist.Integral( bins_lead_tight[0], bins_lead_tight[1], bins_subl_loose[0], bins_subl_loose[1] )
    Ndata_LT = gg_hist.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_tight[0], bins_subl_tight[1] )
    Ndata_LL = gg_hist.Integral( bins_lead_loose[0], bins_lead_loose[1], bins_subl_loose[0], bins_subl_loose[1] )

    # ufloat it!
    Ndata = {}
    Ndata['TT'] = ufloat( Ndata_TT, math.sqrt(Ndata_TT ), 'Ndata_TT' )
    Ndata['TL'] = ufloat( Ndata_TL, math.sqrt(Ndata_TL ), 'Ndata_TL' )
    Ndata['LT'] = ufloat( Ndata_LT, math.sqrt(Ndata_LT ), 'Ndata_LT' )
    Ndata['LL'] = ufloat( Ndata_LL, math.sqrt(Ndata_LL ), 'Ndata_LL' )

    print 'N data TT = ', Ndata['TT']
    print 'N data TL = ', Ndata['TL']
    print 'N data LT = ', Ndata['LT']
    print 'N data LL = ', Ndata['LL']

    # arragnge the cuts by 
    eff_cuts = {}
    eff_cuts['lead'] = {}
    eff_cuts['subl'] = {}
    eff_cuts['lead']['tight'] = cuts[lead_reg]['tight']
    eff_cuts['lead']['loose'] = cuts[lead_reg]['loose']
    eff_cuts['subl']['tight'] = cuts[subl_reg]['tight']
    eff_cuts['subl']['loose'] = cuts[subl_reg]['loose']

    # get 2-d efficiencies from 1-d inputs
    (eff_2d_stat, eff_2d_syst) = generate_2d_efficiencies( templates, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )
    print eff_2d_stat
    (eff_1d_stat, eff_1d_syst) =generate_1d_efficiencies( templates, eff_cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    print 'EFF_1D'
    print eff_1d_stat

    if ndim == 3 :
        results_stat = run_fit( {'TL': Ndata['TL'], 'LT' : Ndata['LT'], 'LL' : Ndata['LL']}, eff_2d_stat )
        results_syst = run_fit( {'TL': Ndata['TL'], 'LT' : Ndata['LT'], 'LL' : Ndata['LL']}, eff_2d_syst )
        #results_stat_manual = run_fit_manual( {'TL': Ndata['TL'], 'LT' : Ndata['LT'], 'LL' : Ndata['LL']}, eff_1d_stat )
        #results_syst_manual = run_fit_manual( {'TL': Ndata['TL'], 'LT' : Ndata['LT'], 'LL' : Ndata['LL']}, eff_1d_syst )
    if ndim == 4 :
        print 'RUNNING FIT WITH 4 DIM'
        results_stat = run_fit( Ndata, eff_2d_stat )
        results_syst = run_fit( Ndata, eff_2d_syst )

    if ndim == 3 :
        idxrf = 0
        idxfr = 1
        idxff = 2

    if ndim == 4 :
        idxrf = 1
        idxfr = 2
        idxff = 3

    print 'results_stat'
    print results_stat
    print 'results_syst'
    print results_syst

    #save_normalized_template_hists( gg_hist, results, templates, eff_2d, bins_lead_loose, bins_subl_loose, ndim, lead_ptrange=lead_ptrange, subl_ptrange=subl_ptrange, outputDir=outputDir )

    #get fitted predictions
    if ndim == 3 :
         p_RR_TT = ufloat(1.0, 0.0 )
         p_RR_TL = ufloat(0.0, 0.0 )
         p_RR_LT = ufloat(0.0, 0.0 )
         p_RR_LL = ufloat(0.0, 0.0 )
         p_RF_TT = results_stat.item(0)*eff_2d_stat['eff_RF_TT']
         p_RF_TL = results_stat.item(0)*eff_2d_stat['eff_RF_TL']
         p_RF_LT = results_stat.item(0)*eff_2d_stat['eff_RF_LT']
         p_RF_LL = results_stat.item(0)*eff_2d_stat['eff_RF_LL']
         p_FR_TT = results_stat.item(1)*eff_2d_stat['eff_FR_LT']
         p_FR_TL = results_stat.item(1)*eff_2d_stat['eff_FR_TL']
         p_FR_LT = results_stat.item(1)*eff_2d_stat['eff_FR_LT']
         p_FR_LL = results_stat.item(1)*eff_2d_stat['eff_FR_LL']
         p_FF_TT = results_stat.item(2)*eff_2d_stat['eff_FF_TT']
         p_FF_TL = results_stat.item(2)*eff_2d_stat['eff_FF_TL']
         p_FF_LT = results_stat.item(2)*eff_2d_stat['eff_FF_LT']
         p_FF_LL = results_stat.item(2)*eff_2d_stat['eff_FF_LL']
    if ndim == 4 : #everybody moves down 1 if 4 dim
         p_RR_TT = results_stat.item(0)*eff_2d_stat['eff_RR_TT']
         p_RR_TL = results_stat.item(0)*eff_2d_stat['eff_RR_TL']
         p_RR_LT = results_stat.item(0)*eff_2d_stat['eff_RR_LT']
         p_RR_LL = results_stat.item(0)*eff_2d_stat['eff_RR_LL']
         p_RF_TT = results_stat.item(1)*eff_2d_stat['eff_RF_TT']
         p_RF_TL = results_stat.item(1)*eff_2d_stat['eff_RF_TL']
         p_RF_LT = results_stat.item(1)*eff_2d_stat['eff_RF_LT']
         p_RF_LL = results_stat.item(1)*eff_2d_stat['eff_RF_LL']
         p_FR_TT = results_stat.item(2)*eff_2d_stat['eff_FR_LT']
         p_FR_TL = results_stat.item(2)*eff_2d_stat['eff_FR_TL']
         p_FR_LT = results_stat.item(2)*eff_2d_stat['eff_FR_LT']
         p_FR_LL = results_stat.item(2)*eff_2d_stat['eff_FR_LL']
         p_FF_TT = results_stat.item(3)*eff_2d_stat['eff_FF_TT']
         p_FF_TL = results_stat.item(3)*eff_2d_stat['eff_FF_TL']
         p_FF_LT = results_stat.item(3)*eff_2d_stat['eff_FF_LT']
         p_FF_LL = results_stat.item(3)*eff_2d_stat['eff_FF_LL']

    print 'Npred FF_LL'
    print p_FF_LL
    print 'Npred FF_LT'
    print p_FF_LT
    print 'Npred FF_TL'
    print p_FF_TL
    print 'Npred FF_TT'
    print p_FF_TT

    print 'Npred RF_LL'
    print p_RF_LL
    print 'Npred RF_LT'
    print p_RF_LT
    print 'Npred RF_TL'
    print p_RF_TL
    print 'Npred RF_TT'
    print p_RF_TT

    print 'Npred FR_LL'
    print p_FR_LL
    print 'Npred FR_LT'
    print p_FR_LT
    print 'Npred FR_TL'
    print p_FR_TL
    print 'Npred FR_TT'
    print p_FR_TT

    print 'Npred RR_LL'
    print p_RR_LL
    print 'Npred RR_LT'
    print p_RR_LT
    print 'Npred RR_TL'
    print p_RR_TL
    print 'Npred RR_TT'
    print p_RR_TT

    # make normalized template histograms
    # look at the leading photon distribution (X) while sublead is loose
    gg_hist_proj_lead_subl_tight = gg_hist.ProjectionX( 'gg_hist_proj_lead_subl_tight', bins_subl_tight[0], bins_subl_tight[1] )
    gg_hist_proj_subl_lead_tight = gg_hist.ProjectionY( 'gg_hist_proj_subl_lead_tight', bins_lead_tight[0], bins_lead_tight[1] )
    gg_hist_proj_lead_subl_loose = gg_hist.ProjectionX( 'gg_hist_proj_lead_subl_loose', bins_subl_loose[0], bins_subl_loose[1] )
    gg_hist_proj_subl_lead_loose = gg_hist.ProjectionY( 'gg_hist_proj_subl_lead_loose', bins_lead_loose[0], bins_lead_loose[1] )

    gg_hist_proj_lead = gg_hist.ProjectionX( 'gg_hist_proj_lead')
    gg_hist_proj_subl = gg_hist.ProjectionY( 'gg_hist_proj_subl')

    hist_temp_rr_subl_loose = templates['lead']['real']['Data'].Clone( 'hist_temp_rr_subl_loose' )
    hist_temp_rr_subl_tight = templates['lead']['real']['Data'].Clone( 'hist_temp_rr_subl_tight' )

    hist_temp_rf_subl_loose = templates['lead']['real']['Data'].Clone( 'hist_temp_rf_subl_loose' )
    hist_temp_rf_subl_tight = templates['lead']['real']['Data'].Clone( 'hist_temp_rf_subl_tight' )

    hist_temp_fr_subl_loose = templates['lead']['fake']['Data'].Clone( 'hist_temp_fr_subl_loose' )
    hist_temp_fr_subl_tight = templates['lead']['fake']['Data'].Clone( 'hist_temp_fr_subl_tight' )

    hist_temp_ff_subl_loose = templates['lead']['fake']['Data'].Clone( 'hist_temp_ff_subl_loose' )
    hist_temp_ff_subl_tight = templates['lead']['fake']['Data'].Clone( 'hist_temp_ff_subl_tight' )

    hist_temp_rr_lead_loose = templates['subl']['real']['Data'].Clone( 'hist_temp_rr_lead_loose' )
    hist_temp_rr_lead_tight = templates['subl']['real']['Data'].Clone( 'hist_temp_rr_lead_tight' )

    hist_temp_rf_lead_loose = templates['subl']['fake']['Data'].Clone( 'hist_temp_rf_lead_loose' )
    hist_temp_rf_lead_tight = templates['subl']['fake']['Data'].Clone( 'hist_temp_rf_lead_tight' )

    hist_temp_fr_lead_loose = templates['subl']['real']['Data'].Clone( 'hist_temp_fr_lead_loose' )
    hist_temp_fr_lead_tight = templates['subl']['real']['Data'].Clone( 'hist_temp_fr_lead_tight' )

    hist_temp_ff_lead_loose = templates['subl']['fake']['Data'].Clone( 'hist_temp_ff_lead_loose' )
    hist_temp_ff_lead_tight = templates['subl']['fake']['Data'].Clone( 'hist_temp_ff_lead_tight' )

    if templates['lead']['real']['Background'] is not None :
        hist_temp_rr_subl_loose.Add( templates['lead']['real']['Background'] )
        hist_temp_rr_subl_tight.Add( templates['lead']['real']['Background'] )
        hist_temp_rf_subl_loose.Add( templates['lead']['real']['Background'] )
        hist_temp_rf_subl_tight.Add( templates['lead']['real']['Background'] )
    if templates['lead']['fake']['Background'] is not None :
        hist_temp_fr_subl_loose.Add( templates['lead']['fake']['Background'] )
        hist_temp_fr_subl_tight.Add( templates['lead']['fake']['Background'] )
        hist_temp_ff_subl_loose.Add( templates['lead']['fake']['Background'] )
        hist_temp_ff_subl_tight.Add( templates['lead']['fake']['Background'] )
    if templates['subl']['real']['Background'] is not None :
        hist_temp_rr_lead_loose.Add( templates['subl']['real']['Background'] )
        hist_temp_rr_lead_tight.Add( templates['subl']['real']['Background'] )
        hist_temp_fr_lead_loose.Add( templates['subl']['real']['Background'] )
        hist_temp_fr_lead_tight.Add( templates['subl']['real']['Background'] )
    if templates['subl']['fake']['Background'] is not None :
        hist_temp_rf_lead_loose.Add( templates['subl']['fake']['Background'] )
        hist_temp_rf_lead_tight.Add( templates['subl']['fake']['Background'] )
        hist_temp_ff_lead_loose.Add( templates['subl']['fake']['Background'] )
        hist_temp_ff_lead_tight.Add( templates['subl']['fake']['Background'] )

    #normalize lead real template according to fit
    hist_temp_rr_subl_loose.Scale( (p_RR_TL+p_RR_LL).n /hist_temp_rr_subl_loose.Integral() )
    hist_temp_rr_subl_tight.Scale( (p_RR_TT+p_RR_LT).n /hist_temp_rr_subl_tight.Integral() )

    hist_temp_rf_subl_loose.Scale( (p_RF_TL+p_RF_LL).n /hist_temp_rf_subl_loose.Integral() )
    hist_temp_rf_subl_tight.Scale( (p_RF_TT+p_RF_LT).n /hist_temp_rf_subl_tight.Integral() )

    hist_temp_fr_subl_loose.Scale( (p_FR_TL+p_FR_LL).n /hist_temp_fr_subl_loose.Integral() )
    hist_temp_fr_subl_tight.Scale( (p_FR_TT+p_FR_LT).n /hist_temp_fr_subl_tight.Integral() )

    hist_temp_ff_subl_loose.Scale( (p_FF_TL+p_FF_LL).n /hist_temp_ff_subl_loose.Integral() )
    hist_temp_ff_subl_tight.Scale( (p_FF_TT+p_FF_LT).n /hist_temp_ff_subl_tight.Integral() )

    hist_temp_rr_lead_loose.Scale( (p_RR_LT+p_RR_LL).n /hist_temp_rr_lead_loose.Integral() )
    hist_temp_rr_lead_tight.Scale( (p_RR_TT+p_RR_TL).n /hist_temp_rr_lead_tight.Integral() )

    hist_temp_rf_lead_loose.Scale( (p_RF_LT+p_RF_LL).n /hist_temp_rf_lead_loose.Integral() )
    hist_temp_rf_lead_tight.Scale( (p_RF_TT+p_RF_TL).n /hist_temp_rf_lead_tight.Integral() )

    hist_temp_fr_lead_loose.Scale( (p_FR_LT+p_FR_LL).n /hist_temp_fr_lead_loose.Integral() )
    hist_temp_fr_lead_tight.Scale( (p_FR_TT+p_FR_TL).n /hist_temp_fr_lead_tight.Integral() )

    hist_temp_ff_lead_loose.Scale( (p_FF_LT+p_FF_LL).n /hist_temp_ff_lead_loose.Integral() )
    hist_temp_ff_lead_tight.Scale( (p_FF_TT+p_FF_TL).n /hist_temp_ff_lead_tight.Integral() )

    hist_temp_rr_proj_lead = hist_temp_rr_subl_loose.Clone( 'hist_temp_rr_proj_lead' )
    hist_temp_rr_proj_lead.Add(hist_temp_rr_subl_tight )
    hist_temp_rr_proj_subl = hist_temp_rr_lead_loose.Clone( 'hist_temp_rr_proj_subl' )
    hist_temp_rr_proj_subl.Add(hist_temp_rr_lead_tight )

    hist_temp_rf_proj_lead = hist_temp_rf_subl_loose.Clone( 'hist_temp_rf_proj_lead' )
    hist_temp_rf_proj_lead.Add(hist_temp_rf_subl_tight )
    hist_temp_rf_proj_subl = hist_temp_rf_lead_loose.Clone( 'hist_temp_rf_proj_subl' )
    hist_temp_rf_proj_subl.Add(hist_temp_rf_lead_tight )

    hist_temp_fr_proj_lead = hist_temp_fr_subl_loose.Clone( 'hist_temp_fr_proj_lead' )
    hist_temp_fr_proj_lead.Add(hist_temp_fr_subl_tight )
    hist_temp_fr_proj_subl = hist_temp_fr_lead_loose.Clone( 'hist_temp_fr_proj_subl' )
    hist_temp_fr_proj_subl.Add(hist_temp_fr_lead_tight )

    hist_temp_ff_proj_lead = hist_temp_ff_subl_loose.Clone( 'hist_temp_ff_proj_lead' )
    hist_temp_ff_proj_lead.Add(hist_temp_ff_subl_tight )
    hist_temp_ff_proj_subl = hist_temp_ff_lead_loose.Clone( 'hist_temp_ff_proj_subl' )
    hist_temp_ff_proj_subl.Add(hist_temp_ff_lead_tight )

    if fitvar == 'chIsoCorr' :

        binwidth_eb = (plotbinning['EB'][2]-plotbinning['EB'][1])/float(plotbinning['EB'][0])
        binwidth_ee = (plotbinning['EE'][2]-plotbinning['EE'][1])/float(plotbinning['EE'][0])

        varbin = {} 
        varbin['EB'] = [plotbinning['EB'][1], plotbinning['EB'][1]+binwidth_eb, plotbinning['EB'][2] ]
        varbin['EE'] = [plotbinning['EE'][1], plotbinning['EE'][1]+binwidth_ee, plotbinning['EE'][2] ]

        print varbin

        gg_hist_proj_lead_subl_tight = sampManData.do_variable_rebinning( gg_hist_proj_lead_subl_tight, varbin[lead_reg] )
        gg_hist_proj_lead_subl_loose = sampManData.do_variable_rebinning( gg_hist_proj_lead_subl_loose, varbin[lead_reg] )
        hist_temp_ff_subl_loose = sampManData.do_variable_rebinning( hist_temp_ff_subl_loose, varbin[lead_reg] )
        hist_temp_ff_subl_tight = sampManData.do_variable_rebinning( hist_temp_ff_subl_tight, varbin[lead_reg] )
        hist_temp_fr_subl_loose = sampManData.do_variable_rebinning( hist_temp_fr_subl_loose, varbin[lead_reg] )
        hist_temp_fr_subl_tight = sampManData.do_variable_rebinning( hist_temp_fr_subl_tight, varbin[lead_reg] )
        hist_temp_rf_subl_loose = sampManData.do_variable_rebinning( hist_temp_rf_subl_loose, varbin[lead_reg] )
        hist_temp_rf_subl_tight = sampManData.do_variable_rebinning( hist_temp_rf_subl_tight, varbin[lead_reg] )
        hist_temp_rr_subl_loose = sampManData.do_variable_rebinning( hist_temp_rr_subl_loose, varbin[lead_reg] )
        hist_temp_rr_subl_tight = sampManData.do_variable_rebinning( hist_temp_rr_subl_tight, varbin[lead_reg] )
        hist_temp_ff_proj_lead  = sampManData.do_variable_rebinning( hist_temp_ff_proj_lead , varbin[lead_reg] )
        hist_temp_fr_proj_lead  = sampManData.do_variable_rebinning( hist_temp_fr_proj_lead , varbin[lead_reg] )
        hist_temp_rf_proj_lead  = sampManData.do_variable_rebinning( hist_temp_rf_proj_lead , varbin[lead_reg] )
        hist_temp_rr_proj_lead  = sampManData.do_variable_rebinning( hist_temp_rr_proj_lead , varbin[lead_reg] )

        gg_hist_proj_subl_lead_tight = sampManData.do_variable_rebinning( gg_hist_proj_subl_lead_tight, varbin[subl_reg] )
        gg_hist_proj_subl_lead_loose = sampManData.do_variable_rebinning( gg_hist_proj_subl_lead_loose, varbin[subl_reg] )
        hist_temp_ff_lead_loose = sampManData.do_variable_rebinning( hist_temp_ff_lead_loose, varbin[subl_reg] )
        hist_temp_ff_lead_tight = sampManData.do_variable_rebinning( hist_temp_ff_lead_tight, varbin[subl_reg] )
        hist_temp_rf_lead_loose = sampManData.do_variable_rebinning( hist_temp_rf_lead_loose, varbin[subl_reg] )
        hist_temp_rf_lead_tight = sampManData.do_variable_rebinning( hist_temp_rf_lead_tight, varbin[subl_reg] )
        hist_temp_fr_lead_loose = sampManData.do_variable_rebinning( hist_temp_fr_lead_loose, varbin[subl_reg] )
        hist_temp_fr_lead_tight = sampManData.do_variable_rebinning( hist_temp_fr_lead_tight, varbin[subl_reg] )
        hist_temp_rr_lead_loose = sampManData.do_variable_rebinning( hist_temp_rr_lead_loose, varbin[subl_reg] )
        hist_temp_rr_lead_tight = sampManData.do_variable_rebinning( hist_temp_rr_lead_tight, varbin[subl_reg] )
        hist_temp_ff_proj_subl  = sampManData.do_variable_rebinning( hist_temp_ff_proj_subl , varbin[subl_reg] )
        hist_temp_fr_proj_subl  = sampManData.do_variable_rebinning( hist_temp_fr_proj_subl , varbin[subl_reg] )
        hist_temp_rf_proj_subl  = sampManData.do_variable_rebinning( hist_temp_rf_proj_subl , varbin[subl_reg] )
        hist_temp_rr_proj_subl  = sampManData.do_variable_rebinning( hist_temp_rr_proj_subl , varbin[subl_reg] )

    gg_hist_proj_subl_lead_tight.SetMarkerSize(1.1)
    gg_hist_proj_subl_lead_tight.SetMarkerStyle(21)
    gg_hist_proj_subl_lead_tight.SetMarkerColor(ROOT.kBlack)
    gg_hist_proj_subl_lead_loose.SetMarkerSize(1.1)
    gg_hist_proj_subl_lead_loose.SetMarkerStyle(21)
    gg_hist_proj_subl_lead_loose.SetMarkerColor(ROOT.kBlack)

    gg_hist_proj_lead_subl_tight.SetMarkerSize(1.1)
    gg_hist_proj_lead_subl_tight.SetMarkerStyle(21)
    gg_hist_proj_lead_subl_tight.SetMarkerColor(ROOT.kBlack)
    gg_hist_proj_lead_subl_loose.SetMarkerSize(1.1)
    gg_hist_proj_lead_subl_loose.SetMarkerStyle(21)
    gg_hist_proj_lead_subl_loose.SetMarkerColor(ROOT.kBlack)

    format_hist( hist_temp_rr_subl_loose, ROOT.kGreen )
    format_hist( hist_temp_rr_subl_tight, ROOT.kGreen )
    format_hist( hist_temp_rr_lead_loose, ROOT.kGreen )
    format_hist( hist_temp_rr_lead_tight, ROOT.kGreen )
    format_hist( hist_temp_rr_proj_subl , ROOT.kGreen )
    format_hist( hist_temp_rr_proj_lead , ROOT.kGreen )

    format_hist( hist_temp_rf_subl_loose, ROOT.kMagenta )
    format_hist( hist_temp_rf_subl_tight, ROOT.kMagenta )
    format_hist( hist_temp_rf_lead_loose, ROOT.kMagenta )
    format_hist( hist_temp_rf_lead_tight, ROOT.kMagenta )
    format_hist( hist_temp_rf_proj_subl , ROOT.kMagenta )
    format_hist( hist_temp_rf_proj_lead , ROOT.kMagenta )

    format_hist( hist_temp_fr_subl_loose, ROOT.kCyan )
    format_hist( hist_temp_fr_subl_tight, ROOT.kCyan )
    format_hist( hist_temp_fr_lead_loose, ROOT.kCyan )
    format_hist( hist_temp_fr_lead_tight, ROOT.kCyan )
    format_hist( hist_temp_fr_proj_subl , ROOT.kCyan )
    format_hist( hist_temp_fr_proj_lead , ROOT.kCyan )

    format_hist( hist_temp_ff_subl_loose, ROOT.kRed )
    format_hist( hist_temp_ff_subl_tight, ROOT.kRed )
    format_hist( hist_temp_ff_lead_loose, ROOT.kRed )
    format_hist( hist_temp_ff_lead_tight, ROOT.kRed )
    format_hist( hist_temp_ff_proj_subl , ROOT.kRed )
    format_hist( hist_temp_ff_proj_lead , ROOT.kRed )

    

    if lead_reg == 'EE' and gg_hist_proj_lead_subl_tight.GetNbinsX() > 100  :
        gg_hist_proj_lead_subl_tight.Rebin(10)
        gg_hist_proj_lead_subl_loose.Rebin(10)
        hist_temp_ff_subl_loose.Rebin(10)
        hist_temp_ff_subl_tight.Rebin(10)
        hist_temp_fr_subl_loose.Rebin(10)
        hist_temp_fr_subl_tight.Rebin(10)
        hist_temp_rf_subl_loose.Rebin(10)
        hist_temp_rf_subl_tight.Rebin(10)
        hist_temp_rr_subl_loose.Rebin(10)
        hist_temp_rr_subl_tight.Rebin(10)

        hist_temp_ff_proj_lead .Rebin(10)
        hist_temp_fr_proj_lead .Rebin(10)
        hist_temp_rf_proj_lead .Rebin(10)
        hist_temp_rr_proj_lead .Rebin(10)

    if subl_reg == 'EE' and gg_hist_proj_subl_lead_tight.GetNbinsX() > 100 :
        gg_hist_proj_subl_lead_tight.Rebin(10)
        gg_hist_proj_subl_lead_loose.Rebin(10)
        hist_temp_ff_lead_loose.Rebin(10)
        hist_temp_ff_lead_tight.Rebin(10)
        hist_temp_rf_lead_loose.Rebin(10)
        hist_temp_rf_lead_tight.Rebin(10)
        hist_temp_fr_lead_loose.Rebin(10)
        hist_temp_fr_lead_tight.Rebin(10)
        hist_temp_rr_lead_loose.Rebin(10)
        hist_temp_rr_lead_tight.Rebin(10)

        hist_temp_ff_proj_subl .Rebin(10)
        hist_temp_fr_proj_subl .Rebin(10)
        hist_temp_rf_proj_subl .Rebin(10)
        hist_temp_rr_proj_subl .Rebin(10)

    #can_proj_lead_subl_loose = ROOT.TCanvas('proj_lead_subl_loose', '')
    #can_proj_lead_subl_tight = ROOT.TCanvas('proj_lead_subl_tight', '')
    #can_proj_subl_lead_loose = ROOT.TCanvas('proj_subl_lead_loose', '')
    #can_proj_subl_lead_tight = ROOT.TCanvas('proj_subl_lead_tight', '')
    #can_proj_lead = ROOT.TCanvas('proj_lead', '')
    #can_proj_subl = ROOT.TCanvas('proj_subl', '')

    can_proj_lead_subl_loose = ROOT.TCanvas(str(uuid.uuid4()), '')
    can_proj_lead_subl_tight = ROOT.TCanvas(str(uuid.uuid4()), '')
    can_proj_subl_lead_loose = ROOT.TCanvas(str(uuid.uuid4()), '')
    can_proj_subl_lead_tight = ROOT.TCanvas(str(uuid.uuid4()), '')

    can_proj_lead = ROOT.TCanvas(str(uuid.uuid4()), '')
    can_proj_subl = ROOT.TCanvas(str(uuid.uuid4()), '')

    namePostfix = '__%s-%s' %( lead_reg, subl_reg )
    if lead_ptrange[0] is not None :
        if lead_ptrange[1] is None :
            namePostfix += '__pt_%d-max' %( lead_ptrange[0])
        else :
            namePostfix += '__pt_%d-%d' %( lead_ptrange[0], lead_ptrange[1])

    if subl_ptrange[0] is not None :
        if subl_ptrange[1] is None :
            namePostfix += '__sublpt_%d-max' %( subl_ptrange[0])
        else :
            namePostfix += '__sublpt_%d-%d' %( subl_ptrange[0], subl_ptrange[1])

    outputNamePLST = None
    outputNamePLSL = None
    outputNamePSLT = None
    outputNamePSLL = None
    outputNamePL = None
    outputNamePS = None
    if outputDir is not None :
        outputNamePLST = outputDir + '/fit_with_data_proj_lead_subl_tight%s%s.pdf' %(outputPrefix, namePostfix)
        outputNamePLSL = outputDir + '/fit_with_data_proj_lead_subl_loose%s%s.pdf' %(outputPrefix, namePostfix)
        outputNamePSLT = outputDir + '/fit_with_data_proj_subl_lead_tight%s%s.pdf' %(outputPrefix, namePostfix)
        outputNamePSLL = outputDir + '/fit_with_data_proj_subl_lead_loose%s%s.pdf' %(outputPrefix, namePostfix)
        outputNamePL = outputDir + '/fit_with_data_proj_lead_%s%s.pdf' %(outputPrefix, namePostfix)
        outputNamePS = outputDir + '/fit_with_data_proj_subl_%s%s.pdf' %(outputPrefix, namePostfix)

    if fitvar == 'sigmaIEIE' :
        labvar = '#sigma i#eta i#eta'
    if fitvar == 'chIsoCorr' :
        labvar = 'chHadIso'
    if fitvar == 'neuIsoCorr' :
        labvar = 'neuHadIso'

    draw_template(can_proj_lead_subl_loose, [gg_hist_proj_lead_subl_loose, hist_temp_rr_subl_loose, hist_temp_rf_subl_loose, hist_temp_fr_subl_loose, hist_temp_ff_subl_loose], sampManData, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+real prediction', 'real+fake prediction', 'fake+real prediction', 'fake+fake prediction' ], outputName=outputNamePLSL, label='#splitline{Lead %s}{sublead loose}' %labvar, axis_label=labvar )
    draw_template(can_proj_lead_subl_tight, [gg_hist_proj_lead_subl_tight, hist_temp_rr_subl_tight, hist_temp_rf_subl_tight, hist_temp_fr_subl_tight, hist_temp_ff_subl_tight], sampManData, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+real prediction', 'real+fake prediction', 'fake+real prediction', 'fake+fake prediction' ], outputName=outputNamePLST, label='#splitline{Lead %s}{sublead tight}' %labvar, axis_label=labvar )

    draw_template(can_proj_subl_lead_loose, [gg_hist_proj_subl_lead_loose, hist_temp_rr_lead_loose, hist_temp_rf_lead_loose, hist_temp_fr_lead_loose, hist_temp_ff_lead_loose], sampManData, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+real prediction', 'real+fake prediction', 'fake+real prediction', 'fake+fake prediction' ], outputName=outputNamePSLL, label='#splitline{Sublead %s}{lead loose}' %labvar, axis_label=labvar )
    draw_template(can_proj_subl_lead_tight, [gg_hist_proj_subl_lead_tight, hist_temp_rr_lead_tight, hist_temp_rf_lead_tight, hist_temp_fr_lead_tight, hist_temp_ff_lead_tight], sampManData, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+real prediction', 'real+fake prediction', 'fake+real prediction', 'fake+fake prediction' ], outputName=outputNamePSLT, label='#splitline{Sublead %s}{lead tight}'  %labvar, axis_label=labvar)

    draw_template(can_proj_lead, [gg_hist_proj_lead, hist_temp_rr_proj_lead, hist_temp_rf_proj_lead, hist_temp_fr_proj_lead, hist_temp_ff_proj_lead], sampManData, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+real prediction', 'real+fake prediction', 'fake+real prediction', 'fake+fake prediction' ], outputName=outputNamePL, label='Lead %s' %labvar, axis_label=labvar )
    draw_template(can_proj_subl, [gg_hist_proj_subl, hist_temp_rr_proj_subl, hist_temp_rf_proj_subl, hist_temp_fr_proj_subl, hist_temp_ff_proj_subl], sampManData, normalize=False, first_hist_is_data=True, legend_entries=['Data', 'real+real prediction', 'real+fake prediction', 'fake+real prediction', 'fake+fake prediction' ], outputName=outputNamePL, label='Sublead %s' %labvar, axis_label=labvar )

    text_results_stat = collect_results( results_stat,Ndata, eff_2d_stat, templates, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim)
    text_results_syst = collect_results( results_syst,Ndata, eff_2d_stat, templates, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim)

    return text_results_stat, text_results_syst
    
def format_hist( hist, color ) :

    hist.SetLineColor( color )
    hist.SetMarkerColor( color )

    hist.SetLineWidth(2)
    hist.SetMarkerSize(0)
    hist.SetStats(0)



def run_fit( data, efficiencies ) :

    # make the matrix
    matrix = generate_eff_matrix( efficiencies, ndim=len(data) )
    print matrix

    #do the fit!  Invert the matrix and multiply the by counts vectors
    if len( data ) == 3 :
        results = solve_matrix_eq( matrix, [data['TL'], data['LT'], data['LL']] )
    elif len(data) == 4 :
        results = solve_matrix_eq( matrix, [data['TT'],data['TL'], data['LT'], data['LL']] )


    return results 

def run_fit_manual( data, eff ) :

    # matrix is 
    # ----------------------
    # RF_TL FR_TL FF_TL
    # RF_LT FR_LT FF_LT
    # RF_LL FR_LL FF_LL
    
    # RF_TL = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']
    # FR_TL = (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']
    # FF_TL = (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']
    # RF_LT = eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
    # FR_LT = eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
    # FF_LT = eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
    # RF_LL = eff['eff_R_L_lead']*eff['eff_F_L_subl']
    # FR_LL = eff['eff_F_L_lead']*eff['eff_R_L_subl']
    # FF_LL = eff['eff_F_L_lead']*eff['eff_F_L_subl']
    # RF_TT = (1-eff['eff_R_L_lead'])*(1-eff['eff_F_L_subl'])
    # FR_TT = (1-eff['eff_F_L_lead'])*(1-eff['eff_R_L_subl'])
    # FF_TT = (1-eff['eff_F_L_lead'])*(1-eff['eff_F_L_subl'])

    # determinant = RF_TL*FR_LT*FF_LL + FR_TL*FF_LT*RF_LL + FF_TL*RF_LT*FR_LL - FF_TL*FR_LT*RF_LL - FR_TL*RF_LT*FF_LL - RF_TL*FF_LT*FR_LL
    # determinant = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] 
    #             + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #             + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    #             - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #             - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    #             - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    
    # Inverted matrix
    # Inv_11 = FR_LT*FF_LL-FF_LT*FR_LL
    # Inv_12 = FF_TL*FR_LL-FR_TL*FF_LL
    # Inv_13 = FR_TL*FF_LT-FF_TL*FR_LT
    # Inv_21 = FF_LT*RF_LL-RF_LT*FF_LL
    # Inv_22 = RF_TL*FF_LL-FF_TL*RF_LL
    # Inv_23 = FF_TL*RF_LT-RF_TL*FF_LT
    # Inv_31 = RF_LT*FR_LL-FR_LT*RF_LL
    # Inv_32 = FR_TL*RF_LL-RF_TL*FR_LL
    # Inv_33 = RF_TL*FR_LT-FR_TL*RF_LT

    # Inv_11 = eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    #        - eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    # Inv_12 = (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    #        - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    # Inv_13 = (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
    #        - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
    # Inv_21 = eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #        - eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    # Inv_22 = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
    #        - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    # Inv_23 = (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
    #        - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
    # Inv_31 = eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    #        - eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    # Inv_32 = (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
    #        - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
    # Inv_33 = (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
    #        - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])

    # alpha_rf = (1/determinant) * ( Inv_11 * Data['TL'] + Inv_12*Data['LT'] + Inv_13 * Data['LL'])
    # alpha_fr = (1/determinant) * ( Inv_21 * Data['TL'] + Inv_22*Data['LT'] + Inv_23 * Data['LL'])
    # alpha_ff = (1/determinant) * ( Inv_31 * Data['TL'] + Inv_32*Data['LT'] + Inv_33 * Data['LL'])
    alpha_rf = ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] 
                      + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
              * ( (  eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                   - eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] )*data['TL']
                + (  (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                   - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['LT']
                + (   (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl']) )*data['LL']
              ) )

    alpha_fr = ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']     
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                  - eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['TL'] 
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                  - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['LT']
              + (   (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
                  - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl']) ) *data['LL']
              ) )
                
    alpha_ff = ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']    
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                  - eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['TL']
              + (  (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                 - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) * data['LT']
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
                  - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl']) )*data['LL']
              ) )


    nPred_RF_TT = ( (1-eff['eff_R_L_lead'])*(1-eff['eff_F_L_subl'])* 
                      ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] 
                      + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                      - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
              * ( (  eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                   - eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] )*data['TL']
                + (  (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                   - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['LT']
                + (   (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl']) )*data['LL']
              ) ) )

    nPred_FR_TT = ( (1-eff['eff_F_L_lead'])*(1-eff['eff_R_L_subl'])* 
                   ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']     
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                  - eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl'] )*data['TL'] 
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                  - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['LT']
              + (   (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])
                  - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl']) ) *data['LL']
              ) ) )

    nPred_FF_TT = ( (1-eff['eff_F_L_lead'])*(1-eff['eff_F_L_subl'])* 
                  ( (1.0/( (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']    
                    + (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    + (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_F_L_subl']
                    - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) )
            * ( (   eff['eff_R_L_lead']*(1-eff['eff_F_L_subl'])*eff['eff_F_L_lead']*eff['eff_R_L_subl']
                  - eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])*eff['eff_R_L_lead']*eff['eff_F_L_subl'] )*data['TL']
              + (  (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*eff['eff_F_L_subl']
                 - (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*eff['eff_R_L_subl'] ) * data['LT']
              + (   (1-eff['eff_R_L_lead'])*eff['eff_F_L_subl']*eff['eff_F_L_lead']*(1-eff['eff_R_L_subl'])
                  - (1-eff['eff_F_L_lead'])*eff['eff_R_L_subl']*eff['eff_R_L_lead']*(1-eff['eff_F_L_subl']) )*data['LL']
              ) ) )
       
    return {'alpha_RF' : alpha_rf, 'alpha_FR' : alpha_fr, 'alpha_FF' : alpha_ff, 'pred_RF_TT' : nPred_RF_TT, 'pred_FR_TT' : nPred_FR_TT, 'pred_FF_TT' : nPred_FF_TT }
       
       
#def save_normalized_template_hists( data_hist, results, templates, efficiencies, bins_lead_loose, bins_subl_loose, ndim, lead_ptrange=None, subl_ptrange=None, outputDir=None ) :
#    
#    if outputDir is None :
#        return


def collect_results( results, data, efficiencies, templates, bins_lead_loose, bins_lead_tight, bins_subl_loose, bins_subl_tight, ndim  ) :

    text_results = collections.OrderedDict()

    for key, val in efficiencies.iteritems() :
        text_results[key] = val

    if ndim == 4 :

        text_results['Ndata_TT'] = data['TT']
        text_results['Ndata_TL'] = data['TL']
        text_results['Ndata_LT'] = data['LT']
        text_results['Ndata_LL'] = data['LL']

        text_results['alpha_RR'] = results.item(0)
        text_results['alpha_RF'] = results.item(1)
        text_results['alpha_FR'] = results.item(2)
        text_results['alpha_FF'] = results.item(3)

        text_results['Npred_RR_TT'] = text_results['alpha_RR']*text_results['eff_RR_TT']
        text_results['Npred_RR_TL'] = text_results['alpha_RR']*text_results['eff_RR_TL']
        text_results['Npred_RR_LT'] = text_results['alpha_RR']*text_results['eff_RR_LT']
        text_results['Npred_RR_LL'] = text_results['alpha_RR']*text_results['eff_RR_LL']

    else :
        text_results['Ndata_TT'] = ufloat(0, 0)
        text_results['Ndata_TL'] = data['TL']
        text_results['Ndata_LT'] = data['LT']
        text_results['Ndata_LL'] = data['LL']

        text_results['alpha_RF'] = results.item(0)
        text_results['alpha_FR'] = results.item(1)
        text_results['alpha_FF'] = results.item(2)


    text_results['Npred_RF_TT'] = text_results['alpha_RF']*text_results['eff_RF_TT']
    text_results['Npred_RF_TL'] = text_results['alpha_RF']*text_results['eff_RF_TL']
    text_results['Npred_RF_LT'] = text_results['alpha_RF']*text_results['eff_RF_LT']
    text_results['Npred_RF_LL'] = text_results['alpha_RF']*text_results['eff_RF_LL']

    text_results['Npred_FR_TT'] = text_results['alpha_FR']*text_results['eff_FR_TT']
    text_results['Npred_FR_TL'] = text_results['alpha_FR']*text_results['eff_FR_TL']
    text_results['Npred_FR_LT'] = text_results['alpha_FR']*text_results['eff_FR_LT']
    text_results['Npred_FR_LL'] = text_results['alpha_FR']*text_results['eff_FR_LL']

    text_results['Npred_FF_TT'] = text_results['alpha_FF']*text_results['eff_FF_TT']
    text_results['Npred_FF_TL'] = text_results['alpha_FF']*text_results['eff_FF_TL']
    text_results['Npred_FF_LT'] = text_results['alpha_FF']*text_results['eff_FF_LT']
    text_results['Npred_FF_LL'] = text_results['alpha_FF']*text_results['eff_FF_LL']

    # add the template integrals to results

    int_lead_real_loose = get_integral_and_error(templates['lead']['real']['Data'], bins_lead_loose )
    int_lead_real_tight = get_integral_and_error(templates['lead']['real']['Data'], bins_lead_tight )
    int_lead_fake_loose = get_integral_and_error(templates['lead']['fake']['Data'], bins_lead_loose )
    int_lead_fake_tight = get_integral_and_error(templates['lead']['fake']['Data'], bins_lead_tight )

    int_subl_real_loose = get_integral_and_error(templates['subl']['real']['Data'], bins_subl_loose )
    int_subl_real_tight = get_integral_and_error(templates['subl']['real']['Data'], bins_subl_tight )
    int_subl_fake_loose = get_integral_and_error(templates['subl']['fake']['Data'], bins_subl_loose )
    int_subl_fake_tight = get_integral_and_error(templates['subl']['fake']['Data'], bins_subl_tight )


    if templates['lead']['real']['Background'] is not None :
        int_lead_real_loose = int_lead_real_loose +  get_integral_and_error(templates['lead']['real']['Background'], bins_lead_loose )
    if templates['lead']['real']['Background'] is not None :
        int_lead_real_tight = int_lead_real_tight +  get_integral_and_error(templates['lead']['real']['Background'], bins_lead_tight )
    if templates['lead']['fake']['Background'] is not None :
        int_lead_fake_loose = int_lead_fake_loose +  get_integral_and_error(templates['lead']['fake']['Background'], bins_lead_loose )
    if templates['lead']['fake']['Background'] is not None :
        int_lead_fake_tight = int_lead_fake_tight +  get_integral_and_error(templates['lead']['fake']['Background'], bins_lead_tight )

    if templates['subl']['real']['Background'] is not None :
        int_subl_real_loose = int_subl_real_loose +  get_integral_and_error(templates['subl']['real']['Background'], bins_subl_loose )
    if templates['subl']['real']['Background'] is not None :
        int_subl_real_tight = int_subl_real_tight +  get_integral_and_error(templates['subl']['real']['Background'], bins_subl_tight )
    if templates['subl']['fake']['Background'] is not None :
        int_subl_fake_loose = int_subl_fake_loose +  get_integral_and_error(templates['subl']['fake']['Background'], bins_subl_loose )
    if templates['subl']['fake']['Background'] is not None :
        int_subl_fake_tight = int_subl_fake_tight +  get_integral_and_error(templates['subl']['fake']['Background'], bins_subl_tight )

    text_results['template_int_lead_real_loose'] = int_lead_real_loose
    text_results['template_int_lead_real_tight'] = int_lead_real_tight
    text_results['template_int_lead_fake_loose'] = int_lead_fake_loose
    text_results['template_int_lead_fake_tight'] = int_lead_fake_tight
    text_results['template_int_subl_real_loose'] = int_subl_real_loose
    text_results['template_int_subl_real_tight'] = int_subl_real_tight
    text_results['template_int_subl_fake_loose'] = int_subl_fake_loose
    text_results['template_int_subl_fake_tight'] = int_subl_fake_tight

    return text_results


def generate_1d_efficiencies( templates, cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=None ) :

    (int_stat, int_syst) = get_template_integrals( templates, cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    (eff_1d_stat, eff_1d_syst) = get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    return eff_1d_stat, eff_1d_syst

def generate_2d_efficiencies( templates, cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=None ) :

    (int_stat, int_syst) = get_template_integrals( templates, cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    (eff_1d_stat, eff_1d_syst) = get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=systematics )

    eff_stat = collections.OrderedDict()
    eff_syst = collections.OrderedDict()

    stat_eff_R_L_lead = eff_1d_stat['eff_R_L_lead']
    stat_eff_F_L_lead = eff_1d_stat['eff_F_L_lead']
    stat_eff_R_L_subl = eff_1d_stat['eff_R_L_subl']
    stat_eff_F_L_subl = eff_1d_stat['eff_F_L_subl']

    syst_eff_R_L_lead = eff_1d_syst['eff_R_L_lead']
    syst_eff_F_L_lead = eff_1d_syst['eff_F_L_lead']
    syst_eff_R_L_subl = eff_1d_syst['eff_R_L_subl']
    syst_eff_F_L_subl = eff_1d_syst['eff_F_L_subl']

    # tight efficiencies are just 1-loose efficiencies
    stat_eff_R_T_lead = 1 - stat_eff_R_L_lead
    stat_eff_F_T_lead = 1 - stat_eff_F_L_lead
    stat_eff_R_T_subl = 1 - stat_eff_R_L_subl
    stat_eff_F_T_subl = 1 - stat_eff_F_L_subl

    syst_eff_R_T_lead = 1 - syst_eff_R_L_lead
    syst_eff_F_T_lead = 1 - syst_eff_F_L_lead
    syst_eff_R_T_subl = 1 - syst_eff_R_L_subl
    syst_eff_F_T_subl = 1 - syst_eff_F_L_subl

    eff_stat['eff_RR_TT'] = stat_eff_R_T_lead*stat_eff_R_T_subl 
    eff_stat['eff_RR_TL'] = stat_eff_R_T_lead*stat_eff_R_L_subl 
    eff_stat['eff_RR_LT'] = stat_eff_R_L_lead*stat_eff_R_T_subl 
    eff_stat['eff_RR_LL'] = stat_eff_R_L_lead*stat_eff_R_L_subl 

    eff_stat['eff_RF_TT'] = stat_eff_R_T_lead*stat_eff_F_T_subl 
    eff_stat['eff_RF_TL'] = stat_eff_R_T_lead*stat_eff_F_L_subl 
    eff_stat['eff_RF_LT'] = stat_eff_R_L_lead*stat_eff_F_T_subl 
    eff_stat['eff_RF_LL'] = stat_eff_R_L_lead*stat_eff_F_L_subl 

    eff_stat['eff_FR_TT'] = stat_eff_F_T_lead*stat_eff_R_T_subl 
    eff_stat['eff_FR_TL'] = stat_eff_F_T_lead*stat_eff_R_L_subl 
    eff_stat['eff_FR_LT'] = stat_eff_F_L_lead*stat_eff_R_T_subl 
    eff_stat['eff_FR_LL'] = stat_eff_F_L_lead*stat_eff_R_L_subl 

    eff_stat['eff_FF_TT'] = stat_eff_F_T_lead*stat_eff_F_T_subl 
    eff_stat['eff_FF_TL'] = stat_eff_F_T_lead*stat_eff_F_L_subl 
    eff_stat['eff_FF_LT'] = stat_eff_F_L_lead*stat_eff_F_T_subl 
    eff_stat['eff_FF_LL'] = stat_eff_F_L_lead*stat_eff_F_L_subl 

    eff_syst['eff_RR_TT'] = syst_eff_R_T_lead*syst_eff_R_T_subl 
    eff_syst['eff_RR_TL'] = syst_eff_R_T_lead*syst_eff_R_L_subl 
    eff_syst['eff_RR_LT'] = syst_eff_R_L_lead*syst_eff_R_T_subl 
    eff_syst['eff_RR_LL'] = syst_eff_R_L_lead*syst_eff_R_L_subl 

    eff_syst['eff_RF_TT'] = syst_eff_R_T_lead*syst_eff_F_T_subl 
    eff_syst['eff_RF_TL'] = syst_eff_R_T_lead*syst_eff_F_L_subl 
    eff_syst['eff_RF_LT'] = syst_eff_R_L_lead*syst_eff_F_T_subl 
    eff_syst['eff_RF_LL'] = syst_eff_R_L_lead*syst_eff_F_L_subl 

    eff_syst['eff_FR_TT'] = syst_eff_F_T_lead*syst_eff_R_T_subl 
    eff_syst['eff_FR_TL'] = syst_eff_F_T_lead*syst_eff_R_L_subl 
    eff_syst['eff_FR_LT'] = syst_eff_F_L_lead*syst_eff_R_T_subl 
    eff_syst['eff_FR_LL'] = syst_eff_F_L_lead*syst_eff_R_L_subl 

    eff_syst['eff_FF_TT'] = syst_eff_F_T_lead*syst_eff_F_T_subl 
    eff_syst['eff_FF_TL'] = syst_eff_F_T_lead*syst_eff_F_L_subl 
    eff_syst['eff_FF_LT'] = syst_eff_F_L_lead*syst_eff_F_T_subl 
    eff_syst['eff_FF_LL'] = syst_eff_F_L_lead*syst_eff_F_L_subl 


    return eff_stat, eff_syst 

def get_1d_loose_efficiencies( int_stat, int_syst, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=None) :

    eff_stat = {}
    eff_syst = {}

    eff_stat['eff_R_L_lead'] = int_stat['lead']['real']['loose'] / (int_stat['lead']['real']['tight']+int_stat['lead']['real']['loose'])
    eff_stat['eff_F_L_lead'] = int_stat['lead']['fake']['loose'] / (int_stat['lead']['fake']['tight']+int_stat['lead']['fake']['loose'])
    eff_stat['eff_R_L_subl'] = int_stat['subl']['real']['loose'] / (int_stat['subl']['real']['tight']+int_stat['subl']['real']['loose'])
    eff_stat['eff_F_L_subl'] = int_stat['subl']['fake']['loose'] / (int_stat['subl']['fake']['tight']+int_stat['subl']['fake']['loose'])

    eff_syst['eff_R_L_lead'] = int_syst['lead']['real']['loose'] / (int_syst['lead']['real']['tight']+int_syst['lead']['real']['loose'])
    eff_syst['eff_F_L_lead'] = int_syst['lead']['fake']['loose'] / (int_syst['lead']['fake']['tight']+int_syst['lead']['fake']['loose'])
    eff_syst['eff_R_L_subl'] = int_syst['subl']['real']['loose'] / (int_syst['subl']['real']['tight']+int_syst['subl']['real']['loose'])
    eff_syst['eff_F_L_subl'] = int_syst['subl']['fake']['loose'] / (int_syst['subl']['fake']['tight']+int_syst['subl']['fake']['loose'])


    # Do systematics
    # the integrals may already have some systematics
    # that are propagated to the eff_*
    # therefore, don't overwrite the existing 
    # systematics, but make a ufloat with a
    # zero value, and non-zero syst
    eff_syst['eff_R_L_lead'] = eff_syst['eff_R_L_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_R_L_lead'].n)*get_syst_uncertainty( 'RealTemplateNom', lead_reg, lead_ptrange, 'real', 'loose' ), 'Template_lead_real_loose')
    eff_syst['eff_F_L_lead'] = eff_syst['eff_F_L_lead'] + ufloat( 0.0, math.fabs(eff_syst['eff_F_L_lead'].n)*get_syst_uncertainty( 'FakeTemplate%s'%systematics, lead_reg, lead_ptrange, 'fake', 'loose' ), 'Template_lead_fake_loose' )
    eff_syst['eff_R_L_subl'] = eff_syst['eff_R_L_subl'] + ufloat( 0.0, math.fabs(eff_syst['eff_R_L_subl'].n)*get_syst_uncertainty( 'RealTemplateNom', subl_reg, lead_ptrange, 'real', 'loose' ), 'Template_subl_real_loose' )
    eff_syst['eff_F_L_subl'] = eff_syst['eff_F_L_subl'] + ufloat( 0.0, math.fabs(eff_syst['eff_F_L_subl'].n)*get_syst_uncertainty( 'FakeTemplate%s'%systematics, subl_reg, lead_ptrange, 'fake', 'loose' ), 'Template_subl_fake_loose' )

    return eff_stat, eff_syst

def get_template_integrals( templates, cuts, lead_reg, subl_reg, lead_ptrange, subl_ptrange, systematics=None) :

    int_stat = {}
    int_stat['lead']={}
    int_stat['subl']={}
    int_stat['lead']['real']={}
    int_stat['subl']['real']={}
    int_stat['lead']['fake']={}
    int_stat['subl']['fake']={}

    int_syst = {}
    int_syst['lead']={}
    int_syst['subl']={}
    int_syst['lead']['real']={}
    int_syst['subl']['real']={}
    int_syst['lead']['fake']={}
    int_syst['subl']['fake']={}

    bins_lead_real_tight = ( templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][0] ), templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][1] ) )
    bins_lead_real_loose = ( templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][0] ), templates['lead']['real']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][1] ) )
    bins_lead_fake_tight = ( templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][0] ), templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['tight'][1] ) )
    bins_lead_fake_loose = ( templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][0] ), templates['lead']['fake']['Data'].GetXaxis().FindBin( cuts['lead']['loose'][1] ) )
    bins_subl_real_tight = ( templates['subl']['real']['Data'].GetXaxis().FindBin( cuts['subl']['tight'][0] ), templates['subl']['real']['Data'].GetXaxis().FindBin( cuts['subl']['tight'][1] ) )
    bins_subl_real_loose = ( templates['subl']['real']['Data'].GetXaxis().FindBin( cuts['subl']['loose'][0] ), templates['subl']['real']['Data'].GetXaxis().FindBin( cuts['subl']['loose'][1] ) )
    bins_subl_fake_tight = ( templates['subl']['fake']['Data'].GetXaxis().FindBin( cuts['subl']['tight'][0] ), templates['subl']['fake']['Data'].GetXaxis().FindBin( cuts['subl']['tight'][1] ) )
    bins_subl_fake_loose = ( templates['subl']['fake']['Data'].GetXaxis().FindBin( cuts['subl']['loose'][0] ), templates['subl']['fake']['Data'].GetXaxis().FindBin( cuts['subl']['loose'][1] ) )

    int_stat['lead']['real']['tight'] = get_integral_and_error( templates['lead']['real']['Data'], bins_lead_real_tight, 'Data_lead_real_tight' )
    int_stat['lead']['real']['loose'] = get_integral_and_error( templates['lead']['real']['Data'], bins_lead_real_loose, 'Data_lead_real_loose' )
    int_stat['lead']['fake']['tight'] = get_integral_and_error( templates['lead']['fake']['Data'], bins_lead_fake_tight, 'Data_lead_fake_tight' )
    int_stat['lead']['fake']['loose'] = get_integral_and_error( templates['lead']['fake']['Data'], bins_lead_fake_loose, 'Data_lead_fake_loose' )
    int_stat['subl']['real']['tight'] = get_integral_and_error( templates['subl']['real']['Data'], bins_subl_real_tight, 'Data_subl_real_tight' )
    int_stat['subl']['real']['loose'] = get_integral_and_error( templates['subl']['real']['Data'], bins_subl_real_loose, 'Data_subl_real_loose' )
    int_stat['subl']['fake']['tight'] = get_integral_and_error( templates['subl']['fake']['Data'], bins_subl_fake_tight, 'Data_subl_fake_tight' )
    int_stat['subl']['fake']['loose'] = get_integral_and_error( templates['subl']['fake']['Data'], bins_subl_fake_loose, 'Data_subl_fake_loose' )

    # If running with systematics, set the data systs to zero
    # May need to implement non-zero systematics for data in the future
    # The overall template systematics should not be set here
    int_syst['lead']['real']['tight'] = ufloat(int_stat['lead']['real']['tight'].n, 0.0 , 'Data_lead_real_tight' )
    int_syst['lead']['real']['loose'] = ufloat(int_stat['lead']['real']['loose'].n, 0.0 , 'Data_lead_real_loose' )
    int_syst['lead']['fake']['tight'] = ufloat(int_stat['lead']['fake']['tight'].n, 0.0 , 'Data_lead_fake_tight' )
    int_syst['lead']['fake']['loose'] = ufloat(int_stat['lead']['fake']['loose'].n, 0.0 , 'Data_lead_fake_loose' )
    int_syst['subl']['real']['tight'] = ufloat(int_stat['subl']['real']['tight'].n, 0.0 , 'Data_subl_real_tight' )
    int_syst['subl']['real']['loose'] = ufloat(int_stat['subl']['real']['loose'].n, 0.0 , 'Data_subl_real_loose' )
    int_syst['subl']['fake']['tight'] = ufloat(int_stat['subl']['fake']['tight'].n, 0.0 , 'Data_subl_fake_tight' )
    int_syst['subl']['fake']['loose'] = ufloat(int_stat['subl']['fake']['loose'].n, 0.0 , 'Data_subl_fake_loose' )

    # Subtract background

    if templates['lead']['real']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['lead']['real']['Background'], bins_lead_real_tight, 'Background_lead_real_tight' )
        bkg_int_loose = get_integral_and_error( templates['lead']['real']['Background'], bins_lead_real_loose, 'Background_lead_real_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty('Background%s'%systematics , lead_reg, lead_ptrange, 'real', 'tight' ), 'Background_lead_real_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'real', 'loose'), 'Background_lead_real_loose' )


        int_stat['lead']['real']['tight'] = int_stat['lead']['real']['tight'] + bkg_int_tight
        int_stat['lead']['real']['loose'] = int_stat['lead']['real']['loose'] + bkg_int_loose

        int_syst['lead']['real']['tight'] = int_syst['lead']['real']['tight'] + syst_bkg_int_tight
        int_syst['lead']['real']['loose'] = int_syst['lead']['real']['loose'] + syst_bkg_int_loose


    if templates['lead']['fake']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['lead']['fake']['Background'], bins_lead_fake_tight, 'Background_lead_fake_tight'  ) 
        bkg_int_loose = get_integral_and_error( templates['lead']['fake']['Background'], bins_lead_fake_loose, 'Background_lead_fake_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'fake', 'tight'), 'Background_lead_fake_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, lead_reg , lead_ptrange, 'fake', 'loose'), 'Background_lead_fake_loose' )

        int_stat['lead']['fake']['tight'] = int_stat['lead']['fake']['tight'] + bkg_int_tight
        int_stat['lead']['fake']['loose'] = int_stat['lead']['fake']['loose'] + bkg_int_loose

        int_syst['lead']['fake']['tight'] = int_syst['lead']['fake']['tight'] + syst_bkg_int_tight
        int_syst['lead']['fake']['loose'] = int_syst['lead']['fake']['loose'] + syst_bkg_int_loose

    if templates['subl']['real']['Background'] is not None :

        bkg_int_tight = get_integral_and_error( templates['subl']['real']['Background'], bins_subl_real_tight, 'Background_subl_real_tight'  ) 
        bkg_int_loose = get_integral_and_error( templates['subl']['real']['Background'], bins_subl_real_loose, 'Background_subl_real_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty( 'Background%s'%systematics, subl_reg , subl_ptrange, 'real', 'tight'), 'Background_subl_real_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, subl_reg , subl_ptrange, 'real', 'loose'), 'Background_subl_real_loose' )

        int_stat['subl']['real']['tight'] = int_stat['subl']['real']['tight'] + bkg_int_tight
        int_stat['subl']['real']['loose'] = int_stat['subl']['real']['loose'] + bkg_int_loose

        int_syst['subl']['real']['tight'] = int_syst['subl']['real']['tight'] + syst_bkg_int_tight
        int_syst['subl']['real']['loose'] = int_syst['subl']['real']['loose'] + syst_bkg_int_loose

    if templates['subl']['fake']['Background'] is not None :
        bkg_int_tight = get_integral_and_error( templates['subl']['fake']['Background'], bins_subl_fake_tight, 'Background_subl_fake_tight'  ) 
        bkg_int_loose = get_integral_and_error( templates['subl']['fake']['Background'], bins_subl_fake_loose, 'Background_subl_fake_loose'  ) 

        syst_bkg_int_tight = ufloat( bkg_int_tight.n, math.fabs(bkg_int_tight.n)*get_syst_uncertainty( 'Background%s'%systematics, subl_reg , subl_ptrange, 'fake', 'tight'), 'Background_subl_fake_tight' )
        syst_bkg_int_loose = ufloat( bkg_int_loose.n, math.fabs(bkg_int_loose.n)*get_syst_uncertainty( 'Background%s'%systematics, subl_reg , subl_ptrange, 'fake', 'loose'), 'Background_subl_fake_loose' )
        int_stat['subl']['fake']['tight'] = int_stat['subl']['fake']['tight'] + bkg_int_tight
        int_stat['subl']['fake']['loose'] = int_stat['subl']['fake']['loose'] + bkg_int_loose
        
        int_syst['subl']['fake']['tight'] = int_syst['subl']['fake']['tight'] + syst_bkg_int_tight
        int_syst['subl']['fake']['loose'] = int_syst['subl']['fake']['loose'] + syst_bkg_int_loose

    return int_stat, int_syst

def get_integral_and_error( hist, bins=None, name='' ) :

    err = ROOT.Double()
    if bins is None :
        val = hist.IntegralAndError( 1, hist.GetNbinsX(), err )
    else :
        if bins[1] is None :
            val = hist.IntegralAndError( bins[0], hist.GetNbinsX(), err )
        else :
            val = hist.IntegralAndError( bins[0], bins[1], err )

    return ufloat( val, err, name )


def get_single_photon_template( selection, binning, sample, reg, fitvar='sigmaIEIE', sampMan=None) :

    if sampMan is None :
        sampMan = sampManLG

    if reg not in ['EB', 'EE'] :
        print 'Region not specified correctly'
        return None

    var = 'ph_pt[0]:ph_%s[0]' %fitvar#y:x

    selection = selection + ' && ph_Is%s[0] ' %( reg )

    data_samp_name = sample['Data']
    bkg_samp_name  = sample.get('Background', None)

    template_hists = {}

    data_samp = sampMan.get_samples(name=data_samp_name )

    if data_samp :
        template_hists['Data'] = clone_sample_and_draw( data_samp[0], var, selection, ( binning[0], binning[1], binning[2],100, 0, 500  ), useSampMan=sampMan ) 
    else :
        print 'Data template sample not found!'
        
    if bkg_samp_name is not None :
        bkg_samp = sampMan.get_samples(name=bkg_samp_name )

        if bkg_samp :
            template_hists['Background'] = clone_sample_and_draw( bkg_samp[0], var, selection, ( binning[0], binning[1], binning[2],100, 0, 500  ), useSampMan=sampMan ) 
        else :
            print 'Background template sample not found!'
    else :
        template_hists['Background']=None

    return template_hists

def generate_eff_matrix( eff_dic, ndim=3 ) :

    eff_matrix = [ [ eff_dic['eff_RF_TL'], eff_dic['eff_FR_TL'], eff_dic['eff_FF_TL'] ],
                   [ eff_dic['eff_RF_LT'], eff_dic['eff_FR_LT'], eff_dic['eff_FF_LT'] ], 
                   [ eff_dic['eff_RF_LL'], eff_dic['eff_FR_LL'], eff_dic['eff_FF_LL'] ] ] 
    
    if ndim == 4 :
        eff_matrix = [ [ eff_dic['eff_RR_TT'], eff_dic['eff_RF_TT'], eff_dic['eff_FR_TT'], eff_dic['eff_FF_TT'] ], 
                       [ eff_dic['eff_RR_TL'], eff_matrix[0][0]    , eff_matrix[0][1]    , eff_matrix[0][2]     ],
                       [ eff_dic['eff_RR_LT'], eff_matrix[1][0]    , eff_matrix[1][1]    , eff_matrix[1][2]     ],
                       [ eff_dic['eff_RR_LL'], eff_matrix[2][0]    , eff_matrix[2][1]    , eff_matrix[2][2]     ] ]

    elif ndim != 3 :
        print 'Only Dim 3 and 4 implemented'
        return None

    return eff_matrix


def solve_matrix_eq( matrix_ntries, vector_entries ) :

    ms = []
    mn = []
    for row in matrix_ntries :
        ms_row = []
        mn_row = []
        for col in row :
            ms_row.append( col.s )
            mn_row.append( col.n )
        ms.append( ms_row )
        mn.append( mn_row )

    matrix = unumpy.umatrix( mn, ms )

    print matrix

    vs = []
    vn = []
    for row in vector_entries :
        vn.append( [ row.n ] )
        vs.append( [ row.s ] )

    vector = unumpy.umatrix( vn, vs )
    
    inv_matrix = None
    try :
        inv_matrix = matrix.getI()
    except :
        print 'Failed to invert matrix, aborting'
        return unumpy.umatrix( [ [1]*len(vs) ], [ [0]*len(vs) ] )

    print inv_matrix
    print vector

    return inv_matrix*vector

def clone_sample_and_draw( samp, var, sel, binning, useSampMan=None ) :

    if useSampMan is not None :
        newSamp = useSampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        useSampMan.create_hist( newSamp, var, sel, binning )
        return newSamp.hist

    else :
        newSamp = sampMan.clone_sample( oldname=samp.name, newname=samp.name+str(uuid.uuid4()), temporary=True ) 
        sampMan.create_hist( newSamp, var, sel, binning )
        return newSamp.hist

def save_templates( templates, outputDir, lead_ptrange=(None,None), subl_ptrange=(None,None),namePostfix='' ) :

    if outputDir is None :
        return

    draw_templates = {'lead' : {}, 'subl' : {} }

    draw_templates['lead']['real'] = templates['lead']['real']['Data'].Clone( 'draw_%s' %templates['lead']['real']['Data'].GetName())
    draw_templates['lead']['fake'] = templates['lead']['fake']['Data'].Clone( 'draw_%s' %templates['lead']['fake']['Data'].GetName())
    draw_templates['subl']['real'] = templates['subl']['real']['Data'].Clone( 'draw_%s' %templates['subl']['real']['Data'].GetName())
    draw_templates['subl']['fake'] = templates['subl']['fake']['Data'].Clone( 'draw_%s' %templates['subl']['fake']['Data'].GetName())

    if templates['lead']['real']['Background'] is not None :
        draw_templates['lead']['real'].Add( templates['lead']['real']['Background'])
    if templates['lead']['fake']['Background'] is not None :
        draw_templates['lead']['fake'].Add( templates['lead']['fake']['Background'])
    if templates['subl']['real']['Background'] is not None :
        draw_templates['subl']['real'].Add( templates['subl']['real']['Background'])
    if templates['subl']['fake']['Background'] is not None :
        draw_templates['subl']['fake'].Add( templates['subl']['fake']['Background'])

    can_lead_real = ROOT.TCanvas('can_lead_real', '')
    can_lead_fake = ROOT.TCanvas('can_lead_fake', '')
    can_subl_real = ROOT.TCanvas('can_subl_real', '')
    can_subl_fake = ROOT.TCanvas('can_subl_fake', '')

    pt_label_lead = None
    pt_label_subl = None
    if lead_ptrange[0] is not None :
        if lead_ptrange[1] == None :
            pt_label_lead = ' p_{T} > %d ' %( lead_ptrange[0] )
        else :
            pt_label_lead = ' %d < p_{T} < %d ' %( lead_ptrange[0], lead_ptrange[1] )
    else :
        pt_label_lead = 'p_{T} inclusive'

    if subl_ptrange[0] is not None :
        if subl_ptrange[1] == None :
            pt_label_subl = ' p_{T} > %d ' %( subl_ptrange[0] )
        else :
            pt_label_subl = ' %d < p_{T} < %d ' %( subl_ptrange[0], subl_ptrange[1] )
    else :
        pt_label_subl = 'p_{T} inclusive'

    draw_template( can_lead_real, draw_templates['lead']['real'], sampManData, normalize=1, label=pt_label_lead, outputName = outputDir+'/template_lead_real%s.pdf' %namePostfix )
    draw_template( can_lead_fake, draw_templates['lead']['fake'], sampManData, normalize=1, label=pt_label_lead, outputName = outputDir+'/template_lead_fake%s.pdf' %namePostfix )
    draw_template( can_subl_real, draw_templates['subl']['real'], sampManData, normalize=1, label=pt_label_subl, outputName = outputDir+'/template_subl_real%s.pdf' %namePostfix )
    draw_template( can_subl_fake, draw_templates['subl']['fake'], sampManData, normalize=1, label=pt_label_subl, outputName = outputDir+'/template_subl_fake%s.pdf' %namePostfix )


def save_results( results, outputDir, namePostfix='' ) :

    if outputDir is None :
        return

    fname = outputDir + '/results%s.pickle' %namePostfix

    if not os.path.isdir( os.path.dirname( fname ) ) :
        os.makedirs( os.path.dirname( fname ) )
    file = open( fname, 'w' )
    pickle.dump( results, file )
    file.close()


def draw_template(can, hists, sampMan, normalize=False, first_hist_is_data=False, axis_label='#sigma i#etai#eta', label=None, legend_entries=[], outputName=None ) :

    if not isinstance(hists, list) :
        hists = [hists]

    can.cd()
    can.SetBottomMargin( 0.12 )
    can.SetLeftMargin( 0.12 )

    added_sum_hist=False
    if len(hists) > 1 and not first_hist_is_data or len(hists)>2 and first_hist_is_data :
        if first_hist_is_data :
            hists_to_sum = hists[1:]
        else :
            hists_to_sum = hists

        sumhist = hists_to_sum[0].Clone( 'sumhist%s' %hists_to_sum[0].GetName())
        for h in hists_to_sum[1:] :
            sumhist.Add(h)

        format_hist( sumhist, ROOT.kBlue+1 )
        hists.append(sumhist)
        added_sum_hist=True

    #get y size
    maxbin = hists[0].GetBinContent(hists[0].GetMaximumBin())
    for h in hists[1: ] :
        if h.GetBinContent(h.GetMaximumBin() ) > maxbin :
            maxbin = h.GetBinContent(h.GetMaximumBin() )

    maxval_hist = maxbin * 1.25
    if normalize :
        maxval_axis = maxval_hist/hists[0].Integral()
    else :
        maxval_axis = maxval_hist
        
    for h in hists :        
        h.GetYaxis().SetRangeUser( 0, maxval_hist )
        h.GetXaxis().SetTitleSize( 0.05 )
        h.GetXaxis().SetLabelSize( 0.05 )
        h.GetYaxis().SetTitleSize( 0.05 )
        h.GetYaxis().SetLabelSize( 0.05 )
        h.GetYaxis().SetTitleOffset( 1.15 )
        h.GetXaxis().SetTitle( axis_label )
        h.SetStats(0)
        h.SetLineWidth( 2 )
        bin_width = h.GetXaxis().GetBinWidth(1)

        if first_hist_is_data :
            h.GetYaxis().SetTitle( 'Events / %.3f ' %bin_width )
        else :
            h.GetYaxis().SetTitle( 'A.U. / %.3f ' %bin_width )

    drawcmd=''
    if not first_hist_is_data :
        drawcmd += 'hist'

    if normalize :
        hists[0].DrawNormalized(drawcmd)
        drawcmd+='hist'
        for h in hists[1:] :
            h.DrawNormalized(drawcmd + 'same')
    else :
        hists[0].Draw(drawcmd)
        drawcmd+='hist'
        for h in hists[1:] :
            h.Draw(drawcmd + 'same')

    leg=None
    if legend_entries :
        drawconf = DrawConfig( None, None, None, legend_config={'legendTranslateX' : -0.1 } )
        leg = sampMan.create_standard_legend( len(hists), draw_config=drawconf )
        if added_sum_hist :
            legend_entries.append( 'Template sum' )

        for ent, hist in zip( legend_entries, hists ) :
            leg.AddEntry( hist, ent )

        leg.Draw()

    if label is not None :
        lab = ROOT.TLatex(0.12, 0.8, label )
        lab.SetTextSize( 0.04 )
        lab.SetNDC()
        lab.SetX(0.15)
        lab.SetY(0.8)
        lab.Draw()

    if outputName is None :
        raw_input('continue')
        
    if outputName is not None :
        if not os.path.isdir( os.path.dirname(outputName) ) :
            os.makedirs( os.path.dirname(outputName) )

        can.SaveAs( outputName )


if __name__ == '__main__' :
    main()