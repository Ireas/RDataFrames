import os
import sys
import logging
import ROOT



# ====================  Constants  =====================================
## folders and files within
FOLDER = '/home/ireas/git_repos/master/data/v1/user.ravinab.346343.PhPy8EG.DAOD_PHYS.e7148_s3681_r13144_p5855.20231104-v0_output/'
FILES = [
    'user.ravinab.35392295._000001.output.root',
]


## root tree and branch names
RECO_TREE_NAME = 'reco'
TRUTH_TREE_NAME = 'truth'
MAJOR_KEY = 'mcChannelNumber'
MINOR_KEY = 'eventNumber'



# ====================  C++ Function Declaration  ======================
ROOT.gSystem.Load("delta_r_matching.so")
ROOT.gInterpreter.Declare('#include "delta_r_matching.h"')



# ====================  Initialization  ================================
## prepare logging
logging.basicConfig(format="{levelname:<8s} {message}", style='{', level=logging.INFO)
logger = logging.getLogger(__name__)


## prepare root
#ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True) # use batch mode (no graphical UI available)
ROOT.gErrorIgnoreLevel = ROOT.kWarning # only show warnings or higher priority messanges


## get all files
file_paths = [os.path.join(FOLDER, file) for file in FILES]


## build TChains
logger.info("initialising TChains")
reco_chain = ROOT.TChain(RECO_TREE_NAME)
truth_chain = ROOT.TChain(TRUTH_TREE_NAME)

logger.info("adding files to TChains:")
for path in file_paths:
	logger.info(f"\t- {path}")
	if not (os.path.isfile(path)):
		logger.error(f"Could not find '{path}'!")
		sys.exit(1)
	reco_chain.Add(path)
	truth_chain.Add(path)


## index truth chain and and assign it as a friend to the reco chain. we need both the DSID and the event number to have a fully unique identifier
logger.info(f"{TRUTH_TREE_NAME} wants to be {RECO_TREE_NAME}'s friend via [{MAJOR_KEY}, {MINOR_KEY}]")
truth_chain.BuildIndex(MAJOR_KEY, MINOR_KEY)
reco_chain.AddFriend(truth_chain)



# ====================  RDataFrame  ====================================
## build RDataFrame
logger.info("building RDataFrame")
df = ROOT.RDataFrame(reco_chain)


## define and fill dataframe with W-mass in GeV
df = df.Range(10)
df = df.Define("Tth_MC_Higgs_decay1_m_gev", "Tth_MC_Higgs_decay1_m / 1000.0")
df = df.Define("test", "my_little_function(truth.Tth_MC_Higgs_decay1_m)")

df.Display("test").Print()


## get number of events
all_count = df.Count().GetValue()


## use minimal conditions in the filter: decay1 pdgId == +/- 24, and decay1 and decay2 pdgIds are equal and opposite
df = df.Filter("(abs(Tth_MC_Higgs_decay1_pdgId) == 24) && ((Tth_MC_Higgs_decay1_pdgId + Tth_MC_Higgs_decay2_pdgId) == 0)")

## count of filtered events
hww_count = df.Count().GetValue()



# ====================  Output  ========================================
## print event counts
print(f"All reco events:        {all_count:>9d}")
print(f"Only H->WW reco events: {hww_count:>9d}")


## produce .pdf table of W-mass
c = ROOT.TCanvas("c", "", 800, 600)
h = df.Histo1D(ROOT.RDF.TH1DModel("w1mass", "", 50, 0.0, 100.0), "Tth_MC_Higgs_decay1_m_gev")
h.Draw()
h.GetXaxis().SetTitle("W_{1} mass [GeV]")
h.GetYaxis().SetTitle("# Events [-]")
h.SetStats(0)
c.Update()
c.SaveAs("w1_mass.pdf")
