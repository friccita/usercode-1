#ifndef RUNANALYSIS_H
#define RUNANALYSIS_H
#include "../../../Analysis/TreeFilter/Core/Core/AnalysisBase.h"
#include <string>
#include <vector>
#include "TTree.h"
#include "TChain.h"
#include "TLorentzVector.h"
class RunModule : public virtual RunModuleBase {
    public :
        RunModule() {}
        void initialize( TChain * chain, TTree *outtree, TFile *outfile, const CmdOptions & options, std::vector<ModuleConfig> & configs) ;
        bool execute( std::vector<ModuleConfig> & config ) ;
        void finalize( ) ;
        void Drawm_lepph1 ( ) const;
        void Drawm_lepph1_0 ( ) const;
        void Drawm_lepph1_1 ( ) const;
        void Drawm_lepph1_2 ( ) const;
        void Drawm_lepph1_3 ( ) const;
        void Drawm_lepph1_4 ( ) const;
        void Drawm_lepph1_5 ( ) const;
        void Drawm_lepph1_6 ( ) const;
        void Drawm_lepph1_7 ( ) const;
        void Drawm_lepph1_8 ( ) const;
        void Drawm_lepph1_9 ( ) const;
        void Drawm_lepph1_10 ( ) const;
        void Drawm_lepph1_11 ( ) const;
        void Drawm_lepph1_12 ( ) const;
        void Drawm_lepph1_13 ( ) const;
        void Drawm_lepph1_14 ( ) const;
        void Drawm_lepph1_15 ( ) const;
        void Drawm_lepph1_16 ( ) const;
        void Drawm_lepph1_17 ( ) const;
        void Drawm_lepph1_18 ( ) const;
        void Drawm_lepph1_19 ( ) const;
        void Drawm_lepph1_20 ( ) const;
        void Drawm_lepph1_21 ( ) const;
        void Drawm_lepph1_22 ( ) const;
        void Drawm_lepph1_23 ( ) const;
        void Drawm_lepph1_24 ( ) const;
        void Drawm_lepph1_25 ( ) const;
        void Drawm_lepph1_26 ( ) const;
        void Drawm_lepph1_27 ( ) const;
        void Drawm_lepph1_28 ( ) const;
        void Drawm_lepph1_29 ( ) const;
        void Drawm_lepph1_30 ( ) const;
        void Drawm_lepph1_31 ( ) const;
        void Drawm_lepph1_32 ( ) const;
        void Drawm_lepph1_33 ( ) const;
        void Drawm_lepph1_34 ( ) const;
        void Drawm_lepph1_35 ( ) const;
        void Drawm_lepph1_36 ( ) const;
        void Drawm_lepph1_37 ( ) const;
        void Drawm_lepph1_38 ( ) const;
        void Drawm_lepph1_39 ( ) const;
        void Drawm_lepph1_40 ( ) const;
        void Drawm_lepph1_41 ( ) const;
        void Drawm_lepph1_42 ( ) const;
        void Drawm_lepph1_43 ( ) const;
        void Drawm_lepph1_44 ( ) const;
        void Drawm_lepph1_45 ( ) const;
        void Drawm_lepph1_46 ( ) const;
        void Drawm_lepph1_47 ( ) const;
        void Drawm_lepph1_48 ( ) const;
        void Drawm_lepph1_49 ( ) const;
        void Drawm_lepph1_50 ( ) const;
        void Drawm_lepph1_51 ( ) const;
        void Drawm_lepph1_52 ( ) const;
        void Drawm_lepph1_53 ( ) const;
        void Drawm_lepph1_54 ( ) const;
        void Drawm_lepph1_55 ( ) const;
        void Drawm_lepph1_56 ( ) const;
        void Drawm_lepph1_57 ( ) const;
        void Drawm_lepph1_58 ( ) const;
        void Drawm_lepph1_59 ( ) const;
        void Drawm_lepph1_60 ( ) const;
        void Drawm_lepph1_61 ( ) const;
        void Drawm_lepph1_62 ( ) const;
        void Drawm_lepph1_63 ( ) const;
        void Drawm_lepph1_64 ( ) const;
        void Drawm_lepph1_65 ( ) const;
        void Drawm_lepph1_66 ( ) const;
        void Drawm_lepph1_67 ( ) const;
        void Drawm_lepph1_68 ( ) const;
        void Drawm_lepph1_69 ( ) const;
        void Drawm_lepph1_70 ( ) const;
        void Drawm_lepph1_71 ( ) const;
        void Drawm_lepph1_72 ( ) const;
        void Drawm_lepph1_73 ( ) const;
        void Drawm_lepph1_74 ( ) const;
        void Drawm_lepph1_75 ( ) const;
        void Drawm_lepph1_76 ( ) const;
        void Drawm_lepph1_77 ( ) const;
        void Drawm_lepph1_78 ( ) const;
        void Drawm_lepph1_79 ( ) const;
        void Drawm_lepph1_80 ( ) const;
        void Drawm_lepph1_81 ( ) const;
        void Drawm_lepph1_82 ( ) const;
        void Drawm_lepph1_83 ( ) const;
        void Drawm_lepph1_84 ( ) const;
        void Drawm_lepph1_85 ( ) const;
        void Drawm_lepph1_86 ( ) const;
        void Drawm_lepph1_87 ( ) const;
        void Drawm_lepph1_88 ( ) const;
        void Drawm_lepph1_89 ( ) const;
        void Drawm_lepph1_90 ( ) const;
        void Drawm_lepph1_91 ( ) const;
        void Drawm_lepph1_92 ( ) const;
        void Drawm_lepph1_93 ( ) const;
        void Drawm_lepph1_94 ( ) const;
        void Drawm_lepph1_95 ( ) const;
        void Drawm_lepph1_96 ( ) const;
        void Drawm_lepph1_97 ( ) const;
        void Drawm_lepph1_98 ( ) const;
        void Drawm_lepph1_99 ( ) const;
        void Drawm_lepph1_100 ( ) const;
        void Drawm_lepph1_101 ( ) const;
        void Drawm_lepph1_102 ( ) const;
        void Drawm_lepph1_103 ( ) const;
        void Drawm_lepph1_104 ( ) const;
        void Drawm_lepph1_105 ( ) const;
        void Drawm_lepph1_106 ( ) const;
        void Drawm_lepph1_107 ( ) const;
        void Drawm_lepph1_108 ( ) const;
        void Drawm_lepph1_109 ( ) const;
        void Drawm_lepph1_110 ( ) const;
        void Drawm_lepph1_111 ( ) const;
        void Drawm_lepph1_112 ( ) const;
        void Drawm_lepph1_113 ( ) const;
        void Drawm_lepph1_114 ( ) const;
        void Drawm_lepph1_115 ( ) const;
        void Drawm_lepph1_116 ( ) const;
        TH1F * hist_m_lepph1; 
        TH1F * hist_m_lepph1_0; 
        TH1F * hist_m_lepph1_1; 
        TH1F * hist_m_lepph1_2; 
        TH1F * hist_m_lepph1_3; 
        TH1F * hist_m_lepph1_4; 
        TH1F * hist_m_lepph1_5; 
        TH1F * hist_m_lepph1_6; 
        TH1F * hist_m_lepph1_7; 
        TH1F * hist_m_lepph1_8; 
        TH1F * hist_m_lepph1_9; 
        TH1F * hist_m_lepph1_10; 
        TH1F * hist_m_lepph1_11; 
        TH1F * hist_m_lepph1_12; 
        TH1F * hist_m_lepph1_13; 
        TH1F * hist_m_lepph1_14; 
        TH1F * hist_m_lepph1_15; 
        TH1F * hist_m_lepph1_16; 
        TH1F * hist_m_lepph1_17; 
        TH1F * hist_m_lepph1_18; 
        TH1F * hist_m_lepph1_19; 
        TH1F * hist_m_lepph1_20; 
        TH1F * hist_m_lepph1_21; 
        TH1F * hist_m_lepph1_22; 
        TH1F * hist_m_lepph1_23; 
        TH1F * hist_m_lepph1_24; 
        TH1F * hist_m_lepph1_25; 
        TH1F * hist_m_lepph1_26; 
        TH1F * hist_m_lepph1_27; 
        TH1F * hist_m_lepph1_28; 
        TH1F * hist_m_lepph1_29; 
        TH1F * hist_m_lepph1_30; 
        TH1F * hist_m_lepph1_31; 
        TH1F * hist_m_lepph1_32; 
        TH1F * hist_m_lepph1_33; 
        TH1F * hist_m_lepph1_34; 
        TH1F * hist_m_lepph1_35; 
        TH1F * hist_m_lepph1_36; 
        TH1F * hist_m_lepph1_37; 
        TH1F * hist_m_lepph1_38; 
        TH1F * hist_m_lepph1_39; 
        TH1F * hist_m_lepph1_40; 
        TH1F * hist_m_lepph1_41; 
        TH1F * hist_m_lepph1_42; 
        TH1F * hist_m_lepph1_43; 
        TH1F * hist_m_lepph1_44; 
        TH1F * hist_m_lepph1_45; 
        TH1F * hist_m_lepph1_46; 
        TH1F * hist_m_lepph1_47; 
        TH1F * hist_m_lepph1_48; 
        TH1F * hist_m_lepph1_49; 
        TH1F * hist_m_lepph1_50; 
        TH1F * hist_m_lepph1_51; 
        TH1F * hist_m_lepph1_52; 
        TH1F * hist_m_lepph1_53; 
        TH1F * hist_m_lepph1_54; 
        TH1F * hist_m_lepph1_55; 
        TH1F * hist_m_lepph1_56; 
        TH1F * hist_m_lepph1_57; 
        TH1F * hist_m_lepph1_58; 
        TH1F * hist_m_lepph1_59; 
        TH1F * hist_m_lepph1_60; 
        TH1F * hist_m_lepph1_61; 
        TH1F * hist_m_lepph1_62; 
        TH1F * hist_m_lepph1_63; 
        TH1F * hist_m_lepph1_64; 
        TH1F * hist_m_lepph1_65; 
        TH1F * hist_m_lepph1_66; 
        TH1F * hist_m_lepph1_67; 
        TH1F * hist_m_lepph1_68; 
        TH1F * hist_m_lepph1_69; 
        TH1F * hist_m_lepph1_70; 
        TH1F * hist_m_lepph1_71; 
        TH1F * hist_m_lepph1_72; 
        TH1F * hist_m_lepph1_73; 
        TH1F * hist_m_lepph1_74; 
        TH1F * hist_m_lepph1_75; 
        TH1F * hist_m_lepph1_76; 
        TH1F * hist_m_lepph1_77; 
        TH1F * hist_m_lepph1_78; 
        TH1F * hist_m_lepph1_79; 
        TH1F * hist_m_lepph1_80; 
        TH1F * hist_m_lepph1_81; 
        TH1F * hist_m_lepph1_82; 
        TH1F * hist_m_lepph1_83; 
        TH1F * hist_m_lepph1_84; 
        TH1F * hist_m_lepph1_85; 
        TH1F * hist_m_lepph1_86; 
        TH1F * hist_m_lepph1_87; 
        TH1F * hist_m_lepph1_88; 
        TH1F * hist_m_lepph1_89; 
        TH1F * hist_m_lepph1_90; 
        TH1F * hist_m_lepph1_91; 
        TH1F * hist_m_lepph1_92; 
        TH1F * hist_m_lepph1_93; 
        TH1F * hist_m_lepph1_94; 
        TH1F * hist_m_lepph1_95; 
        TH1F * hist_m_lepph1_96; 
        TH1F * hist_m_lepph1_97; 
        TH1F * hist_m_lepph1_98; 
        TH1F * hist_m_lepph1_99; 
        TH1F * hist_m_lepph1_100; 
        TH1F * hist_m_lepph1_101; 
        TH1F * hist_m_lepph1_102; 
        TH1F * hist_m_lepph1_103; 
        TH1F * hist_m_lepph1_104; 
        TH1F * hist_m_lepph1_105; 
        TH1F * hist_m_lepph1_106; 
        TH1F * hist_m_lepph1_107; 
        TH1F * hist_m_lepph1_108; 
        TH1F * hist_m_lepph1_109; 
        TH1F * hist_m_lepph1_110; 
        TH1F * hist_m_lepph1_111; 
        TH1F * hist_m_lepph1_112; 
        TH1F * hist_m_lepph1_113; 
        TH1F * hist_m_lepph1_114; 
        TH1F * hist_m_lepph1_115; 
        TH1F * hist_m_lepph1_116; 
            TFile * f;
 };
namespace OUT {
};
#endif
