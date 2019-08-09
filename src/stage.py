'''
    File name      : stage.py
    Author         : Jinwook Jung
    Created on     : Thu 25 Jul 2019 11:57:16 PM EDT
    Last modified  : 2019-08-08 21:33:31
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from subprocess import Popen, PIPE, CalledProcessError
from abc import ABC, abstractmethod


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


class Stage(ABC):
    def __init__(self, config, job_dir, prev_out_dir, user_parms):
        ''' Initialize the instance and populate the necessary/useful
        variables. '''
        self.config = config
        self.job_dir = job_dir
        self.prev_out_dir = prev_out_dir

        self.rdf_path = config["rdf_path"]
        self.design_name = config["design"]["name"]
        self.design = config["design"]

        # Output of previous stage
        self.in_def, self.in_verilog, self.in_sdc = (None,)*3
        if prev_out_dir is not None:
            self.in_def = "{}/{}.def".format(prev_out_dir, self.design_name)
            self.in_verilog = "{}/{}.v".format(prev_out_dir, self.design_name)
            self.in_sdc = "{}/{}.sdc".format(prev_out_dir, self.design_name)
        else:
            # If this is the first stage, just use the original design file
            self.in_verilog = "{}/{}".format(self.rdf_path, self.design["verilog"][0])

            # FIXME
            self.in_sdc = "{}/{}.sdc".format(self.rdf_path, self.design_name)

        # Library/PDK
        self.lib_name = config["design"]["library"]
        self.lib_dir = "{0}/libraries/{1}".format(self.rdf_path, self.lib_name)
        self.liberty = "{0}/libraries/{1}/{1}.lib" \
                       .format(self.rdf_path, config["design"]["library"])
        self.lef = "{0}/libraries/{1}/{1}.lef" \
                       .format(self.rdf_path, config["design"]["library"])
        self.tracks = "{0}/libraries/{1}/tracks.info" \
                       .format(self.rdf_path, config["design"]["library"])

        lib_config_yml = "{0}/libraries/{1}/{1}.yml" \
                         .format(self.rdf_path, self.lib_name)

        self.lib_config = None
        with open(lib_config_yml) as f:
            self.lib_config = yaml.safe_load(f)

        # (TODO) User parameters
        self.user_parms = user_parms    # List of parameters (key/value pairs)


    @abstractmethod
    def run(self):
        pass
