#!/bin/bash

if test "$#" -ne 9; then
    echo "$0: error - wrong number of arguments : $# instead of 9"
    echo "usage: $0 <abc_bin> <abc_rc> <output> \ "
    echo "          <input_blif> \ "
    echo "          <abc script name> <abc map command> <max_fanout> \ "
    echo "          <output_verilog>"
    exit
fi

abc_bin=$1
abc_rc=$2
output=$3
input_lib=$4
input_blif=$5
abc_script=$6
map=$7
max_fanout=$8
output_verilog=$9

$abc_bin -o $output -c "
source $abc_rc;
echo Reading library $input_lib ***;
read $input_lib;
echo Reading abstracted netlist $input_blif ***;
read $input_blif;
echo "print_stats"; print_stats;
echo "print_latch"; print_latch;
echo "print_gates"; print_gates;
echo "print_fanio"; print_fanio;
echo "print_delay"; print_delay;
unmap;
$abc_script;
$map;
cleanup;
echo -n "$map:$abc_script:"; print_stats;
echo Buffering ... ;
buffer -N $max_fanout -v;
echo -n "buffer:$abc_script:"; 
echo "print_stats"; print_stats;
echo "print_latch"; print_latch;
echo "print_gates"; print_gates;
echo "print_fanio"; print_fanio;
echo "print_delay"; print_delay;
echo Saving out $output_verilog ***;
write_verilog $output_verilog
"

