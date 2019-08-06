'''
    File name      : rdf_FastRoute4-lefdef.py
    Author         : Jinwook Jung
    Created on     : Tue 30 Jul 2019 11:26:08 PM EDT
    Last modified  : 2019-07-31 23:00:48
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
    print("Running FastRoute4-lefdef...")
    print("Job directory: {}".format(job_dir))
    print("Previous stage outputs: {}".format(prev_out_dir))

    fastroute = FastRouteRunner(config, job_dir, prev_out_dir, user_parms)
    fastroute.run()

    print("Done.")
    print("")


class FastRouteRunner(object):
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
        print("Hello FastRoute4-lefdef...")

        self._write_rsyn_script()

        self._run_fastroute()

        self._copy_final_output()

    def _write_rsyn_script(self):
        with open("{}/fastroute.rsyn".format(self.job_dir), 'w') as f:
            f.write("open \"generic\" {\n")
            #f.write("  \"lefFiles\" : \"{}\",\n".format(self.lef))
            f.write("  \"lefFiles\" : \"{}/merged_padded_spacing.lef\",\n".format(self.lib_dir))
            f.write("  \"defFiles\" : \"{}/{}.def\"\n".format(self.prev_out_dir, self.design_name))
            f.write("};\n")
            f.write("\n")
            f.write("run \"rsyn.fastRoute\" {\"outfile\" : \"route.guide\"};\n")
            f.write("\n")
            f.write("# outfile: string. indicate the name of the generated guides file\n")
            f.write("# adjustment: float. indicate the percentage reduction of each edge\n")
            f.write("# maxRoutingLayer: integer. indicate the max routing layer available for FastRoute\n")

    def _run_fastroute(self):
        for flute_file in ("PORT9.dat", "POST9.dat", "POWV9.dat"):
            cmd = "ln -s {}/bin/global_route/FastRoute4-lefdef/{} {}" \
                .format(self.rdf_path, flute_file, self.job_dir)

            print(cmd)

            with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
                run_shell_cmd(cmd, f)

        cmd = "cd {};".format(self.job_dir)
        cmd += "{}/bin/global_route/FastRoute4-lefdef/FRlefdef".format(self.rdf_path)
        cmd += " --no-gui"
        cmd += " --script fastroute.rsyn".format(self.job_dir)

        print(cmd)

        with open("{}/out/{}.log".format(self.job_dir, self.design_name), 'a') as f:
            run_shell_cmd(cmd, f)

    def _copy_final_output(self):
        # Copy previous DEF
        cmd = "ln -s {0}/{1}.def {2}/out/{1}.def" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

        # Copy previous Verilog
        cmd = "ln -s {0}/{1}.v {2}/out/{1}.v" \
              .format(self.prev_out_dir, self.design_name, self.job_dir)

        run_shell_cmd(cmd)

        # Copy output route guide.
        cmd = "ln -s {0}/route.guide {0}/out/{1}.guide" \
              .format(self.job_dir, self.design_name)

        run_shell_cmd(cmd)

