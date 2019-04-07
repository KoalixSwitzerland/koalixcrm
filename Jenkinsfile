def application

pipeline {
    agent any
    options {
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '5'))
    }
    environment {
        HETZNER_API_KEY = credentials('HETZNER_API_KEY')
        GOOGLE_APPLICATION_CREDENTIALS = credentials('GOOGLE_APPLICATION_CREDENTIALS')
        PATH_TO_ROOT_SERVER_PRIV_KEY = credentials('PATH_TO_ROOT_SERVER_PRIV_KEY')
        CLOUD_FLARE_API_KEY = credentials('CLOUD_FLARE_API_KEY')
        PASSPHRASE_ROOT_SERVER_PRIV_KEY = credentials('PASSPHRASE_ROOT_SERVER_PRIV_KEY')
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
                elif [ "${BRANCH_NAME}" == "development" ] && [ -z "${CHANGE_ID}" ]; then
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
                echo 'Should run a static code analysis.'
            }
        }
        stage('Build Docker image') {
            steps {
            sh 'docker build -f "Dockerfile.prod" -t koalixswitzerland/koalixcrm:latest .'
            }
        }
        stage('Push Docker image') {
            steps {
                withDockerRegistry([ credentialsId: "8c45eee4-1162-466b-84c5-5f86a52a44cd", url: "" ]) {
                    sh 'docker push koalixswitzerland/koalixcrm:latest'
                }
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                . virtualenv/bin/activate
                if [ -d "koalixcrm_deploy" ]; then
                    rm -rf koalixcrm_deploy
                fi
                mkdir koalixcrm_deploy
                cd koalixcrm_deploy
                git clone git@bitbucket.org:scaphilo/hetzner_jenkins_start_script.git
                pip install -r hetzner_jenkins_start_script/deployment_requirements.txt
                cd hetzner_jenkins_start_script
                python server.py --branch_name=${BRANCH_NAME} --action=deploy --restore_backup=development
                '''
            }
        }
    }
}