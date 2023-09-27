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
        stage('Docker Push Backup') {
            steps {
                echo 'Docker'
                // Add test steps here
                sh '''
                    timestamp=$(date +%s)
                    docker tag clementtyh/dishswap-backend-image:latest clementtyh/dishswap-backend-image:$timestamp
                    docker push clementtyh/dishswap-backend-image:$timestamp
                '''
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
        stage('Clean Up') {
            steps {
                echo 'Cleaning Up'
                // Add deploy steps here
                sh '''
                    docker image prune --all --force
                    docker push clementtyh/dishswap-backend-image:latest
                '''
            }
        }
    }
}
