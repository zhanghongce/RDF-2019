'''
    File name      : rdf_OpenDP.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 10:31:18 PM EDT
    Last modified  : 2019-08-08 21:29:24
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms):
    print("-"*79)
    print("Running OpenDP...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    opendp = OpenDPRunner(config, job_dir, prev_out_dir, user_parms)
    opendp.run()

    print("Done.")
    print("")


class OpenDPRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

    def run(self):
        print("Hello OpenDP...")

        cmd = "{}/bin/detail_place/opendp/opendp".format(self.rdf_path)
        #cmd += " -lef {}".format(self.lef)
        cmd += " -lef {}".format(self.lef_mod)
        cmd += " -def {}".format(self.in_def)
        cmd += " -cpu 4"
        cmd += " -output_def {}/out/{}.def".format(self.job_dir, self.design_name)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

