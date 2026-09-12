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

## Architecture:

![image alt](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/1d88f6bf328df9b8f5451cb91ce24e32db9da0b2/ChatGPT%20Image%20Sep%2012%2C%202026%2C%2010_06_21%20AM.png)


## Application Screenshots

### Home — Upload Interface

Web interface for selecting an image to upload and moderate.

![Home — Upload Interface](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/d8513510303c316dac7f46578913f78545eebca9/01-home.png)

### How It Works

The interface explains image upload, analysis, moderation results, and audit storage.

![How It Works](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/6a8ac3482522b396e5cebe998415cbf86751363b/02-how-it-works.png)

### Image Selected

A selected image is previewed before clicking Upload & Moderate.

![Image Selected](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/5e9250dea582340d2d096ab7dbc166c207c22506/03-image-selected.png)

### Approved Result

The application displays an Approved moderation status.

![Approved Result](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/706d001e6b16678fcfe41c680c780ff1a5955f63/04-approved-result.png)

### Rejected Result

The application displays a Rejected moderation status.

![Rejected Result](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/6330c8278629ab27a7c9c8629ba493ff8b65c8c8/05-rejected-result.png)

### Upload History

The audit page lists filenames, moderation statuses, and upload timestamps.

![Upload History](docs/images/06-upload-history.png)




