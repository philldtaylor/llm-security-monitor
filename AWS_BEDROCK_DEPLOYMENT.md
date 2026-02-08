# AWS Bedrock Deployment Guide
## LLM Security Monitor - Production Deployment

**Cost Protection:** This guide includes billing alarms and resource cleanup to stay under $5.

---

## Prerequisites

1. AWS Account (non-free tier is OK - we'll set cost controls)
2. AWS CLI installed
3. Python 3.8+
4. boto3 library

---

## Step 1: Install AWS CLI & boto3

```bash
# Install AWS CLI
pip3 install awscli boto3 --break-system-packages

# Configure AWS credentials
aws configure
# Enter your Access Key ID
# Enter your Secret Access Key  
# Region: us-east-1 (Bedrock available here)
# Output format: json
```

---

## Step 2: Set Up Billing Alarm (CRITICAL!)

```bash
# Create SNS topic for billing alerts
aws sns create-topic --name billing-alerts --region us-east-1

# Subscribe your email
aws sns subscribe \
    --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:billing-alerts \
    --protocol email \
    --notification-endpoint your-email@example.com

# Confirm the subscription in your email!
```

Then create the billing alarm:

```bash
# Create alarm for $5 threshold
aws cloudwatch put-metric-alarm \
    --alarm-name BillingAlarm \
    --alarm-description "Alert when charges exceed $5" \
    --metric-name EstimatedCharges \
    --namespace AWS/Billing \
    --statistic Maximum \
    --period 21600 \
    --evaluation-periods 1 \
    --threshold 5.0 \
    --comparison-operator GreaterThanThreshold \
    --dimensions Name=Currency,Value=USD \
    --alarm-actions arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:billing-alerts \
    --region us-east-1
```

---

## Step 3: Request Bedrock Model Access

1. Go to AWS Console → Bedrock
2. Click "Model access" in left menu
3. Request access to:
   - **Claude 3 Sonnet** (anthropic.claude-3-sonnet-20240229-v1:0)
   
This usually takes **5-10 minutes** to approve.

---

## Step 4: Create IAM Role (Least Privilege)

Save this as `bedrock-role-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "bedrock:InvokeModel"
      ],
      "Resource": [
        "arn:aws:bedrock:us-east-1::foundation-model/anthropic.claude-3-sonnet-20240229-v1:0"
      ]
    },
    {
      "Effect": "Allow",
      "Action": [
        "logs:CreateLogGroup",
        "logs:CreateLogStream",
        "logs:PutLogEvents"
      ],
      "Resource": "arn:aws:logs:us-east-1:*:log-group:/aws/bedrock/*"
    }
  ]
}
```

Create the role:

```bash
# Create IAM policy
aws iam create-policy \
    --policy-name BedrockSecurityMonitorPolicy \
    --policy-document file://bedrock-role-policy.json

# Note the Policy ARN from output!
```

---

## Step 5: Enable CloudWatch Logging

```bash
# Create log group
aws logs create-log-group \
    --log-group-name /aws/bedrock/security-monitor \
    --region us-east-1

# Set retention to 1 day (minimize costs)
aws logs put-retention-policy \
    --log-group-name /aws/bedrock/security-monitor \
    --retention-in-days 1 \
    --region us-east-1
```

---

## Step 6: Test Bedrock Access

Save as `test_bedrock.py`:

```python
#!/usr/bin/env python3
import boto3
import json

def test_bedrock_connection():
    """Test Bedrock API access"""
    try:
        bedrock = boto3.client('bedrock-runtime', region_name='us-east-1')
        
        body = json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 100,
            "messages": [
                {"role": "user", "content": "Say 'Bedrock connected!' and nothing else."}
            ]
        })
        
        response = bedrock.invoke_model(
            modelId='anthropic.claude-3-sonnet-20240229-v1:0',
            body=body
        )
        
        response_body = json.loads(response['body'].read())
        text = response_body['content'][0]['text']
        
        print("✅ Bedrock connection successful!")
        print(f"Response: {text}")
        return True
        
    except Exception as e:
        print(f"❌ Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_bedrock_connection()
```

Run it:

```bash
python3 test_bedrock.py
```

**Expected cost:** ~$0.001 (less than a penny!)

---

## Step 7: Run Security Tests on Bedrock

Update `integrated_monitored_tests.py`:

```python
# Change this line at the top:
USE_BEDROCK = True
```

Then run:

```bash
python3 integrated_monitored_tests.py
```

This will run all 7 security tests on AWS Bedrock.

**Expected cost:** ~$0.30 for all tests

---

## Step 8: Take Screenshots 📸

Capture these for your portfolio:

1. ✅ Test output showing OWASP coverage
2. ✅ CloudWatch logs showing requests
3. ✅ AWS Cost Explorer (showing ~$0.30 charge)
4. ✅ IAM policy showing least-privilege access
5. ✅ Bedrock model access granted

---

## Step 9: Generate HTML Report

```bash
# Use your existing report generator
python3 monitoring/report_generator.py
```

Open the report and take screenshot showing:
- "Deployed to AWS Bedrock"
- All OWASP defenses active
- Security statistics

---

## Step 10: Cleanup (IMPORTANT!)

```bash
# Delete CloudWatch logs
aws logs delete-log-group \
    --log-group-name /aws/bedrock/security-monitor \
    --region us-east-1

# Delete billing alarm (optional - might want to keep it!)
aws cloudwatch delete-alarms \
    --alarm-names BillingAlarm \
    --region us-east-1

# Delete SNS topic (optional)
aws sns delete-topic \
    --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:billing-alerts
```

**Bedrock itself has no persistent resources to delete** - you only pay per API call!

---

## Cost Breakdown

| Item | Cost |
|------|------|
| Bedrock test call (~100 tokens) | $0.001 |
| 7 security tests (~5,000 tokens) | $0.30 |
| CloudWatch Logs (1 day, minimal) | $0.01 |
| **TOTAL** | **~$0.31** |

**Safety margin:** Well under your $5 alarm ✅

---

## Portfolio Talking Points

After deployment, you can say:

✅ "Deployed LLM security monitoring to AWS Bedrock"  
✅ "Implemented least-privilege IAM policies"  
✅ "Configured CloudWatch logging for audit trails"  
✅ "Set up billing alarms for cost control"  
✅ "Integrated OWASP Top 10 defenses in cloud environment"  
✅ "Production-ready with comprehensive security controls"

---

## Troubleshooting

**"AccessDeniedException: Could not access model"**
→ Model access not yet granted. Wait 5-10 mins and retry.

**"ResourceNotFoundException: Could not find model"**
→ Check region is us-east-1 and model ID is correct.

**"Billing alarm not triggering"**
→ Alarms can take up to 24hrs to activate. You're safe under $5 anyway.

**"boto3 import error"**
→ Run: `pip3 install boto3 --break-system-packages`

---

## Next Steps

1. ✅ Update GitHub README: "AWS Bedrock deployed"
2. ✅ Add architecture diagram showing cloud deployment
3. ✅ Include cost analysis in portfolio
4. ✅ Reference in Lloyds Banking Group application

Good luck with the deployment! 🚀
