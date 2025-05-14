from ansible_analysis.crew import AnsibleAnalysisCrew

def run():
    inputs = {
        'playbook_path': 'playbook.yml'  # <-- Change this to your playbook filename
    }
    AnsibleAnalysisCrew().crew().kickoff(inputs=inputs)

if __name__ == "__main__":
    run()
