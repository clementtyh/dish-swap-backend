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
        
        stage('Manual Approval') {
            steps {
                input "Do you want to proceed with deployment?"
            }
        }

        stage('Deploy') {
            steps {
                echo 'Deploying'
                // Add deploy steps here
                sh '''
                    docker-compose down
                    docker-compose build --no-cache
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
