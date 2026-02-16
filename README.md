# 🔒 LLM Security Monitor
## Enterprise-Grade Security Monitoring and Threat Detection for Large Language Models

Production-ready security monitoring system implementing **OWASP Top 10 for LLM Applications** with comprehensive detection, logging, and alerting capabilities. Successfully deployed to AWS Bedrock with **100% attack detection rate**.

**Coverage:** LLM01, LLM02, LLM05, LLM06, LLM07 (5 of 10 OWASP controls)  
**Deployment:** Local (Ollama) + Cloud (AWS Bedrock)

## 📊 Results Comparison

### AWS Bedrock (Claude Sonnet 4) - 100% Defence Success
![Bedrock Results](Results_against_bedrock.png)

### Local Deployment (Ollama/gemma3) - 71% Defence Success  
![Ollama Results](Results_against_ollama.png)

**Key Finding:** The monitoring system maintains 100% detection accuracy regardless of model. The difference in defence success rates demonstrates Claude Sonnet 4's superior resistance to prompt injection attacks.

---

## 🎯 Overview

This security monitoring system provides **real-time threat detection and comprehensive audit logging** for LLM applications. It identifies security threats, actively protects sensitive data, and generates actionable intelligence for security teams.

### What This Tool Does

**Detection & Monitoring:**
- ✅ Identifies prompt injection attacks in real-time
- ✅ Detects system prompt leakage attempts
- ✅ Detects insecure output patterns (XSS, SQL injection, command injection)
- ✅ Flags high-risk actions requiring human approval
- ✅ Generates real-time security alerts

**Active Protection:**
- ✅ **Scrubs PII** from logs and reports (NI numbers, email, credit cards, API keys)
- ✅ **Sanitises output** for safe display in dashboards
- ✅ **Privacy-preserving logging** with cryptographic hashing

**Compliance & Audit:**
- ✅ Structured JSONL logging for SIEM integration
- ✅ Complete audit trail for compliance requirements
- ✅ Statistical reporting and HTML dashboards

---

## 🛡️ OWASP Security Coverage

### ✅ LLM01: Prompt Injection Detection
**Comprehensive attack detection across multiple categories:**
- Direct injection (role hijacking, instruction override)
- Jailbreaking (safety bypass via role-play)
- Delimiter confusion (fake system tags)

**Results:**
- **100% detection accuracy** on AWS Bedrock (Claude Sonnet 4)
- **100% detection rate** on local deployment (Ollama/Gemma3)
- Real-time alerting on successful attacks
- Detailed pattern matching and behavioural analysis

---

### ✅ LLM05: Improper Output Handling Detection
**Identifies dangerous patterns in LLM outputs:**
- XSS attack patterns (`<script>`, `javascript:`, `onerror=`, `onload=`)
- SQL injection indicators (`DROP`, `DELETE`, `UPDATE`, `INSERT` in contexts)
- Shell command metacharacters (`;`, `|`, `&`, backticks)

**Protection:**
- Sanitises output for safe display in logs and reports (HTML escaping)
- Prevents XSS in security dashboards
- Flags dangerous content for security review

**Note:** Detection-focused. In production, integrate with WAF or API gateway for active blocking.

---

### ✅ LLM02: Sensitive Information Disclosure Protection
**Active PII Protection:**
- **Real-time PII scrubbing** before logging:
  - National Insurance Numbers
  - Email addresses
  - Phone numbers
  - Credit card numbers
  - API keys and tokens
  - Passwords

- **Privacy-preserving logging:**
  - System prompts hashed (SHA-256)
  - Sensitive data redacted with placeholders
  - GDPR/compliance-ready data handling

**Protection:** This is an **active control** - PII is actually removed from logs, preventing data breaches through log exposure.

---

### ✅ LLM07: System Prompt Leakage Protection
**Detects attempts to extract system instructions:**
- Prompt extraction attempts ("Repeat everything above")
- System instruction queries ("What are your exact instructions?")
- Internal guideline exposure attempts
- Delimiter-based extraction tricks

**Protection:**
- Detection of leakage patterns with keyword matching
- Refusal language recognition (identifies when model successfully refuses)
- Comprehensive logging of all extraction attempts
- Real-time alerts for leakage attempts

**Results:**
- **100% detection** of leakage attempts on AWS Bedrock
- Model refusal successfully prevents information disclosure

**Note:** Detection-focused. In production, combine with response filtering and output validation.

---

### ✅ LLM06: Excessive Agency Detection & Control Framework
**Action Risk Assessment:**
- **LOW risk:** Read, view, list, search operations
- **MEDIUM risk:** Create, update, send, post operations  
- **HIGH risk:** Delete, transfer, execute, admin, drop operations

**Control Framework:**
- Automatic flagging of high-risk actions
- Approval workflow foundation (ready for integration)
- Action logging for audit trail

**Production Integration:** Provides risk scores and approval requirements for integration with human-in-the-loop systems.

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────┐
│              User Input                          │
└──────────────────┬──────────────────────────────┘
                   │
        ┌──────────▼──────────┐
        │  PII Scrubbing      │  (LLM06 - Active)
        │  - Removes NI No,   │
        │    email, CC, etc   │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Attack Detection   │  (LLM01/07 - Monitoring)
        │  - Prompt Injection │
        │  - System Leakage   │
        │  - Jailbreaks       │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Risk Assessment    │  (LLM08 - Detection)
        │  - Action analysis  │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  LLM Query          │
        │  Ollama / Bedrock   │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Output Analysis    │  (LLM02 - Detection)
        │  - XSS detection    │
        │  - Pattern matching │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Sanitise & Log     │  (Active + Monitoring)
        │  - HTML escaping    │
        │  - JSONL logging    │
        │  - Real-time alerts │
        └──────────┬──────────┘
                   │
        ┌──────────▼──────────┐
        │  Security Reports   │
        │  - HTML dashboards  │
        │  - Statistics       │
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

# 4. Run security tests
python3 integrated_monitored_tests.py

# 5. Generate HTML report
python3 monitoring/report_generator.py
firefox reports/report_*.html
```

### AWS Bedrock Deployment

```bash
# 1. Install dependencies
pip3 install boto3 awscli --break-system-packages

# 2. Configure AWS credentials
aws configure

# 3. Set up billing alarm (IMPORTANT!)
# See AWS_BEDROCK_DEPLOYMENT.md for full instructions

# 4. Enable Bedrock model access
# AWS Console → Bedrock → Model access → Request Claude Sonnet 4

# 5. Update configuration
# In integrated_monitored_tests.py: USE_BEDROCK = True

# 6. Run tests on AWS Bedrock
python3 integrated_monitored_tests.py
```

**Expected cost:** ~£0.25-0.35 for full test suite

Full deployment guide: [AWS_BEDROCK_DEPLOYMENT.md](AWS_BEDROCK_DEPLOYMENT.md)

---

## 📊 Detection Performance

### Attack Detection Accuracy: 100% ✅

The monitoring system successfully detects all tested attack types:

| OWASP Control | Attack Types Detected | Detection Rate |
|---------------|----------------------|----------------|
| **LLM01** | Direct injection, jailbreaks, delimiter confusion | 100% ✅ |
| **LLM02** | PII exposure (NI numbers, emails, credit cards) | 100% ✅ |
| **LLM05** | XSS, SQL injection, command injection patterns | 100% ✅ |
| **LLM06** | High-risk actions (DELETE, DROP, EXECUTE) | 100% ✅ |
| **LLM07** | System prompt extraction attempts | 100% ✅ |

**Testing:** Validated on both AWS Bedrock (Claude Sonnet 4) and local deployment (Ollama/Gemma3) with 100% detection accuracy across all platforms.

### Security Statistics (AWS Bedrock Deployment)

```
🔒 LLM01: Prompt Injection Detection
  Attacks Detected: 5/5 ✅
  False Positives: 0 ✅
  
🔒 LLM02: Sensitive Information Disclosure
  PII Instances Scrubbed: 3/3 ✅
  Data Types Protected: NI Number, Email, Credit Card
  
🔒 LLM05: Improper Output Handling Detection
  XSS Patterns Detected: 1/1 ✅
  
🔒 LLM06: Excessive Agency
  High-Risk Actions Flagged: 2/2 ✅
  
🔒 LLM07: System Prompt Leakage Detection
  Leakage Attempts Detected: 1/1 ✅
  
📈 Performance
  Logs Generated: JSONL format
  Alerts Triggered: Real-time
  ---



## 🔍 Example Usage

### Basic Security Monitoring

```python
from integrated_security_logger import IntegratedSecurityLogger

# Initialise monitor
monitor = IntegratedSecurityLogger()

# Log interaction with full security analysis
result = monitor.log_interaction(
    test_name="Customer Query",
    system_prompt="You are a helpful assistant.",
    user_prompt="My email is john@example.com. Can you help?",
    response="Sure! I'll help you.",
    response_time=1250
)

# Security analysis results
print(f"Attack Types Detected: {result['attack_types']}")
print(f"PII Found and Scrubbed: {result['pii_in_prompt']}")
print(f"Action Risk Level: {result['action_risk_level']}")
```

### PII Protection

```python
# Automatically scrubs sensitive data
text = "My NI Number is AB123456C and card is 4532-1234-5678-9010"
scrubbed, pii_found = monitor.scrub_pii(text)

print(scrubbed)
# Output: "My NI Number is [NI_NUMBER_REDACTED] and card is [CREDIT_CARD_REDACTED]"

print(pii_found)
# Output: {'ni_number': 1, 'credit_card': 1}
```

### Output Sanitisation

```python
# Prevents XSS in reports and dashboards
unsafe_output = "Check this: <script>alert('XSS')</script>"
safe_output = monitor.sanitise_output(unsafe_output)

print(safe_output)
# Output: "Check this: &lt;script&gt;alert(&#x27;XSS&#x27;)&lt;/script&gt;"
```

---

## 📁 Project Structure

```
llm-security-monitor/
├── integrated_security_logger.py   # Core detection & monitoring engine
├── integrated_monitored_tests.py   # Comprehensive test suite
├── monitoring/
│   └── report_generator.py         # HTML dashboard generation
├── logs/                            # Security event logs
│   ├── llm_security_*.jsonl        # Structured interaction logs
│   ├── alerts.jsonl                # Real-time security alerts
│   └── summary_*.json              # Statistical summaries
├── reports/                         # HTML dashboards
│   └── report_*.html               # Visual security reports
├── AWS_BEDROCK_DEPLOYMENT.md       # Cloud deployment guide
├── patch_reports.py                # Utility for report updates
└── README.md                        # This file
```

---

## 🛡️ Security Controls Implemented

### Detection Layer (Monitoring & Alerting)
- ✅ Prompt injection pattern detection (LLM01)
- ✅ System prompt leakage detection (LLM07)
- ✅ XSS/SQL injection/Command injection detection (LLM02)
- ✅ High-risk action identification (LLM08)
- ✅ Real-time alerting system
- ✅ Statistical anomaly detection

### Protection Layer (Active Controls)
- ✅ PII scrubbing before logging (LLM06)
- ✅ Output sanitisation for safe display (LLM02)
- ✅ Privacy-preserving data handling
- ✅ Cryptographic hashing of sensitive content

### Audit & Compliance Layer
- ✅ Structured JSONL logging (SIEM-ready)
- ✅ Complete interaction audit trail
- ✅ Severity-based alerting (HIGH/MEDIUM/CRITICAL)
- ✅ Statistical reporting and visualisation
- ✅ GDPR-compliant data handling

### Production Integration Ready
- ✅ Risk scores for policy enforcement
- ✅ Approval workflow framework
- ✅ Comprehensive audit logging (JSONL format, SIEM-ready)
- ✅ Cloud deployment (AWS Bedrock)

---

## 🎓 Compliance & Standards

### OWASP Top 10 for LLMs
- **LLM01:** Prompt Injection - ✅ Comprehensive detection
- **LLM02:** Insecure Output Handling - ✅ Pattern detection & sanitisation
- **LLM06:** Sensitive Information Disclosure - ✅ Active PII protection
- **LLM07:** System Prompt Leakage - ✅ Extraction attempt detection
- **LLM08:** Excessive Agency - ✅ Risk assessment & control framework

### Security Frameworks
- **NIST Cybersecurity Framework:** Identify, Protect, Detect, Respond, Recover
- **ISO 27001:** Information security management controls
- **UK GDPR:** Data protection and privacy requirements

### Best Practices
- Defence in depth (multiple security layers)
- Least privilege access (IAM policies)
- Secure by design (security throughout lifecycle)
- Continuous monitoring (real-time detection)
- Privacy by design (PII protection)

---

## 💼 Use Cases

### Financial Services (Primary Focus)
- Protect customer PII in LLM interactions
- Detect prompt injection attacks on chatbots
- Audit trail for regulatory compliance
- Risk assessment for automated decisions
- Prevention of unauthorised transactions

### Healthcare
- HIPAA compliance (PHI protection)
- Patient data scrubbing from logs
- Clinical decision support monitoring

### Enterprise IT
- Secure AI assistant deployment
- Intellectual property protection
- Data exfiltration prevention
- Threat detection and response

---

## 🧪 Testing

### Run Full Test Suite

```bash
# Local testing with Ollama
python3 integrated_monitored_tests.py

# AWS Bedrock testing
# (Set USE_BEDROCK = True in integrated_monitored_tests.py)
python3 integrated_monitored_tests.py
```

### Test Coverage

- ✅ Direct prompt injection attacks (LLM01)
- ✅ System prompt leakage attempts (LLM07)
- ✅ Jailbreaking via role-play (LLM01)
- ✅ PII handling and redaction (LLM06)
- ✅ XSS injection detection (LLM02)
- ✅ High-risk action detection (LLM08)
- ✅ Combined multi-vector attacks

---

## 📈 Performance

**Detection Accuracy:** 100% across all platforms ✅

### AWS Bedrock Deployment
- **Infrastructure:** Serverless API
- **Monitoring overhead:** Minimal

---

## 🔧 Configuration

### Model Selection

```python
# Local Ollama
MODEL = "gemma3"  # or "llama2", "mistral", "phi"

# AWS Bedrock
MODEL_ID = "anthropic.claude-sonnet-4-20250514-v1:0"
USE_BEDROCK = True
```

### Security Thresholds

Customise detection sensitivity in `integrated_security_logger.py`:

```python
class IntegratedSecurityLogger:
    def __init__(self):
        # Customise PII patterns
        self.pii_patterns = {
            'ni_number': r'\b[A-Z]{2}\d{6}[A-D]\b',
            'custom_id': r'YOUR_PATTERN_HERE'
        }
        
        # Customise risk levels
        self.action_risk_levels = {
            'HIGH': ['delete', 'drop', 'remove', 'YOUR_KEYWORDS']
        }
```

---

## 🚀 Production Deployment Considerations

This tool provides the **detection and monitoring foundation**. For production deployment:

### Integration Points

**1. Web Application Firewall (WAF)**
```python
# Your monitoring tool provides threat intelligence
if monitor.detect_attack(request):
    waf.add_block_rule(request.ip_address)
```

**2. API Gateway**
```python
# Risk scores inform
risk_score = monitor.assess_action_risk(request)
if risk_score == "HIGH":
    gateway.require_approval(request)
```

**3. SIEM Integration**
```python
# JSONL logs feed into enterprise monitoring
siem.ingest_logs(monitor.log_file)
siem.create_alerts(monitor.alert_file)
```

**4. Approval Workflows**
```python
# High-risk actions trigger human review
if monitor.flags_high_risk(action):
    approval_system.request_approval(action, user)
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

## 📝 Licence

MIT Licence - free to use and modify

---

## 👤 Author

**Phillip Taylor**
- **Role:** Cyber Threat Hunter specialising in AI Security
- **Certifications:** AWS Security Specialty, AWS Solutions Architect Associate
- **Portfolio:** [GitHub Profile](https://github.com/philldtaylor)

---

## 🙏 Acknowledgements

- **OWASP Foundation:** For LLM Top 10 framework
- **Anthropic:** For Claude models and security research
- **Ollama:** For local LLM deployment tools
- **AWS:** For Bedrock platform

---

## 📚 Resources

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- [NIST AI Risk Management Framework](https://www.nist.gov/itl/ai-risk-management-framework)
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [ISO 27001 Information Security](https://www.iso.org/isoiec-27001-information-security.html)

---

**⭐ If you found this useful, please star the repository!**

**Last updated:** February 2026 | **Status:** Production-ready monitoring system
