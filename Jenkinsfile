node {
    def app

    stage('Clone repository') {
        /* Let's make sure we have the repository cloned to our workspace */

        checkout scm
    }

    stage('Build') {
          steps {
            sh 'docker build -f "Dockerfile-terraform" -t brightbox/terraform:latest .'
            sh 'docker build -f "Dockerfile-cli" -t brightbox/cli:latest .'
          }
    }
    stage('Publish') {
      when {
        branch 'master'
      }
      steps {
        withDockerRegistry([ credentialsId: "6544de7e-17a4-4576-9b9b-e86bc1e4f903", url: "" ]) {
          sh 'docker push brightbox/terraform:latest'
          sh 'docker push brightbox/cli:latest'
        }
      }
    }
}