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

![Upload History](https://github.com/Dhanushbalaji2000/image-moderation-project/blob/19d67e8e5e9a1e951ff9d053516e45878fcb751f/06-upload-history.png)



# Application Request Flow

```text
User
  |
  | HTTPS
  v
Amazon CloudFront
  |
  | AWS WAF evaluates request
  v
Application Load Balancer
  |
  v
Target Group
  |
  +-------------------------+
  |                         |
  v                         v
Private EC2 #1         Private EC2 #2
  |                         |
  |                   Auto Scaling Group
  |
  v
Nginx :80
  |
  v
Gunicorn :8000
  |
  v
Flask Application
  |
  +----------------+----------------+
  |                |                |
  v                v                v
Amazon S3     Rekognition       RDS SQL Server
```

# Image Processing Workflow

When a user uploads an image:

1. The user accesses the application through Amazon CloudFront.
2. AWS WAF evaluates the HTTP request.
3. CloudFront forwards the request to the Application Load Balancer.
4. The ALB selects a healthy EC2 instance from the Target Group.
5. Nginx receives the request on port `80`.
6. Nginx reverse proxies the request to Gunicorn on `127.0.0.1:8000`.
7. Gunicorn passes the request to the Flask application.
8. Flask receives the uploaded image.
9. Boto3 uploads the image to Amazon S3.
10. Flask calls Amazon Rekognition `DetectModerationLabels`.
11. Rekognition analyzes the S3 object and returns moderation labels.
12. Flask determines whether the image is **Approved** or **Rejected**.
13. Flask stores the result and image information in RDS SQL Server.
14. The result is displayed to the user.
15. The `/history` page displays previous moderation records.

Benefits:

- Durable object storage
- Independent of EC2
- Direct integration with Rekognition
- Versioning support
- Lifecycle management
- Scalable storage.

# Project Structure

The following files are currently tracked in this GitHub repository:

```text
image-moderation-project/
│
├── .gitignore
├── app.py
├── requirements.txt
├── test_db.py
│
├── static/
│   └── style.css
│
└── templates/
    ├── base.html
    ├── history.html
    ├── index.html
    └── result.html
```

### Runtime files excluded from GitHub

The following exist on the EC2 application server but are intentionally excluded using `.gitignore`:

```text
.env
venv/
uploads/
__pycache__/
*.pyc
```

`uploads/` contains local/test uploaded images and is not stored in GitHub.

`.env` contains application configuration and is intentionally excluded to prevent credentials or sensitive configuration from being committed.

---


# Technologies Used

| Category | Technology |
|---|---|
| Cloud Platform | AWS |
| Operating System | Amazon Linux |
| Programming Language | Python |
| Framework | Flask |
| Web Server | Nginx |
| WSGI Server | Gunicorn |
| AWS SDK | Boto3 |
| Database Driver | pyodbc |
| Compute | Amazon EC2 |
| Load Balancer | Application Load Balancer |
| Scaling | Auto Scaling Group |
| Storage | Amazon S3 |
| AI / ML Service | Amazon Rekognition |
| Database | Amazon RDS SQL Server |
| CDN | Amazon CloudFront |
| Security | AWS WAF, IAM, Security Groups |
| Networking | VPC, Public/Private Subnets, NAT Gateway |
| Monitoring | Amazon CloudWatch / SNS |


# Troubleshooting Commands

Check Gunicorn service:

```bash
sudo systemctl status image-moderation.service
```

Application logs:

```bash
sudo journalctl -u image-moderation.service -f
```

Test Gunicorn directly:

```bash
curl -i http://127.0.0.1:8000/health
```

Test through Nginx:

```bash
curl -i http://localhost/health
```

Verify IAM identity:

```bash
aws sts get-caller-identity
```

Test S3 access:

```bash
aws s3 ls s3://image-moderation-project/
```

---






