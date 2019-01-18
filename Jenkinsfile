pipeline {
    def application

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
                    pip install -r requirements/heroku_requirements.txt
                    deactivate
                    wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz
                    mkdir geckodriver
                    tar -xzf geckodriver*.tar.gz -C geckodriver
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
                . virtualenv/bin/activate
                export PATH=$PATH:$PWD/geckodriver
                if [ "${BRANCH_NAME}" == "master" ] && [ -z "${CHANGE_ID}" ]; then
                    pytest --cov=koalixcrm --cov-branch --cov-report xml:reports/coverage.xml --cov-report term
                else
                    pytest --cov=koalixcrm --cov-branch --cov-report xml:reports/coverage.xml --cov-report term -m "not version_increase"
                fi'''
            }
            post {
                always {
                    step([$class: 'CoberturaPublisher',
                                   autoUpdateHealth: false,
                                   autoUpdateStability: false,
                                   coberturaReportFile: 'reports/coverage.xml',
                                   failNoReports: false,
                                   failUnhealthy: false,
                                   failUnstable: false,
                                   maxNumberOfBuilds: 10,
                                   onlyStable: false,
                                   sourceEncoding: 'ASCII',
                                   zoomCoverageChart: false])
                }
            }
        }
        stage('Checkstyle + FindBugs') {
            steps {
                echo 'Should deploy jar file on Hetzner via SSH. Not implemented yet.'
            }
        }
        stage('Build Docker image') {
            application = docker.build("koalixswitzerland/koalixcrm")
        }
        stage('Push Docker image') {
            steps {
                docker.withRegistry('https://registry.hub.docker.com', 'docker-hub-credentials') {
                    // app.push("${env.BUILD_NUMBER}")
                    app.push("latest")
                }
            }
        }
        stage('Deploy') {
            steps {
                echo 'Should deploy jar file on Hetzner via SSH. Not implemented yet.'
            }
        }
    }
}