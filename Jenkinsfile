pipeline {
  agent { label 'docker' }
  options {
    buildDiscarder(logRotator(numToKeepStr: '5'))
  }
  triggers {
    cron('@daily')
  }
  stages {
    stage('Build') {
      steps {
        sh 'docker build -t koalixswitzerland/koalixcrm:latest .'
      }
    }
    stage('Publish') {
      when {
        branch 'master'
      }
      steps {
        withDockerRegistry([ credentialsId: "docker-hub-credentials", url: "" ]) {
          sh 'docker push koalixswitzerland/koalixcrm:latest'
        }
      }
    }
  }