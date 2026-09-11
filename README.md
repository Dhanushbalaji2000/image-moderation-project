# AWS Scalable Image Moderation & Processing Pipeline:

A user uploads an image through a web interface. The request enters through AWS WAF and CloudFront, reaches an internet-facing Application Load Balancer, and is routed through a Target Group to a healthy EC2 application server. Nginx receives the HTTP request, proxies it to Gunicorn, and Gunicorn runs the Flask application.
The Flask application uploads the image to Amazon S3, calls Amazon Rekognition DetectModerationLabels using the S3 object, determines whether the image is Approved or Rejected, and stores the audit information in Amazon RDS for Microsoft SQL Server. 

## Project Objective

The objective of this project was to build a secure and scalable AWS application while gaining hands-on experience with:

- Multi-AZ VPC architecture
- Public and private subnets
- Private EC2 application servers
- Application Load Balancer
- Target Groups and health checks
- Auto Scaling
- Nginx, Gunicorn and Flask
- IAM roles and Boto3
- Amazon S3
- Amazon Rekognition
- Amazon RDS SQL Server
- Amazon CloudFront
- AWS WAF
- NAT Gateway
- S3 Versioning and Lifecycle policies
- Monitoring and troubleshooting

