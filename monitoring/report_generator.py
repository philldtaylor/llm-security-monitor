#!/usr/bin/env python3
"""
LLM Security Test Report Generator
Generates HTML reports from security test logs

UPDATED: Changed "Blocked Attacks" to "Attacks Detected" for accuracy
"""

import json
from pathlib import Path
from datetime import datetime

def generate_html_report(log_file):
    """Generate HTML report from JSONL log file"""
    
    # Read log file
    log_path = Path(log_file)
    if not log_path.exists():
        print(f"Error: Log file not found: {log_file}")
        return
    
    # Parse logs
    entries = []
    with open(log_path, 'r') as f:
        for line in f:
            if line.strip():
                entries.append(json.loads(line))
    
    if not entries:
        print("No log entries found")
        return
    
    # Calculate statistics
    total_tests = len(entries)
    successful_attacks = sum(1 for e in entries if e.get('attack_success', False))
    detected_attacks = total_tests - successful_attacks  # CHANGED: was "blocked_attacks"
    detection_rate = (detected_attacks / total_tests * 100) if total_tests > 0 else 0  # CHANGED: was "block_rate"
    
    # Generate HTML
    html = f"""<!DOCTYPE html>
<html>
<head>
    <title>LLM Security Test Report</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        .header {{
            background: #2c3e50;
            colour: white;
            padding: 20px;
            border-radius: 5px;
            margin-bottom: 20px;
        }}
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
            margin-bottom: 20px;
        }}
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 5px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }}
        .stat-value {{
            font-size: 2em;
            font-weight: bold;
            colour: #3498db;
        }}
        .stat-label {{
            colour: #7f8c8d;
            margin-top: 5px;
        }}
        .test-entry {{
            background: white;
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 5px;
            border-left: 4px solid #3498db;
        }}
        .success {{
            border-left-colour: #e74c3c;
        }}
        .detected {{
            border-left-colour: #2ecc71;
        }}
        .test-name {{
            font-weight: bold;
            font-size: 1.1em;
            margin-bottom: 10px;
        }}
        .attack-types {{
            background: #ecf0f1;
            padding: 5px 10px;
            border-radius: 3px;
            display: inline-block;
            margin: 5px 5px 5px 0;
            font-size: 0.9em;
        }}
        .timestamp {{
            colour: #95a5a6;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 LLM Security Test Report</h1>
        <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        <p>Log File: {log_path.name}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{total_tests}</div>
            <div class="stat-label">Total Tests</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="colour: #e74c3c;">{successful_attacks}</div>
            <div class="stat-label">Successful Attacks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="colour: #2ecc71;">{detected_attacks}</div>
            <div class="stat-label">Attacks Detected</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{detection_rate:.0f}%</div>
            <div class="stat-label">Detection Rate</div>
        </div>
    </div>
    
    <h2>Test Details</h2>
"""
    
    # Add test entries
    for entry in entries:
        attack_success = entry.get('attack_success', False)
        status_class = 'success' if attack_success else 'detected'
        status_icon = '❌' if attack_success else '✅'
        
        attack_types = entry.get('attack_types', [])
        attack_types_html = ''.join([
            f'<span class="attack-types">{at}</span>' 
            for at in attack_types
        ]) if attack_types else '<span class="attack-types">No attacks detected</span>'
        
        html += f"""
    <div class="test-entry {status_class}">
        <div class="test-name">{status_icon} {entry.get('test_name', 'Unknown Test')}</div>
        <div class="timestamp">{entry.get('timestamp', 'N/A')}</div>
        <div style="margin-top: 10px;">
            {attack_types_html}
        </div>
        <div style="margin-top: 10px;">
            <strong>Response Time:</strong> {entry.get('response_time_ms', 0):.0f}ms
        </div>
        <div style="margin-top: 10px;">
            <strong>User Prompt:</strong><br>
            <pre style="background: #ecf0f1; padding: 10px; border-radius: 3px; overflow-x: auto;">{entry.get('user_prompt', 'N/A')}</pre>
        </div>
        <div style="margin-top: 10px;">
            <strong>Response:</strong><br>
            <pre style="background: #ecf0f1; padding: 10px; border-radius: 3px; overflow-x: auto;">{entry.get('response', 'N/A')}</pre>
        </div>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    # Save report
    report_dir = Path('reports')
    report_dir.mkdir(exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_file = report_dir / f"report_{log_path.stem}_{timestamp}.html"
    
    with open(report_file, 'w') as f:
        f.write(html)
    
    print(f"✅ Report generated: {report_file}")
    return report_file

if __name__ == "__main__":
    import sys
    
    # Find latest log file if no argument provided
    if len(sys.argv) > 1:
        log_file = sys.argv[1]
    else:
        log_dir = Path('logs')
        log_files = list(log_dir.glob('llm_security_*.jsonl'))
        if not log_files:
            print("No log files found in logs/")
            sys.exit(1)
        log_file = max(log_files, key=lambda p: p.stat().st_mtime)
        print(f"Using latest log file: {log_file}")
    
    generate_html_report(log_file)
