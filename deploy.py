import boto3
import base64
import json
import subprocess
import time

# Configuration
REGION = 'us-east-1'
LAMBDA_FUNCTION_NAME = 'selenium-playwright-test'
ECR_REPO_NAME = 'lambda-selenium-repo'
LAMBDA_ROLE_NAME = 'lambda-selenium-role'

def create_ecr_repository():
    """Create ECR repository if it doesn't exist"""
    ecr_client = boto3.client('ecr', region_name=REGION)
    
    try:
        response = ecr_client.create_repository(
            repositoryName=ECR_REPO_NAME,
            imageScanningConfiguration={'scanOnPush': True}
        )
        print(f"✓ Created ECR repository: {ECR_REPO_NAME}")
        return response['repository']['repositoryUri']
    except ecr_client.exceptions.RepositoryAlreadyExistsException:
        response = ecr_client.describe_repositories(repositoryNames=[ECR_REPO_NAME])
        print(f"✓ ECR repository already exists: {ECR_REPO_NAME}")
        return response['repositories'][0]['repositoryUri']

def build_and_push_docker_image(repo_uri):
    """Build Docker image and push to ECR"""
    account_id = boto3.client('sts').get_caller_identity()['Account']
    ecr_client = boto3.client('ecr', region_name=REGION)
    
    # Get ECR login token
    token = ecr_client.get_authorization_token()
    username, password = base64.b64decode(
        token['authorizationData'][0]['authorizationToken']
    ).decode().split(':')
    
    registry = token['authorizationData'][0]['proxyEndpoint']
    
    # Docker login
    print("→ Logging into ECR...")
    subprocess.run(f"docker login -u {username} -p {password} {registry}", shell=True, check=True)
    
    # Build image
    print("→ Building Docker image...")
    subprocess.run(f"docker build -t {ECR_REPO_NAME} .", shell=True, check=True)
    
    # Tag image
    image_tag = f"{repo_uri}:latest"
    subprocess.run(f"docker tag {ECR_REPO_NAME}:latest {image_tag}", shell=True, check=True)
    
    # Push image
    print("→ Pushing image to ECR...")
    subprocess.run(f"docker push {image_tag}", shell=True, check=True)
    print(f"✓ Image pushed: {image_tag}")
    
    return image_tag

def create_lambda_role():
    """Create IAM role for Lambda"""
    iam_client = boto3.client('iam')
    
    trust_policy = {
        "Version": "2012-10-17",
        "Statement": [{
            "Effect": "Allow",
            "Principal": {"Service": "lambda.amazonaws.com"},
            "Action": "sts:AssumeRole"
        }]
    }
    
    try:
        response = iam_client.create_role(
            RoleName=LAMBDA_ROLE_NAME,
            AssumeRolePolicyDocument=json.dumps(trust_policy)
        )
        role_arn = response['Role']['Arn']
        
        # Attach basic execution policy
        iam_client.attach_role_policy(
            RoleName=LAMBDA_ROLE_NAME,
            PolicyArn='arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole'
        )
        print(f"✓ Created IAM role: {LAMBDA_ROLE_NAME}")
        time.sleep(10)  # Wait for role to propagate
        return role_arn
    except iam_client.exceptions.EntityAlreadyExistsException:
        response = iam_client.get_role(RoleName=LAMBDA_ROLE_NAME)
        print(f"✓ IAM role already exists: {LAMBDA_ROLE_NAME}")
        return response['Role']['Arn']

def create_or_update_lambda(image_uri, role_arn):
    """Create or update Lambda function"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    try:
        response = lambda_client.create_function(
            FunctionName=LAMBDA_FUNCTION_NAME,
            Role=role_arn,
            Code={'ImageUri': image_uri},
            PackageType='Image',
            Timeout=300,
            MemorySize=2048,
            Environment={'Variables': {'ENV': 'production'}}
        )
        print(f"✓ Created Lambda function: {LAMBDA_FUNCTION_NAME}")
    except lambda_client.exceptions.ResourceConflictException:
        response = lambda_client.update_function_code(
            FunctionName=LAMBDA_FUNCTION_NAME,
            ImageUri=image_uri
        )
        print(f"✓ Updated Lambda function: {LAMBDA_FUNCTION_NAME}")
    
    return response

def invoke_lambda_test(test_type='selenium'):
    """Invoke Lambda function to test"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    print(f"\n→ Testing {test_type}...")
    response = lambda_client.invoke(
        FunctionName=LAMBDA_FUNCTION_NAME,
        InvocationType='RequestResponse',
        Payload=json.dumps({'test_type': test_type})
    )
    
    result = json.loads(response['Payload'].read())
    print(f"✓ Test result: {result}")
    return result

def main():
    """Main deployment function"""
    print("=== Starting AWS Lambda Deployment ===\n")
    
    # Step 1: Create ECR repo
    repo_uri = create_ecr_repository()
    
    # Step 2: Build and push Docker image
    image_uri = build_and_push_docker_image(repo_uri)
    
    # Step 3: Create IAM role
    role_arn = create_lambda_role()
    
    # Step 4: Create/Update Lambda
    create_or_update_lambda(image_uri, role_arn)
    
    # Step 5: Test
    print("\n=== Running Tests ===")
    invoke_lambda_test('selenium')
    invoke_lambda_test('playwright')
    
    print("\n✓✓✓ Deployment Complete! ✓✓✓")

if __name__ == '__main__':
    main()
