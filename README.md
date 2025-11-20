# AWS Lambda Selenium & Playwright Testing

A complete implementation of browser automation testing using Selenium and Playwright in AWS Lambda with Docker containers.

## 🎯 Features

- ✅ Docker-based AWS Lambda function
- ✅ Selenium WebDriver with headless Chrome
- ✅ Playwright browser automation
- ✅ Pytest test framework integration
- ✅ Automated deployment with boto3
- ✅ ECR container registry setup
- ✅ Chrome/Chromium pre-installed in container

## 📁 Project Structure
```
lambda-selenium-demo/
├── Dockerfile              # Lambda container with Chrome
├── lambda_function.py      # Lambda handler function
├── deploy.py              # Automated deployment script
├── requirements.txt       # Python dependencies
└── tests/
    ├── test_selenium.py   # Selenium pytest tests
    └── test_playwright.py # Playwright pytest tests
```

## 🚀 Quick Start

### Prerequisites
- AWS CLI configured with credentials
- Docker installed
- Python 3.11+
- boto3 installed

### Deployment Steps

1. **Clone the repository**
```bash
git clone https://github.com/YOUR_USERNAME/lambda-selenium-demo.git
cd lambda-selenium-demo
```

2. **Build Docker image**
```bash
docker build -t lambda-selenium .
```

3. **Deploy to AWS Lambda**
```bash
python deploy.py
```

This script will:
- Create ECR repository
- Build and push Docker image
- Create IAM role for Lambda
- Create/update Lambda function
- Run test invocations

## 🧪 Testing

### Invoke Lambda with Selenium test:
```bash
aws lambda invoke \
  --function-name selenium-playwright-test \
  --payload '{"test_type": "selenium"}' \
  response.json
```

### Invoke Lambda with Playwright test:
```bash
aws lambda invoke \
  --function-name selenium-playwright-test \
  --payload '{"test_type": "playwright"}' \
  response.json
```

## 📋 Configuration

Lambda function settings:
- **Memory**: 2048 MB
- **Timeout**: 300 seconds
- **Runtime**: Python 3.11 (container)
- **Architecture**: x86_64

## 🛠️ Technologies Used

- **AWS Lambda** - Serverless compute
- **AWS ECR** - Container registry
- **Docker** - Containerization
- **Selenium** - Browser automation
- **Playwright** - Modern browser automation
- **Pytest** - Testing framework
- **Chrome/Chromium** - Headless browser
- **Boto3** - AWS SDK for Python

## 📝 Notes

- Chrome and ChromeDriver versions are compatible
- Optimized for Lambda's execution environment
- Handles headless browser configurations
- Memory optimized for browser operations

## 👤 Author

**Goutham**

---

*This is a demonstration project showing AWS Lambda integration with browser automation tools.*
