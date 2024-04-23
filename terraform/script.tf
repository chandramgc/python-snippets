# 1. Install necessary providers:

# providers.tf
provider "aws" {
  region = "your_aws_region"
}

provider "helm" {
  kubernetes {
    config_path = "~/.kube/config"  # adjust the path to your kubeconfig file
  }
}

# 2. Create the EKS cluster:

# eks.tf
module "eks" {
  source          = "terraform-aws-modules/eks/aws"
  cluster_name    = "my-eks-cluster"
  subnets         = ["subnet-xxxxxxxxxxxxxxxxx", "subnet-yyyyyyyyyyyyyyyyy"]  # Update with your subnet IDs
  vpc_id          = "vpc-xxxxxxxxxxxxxxxxx"  # Update with your VPC ID
  cluster_version = "1.21"
  node_groups = {
    eks_nodes = {
      desired_capacity = 2
      max_capacity     = 3
      min_capacity     = 1

      key_name = "your_key_pair_name"  # Update with your key pair name
    }
  }
}
# 3. Install Helm and deploy Jenkins:

# jenkins.tf
resource "helm_release" "jenkins" {
  name       = "jenkins"
  repository = "https://charts.bitnami.com/bitnami"
  chart      = "jenkins"
  version    = "X.X.X"  # Replace with the desired version

  set {
    name  = "jenkinsUser"
    value = "admin"
  }

  set {
    name  = "jenkinsPassword"
    value = "your_jenkins_password"
  }

  depends_on = [module.eks]
}

# 4. Define Jenkins service and deployment:

# jenkins-service.tf
resource "kubernetes_service" "jenkins" {
  metadata {
    name = "jenkins"
  }

  spec {
    selector = {
      app = "jenkins"
    }

    port {
      port        = 8080
      target_port = 8080
    }

    port {
      port        = 50000  # Jenkins slave port
      target_port = 50000
    }

    type = "LoadBalancer"
  }
}

# jenkins-deployment.tf
resource "kubernetes_deployment" "jenkins" {
  metadata {
    name = "jenkins"
    labels = {
      app = "jenkins"
    }
  }

  spec {
    replicas = 1

    selector {
      match_labels = {
        app = "jenkins"
      }
    }

    template {
      metadata {
        labels = {
          app = "jenkins"
        }
      }

      spec {
        container {
          image = "docker.io/bitnami/jenkins:X.X.X"  # Replace with the desired Jenkins version
          name  = "jenkins"

          env {
            name  = "JENKINS_USERNAME"
            value = "admin"
          }

          env {
            name  = "JENKINS_PASSWORD"
            value = "your_jenkins_password"
          }
        }
      }
    }
  }
  depends_on = [
    module.eks,
    kubernetes_deployment.jenkins-slave,
  ]
}

# 5. Define Jenkins slave deployment

# jenkins-slave-deployment.tf
# Create a Kubernetes deployment for Jenkins slave
resource "kubernetes_deployment" "jenkins-slave" {
  metadata {
    name = "jenkins-slave"
    labels = {
      app = "jenkins-slave"
    }
  }

  spec {
    replicas = 2  # Number of slave replicas

    selector {
      match_labels = {
        app = "jenkins-slave"
      }
    }

    template {
      metadata {
        labels = {
          app = "jenkins-slave"
        }
      }

      spec {
        container {
          image = "jenkins/inbound-agent:4.11-1"  # Jenkins slave Docker image
          name  = "jenkins-slave"

          env {
            name  = "JENKINS_URL"
            value = "http://jenkins:8080"
          }

          env {
            name  = "JENKINS_SECRET"
            value = "your_jenkins_secret"
          }

          env {
            name  = "JENKINS_AGENT_NAME"
            value = "jenkins-slave-${POD_NAME}"
          }
        }
      }
    }
  }
}


# 5. Run Terraform:

# bash
# terraform init
# terraform apply


# Make sure to replace placeholder values like `"your_aws_region"`, `"subnet-xxxxxxxxxxxxxxxxx"`, `"vpc-xxxxxxxxxxxxxxxxx"`, `"your_key_pair_name"`, `"X.X.X"`, and `"your_jenkins_password"` with your actual values.