pipeline {
  agent any

  environment {
    DOCKERHUB_CREDENTIALS = 'dockerhub-creds' // Jenkins credential id
    DOCKERHUB_REPO = 'ibrahimsattar'
    KUBECONFIG_CREDENTIAL = 'kubeconfig'       // optional: kubeconfig credential id
  }

  stages {
    stage('Checkout') {
      steps {
        checkout scm
      }
    }

    stage('Build API Image') {
      steps {
        script {
          def apiImage = "${env.DOCKERHUB_REPO}/study-api:${env.BUILD_NUMBER}"
          docker.build(apiImage, 'app/api')
          withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PWD')]) {
            sh "echo $DH_PWD | docker login -u $DH_USER --password-stdin"
            sh "docker push ${apiImage}"
          }
          // tag latest
          sh "docker tag ${apiImage} ${env.DOCKERHUB_REPO}/study-api:latest"
          sh "docker push ${env.DOCKERHUB_REPO}/study-api:latest"
          env.API_IMAGE = "${env.DOCKERHUB_REPO}/study-api:${env.BUILD_NUMBER}"
        }
      }
    }

    stage('Build Frontend Image') {
      steps {
        script {
          def feImage = "${env.DOCKERHUB_REPO}/study-frontend:${env.BUILD_NUMBER}"
          docker.build(feImage, 'app/frontend')
          withCredentials([usernamePassword(credentialsId: "${DOCKERHUB_CREDENTIALS}", usernameVariable: 'DH_USER', passwordVariable: 'DH_PWD')]) {
            sh "echo $DH_PWD | docker login -u $DH_USER --password-stdin"
            sh "docker push ${feImage}"
          }
          sh "docker tag ${feImage} ${env.DOCKERHUB_REPO}/study-frontend:latest"
          sh "docker push ${env.DOCKERHUB_REPO}/study-frontend:latest"
          env.FE_IMAGE = "${env.DOCKERHUB_REPO}/study-frontend:${env.BUILD_NUMBER}"
        }
      }
    }

    stage('Deploy to Kubernetes') {
      steps {
        script {
          // Option A: if you store kubeconfig as a Jenkins secret file named in KUBECONFIG_CREDENTIAL
          withCredentials([file(credentialsId: "${KUBECONFIG_CREDENTIAL}", variable: 'KUBECONFIG_FILE')]) {
            sh 'export KUBECONFIG=$KUBECONFIG_FILE'
            // Replace images in k8s manifests; simple sed replace example:
            sh "sed -i 's#ibrahimsattar/study-api:latest#${env.DOCKERHUB_REPO}/study-api:latest#g' kubernetes/api-deployment.yaml || true"
            sh "sed -i 's#ibrahimsattar/study-frontend:latest#${env.DOCKERHUB_REPO}/study-frontend:latest#g' kubernetes/frontend-deployment.yaml || true"
            sh "kubectl apply -f kubernetes/"
          }
        }
      }
    }

    stage('Smoke Test') {
      steps {
        sh "kubectl get pods -o wide"
        sh "kubectl get svc -o wide"
      }
    }
  }

  post {
    always {
      sh 'echo "Pipeline finished. Collect logs/screenshots."'
    }
  }
}
