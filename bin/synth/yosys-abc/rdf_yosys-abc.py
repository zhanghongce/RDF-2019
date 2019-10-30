'''
    File name      : rdf_yosys-abc.py
    Author         : Jinwook Jung
    Created on     : Sun 28 Jul 2019 12:08:12 AM EDT
    Last modified  : 2019-10-30 17:37:36
    Description    :
'''

import subprocess, os, sys, random, yaml, time

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms, write_run_scripts=False):
    """ Run the point tool and store the outputs at the out directory."""
    print("-"*79)
    print("Running Yosys-ABC...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))
    print("")

    yosys_runner = YosysRunner(config, job_dir, prev_out_dir, user_parms)

    if write_run_scripts:
        yosys_runner.write_run_scripts()
    else:
        yosys_runner.write_run_scripts()
        yosys_runner.run()

    print("Done.")
    print("")


class YosysRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        # Optimization parms
        if user_parms is None or len(user_parms) == 0:
            self.script = 'resyn2rs'
            self.map = 'map -p'
            self.max_fanout = 8

        # FIXME
        try:
            self.script = user_parms["script"]
            self.map = user_parms["map"]
            self.max_fanout = user_parms["max_fanout"]
        except KeyError:
            self.script = 'resyn2rs'
            self.map = 'map -p'
            self.max_fanout = 8

    def write_run_scripts(self):
        self._write_abc_script_txt()

        self._write_synth_tcl()

        yosys_bin = "{}/bin/synth/yosys-abc/yosys".format(self.rdf_path)
        cmd = "cd {}; {} -c synth.tcl".format(self.job_dir, yosys_bin)

        with open("{}/run.sh".format(self.job_dir), 'w') as f:
            f.write("cd {}\n".format(self.job_dir))
            f.write("{} -c synth.tcl".format(yosys_bin))

    def run(self):
        self._write_abc_script_txt()

        self._write_synth_tcl()

        yosys_bin = "{}/bin/synth/yosys-abc/yosys".format(self.rdf_path)
        cmd = "cd {}; {} -c synth.tcl".format(self.job_dir, yosys_bin)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'w') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _write_abc_script_txt(self):
        with open("{}/abc_script.txt".format(self.job_dir), 'w') as f:
            f.write("map\n")
            f.write("\n")
            f.write("source {}/bin/synth/yosys-abc/abc.rc\n".format(self.rdf_path))
            f.write("\n")
            f.write("unmap\n")

            # Start synthesis
            f.write("{}\n".format(self.script))
            f.write("{}\n".format(self.map))
            f.write("cleanup\n")
            f.write("echo \"{}:{}***print_status\"\n".format(self.map, self.script))
            f.write("print_status\n")

            f.write("echo Buffering...\n")
            f.write("dnsize\n")
            f.write("buffer -p -N {} -v\n".format(self.max_fanout))
            f.write("upsize\n")
            f.write("\n")
            f.write("echo \"buffer:{}***print_status\"\n".format(self.script))
            f.write("print_status\n")
            f.write("\n")
            f.write("echo \"***print_stats\"\n")
            f.write("print_stats\n")
            f.write("\n")
            f.write("echo \"***print_latch\"\n")
            f.write("print_latch;\n")
            f.write("\n")
            f.write("echo \"***print_gates\"\n")
            f.write("print_gates;\n")
            f.write("\n")
            f.write("echo \"***print_fanio\"\n")
            f.write("print_fanio\n")

    def _write_synth_tcl(self):
        with open("{}/synth.tcl".format(self.job_dir), 'w') as f:
            f.write("yosys -import\n\n")

            f.write("# Read verilog files...\n")
            for _ in self.design_verilogs:
                f.write("read_verilog {}\n".format(_))
            f.write("\n")

            f.write("# Generic synthesis\n")
            f.write("synth -top {} -flatten\n".format(self.design_name))
            f.write("opt_clean -purge\n")
            f.write("\n")

            f.write("# Registers mapping\n")
            f.write("dfflibmap -liberty {}\n".format(self.liberty))
            f.write("\n")

            # TODO: Support SDC
            f.write("# ABC\n")
            f.write("abc -liberty {} -script abc_script.txt\n".format(self.liberty))
            f.write("\n")

            # Remove assign statements
            tiehi_cell = self.lib_config["TIEHI_CELL_AND_PORT"][0]
            tiehi_port = self.lib_config["TIEHI_CELL_AND_PORT"][1]
            tielo_cell = self.lib_config["TIELO_CELL_AND_PORT"][0]
            tielo_port = self.lib_config["TIELO_CELL_AND_PORT"][1]

            f.write("splitnets -ports; opt\n")
            f.write("hilomap -hicell {{*}}{} {} -locell {{*}}{} {}\n" \
                    .format(tiehi_cell, tiehi_port, tiehi_cell, tiehi_port))
            f.write("\n")

            f.write("opt_clean -purge\n")
            f.write("\n")

            # Cleanup
            f.write("clean\n")
            f.write("opt_clean -purge\n")
            f.write("\n")

            # reports
            f.write("tee -o synth_check.txt check\n")
            f.write("tee -o synth_stat.txt stat -liberty {}\n".format(self.liberty))
            f.write("\n")

            # write synthesized design
            f.write("write_verilog -noattr -noexpr -nohex -nodec out/{}.v".format(self.design_name))

