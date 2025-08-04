provider "aws" {
  region = "us-east-1"
}

# ⚠️ Bucket público y sin cifrado
resource "aws_s3_bucket" "vulnerable_bucket" {
  bucket = "vulnerable-demo-bucket-123456"

  acl    = "public-read"  # ❌ Acceso público
  force_destroy = true

  tags = {
    Name = "Public S3 Bucket"
  }
}

# ⚠️ Security Group con todos los puertos abiertos
resource "aws_security_group" "open_sg" {
  name        = "open-security-group"
  description = "Security group with all ports open"
  vpc_id      = "vpc-xxxxxxxx" # reemplazar por una VPC válida

  ingress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]  # ❌ Acceso global
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ⚠️ EC2 con IP pública
resource "aws_instance" "vulnerable_ec2" {
  ami           = "ami-0c02fb55956c7d316" # Amazon Linux 2
  instance_type = "t2.micro"
  key_name      = "my-insecure-key"  # ❌ clave estática

  associate_public_ip_address = true  # ❌ IP pública directa

  security_groups = [aws_security_group.open_sg.name]

  tags = {
    Name = "Vulnerable EC2"
  }
}
