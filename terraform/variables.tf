variable "aws_region" {
  description = "AWS region for the Student Academic Platform infrastructure."
  type        = string
  default     = "ap-south-1"
}

variable "instance_type" {
  description = "EC2 instance type (free-tier eligible default)."
  type        = string
  default     = "t3.micro"
}

variable "project_name" {
  description = "Project name used for tagging."
  type        = string
  default     = "student-academic-platform"
}

variable "allowed_http_cidr" {
  description = "CIDR allowed to reach the app (restrict before apply)."
  type        = string
  default     = "0.0.0.0/0"
}

variable "app_port" {
  description = "Application container port."
  type        = number
  default     = 5000
}
