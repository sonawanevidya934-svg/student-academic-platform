# Student Academic Platform - infrastructure notes
# SAFE: validation-only workflow. The configuration DEFINES VPC, subnet,
# IGW, route table, security group, EC2, and S3 (see main.tf), but nothing
# is created until someone runs `terraform apply` (NEVER run it here).
# Validation only:
#   terraform fmt -check -diff
#   terraform init -backend=false
#   terraform validate
# NEVER run: terraform apply / terraform destroy (per project safety rules and to avoid AWS charges).
