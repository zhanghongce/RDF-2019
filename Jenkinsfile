pipeline {
    agent any
    parameters {
        choice(
                name: 'benchmark',
                choices: ['i2c', 'tv80'],
                description: 'Choose benchmark circuit you want to try.'
              )
    }
    stages {
        stage('Setup') {
            steps {
                echo "Benchmark: ${params.benchmark}"
                sh '''#!/usr/bin/env bash
                      source /opt/miniconda3/etc/profile.d/conda.sh
                      conda activate
                      cd bin/openroad; ./install.sh; cd ../../
                      cd run; python ../src/rdf.py --config test.yml --test
                   '''
            }
        }
        stage('Logic Synthesis') {
            steps {
                echo 'Running logic synthesis.'
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/synth; bash run.sh
                   '''
            }
        }
        stage('Floorplanning') {
            steps {
                echo "Running floorplanning."
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/floorplan; bash run.sh 
                   '''
            }
        }
        stage('Global Placement') {
            steps {
                echo "Running global placement."
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/global_place; bash run.sh 
                   '''
            }
        }
        stage('Detail Placement') {
            steps {
                echo "Running detail placement."
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/detail_place; bash run.sh
                   '''
            }

        }
        stage('Clock Tree Synthesis') {
            steps {
                echo 'Running clock tree synthesis.'
                sh '''#!/usr/bin/env bash
                      pwd
                      source /opt/miniconda3/etc/profile.d/conda.sh
                      conda activate
                      cd run/rdf.yymmdd.HHMMSS/cts; bash run.sh
                   '''
            }
        }
        stage('Global Routing') {
            steps {
                echo 'Running global routing.'
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/global_route; bash run.sh
                   '''
            }
        }
        stage('Detailed Routing') {
            steps {
                echo 'Running detailed routing.'
                sh '''#!/usr/bin/env bash
                      pwd
                      cd run/rdf.yymmdd.HHMMSS/detail_route; bash run.sh
                   '''
            }
        }
    }
}
