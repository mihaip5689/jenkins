pipeline {
    agent any

    stages {
        stage('Checkout code') {
            steps {
                git branch: 'main', url: 'https://github.com/mihaip5689/jenkins.git'
            }
        }
        stage('Run python script to check for security vulnerabilities') {
            steps {
                bat 'python ./checkSecurityVulnerabilities.py'
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: '9f248ae0-6b7a-4ccc-89e1-16b30e50a667', keyFileVariable: 'key')]) {
                    bat '''
                        scp -i ${key} securePodToDeploy.yaml master@192.168.100.8:/home/master
                        ssh -i ${key} master@192.168.100.8 "kubectl apply -f securePodToDeploy.yaml" '''
                }
            }
        }
    }
}
