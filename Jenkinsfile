pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'us-east-1'
    }

    stages {
        stage('Clone Repository') {
            steps {
                git url: 'https://github.com/rahulunecha/s3toRDS-pipeline.git', branch: 'main'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh 'docker build -t my-app .'
            }
        }

        stage('Push Docker Image to ECR') {
            steps {
                sh '''
                aws ecr get-login-password --region $AWS_DEFAULT_REGION | docker login --username AWS --password-stdin <account-id>.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com
                docker tag my-app:latest <account-id>.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/my-app-repo:latest
                docker push <account-id>.dkr.ecr.$AWS_DEFAULT_REGION.amazonaws.com/my-app-repo:latest
                '''
            }
        }

        stage('Deploy AWS Resources with Terraform') {
            steps {
                sh '''
                cd terraform
                terraform init
                terraform apply -auto-approve
                '''
            }
        }

        stage('Invoke Lambda Function') {
            steps {
                sh '''
                aws lambda invoke --function-name s3-to-rds --cli-binary-format raw-in-base64-out response.json
                cat response.json
                '''
            }
        }
    }
}
