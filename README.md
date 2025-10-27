# Project - Building a Secure, Automated Cloud Application Deployment Framework on AWS

## Folder Structure
- .github/workflows/   # CI/CD workflows
- src/                 # Source code
- Dockerfile           # Container build configuration
- requirements.txt     # Python dependencies
- rollback.sh          # Rollback in acse of failure.




## Steps to Implement Project
### 1. Basics
Create AWS accounts     


### 2. Infrastructure as Code [Automation].
**If we want, we can try to build it manually first 
- Use IaC for automating infra creation [IaC options - Terraform, CloudFormation, AWS CDK]
- IAM roles.
- Create VPC, subnets, attach internet gateway, NAT gateway, update route tables, manually or using IaC. 
- EKS cluster in VPC [private subnets]. Kubernetes Deployment and Service. Consider Auto Scaling. Prometheus/Grafana for pod metrics.
- Set up ECR.
- Set up monitoring using AWS CloudWatch and others. Logging / Tracing. CloudWatch alarms.
- Public access via Ingress. AWS Application Load Balancer (ALB) in public subnets. ALB forwards traffic to your app Pods in private subnets. - - - HTTPS on ALB.
- Deploy ALB Ingress Controller on EKS
- Add Firewalls, 1. Security groups, NACL’s, WAF, Network Firewalls.


### 3. Manage Secrets
- Create and manage secrets using AWS Secrets Manager.


### 4. Development
- Create a GitHub repo with the contributors.
- Develop and test Python based [flask or fast API] applications locally.  [individual feature branches]. Build and test docker images locally. Repo includes,
  - Docker file 
  - requirements.txt
  - Python app files
  - Terraform files


### 5. CI CD
- Push the code to GitHub. Create PR and merge to develop and then to main. Automatic tests before merge, maybe linting or unit tests for Python using CI CD [GitHub Actions]
- As soon code in merged to main branch, CI CD Automation on GitHub Actions will:
- GitHub Actions Secrets for CI/CD.
- Terraform provisions VPC, Firewall, ECR, EKS. [ triggered only when changes are made to infra]
- Builds Docker image
- Push the image to ECR.
- Deploy Kubernetes Deployment/Service via kubectl apply.
- rollback strategies in CI/CD if deployment fails.


### 6. Application Available
- App runs on EKS inside private VPC, behind firewall

