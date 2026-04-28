pipeline {
    agent any

    environment {
        IMAGE_NAME     = "sales-analyzer"
        IMAGE_TAG      = "${BUILD_NUMBER}"
        CONTAINER_NAME = "sales-analyzer-app"
    }

    stages {

        stage('Checkout') {
            steps {
                echo 'Pulling code from GitHub...'
                checkout scm
            }
        }

        stage('Build') {
            steps {
                echo 'Installing dependencies...'
                sh 'pip install -r requirements.txt'
            }
        }

        stage('Run') {
            steps {
                echo 'Running analyzer to verify it works...'
                sh 'python analyzer.py --out report.html'
                echo 'Report generated successfully.'
            }
        }

        stage('Build Docker Image') {
            steps {
                echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}"
                sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} ."
                sh "docker tag ${IMAGE_NAME}:${IMAGE_TAG} ${IMAGE_NAME}:latest"
            }
        }

        stage('Deploy as Container') {
            steps {
                echo 'Deploying container...'
                sh """
                    docker stop ${CONTAINER_NAME} || true
                    docker rm   ${CONTAINER_NAME} || true

                    docker run -d \
                        --name ${CONTAINER_NAME} \
                        -v \$(pwd)/output:/app/output \
                        ${IMAGE_NAME}:${IMAGE_TAG}
                """
                echo 'Container deployed. Report saved to ./output/report.html'
            }
        }
    }

    post {
        success {
            echo "Pipeline SUCCESS - Build #${BUILD_NUMBER} deployed."
            archiveArtifacts artifacts: 'report.html', fingerprint: true
        }
        failure {
            echo "Pipeline FAILED - Check logs above."
        }
        always {
            sh "docker image prune -f || true"
        }
    }
}
