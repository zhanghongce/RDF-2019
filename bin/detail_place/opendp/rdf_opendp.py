'''
    File name      : rdf_OpenDP.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 10:31:18 PM EDT
    Last modified  : 2019-07-30 22:31:18
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
    print("Running OpenDP...")
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    opendp = OpenDPRunner(config, job_dir, prev_out_dir, user_parms)
    opendp.run()

    print("Done.")
    print("")


class OpenDPRunner(object):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        ''' Initialize the instance and populate the necessary/useful
        variables. '''
        self.config = config
        self.job_dir = job_dir
        self.prev_out_dir = prev_out_dir

        self.rdf_path = config["rdf_path"]
        self.design_name = config["design"]["name"]

        self.def_in = "{}/{}.def".format(prev_out_dir, self.design_name)

        self.lib_name = config["design"]["library"]
        self.lib_dir = "{0}/libraries/{1}".format(self.rdf_path, self.lib_name)
        self.liberty = "{0}/libraries/{1}/{1}.lib" \
                       .format(self.rdf_path, config["design"]["library"])
        self.lef = "{0}/libraries/{1}/{1}.lef" \
                       .format(self.rdf_path, config["design"]["library"])
        self.lef_mod = "{0}/libraries/{1}/merged_padded_spacing.lef" \
                       .format(self.rdf_path, config["design"]["library"])
        self.tracks = "{0}/libraries/{1}/tracks.info" \
                       .format(self.rdf_path, config["design"]["library"])

        self.lib_config = None

        lib_config_yml = "{0}/libraries/{1}/{1}.yml" \
                         .format(self.rdf_path, self.lib_name)
        with open(lib_config_yml) as f:
            self.lib_config = yaml.safe_load(f)


    def run(self):
        print("")
        print("Hello OpenDP...")

        cmd = "{}/bin/detail_place/opendp/opendp".format(self.rdf_path)
        cmd += " -lef {}".format(self.lef_mod)
        #cmd += " -lef {}".format(self.lef)
        cmd += " -def {}".format(self.def_in)
        cmd += " -cpu 4"
        cmd += " -output_def {}/out/{}.def".format(self.job_dir, self.design_name)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

