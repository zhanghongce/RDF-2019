This binary is used for resolve two following tasks.
	(1) Lef/Def Checker : Check whether input Lef/Def is fine for performing following routing stage. If not, then refine the Lef/Def file.
	(2) Generate GR Input : Global router input file follow the format in ISPD'08 contest. The binary will generate the input format from input LEF/DEF file.

My Test Command : ./gr_benchmark_parser -lef ../testcase/final.lef -def ../testcase/cordic_ispd.def -layer 9 -lef_out ../testcase/gr_benchmark_parser_output/revised_lef.lef -def_out ../testcase/gr_benchmark_parser_output/revised_def.def -gr_out ../testcase/gr_benchmark_parser_output/cordic_ispd.gr
