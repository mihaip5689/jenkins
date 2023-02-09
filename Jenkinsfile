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
                sh 'python ./checkSecurityVulnerabilities.py'
            }
        }
        stage('Deploy') {
            steps {
                withCredentials([sshUserPrivateKey(credentialsId: 'df0feef0-6f82-4731-87de-8b66d3512f3b', keyFileVariable: 'key')]) {
                    sh """
                        scp -i ${key} -o StrictHostKeyChecking=no securePodToDeploy.yaml master@192.168.100.8:/home/master
                        ssh -i ${key} -o StrictHostKeyChecking=no master@192.168.100.8 "kubectl apply -f securePodToDeploy.yaml"
                        """
                }
            }
        }
    }
}
