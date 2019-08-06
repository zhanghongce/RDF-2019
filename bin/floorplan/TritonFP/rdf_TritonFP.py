'''
    File name      : run.py
    Author         : Jinwook Jung
    Created on     : Fri 26 Jul 2019 12:08:12 AM EDT
    Last modified  : 2019-07-30 22:31:27
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError

def run_shell_cmd(cmd, f=None):
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)

    for line in iter(p.stdout.readline, b''):
        print(">>> {}".format(line.rstrip().decode("utf-8")))

        # FIXME
        if f is not None:
            f.write("{}\n".format(str(line.rstrip())))


def run(config, job_dir, prev_out_dir, user_parms):
    print("Running TritonFP...")
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    triton_fp = TritonFPRunner(config, job_dir, prev_out_dir, user_parms)
    triton_fp.run()

    print("Done.")
    print("")


class TritonFPRunner(object):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        ''' Initialize the instance and populate the necessary/useful
        variables. '''
        self.config = config
        self.job_dir = job_dir
        self.prev_out_dir = prev_out_dir

        self.rdf_path = config["rdf_path"]
        self.design_name = config["design"]["name"]

        self.verilog = "{}/{}.v".format(prev_out_dir, self.design_name)

        self.lib_name = config["design"]["library"]
        self.lib_dir = "{0}/libraries/{1}".format(self.rdf_path, self.lib_name)
        self.liberty = "{0}/libraries/{1}/{1}.lib" \
                       .format(self.rdf_path, config["design"]["library"])
        self.lef = "{0}/libraries/{1}/{1}.lef" \
                       .format(self.rdf_path, config["design"]["library"])

        self.lib_config = None

        lib_config_yml = "{0}/libraries/{1}/{1}.yml" \
                         .format(self.rdf_path, self.lib_name)
        with open(lib_config_yml) as f:
            self.lib_config = yaml.safe_load(f)

        self.tracks = "{0}/libraries/{1}/{2}" \
                       .format(self.rdf_path, config["design"]["library"], self.lib_config["TRACKS_INFO_FILE"])

#        print("(FIXME) Getting total area...")
#        design_name = config["design"]["name"]
#        with open("{}/{}.log".format(prev_out_dir, design_name)) as f:
#            lines = [l for l in (_.strip() for _ in f) if l]
#
#        area = -1
#        for l in lines:
#            tokens = l.split()
#            if tokens[0] == "TOTAL":
#                area = tokens[6]


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
        cmd += " -verilog {}".format(self.verilog)
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

