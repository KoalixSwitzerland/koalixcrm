pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
    stages {
        stage ("Prepare Virtual Environment"){
            steps {
                sh '''
                    if [ -f $virtualenv/bin/activate ]; then
                        rm -rf bin
                    fi
                    virtualenv -p /usr/bin/python3.6 --no-site-packages virtualenv
                    if [ -f $geckodriver ]; then
                        rm -rf geckodriver
                    fi
                '''
            }
        }
        stage ("Install Application Dependencies") {
            steps {
                sh '''
                    . virtualenv/bin/activate
                    pip install -r requirements/test_requirements.txt
                    deactivate
                    wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
                    mkdir geckodriver
                    tar -xzf geckodriver*.tar.gz -C geckodriver
                    export PATH=$PATH:$PWD/geckodriver
                   '''
            }
        }
        stage ("Get Latest Code") {
            steps {
                checkout scm
            }
        }
        stage('Test') {
            steps {
                sh '''
                source ../bin/activate
                pytest --cov=koalixcrm --cov-branch --cov-report xml --cov-report term -m "not version_increase"'''
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }
        stage('Checkstyle + FindBugs') {
            steps {
                echo 'Should deploy jar file on Hetzner via SSH. Not implemented yet.'
            }
        }
        stage('Archive') {
            steps {
                echo 'Should upload artefacts to Nexus. Not implemented yet.'
            }
        }
        stage('Deploy') {
            steps {
                echo 'Should deploy jar file on Hetzner via SSH. Not implemented yet.'
            }
        }
    }
}