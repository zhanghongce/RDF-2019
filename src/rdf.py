'''
    File name      : rdf.py
    Author         : Jinwook Jung
    Created on     : Thu 25 Jul 2019 11:33:57 PM EDT
    Last modified  : 2019-08-04 01:25:31
    Description    : 
'''

import subprocess, os, sys, random, yaml, time
from os import path
from datetime import datetime
from uuid import uuid4
from shutil import copyfile
import importlib


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", action="store", required=True)
    parser.add_argument("--test", action="store_true")
    args, _ = parser.parse_known_args()

    with open(args.config) as f:
        config = yaml.safe_load(f)

    cur_dir = os.getcwd()
    src_dir = path.dirname(path.realpath(__file__))
    rdf_dir = path.dirname(src_dir)

    if args.test:
        job_id = "rdf.yymmdd.HHMMSS"
    else:
        job_id = "rdf.{}".format(datetime.now().strftime('%y%m%d.%H%M%S'))

    print("RDF Root Path: {}".format(rdf_dir))
    print("Job ID: {}".format(job_id))
    job_dir = "{}/{}".format(cur_dir, job_id)

    # Create a job directory with the current job id
    if args.test:
        import shutil
        shutil.rmtree(job_id, ignore_errors=True)
    os.mkdir(job_id)

    # FIXME
    design_data = dict()

    print("Start...")
    print("")

    for k,v in config.items():
        if k == "design":
            design_data = v
            print("Design: {}".format(design_data["name"]))

        elif k == "flow":
            prev_out_dir = None
            for stage in v:
                stage_name = stage["stage"]
                tool = stage["tool"]
                user_parms = stage["user_parms"]

                print("Current stage: {}".format(stage_name))
                print("Creating run directory:")
                run_dir = "{}/{}".format(job_dir, stage_name)
                out_dir = "{}/out".format(run_dir)
                os.makedirs(run_dir)
                os.makedirs(out_dir)

                if stage_name not in \
                        ("synth", "floorplan", "global_place", "detail_place", \
                         "cts", "global_route"):
                    print("Not implemented yet.. skip")
                    continue

                runpy = "{0}/{1}/{2}/{3}/rdf_{3}".format(rdf_dir, "bin", stage_name, tool)
                print("Launching: {}.py".format(runpy))

                # FIXME: Temporarily modify system path... this should be avoided?
                sys.path.insert(0, path.dirname(runpy))
                module = importlib.import_module("rdf_{}".format(tool))

                module.run(config, run_dir, prev_out_dir, user_parms)
                prev_out_dir = out_dir

                print("Done.")
                print("")

        else:
            # TODO: Error handling
            print("Error...")

