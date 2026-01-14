# GlobalVoice AI: Core Infrastructure Provisioning
# Provider: AWS
# Resources: VPC, EKS (Kubernetes), S3 (Media Storage), RDS (PostgreSQL)

provider "aws" {
  region = var.aws_region
}

# 1. S3 Bucket for Media Assets (Videos, Audio, Dubbed versions)
resource "aws_s3_bucket" "media_storage" {
  bucket = "globalvoice-media-assets-${var.environment}"
  
  tags = {
    Name        = "GlobalVoice Media Storage"
    Environment = var.environment
  }
}

# 2. EKS Cluster for Microservices & AI Workers
module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "~> 19.0"

  cluster_name    = "globalvoice-cluster-${var.environment}"
  cluster_version = "1.28"

  vpc_id     = module.vpc.vpc_id
  subnet_ids = module.vpc.private_subnets

  eks_managed_node_groups = {
    # General purpose nodes for API and Frontend
    general = {
      instance_types = ["t3.large"]
      min_size     = 2
      max_size     = 5
      desired_size = 2
    }
    # GPU-optimized nodes for AI Inference (STT, TTS, LipSync)
    ai_workers = {
      instance_types = ["g4dn.xlarge"] # NVIDIA T4 GPUs
      min_size     = 1
      max_size     = 20
      desired_size = 1
      
      labels = {
        workload = "ai-inference"
      }
      
      taints = [
        {
          key    = "nvidia.com/gpu"
          value  = "true"
          effect = "NO_SCHEDULE"
        }
      ]
    }
  }
}

# 3. RDS instance for PostgreSQL
resource "aws_db_instance" "postgres" {
  allocated_storage    = 50
  engine               = "postgres"
  engine_version       = "15.4"
  instance_class       = "db.t4g.medium"
  db_name              = "globalvoice_db"
  username             = var.db_username
  password             = var.db_password
  skip_final_snapshot  = true
}