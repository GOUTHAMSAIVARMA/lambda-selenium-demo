#!/usr/bin/env python3
"""
Simple script to invoke Lambda function and run tests
"""
import boto3
import json
import sys
import argparse

FUNCTION_NAME = 'selenium-playwright-test'
REGION = 'us-east-1'

def invoke_test(test_type='selenium'):
    """Invoke Lambda function with specified test type"""
    lambda_client = boto3.client('lambda', region_name=REGION)
    
    print(f"🚀 Invoking Lambda function: {FUNCTION_NAME}")
    print(f"📝 Test type: {test_type}\n")
    
    try:
        response = lambda_client.invoke(
            FunctionName=FUNCTION_NAME,
            InvocationType='RequestResponse',
            Payload=json.dumps({'test_type': test_type})
        )
        
        # Parse response
        result = json.loads(response['Payload'].read())
        status_code = result.get('statusCode', 500)
        body = json.loads(result.get('body', '{}'))
        
        # Display results
        print("=" * 60)
        print(f"Status Code: {status_code}")
        print(f"Test Type: {body.get('test_type', 'unknown')}")
        print(f"Status: {body.get('status', 'unknown')}")
        print("=" * 60)
        
        if 'page_title' in body:
            print(f"✓ Page Title: {body['page_title']}")
        
        if 'output' in body:
            print(f"\n📊 Test Output:\n{body['output']}")
        
        if 'error' in body:
            print(f"\n❌ Error: {body['error']}")
        
        print("\n✓ Invocation completed successfully!")
        return status_code == 200
        
    except Exception as e:
        print(f"❌ Error invoking Lambda: {str(e)}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Invoke AWS Lambda function to run browser tests'
    )
    parser.add_argument(
        '--test',
        choices=['selenium', 'playwright', 'both'],
        default='both',
        help='Type of test to run (default: both)'
    )
    
    args = parser.parse_args()
    
    if args.test == 'both':
        print("Running both Selenium and Playwright tests...\n")
        selenium_result = invoke_test('selenium')
        print("\n" + "=" * 60 + "\n")
        playwright_result = invoke_test('playwright')
        
        if selenium_result and playwright_result:
            print("\n✓✓✓ All tests passed! ✓✓✓")
            sys.exit(0)
        else:
            print("\n❌ Some tests failed")
            sys.exit(1)
    else:
        success = invoke_test(args.test)
        sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
