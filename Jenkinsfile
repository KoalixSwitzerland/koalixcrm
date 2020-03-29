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
        DOCKER_HUB = credentials('DOCKER_HUB')
        PYPI = credentials('PYPI')
        PYPI_TST = credentials('PYPI_TST')
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
                    wget https://github.com/mozilla/geckodriver/releases/download/v0.23.0/geckodriver-v0.23.0-linux64.tar.gz -q
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
                fi
                deactivate'''
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
        stage('Build and Push PiPy package') {
            steps {
                sh '''
                    . virtualenv/bin/activate
                    pip install --upgrade setuptools wheel twine
                    python setup.py sdist bdist_wheel
                    if [ "${BRANCH_NAME}" == "master" ] && [ -z "${CHANGE_ID}" ]; then
                        if twine upload --verbose --username ${PYPI_USR} --password ${PYPI_PSW} dist/*; then
                           echo "twine upload succeeded"
                        else
                           echo "twine upload did not succeed"
                        fi
                    elif [ "${BRANCH_NAME}" == "development" ] && [ -z "${CHANGE_ID}" ]; then
                       if twine upload --verbose --username ${PYPI_USR} --password ${PYPI_PSW} dist/*; then
                         echo "twine upload succeeded"
                       else
                         echo "twine upload did not succeed"
                       fi
                    fi
                    deactivate'''
            }
        }
        stage('Build Docker image') {
            steps {
                sh '''
                if [ -d "koalixcrm_deploy" ]; then
                    rm -rf koalixcrm_deploy
                fi
                mkdir koalixcrm_deploy
                cd koalixcrm_deploy
                git clone git@bitbucket.org:scaphilo/hetzner_jenkins_start_script.git
                mv hetzner_jenkins_start_script/Dockerfile.prod ../
                mv hetzner_jenkins_start_script/koalixcrm.conf ../
                mv hetzner_jenkins_start_script/entrypoint.sh ../
                cd ..
                if [ "${BRANCH_NAME}" == "master" ] && [ -z "${CHANGE_ID}" ]; then
                    docker login -u ${DOCKER_HUB_USR} -p ${DOCKER_HUB_PSW}
                    docker build -f "Dockerfile.prod" -t koalixswitzerland/koalixcrm:latest . --force-rm
                elif [ "${BRANCH_NAME}" == "development" ] && [ -z "${CHANGE_ID}" ]; then
                    docker login -u ${DOCKER_HUB_USR} -p ${DOCKER_HUB_PSW}
                    docker build -f "Dockerfile.prod" -t koalixswitzerland/koalixcrm:latest . --force-rm
                fi'''
            }
        }
        stage('Push Docker image') {
            steps {
                sh '''
                if [ "${BRANCH_NAME}" == "master" ] && [ -z "${CHANGE_ID}" ]; then
                    docker login -u ${DOCKER_HUB_USR} -p ${DOCKER_HUB_PSW}
                    docker push koalixswitzerland/koalixcrm:latest
                elif [ "${BRANCH_NAME}" == "development" ] && [ -z "${CHANGE_ID}" ]; then
                    docker login -u ${DOCKER_HUB_USR} -p ${DOCKER_HUB_PSW}
                    docker push koalixswitzerland/koalixcrm:latest
                fi
                docker system prune -a -f
                '''
            }
        }
        stage('Deploy') {
            steps {
                sh '''
                . virtualenv/bin/activate
                cd koalixcrm_deploy
                pip install -r hetzner_jenkins_start_script/deployment_requirements.txt
                cd hetzner_jenkins_start_script
                python server_setup.py --branch_name=${BRANCH_NAME} --action=deploy --component koalixcrm-django
                '''
            }
        }
    }
}