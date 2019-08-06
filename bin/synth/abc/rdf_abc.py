'''
    File name      : abc.py
    Author         : Jinwook Jung
    Created on     : Fri 26 Jul 2019 12:08:12 AM EDT
    Last modified  : 2019-08-06 00:17:59
    Description    :
'''

import subprocess, os, sys, random, yaml, time
from verilog_to_blif_converter import *
from latch_mapper import *

from subprocess import Popen, PIPE, CalledProcessError

def run_shell_cmd(cmd, f=None):
    p = subprocess.Popen(cmd,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT,
                         shell=True)

    for line in iter(p.stdout.readline, b''):
        print(">>> {}".format(line.rstrip().decode("ASCII")))

        # FIXME
        if f is not None:
            f.write("{}\n".format(line.rstrip().decode("ASCII")))

class ABCRunner(object):
    class DefaultFlop:
        def __init__(self, lib_config):
            self.name = lib_config["DEFAULT_FLOP"]
            self.dpin = lib_config["DEFAULT_FLOP_DPIN"]
            self.qpin = lib_config["DEFAULT_FLOP_QPIN"]
            self.ckpin = lib_config["DEFAULT_FLOP_CKPIN"]

    def __init__(self, config, job_dir, user_parms):
        ''' Initialize the instance and populate the necessary/useful
        variables. '''
        self.config = config
        self.job_dir = job_dir

        self.rdf_path = config["rdf_path"]
        self.design_name = config["design"]["name"]

        if len(config["design"]["verilog"]) > 1:
            # FIXME: We cannot support it right now...
            sys.exit(-1)        # Raise error, rather than exit.

        self.verilog = "{}/{}".format(self.rdf_path, config["design"]["verilog"][0])

        self.lib_name = config["design"]["library"]
        self.lib_dir = "{0}/libraries/{1}".format(self.rdf_path, self.lib_name)
        self.liberty = "{0}/libraries/{1}/{1}.lib" \
                       .format(self.rdf_path, config["design"]["library"])
        self.lib_config = None

        lib_config_yml = "{0}/libraries/{1}/{1}.yml" \
                         .format(self.rdf_path, self.lib_name)
        with open(lib_config_yml) as f:
            self.lib_config = yaml.safe_load(f)

        print("verilog: {}".format(self.verilog))
        print("liberty: {}".format(self.liberty))

        # Used in latch mapping
        self.dff = self.DefaultFlop(self.lib_config)

        # Optimization parms
        if user_parms is None or len(user_parms) == 0:
            self.script = 'resyn2'
            self.map = 'map'
            self.max_fanout = 16
        else:
            # FIXME...
            self.script = 'resyn2'
            self.map = 'map'
            self.max_fanout = 16

    def run(self):
        print("Hello ABC...")

        # Verilog to BLIF conversion
        self._write_blif()

        # Launch ABC
        self._launch_abc()

        # Map latches
        self._map_latches()

    def _write_blif(self):
        blif_converter = BlifConverter()
        blif_converter.read_verilog(self.verilog)
#        if asserts is not None:
#            blif_converter.read_timing(asserts)
        blif_converter.write_blif("{}/input.blif".format(self.job_dir))

    def _launch_abc(self):
        ''' Launch ABC and generates an (optimized) output verilog.'''
        # Arguments to run ABC
        abc_bin = "{}/bin/synth/abc/abc".format(self.rdf_path)
        abc_rc = "{}/bin/synth/abc/abc.rc".format(self.rdf_path)
        output = "output.txt"
        input_lib = self.liberty
        input_blif = "{}/input.blif".format(self.job_dir)
        output_verilog = "{}/output.v".format(self.job_dir)

        # Launch ABC using the dedicated shell script
        cmd = "{}/bin/synth/abc/run_abc.sh \\\n".format(self.rdf_path)
        cmd += " {} {} {} \\\n".format(abc_bin, abc_rc, output)
        cmd += " {} {} \\\n".format(input_lib, input_blif)
        cmd += " {} {} {} \\\n".format(self.script, self.map, self.max_fanout)
        cmd += " {}\\\n".format(output_verilog)
        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'w') as f:
            run_shell_cmd(cmd, f)

    def _map_latches(self):
        ''' Creates latch-mapped verilog file. '''
        # Clock source and default flop 
        clock_port = self.config["design"]["clock_port"]
        latch_cell = self.lib_config["DEFAULT_FLOP"]
        d, q, ck = self.lib_config["DEFAULT_FLOP_DPIN"], \
                   self.lib_config["DEFAULT_FLOP_QPIN"], \
                   self.lib_config["DEFAULT_FLOP_CKPIN"]

        print(latch_cell)
        print(d)
        print(q)
        print(ck)

        # Map latch
        mapper = LatchMapper(clock_port, latch_cell)
        mapper.latch_dpin, mapper.latch_qpin, mapper.latch_ckpin = d, q, ck
        print("TIEHI_CELL_AND_PORT")
        print(self.lib_config["TIEHI_CELL_AND_PORT"])
        mapper.tie_hi, mapper.tie_hi_out = self.lib_config["TIEHI_CELL_AND_PORT"]
        mapper.tie_lo, mapper.tie_lo_out = self.lib_config["TIELO_CELL_AND_PORT"]

        mapper.read_verilog("{}/output.v".format(self.job_dir))
        mapper.map_latches("{}/out/{}.v".format(self.job_dir, self.design_name))


def run(config, job_dir, prev_out_dir, user_parms):
    """ Run the point tool and store the outputs at the out directory."""
    print("running ABC...")
    print("Run directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))
    print("Done.")
    print("")

    if config["design"]["bench_suite"] != "tau17":
        print("(E) Only tau17 benchmark suites are supported.")
        # FIXME: Raise exceptions?
        return -1

    abc_runner = ABCRunner(config, job_dir, user_parms)

    abc_runner.run()

