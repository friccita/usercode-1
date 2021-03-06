
def MakeTAndPHists( outputfile, tagprobe_min=0, tagprobe_max=1e9, normalize=1 ) :

    global samples
    vals_norm = [15, 5000]
    ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 200, 500 ]
    ptvals_2d = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    etavals_2d = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    #etavals_2d = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, 0.000000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]

    samples.DoTAndP( 'probe_pt', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL', vals_norm, colors=[ROOT.kBlack], normalize=0 )
    hist_norm = samples.get_samples(isRatio=True)[0].hist.Clone('norm')

    samples.DoTAndP( 'probe_eta', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL',etavals , colors=[ROOT.kBlack], normalize=normalize )
    hist_eta = samples.get_samples(isRatio=True)[0].hist.Clone('eta')

    samples.DoTAndP( 'probe_pt', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL', ptvals, colors=[ROOT.kBlack], normalize=normalize )
    hist_pt = samples.get_samples(isRatio=True)[0].hist.Clone('pt')

    samples.DoTAndP( 'probe_pt:probe_eta', 'probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), '!probe_isPhoton && probe_pt > 15 && m_tagprobe > %d && m_tagprobe < %d' %(tagprobe_min, tagprobe_max), 'DYJetsToLL', (etavals_2d,ptvals_2d), colors=[ROOT.kBlack], normalize=0 )
    hist_pt_eta = samples.get_samples(isRatio=True)[0].hist.Clone('pteta')

    file = ROOT.TFile.Open( outputfile, 'RECREATE' )

    hist_eta.Write()
    hist_pt.Write()
    hist_norm.Write()
    hist_pt_eta.Write()

    file.Close()


#---------------------------------------
def MakeTAndPPlots( ) :

    if options.outputDir is None :
        print 'Must provide an output directory via --outputDir.  Will not make plots'
        return
    
    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.01, ymax=0.022, label='unconverted photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.006, ymax=0.018, label='2 track conversion photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mcsub_2conv', 'ratiocan')
    
    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', ymin=0.005, ymax=0.042, label='unconverted photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', label='2 track conversion photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mcsub_2conv', 'ratiocan')


    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50  )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll  && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50)',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.01, ymax=0.022, label='unconverted photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mtcut_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_pt', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )',  ['DataMCSubtracted', 'Z + Jets'], (60, 0, 300, 250 ), xlabel='Electron p_{T} [GeV]', ylabel='Electron to photon fake factor', ymin=0.006, ymax=0.018, label='2 track conversion photons' )
    SaveStack('probe_pt_electron_to_photon_ff_mtcut_mcsub_2conv', 'ratiocan')
    
    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==0 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', ymin=0.005, ymax=0.042, label='unconverted photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mtcut_mcsub_0conv', 'ratiocan')

    DoTAndP( 'probe_eta', 'EventWeight * ( probe_passTight && probe_isPhot && probe_nConvTrk==2 && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )', 'EventWeight * ( tag_isElec && !probe_isPhot && passcut_mll && sqrt(2*met_et*tag_pt*( 1 - cos( met_phi-tag_phi) ) ) < 50 )',  ['DataMCSubtracted', 'Z + Jets'], (50, -2.5, 2.5 ), xlabel='Electron #eta', ylabel='Electron to photon fake factor', label='2 track conversion photons' )
    SaveStack('probe_eta_electron_to_photon_ff_mtcut_mcsub_2conv', 'ratiocan')


def MakeDiPhotonTemplatePlots() :

    global samples

    #signal_selection = ' PUWeight * (mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 && ph_IsEB[0] )'
    #signal_sample = 'Data'
    signal_selection = ' PUWeight * (mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && leadPhot_leadLepDR>0.4 && ph_IsEB[0] && ph_truthMatch_ph[0] && abs(ph_truthMatchMotherPID_ph[0]) < 25 )'
    signal_sample = 'Wgamma'

    #bkg_selection =  ' PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_chIsoCorr[0] > 2 && ph_chIsoCorr[0] < 5 && ph_IsEB[0]  )', (60, 0, 0.03) )
    bkg_selection = ' PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_passChIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1  && ph_IsEB[0]  )'
    #bkg_selection =  ' PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_passChIsoCorrMedium[0] && ph_IsEB[0] )', (60, 0, 0.03) )
    #bkg_selection =  ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] )', (60, 0, 0.03) )
    #bkg_selection =  ' PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] && ph_passChIsoCorrMedium[0] )', (60, 0, 0.03) )

    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] )', ['Data', 'Data'], (30, 0, 0.03), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.001' )
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] )'], ['Data', 'Data'], (30, 0, 0.03), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.001' )
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] && ph_IsEB[0] )'], ['Data', 'Data'], (30, 0, 0.03), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.001', colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation cuts', 'Apply Ch Iso cut on sublead photon'] )
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] && ph_IsEB[0] )'], ['Data', 'Data'], (30, 0, 0.03), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.001', colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation cuts', 'Apply Ch Iso cut on sublead photon'] )
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEE[0] )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] && ph_IsEE[0] )'], ['Data', 'Data'], (20, 0, 0.1), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.005', colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation cuts', 'Apply Ch Iso cut on sublead photon'] )
    #SaveStack('sieieLead_mgg_nocut_vs_sublChIso_ee')
    #1
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] )'], ['Data', 'Data'], (30, 0, 0.03), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Normalized Events / 0.001', rlabel='No cut / cut', colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation cuts', 'Apply Ch Iso cut on sublead photon']  )
    #SaveStack('sieieLead_mgg_nocut_vs_sublChIso_eb', 'base')
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEB[0] )'], ['Data', 'Data'], (30, 0, 0.03), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Normalized Events / 0.001', rlabel='No cut / cut', colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation cuts', 'Apply iso cuts on sublead photon']  )
    #SaveStack('sieieLead_mgg_nocut_vs_sublChIsoNeuIsoPhoIso_eb', 'base')
    #samples.CompareSelections( 'ph_sigmaIEIE[0]', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEE[0] )', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && ph_IsEE[0] )'], ['Data', 'Data'], (20, 0, 0.1), normalize=1, doratio=1, xlabel='Lead photon #sigma i#eta i#eta', ylabel='Normalized Events / 0.005', rlabel='No cut / cut', colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation cuts', 'Apply iso cuts on sublead photon']  )
    #SaveStack('sieieLead_mgg_nocut_vs_sublChIsoNeuIsoPhoIso_ee', 'base')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEE[0] )', (20, 0, 0.1),xlabel='Lead photon #sigma i#eta i#eta', ylabel='Normalized Events / 0.005')
    #SaveStack( 'sieieLead_mgg_noIsoLead_noIsoSubl_ee', 'base' )
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] )', (30, 0, 0.0.3),xlabel='Lead photon #sigma i#eta i#eta', ylabel=' Events / 0.001')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] )', (30, 0, 0.03),xlabel='Lead photon #sigma i#eta i#eta', ylabel=' Events / 0.001')
    #SaveStack( 'sieieLead_mgg_noIsoLead_noIsoSubl_eb', 'base' )
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] && ph_passChIsoCorrMedium[1] )', (30, 0, 0.03),xlabel='Lead photon #sigma i#eta i#eta', ylabel=' Events / 0.001')
    #SaveStack( 'sieieLead_mgg_noIsoLead_ChIsoSubl_eb', 'base' )
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEE[0] && ph_passChIsoCorrMedium[1] )', (20, 0, 0.1),xlabel='Lead photon #sigma i#eta i#eta', ylabel='Normalized Events / 0.005')
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEE[0] && ph_passChIsoCorrMedium[1] )', (20, 0, 0.1),xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.005')
    #SaveStack( 'sieieLead_mgg_noIsoLead_ChIsoSubl_ee', 'base' )
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] )', (20, 0, 0.1),xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.005')
    #SaveStack( 'sieieLead_mgg_noIsoLead_AllIsoSubl_ee', 'base' )
    #samples.Draw('ph_sigmaIEIE[0]', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==2 && ph_phDR>0.3 && ph_HoverE12[0]<0.05 && ph_HoverE12[1]<0.05 && ph_eleVeto[0]==0 && ph_eleVeto[1]==0 && ph_IsEB[0] && ph_passChIsoCorrMedium[1] && ph_passNeuIsoCorrMedium[1] && ph_passPhoIsoCorrMedium[1] )', (30, 0, 0.03),xlabel='Lead photon #sigma i#eta i#eta', ylabel='Events / 0.001')
    #SaveStack( 'sieieLead_mgg_noIsoLead_AllIsoSubl_eb', 'base' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0] && ph_passChIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0] && ph_passChIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events', doratio=1, rlabel='No cut / cut' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0] && ph_passChIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events', doratio=1, rlabel='No cut / cut', normalize=1, colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation Cuts', 'Apply Ch Iso cut'] )
    #SaveStack( 'nVtx_mg_noIso_vs_ChIso_eb', 'base' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEE[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0] && ph_passChIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events', doratio=1, rlabel='No cut / cut', normalize=1, colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation Cuts', 'Apply Ch Iso cut'] )
    #SaveStack( 'nVtx_mg_noIso_vs_ChIso_ee', 'base' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEE[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0] && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events', doratio=1, rlabel='No cut / cut', normalize=1, colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation Cuts', 'Apply all iso cuts'] )
    #SaveStack( 'nVtx_mg_noIso_vs_AllIso_ee', 'base' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEE[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEE[0] && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events', doratio=1, rlabel='No cut / cut', normalize=1, colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation Cuts', 'Apply all iso cuts'] )
    #SaveStack( 'nVtx_mg_noIso_vs_AllIso_ee', 'base' )
    #samples.CompareSelections( 'nVtx', ['PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0]) ', 'PUWeight * ( mu_passtrig_n>0 && mu_n==1 && ph_n==1 && ph_eleVeto[0]==0 && ph_HoverE12[0]<0.05 && ph_IsEB[0] && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0]) '], ['Data']*2, (50, 0, 50), xlabel='Vertex multiplicity', ylabel='Events', doratio=1, rlabel='No cut / cut', normalize=1, colors=[ROOT.kBlack, ROOT.kRed], legend_entries=['No Isolation Cuts', 'Apply all iso cuts'] )
    #SaveStack( 'nVtx_mg_noIso_vs_AllIso_eb', 'base' )


    bkg_sample = 'DataRealPhotonSub'
    #bkg_sample = 'Zgammastar'

    sig_template_samp = samples.get_samples(name=signal_sample )
    if sig_template_samp :
        newEBSigsamp = samples.clone_sample( oldname=sig_template_samp[0].name, newname='DataSigTemplateEB', temporary=True )
        newEESigsamp = samples.clone_sample( oldname=sig_template_samp[0].name, newname='DataSigTemplateEE', temporary=True )
        newEBSigsampNeg = samples.clone_sample( oldname=sig_template_samp[0].name, newname='DataSigTemplateEBNeg', temporary=True )
        newEESigsampNeg = samples.clone_sample( oldname=sig_template_samp[0].name, newname='DataSigTemplateEENeg', temporary=True )
        #signal template, EB
        samples.create_hist( newEBSigsamp, 'ph_sigmaIEIE[0]', signal_selection , (60, -0.03, 0.03) )
        samples.create_hist( newEBSigsampNeg, '-1*ph_sigmaIEIE[0]', signal_selection , (60, -0.030, 0.03) )
        sig_template_hist_eb = newEBSigsamp.hist

        ##signal template, EE
        #samples.create_hist( newEESigsamp, 'ph_sigmaIEIE[0]', ' PUWeight * (mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passChIsoCorrMedium[0] && ph_passNeuIsoCorrMedium[0] && ph_passPhoIsoCorrMedium[0] && fabs( m_leplepph-91.2 ) < 5 && leadPhot_sublLepDR > 0.4 && leadPhot_sublLepDR<1 && leadPhot_leadLepDR>0.4 && ph_IsEE[0])', (50, 0, 0.1) )
        #sig_template_hist_ee = newEESigsamp.hist


    #background template, EB
    bkg_template_samp = samples.get_samples(name=bkg_sample)
    if bkg_template_samp :
        newEBBkgsamp = samples.clone_sample( oldname=bkg_template_samp[0].name, newname='DataMCSubBkgTemplateEB', temporary=True )
        newEEBkgsamp = samples.clone_sample( oldname=bkg_template_samp[0].name, newname='DataMCSubBkgTemplateEE', temporary=True )
        newEBBkgsampNeg = samples.clone_sample( oldname=bkg_template_samp[0].name, newname='DataMCSubBkgTemplateEBNeg', temporary=True )
        newEEBkgsampNeg = samples.clone_sample( oldname=bkg_template_samp[0].name, newname='DataMCSubBkgTemplateEENeg', temporary=True )
        samples.create_hist( newEBBkgsamp, 'ph_sigmaIEIE[0]' , bkg_selection , (60, -0.03, 0.03) )
        samples.create_hist( newEBBkgsampNeg, '-1*ph_sigmaIEIE[0]', bkg_selection , (60, -0.03, 0.03) )
        bkg_template_hist_eb = newEBBkgsamp.hist
        bkg_template_hist_eb_neg = newEBBkgsampNeg.hist

        ##background template, EE
        #samples.create_hist( newEEBkgsamp, 'ph_sigmaIEIE[0]', ' PUWeight * ( mu_passtrig_n>0 && mu_n==2 && ph_n==1 && ph_HoverE12[0] < 0.05 && ph_passNeuIsoCorrMedium[0] && fabs( m_leplep-91.2 ) < 5 && leadPhot_sublLepDR >1 && leadPhot_leadLepDR>1 && ph_SCRChIso[0] > 5 && ph_SCRChIso[0] < 10 && ph_IsEE[0] )', (50, 0, 0.1) )
        #bkg_template_hist_ee = newEEBkgsamp.hist

    RRhist = ROOT.TH1F( 'RRhist', 'RRhist', 60, -0.03, 0.03 )
    RFhist = ROOT.TH1F( 'RFhist', 'RFhist', 60, -0.03, 0.03 )
    FFhist = ROOT.TH1F( 'FFhist', 'FFhist', 60, -0.03, 0.03 )

    RRhist.Add( newEBSigsamp.hist)
    RRhist.Add( newEBSigsampNeg.hist)
    RFhist.Add( newEBSigsamp.hist)
    RFhist.Add( newEBBkgsampNeg.hist)
    RFhist.Add( newEBSigsampNeg.hist)
    RFhist.Add( newEBBkgsamp.hist)
    FFhist.Add( newEBBkgsamp.hist)
    FFhist.Add( newEBBkgsampNeg.hist)

    samples.create_standard_canvas()
    samples.curr_canvases['base'].cd()

    RRhist.SetLineColor( ROOT.kGreen )
    RFhist.SetLineColor( ROOT.kBlue+1 )
    FFhist.SetLineColor( ROOT.kRed+1 )

    RRhist.DrawNormalized('hist')
    RFhist.DrawNormalized('histsame')
    FFhist.DrawNormalized('histsame')

    raw_input('continue')



#--- ------------------------------------
def MakeZHCutFlowTables( channel='EE' ) :

    global samples

    cut_flow = ['']
    if channel == 'EE' :
        cut_base = 'EventWeight * ( passtrig_electron %s)'
        cut_flow.append('IsEE')
    if channel == 'MM' :
        cut_base = 'EventWeight * ( passtrig_muon %s)'
        cut_flow.append('IsMM')

    cut_flow += ['passcut_os', 'passcut_thirdlepveto', 'passcut_mll', 'passcut_met', 'passcut_dphill', 'passcut_ll_dphi_met', 'passcut_fracdiff', 'passcut_met_dphi_trackmet', 'passcut_jetveto']

    cut_selections = []
    for idx in range(1, len(cut_flow)+1 ) :
        cut_selections.append( cut_base%( ' && '.join(cut_flow[0:idx]) ) )

    print cut_selections
    print len(cut_selections)
    cut_labels = ['Trigger', 'DiLep', 'OS', 'ThirdLep', 'Mll', 'Met', 'DPhill', 'ZMetDphi', 'FracDiff', 'MetTrkDPhi', 'JetVeto']

    samples.MakeCutflowTable('met_et', cut_selections, cut_labels, (50, 0, 5000))
    
#---------------------------------------
def MakeQCDCRPlots() :

    global samples
    if options.outputDir is None :
        print 'Must provide an output directory via --outputDir.  Will not make plots'
        return

    #samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio && !ph_pass_fside && !ph_pass_deltae ) ) ', ( 64, -2, 30 ), xlabel='Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=1e12, ymin=1 )
    #SaveStack('ph_corriso_30_invertall', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio || !ph_pass_fside || !ph_pass_deltae ) ) ', ( 64, -2, 30 ), xlabel='Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=1e13, ymin=1 )
    SaveStack('ph_corriso_30_invertany', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( ( !ph_pass_eratio && !ph_pass_fside ) || ( !ph_pass_eratio && !ph_pass_deltae ) || ( !ph_pass_fside && !ph_pass_deltae ) ) )', ( 64, -2, 30 ), xlabel='Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=5e12, ymin=1 )
    SaveStack('ph_corriso_30_invertmaj', 'base')

    samples.Draw('ph_pt', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_corriso_30 > 10000 && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio && !ph_pass_fside && !ph_pass_deltae ) ) ', ( 100, 0, 500, 25 ), xlabel='p_{T} [GeV]', noAtlasLabel=True, doratio=0, logy=True, ymax=1e9, ymin=0.01 )
    SaveStack('ph_pt_invertall_noniso', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0 && ph_corriso_30 > 10000  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( !ph_pass_eratio || !ph_pass_fside || !ph_pass_deltae ) ) ', ( 100, 0, 500, 25 ), xlabel='p_{T} [GeV]', noAtlasLabel=True, doratio=0, logy=True, ymax=1e9, ymin=0.01 )
    SaveStack('ph_pt_invertany_noniso', 'base')

    samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0 && ph_corriso_30 > 10000  && ph_pass_hadleak && ph_pass_middle && ph_pass_middle && ph_pass_wstot && ph_pass_weta1 && ph_pass_ar && ph_pass_demax2 && ph_pass_f1 && ( ( !ph_pass_eratio && !ph_pass_fside ) || ( !ph_pass_eratio && !ph_pass_deltae ) || ( !ph_pass_fside && !ph_pass_deltae ) ) )', ( 100, 0, 500, 25 ), xlabel='p_{T} [GeV]', noAtlasLabel=True, doratio=0, logy=True, ymax=1e9, ymin=0.01 )
    SaveStack('ph_pt_invertmaj_noniso', 'base')

    #samples.Draw('ph_corriso_30/1000.0', 'EventWeight * ( ph_n == 1 && ph_pt > 30.0 && ph_nConvTrk == 0  && ph_pass_tight ) ', ( 64, -2, 30 ), xlabel='Photon Calorimeter Isolation [GeV]', ylabel='Events / 0.5 GeV', noAtlasLabel=True, doratio=0, logy=True, ymax=1e13, ymin=100 )
    #SaveStack('ph_corriso_30_tightnoiso', 'base')

def MakeTAndPCompPlots( ) :
    global samples
    #ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 500 ]
    #etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    #etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, 0.000000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    for pidx, pmin in enumerate(ptvals[:-1]) :
        pmax = ptvals[pidx+1]
        for eidx, emin in enumerate(etavals[:-1]) :
            emax = etavals[eidx+1]
            eta_precision = 1
            eta_precisionm = 1
            if math.fabs(int(emin*10)-emin) != 0 : 
                eta_precision = 3
            if math.fabs(int(emax*10)-emax) != 0 :
                eta_precisionm=3
            samples.CompareSelections('m_tagprobe', ['!probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax), 'probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax)], ['DYJetsToLL', 'DYJetsToLL'], (100, 0, 500), colors=[ROOT.kBlack, ROOT.kRed], doratio=0, logy=1, legend_entries=['Probe electrons', 'Probe photons'], ymax_scale=10, xlabel='M_{tag, probe} [GeV]', extra_label='#splitline{%d < p_{T} < %d}{%.*f < #eta < %.*f}' %( pmin, pmax, eta_precision, emin, eta_precisionm, emax ) )
            SaveStack( 'm_tagprobe_pt_%d_%d_eta_%f_%f' %( pmin, pmax, emin, emax), 'base' )
          
def MakeTAndPCompPlotsFull( ) :
    global samples

    #ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 60, 70, 80, 100, 150, 500 ]
    #etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.900000, -1.800000, -1.700000, -1.566000, -1.479000, -1.400000, -1.300000, -1.200000, -1.100000, -1.000000, -0.800000, -0.600000, -0.400000, -0.200000, 0.000000, 0.200000, 0.400000, 0.600000, 0.800000, 1.000000, 1.100000, 1.200000, 1.300000, 1.400000, 1.479000, 1.566000, 1.700000, 1.800000, 1.900000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    #ptvals = [25, 30, 35, 40, 45, 50, 500 ]
    etavals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]

    for pidx, pmin in enumerate(ptvals[:-1]) :
        pmax = ptvals[pidx+1]
        for eidx, emin in enumerate(etavals[:-1]) :
            emax = etavals[eidx+1]
            eta_precision = 1
            eta_precisionm = 1
            if math.fabs(int(emin*10)-emin) != 0 : 
                eta_precision = 3
            if math.fabs(int(emax*10)-emax) != 0 :
                eta_precisionm=3

            samples.Draw('m_tagprobe', '!probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax),  (100, 0, 200), ymin=10, ymax_scale=10, xlabel='M_{tag, probe} [GeV]', extra_label='#splitline{Probe Electrons}{#splitline{%d < p_{T} < %d}{%.*f < #eta < %.*f}}' %( pmin, pmax, eta_precision, emin, eta_precisionm, emax), extra_label_loc='TopLeft', logy=1, noAtlasLabel=True  )
            SaveStack( 'm_tagprobe_probeEl_pt_%d_%d_eta_%f_%f' %( pmin, pmax, emin, emax), 'base' )

            samples.Draw('m_tagprobe', 'probe_isPhoton && probe_pt > %d && probe_pt < %d && probe_eta > %f && probe_eta < %f ' %( pmin, pmax, emin, emax),  (100, 0, 200), ymin=10, ymax_scale=10, xlabel='M_{tag, probe} [GeV]', extra_label='#splitline{Probe Photons}{#splitline{%d < p_{T} < %d}{%.*f < #eta < %.*f}}' %( pmin, pmax, eta_precision, emin, eta_precisionm, emax ), extra_label_loc='TopLeft', logy=1, noAtlasLabel=True )
            SaveStack( 'm_tagprobe_probePh_pt_%d_%d_eta_%f_%f' %( pmin, pmax, emin, emax), 'base' )
          
def FitTAndPComp( ) :
    global samples

    #ptvals = [15, 20, 25, 30, 35, 40, 45, 50, 500 ]
    ptvals = [-2.500000, -2.450000, -2.400000, -2.350000, -2.300000, -2.200000, -2.100000, -2.000000, -1.566000, -1.479000, -1.200000, -0.800000, -0.200000, 0.000000, 0.200000, 0.800000, 1.200000, 1.479000, 1.566000, 2.000000, 2.100000, 2.200000, 2.300000, 2.350000, 2.400000, 2.450000,2.5]
    meanhist = ROOT.TH1F( 'mean', '', len(ptvals)-1, array('f', ptvals))
    widthhist = ROOT.TH1F( 'width', '', len(ptvals)-1, array('f', ptvals))
    for pidx, pmin in enumerate(ptvals[:-1]) :
        pmax = ptvals[pidx+1]

        #samples.CompareSelections('m_lepph1', ['EventWeight * (el_n==1 && ph_n==1 && ph_pt[0] > %d && ph_pt[0] < %d)' %(pmin, pmax)]*2, ['DYJetsToLL', 'DYJetsToLLFF'], (500, 0, 500), doratio=0 )
        samples.CompareSelections('m_lepph1', ['EventWeight * (el_n==1 && ph_n==1 && ph_eta[0] > %f && ph_eta[0] < %f)' %(pmin, pmax)]*2, ['DYJetsToLL', 'DYJetsToLLFF'], (500, 0, 500), doratio=0 )

        hist_lg = samples.get_samples(name='DYJetsToLL0')[0].hist
        hist_ff = samples.get_samples(name='DYJetsToLLFF1')[0].hist

        func = ROOT.TF1( 'gaus', 'gaus(0)', 86, 96 )
        func.SetParameter(0, hist_lg.GetBinContent( hist_lg.FindBin( 91) ) )
        func.SetParameter(1, 91)
        func.SetParameter(2, 3)

        hist_lg.Fit( func, 'R')
        mean_lg = func.GetParameter(1)
        width_lg = func.GetParameter(2)

        func.SetParameter(0, hist_ff.GetBinContent( hist_ff.FindBin( 91) ) )
        func.SetParameter(1, 91)
        func.SetParameter(2, 3)
        hist_ff.Fit( func, 'R' )
        mean_ff = func.GetParameter(1)
        width_ff = func.GetParameter(2)

        meanhist.SetBinContent( pidx+1, mean_lg - mean_ff )
        widthhist.SetBinContent( pidx+1, width_lg - width_ff )

        print 'Pt range = %d - %d' %( pmin, pmax )
        print 'Delta mean = %f' %(mean_lg - mean_ff)
        print 'Delta width = %f' %(width_lg - width_ff)

    meanhist.Draw()
    raw_input('continue')
    widthhist.Draw()
    raw_input('continue')


