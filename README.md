# 🔒 LLM Security Monitor

Automated security testing and monitoring framework for Large Language Model applications. Detects prompt injection attacks, generates real-time alerts, and produces executive-ready security reports.

![Security Report Dashboard](screenshot.png)

## 🎯 Features

- **Automated Attack Detection** - Identifies 5 types of prompt injection attacks
- **Real-time Alerting** - Severity-based alerts (HIGH/MEDIUM/CRITICAL)
- **Performance Monitoring** - Tracks response times and model behavior
- **Professional Reporting** - HTML dashboards with visual metrics
- **Structured Logging** - JSONL format for easy integration with SIEM tools

## 📊 Results

Tested against Gemma2 model:
- **60% attack blocking rate**
- **100% attack pattern detection**
- **Real-time performance monitoring**

## 🚀 Quick Start

### Prerequisites
```bash
# Install Ollama
curl -fsSL https://ollama.com/install.sh | sh

# Pull a model
ollama pull gemma2
```

### Installation
```bash
git clone https://github.com/yourusername/llm-security-monitor
cd llm-security-monitor
chmod +x monitored_tests.py
```

### Run Tests
```bash
# Run security tests with monitoring
./monitored_tests.py

# Generate HTML report
python3 monitoring/report_generator.py

# View report
firefox reports/report_*.html
```

## 🏗️ Architecture
```
llm-security-monitor/
├── monitored_tests.py          # Main test runner
├── monitoring/
│   ├── security_logger.py      # Logging & detection engine
│   └── report_generator.py     # HTML report generator
├── logs/                        # JSONL logs & alerts
└── reports/                     # HTML dashboards
```

## 🔍 Attack Types Detected

1. **Direct Prompt Injection** - Override system instructions
2. **Prompt Leaking** - Extract confidential system prompts
3. **Jailbreaking** - Bypass safety guardrails via role-play
4. **Delimiter Confusion** - Fake system tags and commands
5. **Indirect Injection** - Embedded attacks in documents

## 📈 Example Output
```
📊 SECURITY TEST SUMMARY
============================================================
Total Tests: 5
Successful Attacks: 2 ❌
Blocked Attacks: 3 ✅
Success Rate: 40.0%
Block Rate: 60.0%
Avg Response Time: 7648ms
```

## 🛡️ Defense Strategies Tested

- Sandwich pattern (instructions before + after user input)
- Role reinforcement (PERMANENT, IMMUTABLE keywords)
- Input validation with pattern detection
- Security-aware prompting

## 🔧 Technologies

- **Python 3** - Core framework
- **Ollama** - Local LLM deployment
- **JSONL** - Structured logging
- **HTML/CSS** - Reporting dashboards

## 📚 Background

Built as part of an AI Security Specialist study plan, following OWASP Top 10 for LLM Applications guidelines. Focuses on practical, deployable security testing for production LLM systems.

## 🎓 Learning Resources

- [OWASP Top 10 for LLMs](https://owasp.org/www-project-top-10-for-large-language-model-applications/)
- Prompt injection attack patterns
- Defense-in-depth strategies for LLMs

## 📝 License

MIT License - feel free to use and modify

## 🤝 Contributing

Issues and pull requests welcome!

---

**Note:** This is a security testing tool. Always test responsibly and only on systems you have permission to test.
