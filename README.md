DATC Robust Design Flow 2019
===

Introduction...

Getting Started
---

You can run it by:
```
cd run
python ../src/rdf.py --config rdf.yml --test
```

Configuring RDF Flow
---

### Design configuration


### Flow configuration


### Library configuration


### Example YAML config file

Example RDF configuration file in YAML format:

```
---

rdf_path: /path/to/your/rdf/installation/RDF-2019
job_dir: /path/to/job/directory/not/implemented/yet

design:
    name:        ac97_ctrl
    clock_port:  clk
    bench_suite: tau17
    library:     nangate45

    # Floorplan configuration
    target_utilization: 50
    aspect_ratio: 1

    # Input Verilog files (can be multiple files)
    verilog:     
        - benchmarks/tau17/ac97_ctrl/ac97_ctrl.v

flow:
    - stage: synth
      tool: abc         # ABC or Yosys
      user_parms: 
          max_fanout: 16
          script: resyn2
          map:    map

    - stage: floorplan
      tool: TritonFP 
      user_parms: []

    - stage: global_place
      tool: RePlAce     # RePlAce, EhPlacer, ComPLx+FastPlace, NTUPlace, FZUPlace
      user_parms: []

    - stage: detail_place
      tool: opendp      # opendp, MCHL_T
      user_parms: []

    - stage: size
      tool: TritonSizer
      user_parms: []

    - stage: cts
      tool: TritonCTS
      user_parms: []

    - stage: global_route
      tool: FastRoute4-lefdef    # FastRoute4-lefdef, NCTUgr
      user_parms: []

    - stage: detail_route
      tool: TritonRoute          # TritonRoute, DrCU, NCTUdr
      user_parms: []
```



Preparing Libraries
---

Explain using ASAP7 as an example.
```
magic.tech
tracks.info
tritonCTS LUTs
gds
```


Adding Your Pont Tool Binaries
---

`./bin/<stage>/<tool_name>/`

Each tool must include runner python script.
This python script takes json file, which describes the parameters to run.

RDF will call `<rdf_path>/bin/<stage>/<tool_name>/rdf_<tool_name>.py`.



Contributors
---

### Current DATC Committee members

* Iris Hui-Ru Jiang - National Taiwan University
* Andrew B. Kahng - University of California San Diego
* Jianli Chen - Fuzhou University
* Jinwook Jung - IBM Thomas J. Watson Research Center
* Victor N. Kravets - IBM Thomas J. Watson Research Center
* Yih-Lang Li - National Chiao Tung University

### Code committers

* Mingyu Woo - UCSD
* Shih-Ting Lin - NCTU

### Tool contributors

* Nima Karimpour and Laleh Behjat - University of Calgary
* Myung-Chul Kim and Igor Markov (for ComPLx)
* Shinichi Nishizawa and Hidetoshi Onodera (for NCTUcell)
* OpenROAD team

