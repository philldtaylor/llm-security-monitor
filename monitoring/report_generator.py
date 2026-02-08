#!/usr/bin/env python3
"""
Generate HTML reports from security logs
"""

import json
from pathlib import Path
from datetime import datetime

def generate_html_report(log_file):
    """Generate an HTML report from a JSONL log file"""
    
    # Read all log entries
    entries = []
    with open(log_file, 'r') as f:
        for line in f:
            entries.append(json.loads(line))
    
    # Calculate statistics
    total = len(entries)
    successful = sum(1 for e in entries if e['attack_success'])
    blocked = total - successful
    
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
            color: white;
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
            color: #3498db;
        }}
        .stat-label {{
            color: #7f8c8d;
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
            border-left-color: #e74c3c;
        }}
        .blocked {{
            border-left-color: #2ecc71;
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
            color: #95a5a6;
            font-size: 0.9em;
        }}
    </style>
</head>
<body>
    <div class="header">
        <h1>🔒 LLM Security Test Report</h1>
        <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <p>Log File: {log_file.name}</p>
    </div>
    
    <div class="stats">
        <div class="stat-card">
            <div class="stat-value">{total}</div>
            <div class="stat-label">Total Tests</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: #e74c3c;">{successful}</div>
            <div class="stat-label">Successful Attacks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value" style="color: #2ecc71;">{blocked}</div>
            <div class="stat-label">Blocked Attacks</div>
        </div>
        <div class="stat-card">
            <div class="stat-value">{blocked/max(total,1)*100:.0f}%</div>
            <div class="stat-label">Block Rate</div>
        </div>
    </div>
    
    <h2>Test Details</h2>
"""
    
    # Add each test entry
    for entry in entries:
        status_class = "success" if entry['attack_success'] else "blocked"
        status_icon = "❌" if entry['attack_success'] else "✅"
        
        attack_tags = "".join([
            f'<span class="attack-types">{at}</span>' 
            for at in entry['attack_types']
        ])
        
        html += f"""
    <div class="test-entry {status_class}">
        <div class="test-name">{status_icon} {entry['test_name']}</div>
        <div class="timestamp">{entry['timestamp']}</div>
        <div style="margin-top: 10px;">
            {attack_tags or '<span class="attack-types">No attacks detected</span>'}
        </div>
        <div style="margin-top: 10px;">
            <strong>Response Time:</strong> {entry['response_time_ms']:.0f}ms
        </div>
        <div style="margin-top: 10px;">
            <strong>User Prompt:</strong><br>
            <pre style="background: #ecf0f1; padding: 10px; border-radius: 3px; overflow-x: auto;">{entry['user_prompt']}</pre>
        </div>
        <div style="margin-top: 10px;">
            <strong>Response:</strong><br>
            <pre style="background: #ecf0f1; padding: 10px; border-radius: 3px; overflow-x: auto;">{entry['response'][:500]}{'...' if len(entry['response']) > 500 else ''}</pre>
        </div>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    # Save HTML report
    report_file = Path("reports") / f"report_{log_file.stem}.html"
    report_file.parent.mkdir(exist_ok=True)
    
    with open(report_file, 'w') as f:
        f.write(html)
    
    print(f"\n📊 HTML Report generated: {report_file}")
    print(f"   Open it in your browser to view!")
    
    return report_file

if __name__ == "__main__":
    # Find the most recent log file
    log_dir = Path("logs")
    log_files = sorted(log_dir.glob("llm_security_*.jsonl"))
    
    if log_files:
        latest_log = log_files[-1]
        print(f"Generating report for: {latest_log}")
        generate_html_report(latest_log)
    else:
        print("No log files found! Run monitored_tests.py first.")