'''
    File name      : rdf_TritonRoute.py
    Author         : Jinwook Jung
    Created on     : Thu 08 Aug 2019 09:46:48 PM EDT
    Last modified  : 2019-08-08 21:46:48
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms, write_run_scripts=False):
    print("-"*79)
    print("Running TritonRoute...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    triton_route = TritonRouteRunner(config, job_dir, prev_out_dir, user_parms)
    triton_route.write_run_scripts()

    if not write_run_scripts:
        triton_route.run()

    print("Done.")
    print("")


class TritonRouteRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)
        self.in_guide = "{}/{}.guide".format(self.prev_out_dir, self.design_name)

    def write_run_scripts(self):
        self._write_parm_file()

        with open("{}/run.sh".format(self.job_dir), 'w') as f:
            cmd = "cd {};".format(self.job_dir)
            cmd += "{}/bin/detail_route/TritonRoute/TritonRoute".format(self.rdf_path)
            cmd += " triton_route.parm"

            f.write("{}\n".format(cmd))

    def run(self):
        print("Hello TritonRoute...")

        self._write_parm_file()

        self._run_triton_route()

        self._copy_final_output()

    def _write_parm_file(self):
        with open("{}/triton_route.parm".format(self.job_dir), 'w') as f:
            f.write("lef:{}\n".format(self.lef_mod))
            f.write("def:{}\n".format(self.in_def))
            f.write("guide:{}\n".format(self.in_guide))
            f.write("output:tr.def\n")
            f.write("outputTA:test_TA.def\n")
            f.write("outputguide:output_guide.mod\n")
            f.write("outputMaze:maze.log\n")
            f.write("threads:32\n")
            f.write("cpxthreads:1\n")
            f.write("verbose:1\n")
            f.write("gap:0\n")
            f.write("timeout:36000\n")

    def _run_triton_route(self):
        cmd = "cd {};".format(self.job_dir)
        cmd += "{}/bin/detail_route/TritonRoute/TritonRoute".format(self.rdf_path)
        cmd += " triton_route.parm"

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        pass

