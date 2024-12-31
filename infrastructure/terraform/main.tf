terraform {
  required_version = ">= 1.0.0"
  
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 4.0"
    }
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }

  backend "s3" {
    # Configure your backend here
  }
}

# AWS Configuration
module "eks_cluster" {
  source = "./modules/eks"
  # Add variables as needed
}

# GCP Configuration
module "gke_cluster" {
  source = "./modules/gke"
  # Add variables as needed
}

# Azure Configuration
module "aks_cluster" {
  source = "./modules/aks"
  # Add variables as needed
}
