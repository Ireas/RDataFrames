#!/usr/bin/env python

import ROOT
import os
import sys
import logging

# Enable logging
logging.basicConfig(format="{levelname:<8s} {message}", style='{', level=logging.INFO)
logger = logging.getLogger(__name__)

# Enable implicit Multi-threading
ROOT.EnableImplicitMT()
ROOT.gROOT.SetBatch(True)
ROOT.gErrorIgnoreLevel = ROOT.kWarning

# File names
folder = '<CHANGE ME!!!>'
files = [
    'user.ravinab.35392295._000002.output.root',
]

file_paths = [os.path.join(folder, file) for file in files]

# Tree names
logger.info("Initialising TChains")
reco_tree_name = 'reco'
truth_tree_name = 'truth'

# Index columns
major_key = 'mcChannelNumber'
minor_key = 'eventNumber'

# Build TChains
reco_chain = ROOT.TChain(reco_tree_name)
truth_chain = ROOT.TChain(truth_tree_name)

print("Adding files to TChains:")
for path in file_paths:
    print(f"  - {path}")
    if not (os.path.isfile(path)):
        logger.error(f"Could not find '{path}'!")
        sys.exit(1)

    reco_chain.Add(path)
    truth_chain.Add(path)

# Index truth chain and and assign it as a friend to the reco chain
# We need both the DSID and the event number to have a fully unique identifier
logger.info(f"{truth_tree_name} wants to be {reco_tree_name}'s friend via [{major_key}, {minor_key}]")
truth_chain.BuildIndex(major_key, minor_key)
reco_chain.AddFriend(truth_chain)

# Now build a RDataFrame and do stuff with it :)
logger.info("Building RDataFrame for fun and profit")
df = ROOT.RDataFrame(reco_chain)

# Generate W-mass in GeV
df = df.Define("Tth_MC_Higgs_decay1_m_gev", "Tth_MC_Higgs_decay1_m / 1000.0")

# Filter by Higgs decay - adjust to what you want to do here...
all_count = df.Count().GetValue()
# Use minimal conditions in the filter: decay1 pdgId == +/- 24, and decay1 and decay2 pdgIds are equal and opposite
df = df.Filter("(abs(Tth_MC_Higgs_decay1_pdgId) == 24) && ((Tth_MC_Higgs_decay1_pdgId + Tth_MC_Higgs_decay2_pdgId) == 0)")
hww_count = df.Count().GetValue()

print(f"All reco events:        {all_count:>9d}")
print(f"Only H->WW reco events: {hww_count:>9d}")

# Print a table of W-masses
# TODO: Here, you guys would instead perform the truth-reco matching and figure out which jets do what :D

c = ROOT.TCanvas("c", "", 800, 600)
h = df.Histo1D(ROOT.RDF.TH1DModel("w1mass", "", 50, 0.0, 100.0), "Tth_MC_Higgs_decay1_m_gev")
#h = df.Histo1D("Tth_MC_Higgs_decay1_m_gev")
h.Draw()
h.GetXaxis().SetTitle("W_{1} mass [GeV]")
h.GetYaxis().SetTitle("# Events [-]")
h.SetStats(0)
c.Update()
c.SaveAs("w1_mass.pdf")
