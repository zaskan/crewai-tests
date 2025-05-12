import os
import re
import sys
import argparse
from openai import OpenAI
from crewai import Crew, Agent
from pydantic import BaseModel

# Initialize OpenAI client
client = OpenAI()

# Retrieve OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please set OPENAI_API_KEY in your environment variables.")

# Parse command-line arguments
parser = argparse.ArgumentParser(description="Analyze an Ansible playbook from the filesystem.")
parser.add_argument("playbook_path", help="Path to the Ansible playbook file")
args = parser.parse_args()

# Define an agent to read the Ansible playbook from the filesystem
class FileReaderAgent(Agent, BaseModel):
    role: str = "File Reader"
    goal: str = "Read the Ansible playbook from the local filesystem"
    backstory: str = "A meticulous agent designed to read and process files efficiently."

    def run(self, playbook_path):
        try:
            with open(playbook_path, "r") as file:
                return file.read()
        except FileNotFoundError:
            return f"Error: File '{playbook_path}' not found."
        except Exception as e:
            return f"Error reading file: {str(e)}"

# Define an agent to analyze the playbook contents
class AnalyzerAgent(Agent, BaseModel):
    role: str = "Analyzer"
    goal: str = "Identify tasks within the Ansible playbook"
    backstory: str = "An AI-powered inspector capable of parsing Ansible YAML files."

    def run(self, playbook_content):
        tasks = []
        lines = playbook_content.split("\n")
        for line in lines:
            if "- name:" in line:
                tasks.append(line.strip())

        return tasks if tasks else ["No tasks found in playbook"]

# Define an agent to explain the playbook using OpenAI
class ExplainerAgent(Agent, BaseModel):
    role: str = "Explainer"
    goal: str = "Provide clear explanations of the playbook's tasks"
    backstory: str = "An AI assistant specializing in Ansible playbook analysis."

    def run(self, analysis):
        explanation = "## Ansible Playbook Analysis\n\nThis playbook contains the following tasks:\n\n"
        explanation += "\n".join(f"- {task}" for task in analysis)

        # Generate explanation using OpenAI
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Explain the following Ansible tasks in simple terms and provide a score from 1 to 5 (being five the more dangerous) based on the destructive potential of this task."},
                {"role": "user", "content": explanation}
            ]
        )

        detailed_explanation = response.choices[0].message.content

        # Extract scores from response
        scores = [int(match.group()) for match in re.finditer(r"\b[1-5]\b", detailed_explanation)]

        # Calculate average score
        avg_score = round(sum(scores) / len(scores)) if scores else 0

        # Write the explanation to a Markdown file
        with open(args.playbook_path + ".md", "w") as md_file:
            md_file.write(f"{explanation}\n\n### Detailed Explanation\n\n{detailed_explanation}\n\n")
            md_file.write(f"### Average Destructive Potential Score\n\n{avg_score}")

        return avg_score

# Initialize crew and agents
reader = FileReaderAgent()
analyzer = AnalyzerAgent()
explainer = ExplainerAgent()

crew = Crew(agents=[reader, analyzer, explainer])

# Run the crew with the provided playbook file path
playbook_content = reader.run(args.playbook_path)
analysis = analyzer.run(playbook_content)
avg_score = explainer.run(analysis)

# Exit with the average score as the exit code
sys.exit(avg_score)

