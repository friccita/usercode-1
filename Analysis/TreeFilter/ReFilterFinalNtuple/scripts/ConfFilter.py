from core import Filter
import inspect
import sys

def get_remove_filter() :
    """ Define list of regex strings to filter input branches to remove from the output.
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableRemoveFilter on the command line.
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def get_keep_filter() :
    """ Define list of regex strings to filter input branches to retain in the output.  
        Defining a non-empty list does not apply the filter, 
        you must also supply --enableKeepFilter on the command line
        If both filters are used, all branches in keep_filter are used
        except for those in remove_filter """

    return []

def config_analysis( alg_list, args ) :
    """ Configure analysis modules. Order is preserved """

    # run on the function provided through
    # the args
    for s in inspect.getmembers(sys.modules[__name__]) :
        if s[0] == args['function'] :
            print '*********************************'
            print 'RUN %s' %( args['function'] )
            print '*********************************'
            s[1]( alg_list, args )



    #make_nominal_unblind( alg_list, args, blind_pt=None )

    #make_nominal_unblind_noEleVeto( alg_list, args, blind_pt=None )

    #make_nominal_unbzrej( alg_list, args )

    #make_final_mu( alg_list, args, blind_pt = None, loose=True )

    #make_final_el( alg_list, args, blind_pt = None )

    #make_looseID_noEleVeto( alg_list, args )

    #make_looseID_bothEleVeto( alg_list, args )
    
    #make_looseID_invEleVetoLead( alg_list, args )
    
    #make_looseID_invEleVetoSubl( alg_list, args )

    #make_wgjj( alg_list, args) 

    #make_zgjj( alg_list, args) 

def make_final_mu( alg_list, args ) :

    loose = args.get('loose', False )
    print 'loose = ', loose

    notrig = args.get('notrig', False )
    print 'notrig = ', notrig

    mtvar = args.get('mt_var', 'mt_lep_met')
    print 'mtvar = ', mtvar

    mtcut = args.get('mtcut', ' > 40')
    print 'mtcut = ', mtcut

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    if not loose :
        filter_photon.cut_ph_pt = ' > 15 '
    alg_list.append(filter_photon)

    if not loose :
        filter_muon = Filter( 'FilterMuon' )
        filter_muon.cut_mu_pt = ' > 10 '
        alg_list.append(filter_muon)

        filter_ele = Filter( 'FilterElectron' )
        filter_ele.cut_el_pt = ' > 10 '
        alg_list.append(filter_ele)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' == 2 '
    filter_event.cut_nMu = ' == 1 '
    filter_event.cut_nEl = ' == 0 '

    if not notrig :
        filter_event.cut_nMuTrig = ' > 0 '

    filter_event.cut_dr_lep_ph1 = ' > 0.4 '
    filter_event.cut_dr_lep_ph2 = ' > 0.4 '
    filter_event.cut_dr_ph1_ph2 = ' > 0.4 '

    if not loose :
        # remove diphoton mass cut
        #filter_event.cut_mgg = ' > 15 '
        setattr( filter_event, 'cut_%s' %mtvar, mtcut )

    alg_list.append( filter_event )

    blind_pt = args.get('blind_pt', None )
    if blind_pt == 'None' :
        blind_pt = None

    if blind_pt is not None :
        isData = args.pop('isData', 'False')
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_ph_pt_lead = ' < %d ' %int(blind_pt)
        filter_blind.add_var( 'isData', isData )
        alg_list.append(filter_blind)


def make_final_el( alg_list, args ) :

    loose = args.get('loose', False )
    print 'loose = ', loose

    nozmass = args.get('nozmass', False )
    print 'nozmass = ', nozmass

    zmasscr = args.get('zmasscr', False )
    print 'zmasscr = ', zmasscr

    notrig = args.get('notrig', False )
    print 'notrig = ', notrig

    invpixlead = args.get('invpixlead', False )
    print 'invpixlead = ', invpixlead

    invpixsubl = args.get('invpixsubl', False )
    print 'invpixsubl = ', invpixsubl

    mtvar = args.get('mt_var', 'mt_lep_met')
    print 'mtvar = ', mtvar

    mtcut = args.get('mtcut', ' > 40')
    print 'mtcut = ', mtcut

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    if not loose :
        filter_photon.cut_ph_pt = ' > 15 '

    alg_list.append(filter_photon)

    if not loose :
        filter_muon = Filter( 'FilterMuon' )
        filter_muon.cut_mu_pt = ' > 10 '
        alg_list.append(filter_muon)
    
        filter_ele = Filter( 'FilterElectron' )
        filter_ele.cut_el_pt = ' > 10 '
        alg_list.append(filter_ele)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' == 2 '
    filter_event.cut_nEl = ' == 1 '
    filter_event.cut_nMu = ' == 0 '

    if not notrig :
        filter_event.cut_nElTrig = ' > 0 '

    if invpixlead :
        filter_event.cut_hasPixSeed_leadph12 = ' == True '
    else :
        filter_event.cut_hasPixSeed_leadph12 = ' == False '
    if invpixsubl :
        filter_event.cut_hasPixSeed_sublph12 = ' == True '
    else :
        filter_event.cut_hasPixSeed_sublph12 = ' == False '

    filter_event.cut_dr_lep_ph1 = ' > 0.4 '
    filter_event.cut_dr_lep_ph2 = ' > 0.4 '
    filter_event.cut_dr_ph1_ph2 = ' > 0.4 '

    if not loose :
        setattr( filter_event, 'cut_%s' %mtvar, mtcut )
        # remove mgg Cut
        #filter_event.cut_mgg = ' > 15 '
        if not nozmass :
            if zmasscr :
                filter_event.cut_m_lepphph= ' > 86.2 & < 96.2  '
            else :
                filter_event.cut_m_lepphph= ' > 86.2 & < 96.2  '
                filter_event.cut_m_lepph1= ' > 86.2 & < 96.2  '
                filter_event.cut_m_lepph2= ' > 86.2 & < 96.2  '
                filter_event.invert( 'cut_m_lepphph' )
                filter_event.invert( 'cut_m_lepph1' )
                filter_event.invert( 'cut_m_lepph2' )



    alg_list.append( filter_event )

    blind_pt = args.get('blind_pt', None )
    if blind_pt == 'None' :
        blind_pt = None

    print 'BLIND PT  = ', blind_pt

    if blind_pt is not None :
        isData = args.pop('isData', 'False')
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_ph_pt_lead = ' < %d ' %int(blind_pt)
        filter_blind.add_var( 'isData', isData )
        alg_list.append(filter_blind)


def make_nominal_unblind( alg_list, args ) :
    
    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '

    filter_event.cut_hasPixSeed_leadph12 = ' == False '
    filter_event.cut_hasPixSeed_sublph12 = ' == False '

    alg_list.append( filter_event )

    blind_pt = args.get('blind_pt', None )
    if blind_pt == 'None' :
        blind_pt = None

    if blind_pt is not None :
        isData = args.pop('isData', 'False')
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_ph_pt_lead = ' < %d ' %int(blind_pt)
        filter_blind.add_var( 'isData', isData )
        alg_list.append(filter_blind)

def make_nominal_unblind_noEleVeto( alg_list, args ) :
    
    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '

    alg_list.append( filter_event )

    blind_pt = args.get('blind_pt', None )
    if blind_pt == 'None' :
        blind_pt = None

    if blind_pt is not None :
        isData = args.pop('isData', 'False')
        filter_blind = Filter( 'FilterBlind' )
        filter_blind.cut_ph_pt_lead = ' < %d ' %int(blind_pt)
        filter_blind.add_var( 'isData', isData )
        alg_list.append(filter_blind)

def make_nominal_unbzrej( alg_list, args ) :

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '

    filter_event.cut_hasPixSeed_leadph12 = ' == False '
    filter_event.cut_hasPixSeed_sublph12 = ' == False '

    alg_list.append( filter_event )

    isData = args.pop('isData', 'False')
    filter_blind = Filter( 'FilterBlind' )
    filter_blind.add_var( 'isData', isData )
    filter_blind.cut_m_lepphph= ' > 86.2 & < 96.2  '
    filter_blind.cut_m_lepph1= ' > 86.2 & < 96.2  '
    filter_blind.cut_m_lepph2= ' > 86.2 & < 96.2  '
    alg_list.append(filter_blind)

def make_looseID_noEleVeto( alg_list, args ) :

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_mediumNoSIEIE = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '

    alg_list.append( filter_event )


def make_looseID_bothEleVeto( alg_list, args ) :

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_mediumNoSIEIE = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '
    filter_event.cut_hasPixSeed_leadph12 = ' == False '
    filter_event.cut_hasPixSeed_sublph12 = ' == False '

    alg_list.append( filter_event )


def make_looseID_invEleVetoSubl( alg_list, args ) :

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_mediumNoSIEIE = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '
    filter_event.cut_hasPixSeed_leadph12 = ' == False '
    filter_event.cut_hasPixSeed_sublph12 = ' == True '

    alg_list.append( filter_event )

def make_looseID_invEleVetoLead( alg_list, args ) :

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_mediumNoSIEIE = ' == True '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' > 1 '
    filter_event.cut_hasPixSeed_leadph12 = ' == True '
    filter_event.cut_hasPixSeed_sublph12 = ' == False '

    alg_list.append( filter_event )

def make_final_mumu( alg_list, args ) :

    invpixlead = args.get('invpixlead', False )
    print 'invpixlead = ', invpixlead

    invpixsubl = args.get('invpixsubl', False )
    print 'invpixsubl = ', invpixsubl

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    filter_photon.cut_ph_pt = ' > 15 '
    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_ele = Filter( 'FilterElectron' )
    filter_ele.cut_el_pt = ' > 10 '
    alg_list.append(filter_ele)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' == 2 '
    filter_event.cut_nMu = ' == 2 '
    filter_event.cut_nEl = ' == 0 '

    filter_event.cut_dr_lep_ph1 = ' > 0.4 '
    filter_event.cut_dr_lep_ph2 = ' > 0.4 '
    filter_event.cut_dr_subllep_ph1 = ' > 0.4 '
    filter_event.cut_dr_subllep_ph2 = ' > 0.4 '
    filter_event.cut_dr_ph1_ph2 = ' > 0.4 '

    filter_event.cut_m_leplep = ' > 40 '

    #if invpixlead :
    #    filter_event.cut_hasPixSeed_leadph12 = ' == True '
    #else :
    #    filter_event.cut_hasPixSeed_leadph12 = ' == False '
    #if invpixsubl :
    #    filter_event.cut_hasPixSeed_sublph12 = ' == True '
    #else :
    #    filter_event.cut_hasPixSeed_sublph12 = ' == False '

    alg_list.append( filter_event )

def make_final_elel( alg_list, args ) :

    invpixlead = args.get('invpixlead', False )
    print 'invpixlead = ', invpixlead

    invpixsubl = args.get('invpixsubl', False )
    print 'invpixsubl = ', invpixsubl

    filter_photon = Filter( 'FilterPhoton' )
    filter_photon.cut_ph_medium = ' == True '
    filter_photon.cut_ph_pt = ' > 15 '

    alg_list.append(filter_photon)

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)
    
    filter_ele = Filter( 'FilterElectron' )
    filter_ele.cut_el_pt = ' > 10 '
    alg_list.append(filter_ele)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' == 2 '
    filter_event.cut_nEl = ' == 2 '
    filter_event.cut_nMu = ' == 0 '

    filter_event.cut_dr_lep_ph1 = ' > 0.4 '
    filter_event.cut_dr_lep_ph2 = ' > 0.4 '
    filter_event.cut_dr_subllep_ph1 = ' > 0.4 '
    filter_event.cut_dr_subllep_ph2 = ' > 0.4 '
    filter_event.cut_dr_ph1_ph2 = ' > 0.4 '

    filter_event.cut_m_leplep = ' > 40 '

    #if invpixlead :
    #    filter_event.cut_hasPixSeed_leadph12 = ' == True '
    #else :
    #    filter_event.cut_hasPixSeed_leadph12 = ' == False '
    #if invpixsubl :
    #    filter_event.cut_hasPixSeed_sublph12 = ' == True '
    #else :
    #    filter_event.cut_hasPixSeed_sublph12 = ' == False '

    alg_list.append( filter_event )


def make_wgjj( alg_list, args ) :

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_jet = Filter( 'FilterJet' )
    filter_jet.cut_jet_pt = ' > 30 '
    alg_list.append(filter_jet)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' == 1 '
    filter_event.cut_nLepTrig = ' > 0 '
    filter_event.cut_nLep = ' == 1 '
    filter_event.cut_nJet30 = ' > 1 '
    filter_event.cut_nJet40 = ' > 0 '

    filter_event.cut_mt_lep_met = ' > 30 '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'CalcDiJetVars' ) )

def make_zgjj( alg_list, args ) :

    filter_muon = Filter( 'FilterMuon' )
    filter_muon.cut_mu_pt = ' > 10 '
    alg_list.append(filter_muon)

    filter_jet = Filter( 'FilterJet' )
    filter_jet.cut_jet_pt = ' > 30 '
    alg_list.append(filter_jet)

    filter_event = Filter('FilterEvent')
    filter_event.cut_nPh = ' == 1 '
    filter_event.cut_nLepTrig = ' > 0 '
    filter_event.cut_nLep = ' == 2 '
    filter_event.cut_nJet30 = ' > 1 '

    alg_list.append( filter_event )

    alg_list.append( Filter( 'CalcDiJetVars' ) )
