pipeline {
    agent any

    stages {
        stage('Build') {
            steps {
                echo 'Building...'
                // Add build steps here
                 sh '''
                    docker --version
                    pwd
                '''
            }
        }
        stage('Test') {
            steps {
                echo 'Testing'
                // Add test steps here
            }
        }
        stage('Docker Push Stable Backup') {
            steps {
                echo 'Docker'
                // Add test steps here
                sh '''
                    docker tag registry.hub.docker.com/clementtyh/dishswap-backend:latest clementtyh/dishswap-backend:stable
                '''
                script {
                    // Log in to Docker Hub
                    docker.withRegistry('https://registry.hub.docker.com', 'fd312ca4-a214-47f0-bff0-453e4b3ed27d') {
                        // This block runs with Docker authentication
                        // You can push and pull Docker images here
                        docker.image('clementtyh/dishswap-backend:stable').push()
                    }
                }
            }
        }

        stage('Build Container') {
            steps {
                echo 'Building Container'
                // Add deploy steps here
                sh '''
                    docker-compose down
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
                        def scanLogPath = "/home/kiriko/scan_logs/scan_${BUILD_ID}.log"

                        // Run Trivy scan and redirect the output to the timestamped scan.log file
                        sh "trivy image clementtyh/dishswap-backend:latest > ${scanLogPath}"

                        // Archive the scan log for later reference (optional)
                        archiveArtifacts "${scanLogPath}"
                    }
                }
            }
        }
        
        stage('Manual Approval') {
            steps {
                input "Check the latest scan results in /home/kiriko/scan_logs. Do you want to proceed with deployment?"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying'
                // Add deploy steps here
                sh '''
                    docker-compose up -d
                '''
            }
        }
        
        stage('Docker Push Latest Backup') {
            steps {
                echo 'Docker'
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
