pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
    stages {
        stage('Test') {
            steps {
                sh '''
                wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
                mkdir geckodriver
                tar -xzf geckodriver*.tar.gz -C geckodriver
                export PATH=$PATH:$PWD/geckodriver
                python setup.py install
                pip install -r requirements/heroku_requirements.txt
                pytest --cov=koalixcrm --cov-branch --cov-report xml --cov-report term -m "not version_increase"'''
            }
            post {
                always {
                    junit '**/target/surefire-reports/*.xml'
                }
            }
        }
        stage('Test') {
            steps {
                echo 'Should deploy jar file on Hetzner via SSH. Not implemented yet.'
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