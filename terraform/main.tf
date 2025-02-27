provider "aws" {
  region = "us-east-1"
}

# S3 Bucket
resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-data-bucket"
}

# RDS MySQL Instance
resource "aws_db_instance" "my_db" {
  identifier           = "mydb-instance"
  engine              = "mysql"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  db_name             = "mydb"
  username            = "admin"
  password            = "password123"
  publicly_accessible = true
}

# ECR Repository
resource "aws_ecr_repository" "my_repo" {
  name = "my-app-repo"
}

# Lambda Function
resource "aws_lambda_function" "my_lambda" {
  function_name = "s3-to-rds"
  image_uri     = "${aws_ecr_repository.my_repo.repository_url}:latest"
  package_type  = "Image"

  environment {
    variables = {
      S3_BUCKET  = aws_s3_bucket.data_bucket.bucket
      DB_HOST    = aws_db_instance.my_db.address
      DB_USER    = "admin"
      DB_PASSWORD = "password123"
      DB_NAME    = "mydb"
    }
  }
}
