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
                sh 'pip3 install -r requirements.txt'
            }
        }

        stage('Test') {
            steps {
                echo 'Running tests...'
                sh 'pip3 install pytest --quiet'
                sh 'pytest test_analyzer.py -v --junitxml=test-results.xml'
            }
            post {
                always {
                    junit 'test-results.xml'
                }
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
                        -v \$(pwd)/output:/app/output \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """
                echo 'Container deployed successfully.'
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

