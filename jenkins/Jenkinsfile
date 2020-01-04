pipeline {
    agent any
    parameters {
        string(
                name: 'TargetUtilization', 
                description: 'Target utilization (available value: 0-95).'
              )
        choice(
                name: 'Placer',
                choices: ['NTUPlace3', 'ComPLx'],
                description: 'Pick the placer you want to try.'
              )
        string(
                name: 'MaxDensity', 
                description: 'Maximum local density (available value: 0-95).'
              )
    }
    stages {
        stage('Setup') {
            steps {
                echo "Target utilization: ${params.TargetUtilization}"
                echo "Placer            : ${params.Placer}"
                echo "Maximum density   : ${params.MaxDensity}"
            }
        }
        stage('Floorplanning') {
            steps {
                echo 'Running Floorplan.'
            }
        }
        stage('Placement') {
            steps {
                echo "Running placement (placer: ${params.Placer})"
                sh "bash ./src/place.sh ${params.Placer}"
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
 
