'''
    File name      : stage.py
    Author         : Jinwook Jung
    Created on     : Thu 25 Jul 2019 11:57:16 PM EDT
    Last modified  : 2020-01-06 13:27:13
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
    def __init__(self, config, stage_dir, prev_out_dir, user_parms, write_run_scripts=False):
        ''' Initialize the instance and populate the necessary/useful
        variables. '''
        self.config = config
        self.stage_dir = stage_dir
        self.prev_out_dir = prev_out_dir

        self.rdf_path = config["rdf_path"]
        self.design_name = config["design"]["name"]
        self.design = config["design"]
        self.techlib_path = "techlibs"      # FIXME: Make this changeble in config file.

        # Output of previous stage
        self.in_def, self.in_verilog, self.in_sdc = (None,)*3
        if prev_out_dir is not None:
            self.in_def = "{}/{}.def".format(prev_out_dir, self.design_name)
            self.in_verilog = "{}/{}.v".format(prev_out_dir, self.design_name)
            self.in_sdc = "{}/{}.sdc".format(prev_out_dir, self.design_name)
        else:
            # If this is the first stage, just use the original design file
            self.in_verilog = None
            self.in_def = None
            self.in_sdc = "{}/{}.sdc".format(self.rdf_path, self.design_name)
            self.design_verilogs = ["{}/{}".format(self.rdf_path, _) for _ in self.design["verilog"]]

        # Library/PDK
        self.lib_name = config["design"]["library"]
        self.lib_dir = "{0}/{1}/{2}".format(self.rdf_path, self.techlib_path, self.lib_name)
        self.liberty = "{0}/{1}/{2}/{2}.lib" \
                       .format(self.rdf_path, self.techlib_path, self.lib_name)
        self.lef = "{0}/{1}/{2}/{2}.lef" \
                       .format(self.rdf_path, self.techlib_path, self.lib_name)
        self.tracks = "{0}/{1}/{2}/tracks.info" \
                       .format(self.rdf_path, self.techlib_path, self.lib_name)
        lib_config_yml = "{0}/{1}/{2}/{2}.yml" \
                         .format(self.rdf_path, self.techlib_path, self.lib_name)

        self.lib_config = None
        with open(lib_config_yml) as f:
            self.lib_config = yaml.safe_load(f)

        # (TODO) User parameters
        self.user_parms = user_parms    # List of parameters (key/value pairs)

    def create_run_script_template(self):
        with open("{}/run.sh".format(self.stage_dir), 'w') as f:
            f.write("#!/bin/bash\n\n")
            f.write("export RDF_PATH=\"{}\"\n".format(self.rdf_path))
            f.write("export RDF_STAGE_DIR=\"{}\"\n".format(self.stage_dir))
            f.write("export RDF_TOOL_BIN_PATH=\"${RDF_PATH}/bin\"\n")
            f.write("\n")

    @abstractmethod
    def write_run_scripts(self):
        pass

    @abstractmethod
    def run(self):
        pass
