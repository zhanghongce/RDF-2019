#!/bin/bash

# Input Lef
InputLef="./testcase/final.lef"
# Input Def
InputDef="./testcase/cordic_ispd.def"
# Number of Metal Layer
Layer="9"
# Refined Lef from gr_benchmark_parser
RefinedLef="./testcase/gr_benchmark_parser_output/revised_lef.lef"
# Refined Def from gr_benchmark_parser
RefinedDef="./testcase/gr_benchmark_parser_output/revised_def.def"
# Not only the output from gr_benchmark_parser, but also the input for NCTUgr
GR_input="./testcase/gr_benchmark_parser_output/cordic_ispd.gr"
#routing guide output from NCTUgr
Init_Guide="./testcase/gr_output/cordic_ispd.guide"
#final routing guide output from routing_guide_checker
Refined_Guide="./testcase/routing_guide_checker_output/cordic_ispd.guide"
#def file output from detailed router
Final_Def="./testcase/dr_output/final.def"


#------------------------------------------------------------------------------
# gr_benchmark_parser
#------------------------------------------------------------------------------
cmd1="./1.gr_benchmark_parser/gr_benchmark_parser -lef $InputLef -def $InputDef -layer $Layer -lef_out $RefinedLef -def_out $RefinedDef -gr_out $GR_input"
echo $cmd1; 
$cmd1
#------------------------------------------------------------------------------
# NCTUgr
#------------------------------------------------------------------------------
cmd2="./2.global_routing/NCTUgr REGULAR_ISPD $GR_input ./2.global_routing/Parameter_Files/RegularHighQuality.set $Init_Guide"
echo $cmd2; 
$cmd2
#------------------------------------------------------------------------------
# routing_guide_checker
#------------------------------------------------------------------------------
cmd3="./3.routing_guide_checker/routing_guide_checker -lef $RefinedLef -def $RefinedDef -guide $Init_Guide -layer $Layer -guide_out $Refined_Guide"
echo $cmd3; 
$cmd3
#------------------------------------------------------------------------------
# dr_cu or NCTUdr
#------------------------------------------------------------------------------
# Option for Detailed Router
RUN_NCTUdr="./4.detailed_routing/NCTUdr/NCTUdr -lef $RefinedLef -def $RefinedDef -guide $Refined_Guide -threads 1 -output $Final_Def"
RUN_dr_cu="./4.detailed_routing/dr_cu/dr_cu -lef $RefinedLef -def $RefinedDef -guide $Refined_Guide -threads 1 -output $Final_Def"
echo $RUN_dr_cu; 
$RUN_dr_cu
