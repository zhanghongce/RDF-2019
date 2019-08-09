'''
    File name      : run_TritonFP.py
    Author         : Jinwook Jung
    Created on     : Fri 26 Jul 2019 12:08:12 AM EDT
    Last modified  : 2019-08-08 21:31:16
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms):
    print("-"*79)
    print("Running TritonFP...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    triton_fp = TritonFPRunner(config, job_dir, prev_out_dir, user_parms)
    triton_fp.run()

    print("Done.")
    print("")


class TritonFPRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

    def run(self):
        print("Hello TritonFP...")

        print("Running Verilog to DEF conversion...")
        self._run_verilog_to_def()

        print("Running IO Placement...")
        self._run_io_placement()

        print("Running Macro Placement...")
        self._run_macro_placement()

        print("Running Tapcell Placement...")
        self._run_tapcell_placement()

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

    def _run_verilog_to_def(self):
        cmd = "{}/bin/floorplan/TritonFP/verilog2def".format(self.rdf_path)
        cmd += " -lef {}".format(self.lef)
        cmd += " -liberty {}".format(self.liberty)
        cmd += " -verilog {}".format(self.in_verilog)
        cmd += " -top_module {}".format(self.design_name)
        cmd += " -units {}".format(self.lib_config["VERILOG2DEF_DBU"])
        cmd += " -site {}".format(self.lib_config["PLACE_SITE"])
        cmd += " -utilization {}".format(self.config["design"]["target_utilization"])
        cmd += " -tracks {}".format(self.tracks)
        cmd += " -core_space {}".format(self.lib_config["CORE_SPACE"])
        cmd += " -def {}/{}".format(self.job_dir, "init.def")

        print("\n$ {}\n".format(cmd))

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

    def _run_io_placement(self):
        cmd = "{}/bin/floorplan/TritonFP/ioPlacer".format(self.rdf_path)
        cmd += " --input-lef {}".format(self.lef)
        cmd += " --input-def {}/{}".format(self.job_dir, "init.def")
        cmd += " --output {}/out/{}.def".format(self.job_dir, self.design_name)
        cmd += " --hmetal {}".format(self.lib_config["IO_PLACER_HMETAL"])
        cmd += " --vmetal {}".format(self.lib_config["IO_PLACER_VMETAL"])
        cmd += " --force-spread 1"
        cmd += " --random 1"
        cmd += " --wirelen 1"

        print("\n$ {}\n".format(cmd))

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

    def _run_macro_placement(self):
        pass

    def _apply_pdn(self):
        pass

    def _run_tapcell_placement(self):
        cmd = "{}/bin/floorplan/TritonFP/tapcell".format(self.rdf_path)
        cmd += " -lef {}".format("")
        cmd += " -def {}".format("")
        cmd += " -rule {}".format("")
        cmd += " -welltap {}".format("")
        cmd += " -endcap {}".format("")
        cmd += " -rows"
        cmd += " -outdef {}".format("")

        print("\n$ {}\n".format(cmd))

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

