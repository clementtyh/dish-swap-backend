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
                echo 'Testing...'
                // Add test steps here
            }
        }
        stage('Deploy') {
            steps {
                echo 'Deploying...'
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
                echo 'Deploying...'
                // Add deploy steps here
                sh '''
                    docker image prune --all --force
                '''
            }
        }
    }
}
