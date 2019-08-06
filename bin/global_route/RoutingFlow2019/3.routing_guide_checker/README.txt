This binary is used for resolve following task.
	(1) Routing Guide Checker : Check whether input routing guide from global router is fine for performing following detailed routing stage. 
		If not, then refine the routing guide file.
	
My Test Command : ./routing_guide_checker -lef ../testcase/final.lef -def ../testcase/cordic_ispd.def -guide ../testcase/cordic_ispd.gui_out ../testcase/gr_bede -layer 9 -guide_out ../testcase/routing_guide_checker_output/cordic_ispd_refined.guide