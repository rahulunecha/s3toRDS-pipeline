resource "aws_s3_bucket" "data_bucket" {
  bucket = "my-data-bucket"
}

resource "aws_db_instance" "rds_instance" {
  engine            = "mysql"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  username          = "admin"
  password          = "password123"
}

resource "aws_lambda_function" "data_handler" {
  function_name = "dataHandler"
  image_uri     = aws_ecr_repository.data_pipeline.repository_url
  package_type  = "Image"
  role          = aws_iam_role.lambda_role.arn
}

resource "aws_ecr_repository" "data_pipeline" {
  name = "data-pipeline"
}

resource "aws_iam_role" "lambda_role" {
  name = "lambda-execution-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Action = "sts:AssumeRole",
        Effect = "Allow",
        Principal = {
          Service = "lambda.amazonaws.com"
        }
      },
    ]
  })
}
