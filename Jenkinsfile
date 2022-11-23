pipeline {
    agent {label "ubuntu"}

    stages {
        stage('SCM Checkout') {
            steps {
                checkout([
                    $class: 'GitSCM',
                    branches: scm.branches,
                    doGenerateSubmoduleConfigurations: true,
                    extensions: scm.extensions + [[$class: 'SubmoduleOption', parentCredentials: true]],
                    userRemoteConfigs: scm.userRemoteConfigs
                ])
                sh 'sudo cp -rvf * /root/mlops2'
            }
        }
        stage('Build') {
            steps {
                sh 'sudo docker-compose -f /root/mlops2/docker-compose.yml build'
            }
        }
        stage('Deploy') {
            steps {
                sh 'sudo mkdir /root/mlops2/sql'
                sh 'sudo docker-compose -f /root/mlops2/docker-compose.yml up -d'
            }
        }
    }
}
