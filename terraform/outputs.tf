output "project_name" {
  description = "Project identifier."
  value       = var.project_name
}

output "aws_region" {
  description = "Configured AWS region."
  value       = var.aws_region
}

output "vpc_id" {
  description = "ID of the application VPC."
  value       = aws_vpc.main.id
}

output "subnet_id" {
  description = "ID of the public subnet."
  value       = aws_subnet.public.id
}

output "security_group_id" {
  description = "ID of the application security group."
  value       = aws_security_group.app.id
}

output "s3_bucket_name" {
  description = "Name of the application S3 bucket."
  value       = aws_s3_bucket.app_data.id
}

output "ec2_public_ip" {
  description = "Public IP of the application EC2 instance."
  value       = aws_instance.app.public_ip
}

output "ec2_public_dns" {
  description = "Public DNS of the application EC2 instance."
  value       = aws_instance.app.public_dns
}
