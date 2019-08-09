'''
    File name      : rdf_RePlAce.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 10:31:18 PM EDT
    Last modified  : 2019-08-08 21:39:33
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms):
    print("-"*79)
    print("Running RePlAce...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    replace = RePlAceRunner(config, job_dir, prev_out_dir, user_parms)
    replace.run()

    print("Done.")
    print("")


class RePlAceRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

    def run(self):
        print("Hello RePlAce...")

        cmd = "{}/bin/global_place/RePlAce/RePlAce".format(self.rdf_path)
        cmd += " -bmflag etc"
        # cmd += " -lef {}".format(self.lef)
        cmd += " -lef {}".format(self.lef_mod)
        cmd += " -def {}".format(self.in_def)
        cmd += " -onlyGP"
        cmd += " -output {}".format(self.job_dir)

        # FIXME: Check the existence of each user parm and its value range.
        if "target_density" in self.user_parms.keys():
            cmd += " -den {}".format(self.user_parms["target_density"])

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

        self._copy_final_output()

    def _copy_final_output(self):
        cmd = "ln -s {0}/etc/{1}/experiment000/{1}_final.def {0}/out/{1}.def" \
              .format(self.job_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

