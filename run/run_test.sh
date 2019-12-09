python ../src/rdf.py --config rdf.yml --test --write-run-scripts
cd rdf.yymmdd.HHMMSS
cd synth; bash run.sh
cd ../floorplan/; bash run.sh
cd ../global_place/; bash run.sh
cd ../detail_place/; bash run.sh
cd ../cts; bash run.sh
cd ../global_route; bash run.sh
cd ../detail_route; bash run.sh
