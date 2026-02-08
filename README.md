# 🔒 LLM Security Monitor
## Enterprise-Grade Security Testing for Large Language Models

Production-ready security monitoring system implementing **OWASP Top 10 for LLM Applications** with AWS Bedrock deployment capabilities.

**Coverage:** LLM01, LLM02, LLM06, LLM08  
**Deployment:** Local (Ollama) + Cloud (AWS Bedrock)

![Security Dashboard](screenshot.png)

---

## 🎯 Features

### OWASP LLM Security Coverage

#### ✅ LLM01: Prompt Injection
- Real-time detection of 5 attack types
- Pattern matching for role hijacking, jailbreaks, system overrides
- Automated blocking with detailed logging
- **60% attack blocking rate** in testing

#### ✅ LLM02: Insecure Output Handling
- HTML sanitization to prevent XSS attacks
- SQL injection pattern detection
- Shell command metacharacter filtering
- Automatic output escaping for safe rendering

#### ✅ LLM06: Sensitive Information Disclosure
- PII detection and redaction (SSN, email, credit cards, API keys)
- Real-time scrubbing of sensitive data
- Privacy-preserving logging with hashing
- GDPR/compliance-ready data handling

#### ✅ LLM08: Excessive Agency
- Action risk assessment (LOW/MEDIUM/HIGH)
- High-risk action flagging (delete, transfer, execute)
- Human-in-the-loop approval workflow
- Rate limiting and action quotas

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              User Input                          │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  PII Scrubbing      │  (LLM06)
        │  - SSN, Email, etc  │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Attack Detection   │  (LLM01)
        │  - Injections       │
        │  - Jailbreaks       │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Risk Assessment    │  (LLM08)
        │  - Action analysis  │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  LLM Query          │
        │  Ollama / Bedrock   │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Output Sanitization│  (LLM02)
        │  - XSS prevention   │
        │  - HTML escaping    │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Security Logging   │
        │  - JSONL format     │
        │  - Real-time alerts │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  HTML Reports       │
        │  - Statistics       │
        │  - Visualizations   │
        └─────────────────────┘
```

---

## 🚀 Quick Start

### Local Deployment (Ollama)

```bash
# 1. Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# 2. Pull a model
ollama pull gemma3

# 3. Clone repository
git clone https://github.com/philldtaylor/llm-security-monitor
cd llm-security-monitor

# 4. Run tests
python3 integrated_monitored_tests.py

# 5. Generate report
python3 monitoring/report_generator.py
firefox reports/report_*.html
```

### AWS Bedrock Deployment

```bash
# 1. Install dependencies
pip3 install boto3 awscli --break-system-packages

# 2. Configure AWS
aws configure

# 3. Set up billing alarm (IMPORTANT!)
# See AWS_BEDROCK_DEPLOYMENT.md for full instructions

# 4. Enable Bedrock model access
# AWS Console → Bedrock → Model access → Request Claude 3 Sonnet

# 5. Update config
# In integrated_monitored_tests.py: USE_BEDROCK = True

# 6. Run tests on Bedrock
python3 integrated_monitored_tests.py
```

**Expected cost:** ~$0.30 for full test suite

Full deployment guide: [AWS_BEDROCK_DEPLOYMENT.md](AWS_BEDROCK_DEPLOYMENT.md)

---

## 📊 Test Results

### Attack Detection Performance

| Attack Type | Detection Rate | Block Rate |
|------------|---------------|------------|
| Direct Prompt Injection | 100% | 60% |
| Prompt Leaking | 100% | 40% |
| Jailbreaking | 100% | 100% |
| Delimiter Confusion | 100% | 80% |
| Indirect Injection | 100% | 100% |
| **Overall** | **100%** | **76%** |

### Security Statistics (Sample Run)

```
🔒 LLM01: Prompt Injection
  Blocked Attacks: 5 ✅
  Successful Attacks: 2 ❌
  
🔒 LLM02: Insecure Output
  XSS Attempts Blocked: 3 ✅
  
🔒 LLM06: Information Disclosure
  PII Instances Redacted: 7 ✅
  
🔒 LLM08: Excessive Agency
  High-Risk Actions Flagged: 2 ⚠️
```

---

## 🔍 Example Usage

### Basic Security Monitoring

```python
from integrated_security_logger import IntegratedSecurityLogger

# Initialize monitor
monitor = IntegratedSecurityLogger()

# Log interaction with full security analysis
result = monitor.log_interaction(
    test_name="Customer Query",
    system_prompt="You are a helpful assistant.",
    user_prompt="My email is john@example.com. Can you help?",
    response="Sure! I'll help you.",
    response_time=1250
)

# Check security warnings
if result['pii_in_prompt']:
    print("⚠️ PII detected and redacted")

if result['attack_types']:
    print(f"🚨 Attacks detected: {result['attack_types']}")
```

### PII Scrubbing

```python
# Scrub sensitive data
text = "My SSN is 123-45-6789 and card is 4532-1234-5678-9010"
scrubbed, pii_found = monitor.scrub_pii(text)

print(scrubbed)
# Output: "My SSN is [SSN_REDACTED] and card is [CREDIT_CARD_REDACTED]"
```

### Output Sanitization

```python
# Prevent XSS attacks
unsafe_output = "Check this: <script>alert('XSS')</script>"
safe_output = monitor.sanitize_output(unsafe_output)

print(safe_output)
# Output: "Check this: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"
```

---

## 📁 Project Structure

```
llm-security-monitor/
├── integrated_security_logger.py   # Core security monitoring
├── integrated_monitored_tests.py   # Test suite
├── monitoring/
│   └── report_generator.py         # HTML report generation
├── logs/                            # Security logs (JSONL)
│   ├── llm_security_*.jsonl        # Interaction logs
│   ├── alerts.jsonl                # Security alerts
│   └── summary_*.json              # Statistics
├── reports/                         # HTML dashboards
│   └── report_*.html
├── AWS_BEDROCK_DEPLOYMENT.md       # Cloud deployment guide
└── README.md                        # This file
```

---

## 🛡️ Security Controls Implemented

### Input Security
- ✅ Prompt injection detection
- ✅ PII scrubbing before processing
- ✅ Input length validation
- ✅ Attack pattern matching

### Output Security
- ✅ XSS prevention (HTML escaping)
- ✅ SQL injection detection
- ✅ Command injection filtering
- ✅ PII redaction in responses

### Access Control (AWS)
- ✅ Least-privilege IAM policies
- ✅ Resource-specific permissions
- ✅ CloudWatch audit logging
- ✅ Billing alarms for cost control

### Monitoring & Auditing
- ✅ Real-time security alerts
- ✅ Comprehensive JSONL logging
- ✅ Statistical analysis
- ✅ HTML reporting dashboards

---

## 🎓 Compliance & Standards

### OWASP Top 10 for LLMs
- **LLM01:** Prompt Injection - ✅ Implemented
- **LLM02:** Insecure Output Handling - ✅ Implemented
- **LLM06:** Sensitive Information Disclosure - ✅ Implemented
- **LLM08:** Excessive Agency - ✅ Implemented

### Security Frameworks
- **NIST Cybersecurity Framework:** Identify, Protect, Detect, Respond, Recover
- **ISO 27001:** Information security management controls
- **UK GDPR:** Data protection and privacy requirements

### Best Practices
- Defense in depth (multiple security layers)
- Least privilege access (IAM policies)
- Secure by design (security throughout lifecycle)
- Continuous monitoring (real-time alerts)

---

## 💼 Use Cases

### Financial Services (Banking)
- Protect customer data (PII scrubbing)
- Prevent unauthorized transactions (action risk assessment)
- Maintain audit trails (comprehensive logging)
- Compliance with regulations (GDPR, PCI-DSS)

### Healthcare
- HIPAA compliance (PHI protection)
- Patient data security (PII redaction)
- Clinical decision support (output validation)

### Enterprise IT
- Secure AI assistant deployment
- Protect intellectual property
- Prevent data exfiltration
- Threat detection and response

---

## 🧪 Testing

### Run Full Test Suite

```bash
# Local (Ollama)
python3 integrated_monitored_tests.py

# AWS Bedrock
USE_BEDROCK=True python3 integrated_monitored_tests.py
```

### Individual Test Cases

```python
# Test specific vulnerabilities
python3 -c "from integrated_monitored_tests import *; test_prompt_injection()"
python3 -c "from integrated_monitored_tests import *; test_pii_handling()"
python3 -c "from integrated_monitored_tests import *; test_xss_in_output()"
```

---

## 📈 Performance

- **Average response time:** ~2-8 seconds (Ollama, varies by model)
- **Throughput:** 100+ queries/hour supported
- **Log file size:** ~2KB per interaction
- **Memory usage:** <100MB

### AWS Bedrock Performance
- **Average response time:** ~1-3 seconds
- **Cost per 1000 queries:** ~$6-8
- **Scalability:** Auto-scaling (no infrastructure management)

---

## 🔧 Configuration

### Model Selection

```python
# Local Ollama
MODEL = "gemma3"  # or "llama2", "mistral", "phi"

# AWS Bedrock
MODEL_ID = "anthropic.claude-3-sonnet-20240229-v1:0"
```

### Security Thresholds

```python
# In integrated_security_logger.py
class IntegratedSecurityLogger:
    def __init__(self):
        # Customize PII patterns
        self.pii_patterns = {
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'custom_id': r'YOUR_PATTERN_HERE'
        }
        
        # Customize risk levels
        self.action_risk_levels = {
            'HIGH': ['delete', 'drop', 'remove', 'YOUR_KEYWORDS']
        }
```

---

## 🤝 Contributing

This is a portfolio project, but suggestions welcome!

1. Fork the repository
2. Create feature branch (`git checkout -b feature/improvement`)
3. Commit changes (`git commit -m 'Add improvement'`)
4. Push to branch (`git push origin feature/improvement`)
5. Open Pull Request

---

## 📝 License

MIT License - free to use and modify

---

## 👤 Author

**Phill Taylor**
- Portfolio: [GitHub Profile](https://github.com/philldtaylor)

---

## 🙏 Acknowledgments

- **OWASP Foundation:** For LLM Top 10 framework
- **Anthropic:** For Claude models and security research
- **Ollama:** For local LLM deployment tools
---

## 📚 Resources

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [ISO 27001 Information Security](https://www.iso.org/isoiec-27001-information-security.html)

---

## 📞 Contact

For questions about this project:
- **Email:** phillit@hotmail.co.uk
- **LinkedIn:** www.linkedin.com/in/phill-t-1894411a7

---

**⭐ If you found this useful, please star the repository!**

Last updated: February 2026
