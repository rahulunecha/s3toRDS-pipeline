pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t data-pipeline .'
            }
        }

        stage('Push to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <account-id>.dkr.ecr.us-east-1.amazonaws.com
                docker tag data-pipeline:latest <account-id>.dkr.ecr.us-east-1.amazonaws.com/data-pipeline:latest
                docker push <account-id>.dkr.ecr.us-east-1.amazonaws.com/data-pipeline:latest
                '''
            }
        }

        stage('Deploy with Terraform') {
            steps {
                sh '''
                cd terraform
                terraform init
                terraform apply -auto-approve
                '''
            }
        }
    }
}
