pipeline {
    agent any

    environment {
        IMAGE_NAME     = "sales-analyzer"
        IMAGE_TAG      = "${BUILD_NUMBER}"
        CONTAINER_NAME = "sales-analyzer-app"
    }

    stages {

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip3 install -r requirements.txt --break-system-packages'
            }
        }

        stage('Deploy as Container') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"

                echo 'Deploying container...'
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm   ${CONTAINER_NAME} || true

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -p 9090:9090 \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """
                echo 'Dashboard available at http://192.168.1.19:9090/report.html'
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS - Build #${BUILD_NUMBER} deployed."
        }
        failure {
            echo "Pipeline FAILED - Check logs above."
        }
        always {
            sh "docker image prune -f || true"
        }
    }
}
