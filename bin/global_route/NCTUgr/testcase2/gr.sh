./gr_benchmark_parser -lef ./nangate45.lef -def ./ac97_ctrl.def -layer 10 -lef_out test.lef -def_out test.def -gr_out test.gr 
./NCTUgr REGULAR_ISPD ./test.gr ./Parameter_Files/RegularHighQuality.set nctugr.guide
./routing_guide_checker -lef ./nangate45.lef -def ./ac97_ctrl.def -guide nctugr.guide -layer 10 -guide_out final.guide
./dr_cu -lef ./nangate45.lef -def ./ac97_ctrl.def -threads 8 -guide final.guide -output dr_cu.def
