'''
    File name      : rdf_TritonCTS.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 11:26:08 PM EDT
    Last modified  : 2019-07-31 01:11:05
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
    print("Running TritonCTS...")
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    triton_cts = TritonCTSRunner(config, job_dir, prev_out_dir, user_parms)
    triton_cts.run()

    print("Done.")
    print("")


class TritonCTSRunner(object):
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
        self.tracks = "{0}/libraries/{1}/tracks.info" \
                       .format(self.rdf_path, config["design"]["library"])

        self.lib_config = None

        lib_config_yml = "{0}/libraries/{1}/{1}.yml" \
                         .format(self.rdf_path, self.lib_name)
        with open(lib_config_yml) as f:
            self.lib_config = yaml.safe_load(f)


    def run(self):
        print("Hello TritonCTS...")

        self._write_config_file()

        self._run_triton_cts()

        self._copy_final_output()

    def _write_config_file(self):
        # FIXME: Get width and height of the design....
        with open("{}/{}.def".format(self.prev_out_dir, self.design_name)) as f:
            lines = [l for l in (_.strip() for _ in f) if l]

        units, w_dbu, h_dbu = (None,)*3
        for l in lines:
            if l.startswith("UNITS"):
                tokens = l.split()
                units = int(tokens[3])
            elif l.startswith("DIEAREA"):
                tokens = l.split()
                w_dbu, h_dbu = int(tokens[6]), int(tokens[7])
        w, h = float(w_dbu)/units, float(h_dbu)/units

        with open("{}/triton_cts.cfg".format(self.job_dir), 'w') as f:
            f.write("lef {}/merged_padded_spacing.lef\n".format(self.lib_dir))
            f.write("path {}/{}.def\n".format(self.prev_out_dir, self.design_name))
            f.write("verilog {}/{}.v\n".format(self.prev_out_dir, self.design_name))
            f.write("design {}/{}.v\n".format(self.prev_out_dir, self.design_name))
            f.write("target_skew {}\n".format(50))
            f.write("width {}\n".format(w))
            f.write("height {}\n".format(h))
            f.write("tech {}\n".format(self.lib_config["PROCESS"]))
            f.write("ck_port {}\n".format(self.config["design"]["clock_port"]))
            f.write("db_units {}\n".format(2000))
            f.write("root_buff {}\n".format(self.lib_config["CTS_BUF_CELL"]))
            f.write("toler {}\n".format(1000))

    def _run_triton_cts(self):
        cmd = "{}/bin/cts/TritonCTS/runTritonCTS.tcl".format(self.rdf_path)
        cmd += " -configFilePath={}/{}".format(self.job_dir, "triton_cts.cfg")
        cmd += " -scriptsPath={}/bin/cts/TritonCTS/scripts".format(self.rdf_path)
        cmd += " -techFilesPath={}/{}".format(self.lib_dir, self.lib_config["CTS_TECH_DIR"])
        cmd += " -lefDefParserPath={}/bin/cts/TritonCTS/bin/lefdef2cts".format(self.rdf_path)
        cmd += " -executablePath={}/bin/cts/TritonCTS/bin/genHtree".format(self.rdf_path)
        cmd += " -legalizerPath={}/bin/detail_place/opendp/opendp".format(self.rdf_path)
        cmd += " -outputPath={}/TritonCTS".format(self.job_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        cmd = "ln -s {0}/TritonCTS/cts_final.def {0}/out/{1}.def" \
              .format(self.job_dir, self.design_name)

        run_shell_cmd(cmd)

        # Copy previous verilog file
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

