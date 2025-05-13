import sys
import argparse
from utils import parse_yaml
from crew import security_analysis_crew
from tasks import analyze_playbook, get_playbook_context, explain_task_security

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Analyze an Ansible playbook from the filesystem.")
parser.add_argument("playbook_path", help="Path to the Ansible playbook file")
args = parser.parse_args()

# Run the process
playbook_content = parse_yaml(args.playbook_path)
playbook_purpose = get_playbook_context(playbook_content)
tasks = analyze_playbook(playbook_content)
security_report = explain_task_security(tasks, args.playbook_path, playbook_purpose)

# Write to Markdown file
with open("security_report.md", "w") as report_file:
    report_file.writelines(security_report)

# Exit with the average score
sys.exit(round(sum(int(line.split('|')[-2]) for line in security_report if '|' in line) / len(tasks)))
