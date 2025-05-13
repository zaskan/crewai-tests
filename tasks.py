from crewai import Task
from openai import OpenAI
import yaml

# Initialize OpenAI client
client = OpenAI()

def read_playbook(file_path):
    """Reads and parses an Ansible playbook from a YAML file."""
    try:
        with open(file_path, "r") as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        return f"Error: File '{file_path}' not found."
    except yaml.YAMLError:
        return "Error: Invalid YAML format in playbook."

def analyze_playbook(playbook_content):
    """Extracts tasks, modules, and configurations from the playbook."""
    tasks = []
    if isinstance(playbook_content, list):
        for item in playbook_content:
            if "tasks" in item:
                for task in item["tasks"]:
                    module_name = next(iter(task.keys() - {"name"}), "unknown_module")
                    module_args = task.get(module_name, {})
                    tasks.append((module_name, module_args))
    return tasks if tasks else ["No valid tasks found"]

def get_playbook_context(playbook_content):
    """Generates a high-level understanding of the playbook."""
    tasks_summary = [f"{task.keys()}" for task in playbook_content if "tasks" in task]
    prompt = f"Analyze these Ansible tasks and determine the overall playbook purpose:\n{tasks_summary}"

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "system", "content": prompt}]
    )

    return response.choices[0].message.content

def explain_task_security(tasks, filename, playbook_purpose):
    """Evaluates tasks for security risks using contextual knowledge."""
    reports = []
    total_score = 0

    for module_name, module_args in tasks:
        prompt = f"Analyze the security risks of the Ansible module '{module_name}' with arguments: {module_args}. "
        prompt += f"Consider its implementation in this playbook context: {playbook_purpose}. Provide a one-sentence summary (max 50 words) and a risk score (1-5), focusing on misconfigurations or vulnerabilities."

        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": prompt}]
        )

        explanation = response.choices[0].message.content
        risk_score = int(next(iter(filter(str.isdigit, explanation.split())), 0))
        total_score += risk_score

        reports.append(f"|{filename}|**{module_name}**|{explanation}|{risk_score}|\n")

    avg_score = round(total_score / len(tasks)) if tasks else 0
    reports.append(f"\n## Average Destructive Potential Score: {avg_score}\n")

    return reports