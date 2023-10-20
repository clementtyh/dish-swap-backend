pipeline {
    agent any

    stages {
        stage('Building Test Environment') {
            steps {
                echo 'Building...'
                // Add test steps here
                script {
                    // Set up the virtual environment
                    sh 'python3 -m venv venv'

                    sh 'sudo chmod +x ./venv/bin/activate'

                    // Activate the virtual environment
                    sh './venv/bin/activate'

                    // Upgrade pip within the virtual environment
                    sh './venv/bin/pip install --upgrade pip'

                    sh './venv/bin/pip install -r requirements.txt'
                }
            }
        }

        stage('Unit Test') {
            steps {
                echo 'Testing...'
                // Add test steps here
                script {
                    sh 'export JWT_PUBLIC_KEY_PATH="/home/kiriko/dishswap_keys/public_key.pem"'
                    sh 'export JWT_PRIVATE_KEY_PATH="/home/kiriko/dishswap_keys/private_key.pem"'
                    // Activate the virtual environment
                    sh './venv/bin/activate'

                    sh './venv/bin/pytest'
                }
            }
        }
        
        stage('Docker Push Stable Backup') {
            steps {
                echo 'Pushing Stable Build'
                script {
                    def dockerTag = "clementtyh/dishswap-backend:b0.${BUILD_ID.toInteger() - 1}"
        
                    sh "docker tag registry.hub.docker.com/clementtyh/dishswap-backend:latest ${dockerTag}"

                    // Log in to Docker Hub and push the image
                    docker.withRegistry('https://registry.hub.docker.com', 'fd312ca4-a214-47f0-bff0-453e4b3ed27d') {
                        docker.image("${dockerTag}").push()
                    }
                }
            }
        }

        stage('Build Container') {
            steps {
                echo 'Building Container'
                // Add deploy steps here
                sh '''
                    docker-compose build --no-cache
                '''
            }
        }

        stage('Container Scan') {
            steps {
                echo 'Scanning Container'
                timestamps {
                    script {
                        // Define the path for the scan.log file with a timestamp
                        def scanLogPath = "/var/lib/jenkins/scan_logs/scan_${BUILD_ID}.log"

                        // Run Trivy scan and redirect the output to the timestamped scan.log file
                        sh "trivy image clementtyh/dishswap-backend:latest > ${scanLogPath}"
                    }
                }
            }
        }
        
        stage('Approve Deployment') {
            steps {
                script {
                    // Define the path for the scan.log file with a timestamp
                    def scanLogPath = "/var/lib/jenkins/scan_logs/scan_${BUILD_ID}.log"

                    // Display information about the scan results and ask for manual approval
                    input message: """
                        Check the latest scan results in ${scanLogPath}.
                        Do you want to proceed with deployment?
                    """
                }
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying'
                // Add deploy steps here
                sh '''
                    docker-compose down
                    docker-compose up -d
                '''
            }
        }
        
        stage('Docker Push Latest Backup') {
            steps {
                echo 'Pushing Latest Build'
                script {
                    // Log in to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'fd312ca4-a214-47f0-bff0-453e4b3ed27d') {
                        // This block runs with Docker authentication
                        // You can push and pull Docker images here
                        docker.image('clementtyh/dishswap-backend:latest').push()
                    }
                }
            }
        }
        
        stage('Clean Up') {
            steps {
                echo 'Cleaning Up'
                // Add deploy steps here
                sh '''
                    docker image prune --all --force
                '''
            }
        }
    }
}
