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
                sh "conda activate"
                sh "cd run; python ../src/rdf.py --config test.yml --test"
            }
        }
        stage('Logic Synthesis') {
            steps {
                echo 'Running logic synthesis.'
            }
        }
        stage('Global Placement') {
            steps {
                echo "Running global placement."
            }
        }
        stage('Detail Placement') {
            steps {
                echo "Running detail placement."
            }

        }
        stage('Clock Tree Synthesis') {
            steps {
                echo 'Running clock tree synthesis.'
            }
        }
        stage('Global Routing') {
            steps {
                echo 'Running global routing.'
            }
        }
        stage('Detailed Routing') {
            steps {
                echo 'Running detailed routing.'
            }
        }
    }
}
 
