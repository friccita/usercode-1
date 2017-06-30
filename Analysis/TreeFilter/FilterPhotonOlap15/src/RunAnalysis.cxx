#include "include/RunAnalysis.h"

#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <boost/foreach.hpp>
#include <boost/algorithm/string.hpp>
#include <sys/types.h>
#include <sys/stat.h>
#include <math.h>
#include <stdlib.h>

#include "include/BranchDefs.h"
#include "include/BranchInit.h"

#include "Core/Util.h"

#include "TFile.h"
#include "TLorentzVector.h"

int main(int argc, char **argv)
{

    //TH1::AddDirectory(kFALSE);
    CmdOptions options = ParseOptions( argc, argv );

    // Parse the text file and form the configuration object
    AnaConfig ana_config = ParseConfig( options.config_file, options );
    std::cout << "Configured " << ana_config.size() << " analysis modules " << std::endl;

    RunModule runmod;
    ana_config.Run(runmod, options);

    std::cout << "^_^ Finished ^_^" << std::endl;


}

void RunModule::initialize( TChain * chain, TTree * outtree, TFile *outfile,
                            const CmdOptions & options, std::vector<ModuleConfig> &configs ) {

    // *************************
    // initialize trees
    // *************************
    InitINTree(chain);
    InitOUTTree( outtree );
    
    // *************************
    // Set defaults for added output variables
    // *************************

    // *************************
    // Declare Branches
    // *************************

}

bool RunModule::execute( std::vector<ModuleConfig> & configs ) {

    // In BranchInit
    CopyInputVarsToOutput();

    // loop over configured modules
    bool save_event = true;
    BOOST_FOREACH( ModuleConfig & mod_conf, configs ) {
        save_event &= ApplyModule( mod_conf );
    }

    return save_event;

}

bool RunModule::ApplyModule( ModuleConfig & config ) const {

    // This bool is used for filtering
    // If a module implements an event filter
    // update this variable and return it
    // to apply the filter
    bool keep_evt = true;

    // Example :
    if( config.GetName() == "FilterPhoton" ) {
        keep_evt &= FilterPhoton( config );
    }
    if( config.GetName() == "FilterGenHT" ) {
        keep_evt &= FilterGenHT( config );
    }
    if( config.GetName() == "FilterMTRes" ) {
        keep_evt &= FilterMTRes( config );
    }

    return keep_evt;

}

// ***********************************
//  Define modules here
//  The modules can do basically anything
//  that you want, fill trees, fill plots, 
//  caclulate an event filter
// ***********************************
//

bool RunModule::FilterGenHT( ModuleConfig & config ) const {

    bool keep_event = true;

    if(!config.PassFloat( "cut_genht", OUT::GenHT ) ) keep_event = false;

    return keep_event;
}

bool RunModule::FilterMTRes( ModuleConfig & config ) const {

    bool keep_event = true;

    if(!config.PassFloat( "cut_mtres", OUT::mt_res ) ) keep_event = false;

    return keep_event;
}

bool RunModule::FilterPhoton( ModuleConfig & config ) const {

    bool keep_event = true;

    std::vector<TLorentzVector> gen_phot;
    for( unsigned i = 0; i < OUT::trueph_n ; ++i ) {

        float phot_pt = OUT::trueph_pt->at(i);
        float phot_eta = OUT::trueph_eta->at(i);
        float phot_phi = OUT::trueph_phi->at(i);

        if( !config.PassFloat( "cut_genph_pt", phot_pt ) ) continue;

        TLorentzVector phlv;
        phlv.SetPtEtaPhiM( phot_pt, phot_eta, phot_phi, 0.0 );

        gen_phot.push_back(phlv);

    }

    if( !config.PassInt( "cut_n_gen_phot", gen_phot.size() ) ) keep_event=false;

    return keep_event;
    
}

