'''
    File name      : rdf_ComPLx.py
    Author         : Jinwook Jung
    Created on     : Tue 13 Aug 2019 11:52:53 PM EDT
    Last modified  : 2019-08-14 00:09:09
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

# FIXME
sys.path.insert(0, '../../../src/stage.py')
from stage import *


def run(config, job_dir, prev_out_dir, user_parms):
    print("-"*79)
    print("Running ComPLx...")
    print("-"*79)
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    complx = ComPLxRunner(config, job_dir, prev_out_dir, user_parms)
    complx.run()

    print("Done.")
    print("")


class ComPLxRunner(Stage):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        super().__init__(config, job_dir, prev_out_dir, user_parms)

        self.lef_mod = "{}/merged_padded_spacing.lef".format(self.lib_dir)

        # FIXME
        self.bookshelf = "out.aux"

    def run(self):
        print("Hello ComPLx...")

        self._write_bookshelf()

        self._run_complx()

        self._write_def()

        self._copy_final_output()

    def _write_bookshelf(self):
        cmd = "cd {} && {}/bin/global_place/ComPLx/bookshelf_writer".format(self.job_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef)
        cmd += " --def {}".format(self.in_def)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _run_complx(self):
        cmd = "cd {} && {}/bin/global_place/ComPLx/ComPLx.exe".format(self.job_dir, self.rdf_path)
        cmd += " -f {}".format(self.bookshelf)
        if "target_density" in self.user_parms.keys():
            cmd += " -ut {}".format(float(self.user_parms["target_density"]))

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _write_def(self):
        cmd = "cd {} && {}/bin/global_place/ComPLx/place_updater".format(self.job_dir, self.rdf_path)
        cmd += " --lef {}".format(self.lef)
        cmd += " --def {}".format(self.in_def)
        cmd += " --pl {}/out-ComPLx.pl".format(self.job_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            f.write("\n")
            f.write("# Command: {}\n".format(cmd))
            f.write("\n")
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        cmd = "ln -s {0}/out.def {0}/out/{1}.def" \
              .format(self.job_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

