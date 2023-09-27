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
        stage('Docker Login') {
            steps {
                echo 'Docker Login'
                // Add test steps here
                sh '''
                    cat /home/kiriko/docker_keys/docker_passwd.txt | docker login --username clementtyh --password-stdin
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
                '''
            }
        }
    }
}
