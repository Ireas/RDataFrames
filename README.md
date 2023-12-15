(manually cloned from gitLab to gitHub)

# Truth Reco Matching

Just a very small skeleton to show off how we can harness `RDataFrame` in columnar analyses for great benefit.

Hopefully you guys agree that the fairly simple python script here might make things a bit simpler than running fully
in C++...

Currently, it simply uses a single file to build a truth and a reco TChain - similar to what you already did in C++.
Then, it uses the `mcChannelNumber` (basically the DSID) and `eventNumber` to match the two TChains via happy tree
friends (no, not that one!) to avoid the current loop necessary in the previous code.

By using RDataFrames, it should be fairly straightforward to define event filters (e.g. to only get H->WW decays),
check kinematic distributions (I already implemented a very simple example for each in the skeleton), or do more
complicated things such as truth-reco matching.

For that it might be necessary to inject some C++ code after all (sorry...). Details can be found in the
[RDataFrame reference guide](https://root.cern/doc/master/classROOT_1_1RDataFrame.html) (that one also describes the
friend tree method used to match up truth and reco trees somewhere fairly far down...).

Lastly, running natively in python via RDataFrames should also make it more straightforward to convert the data into
`.h5` for SPANet training, since RDataFrames natively support extraction of columns (= input variables) into other
python types.

Maybe give the code a try and give me a shout for any questions on this :)
