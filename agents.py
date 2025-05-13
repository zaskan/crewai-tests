from crewai import Agent
from pydantic import BaseModel
from openai import OpenAI
import os

# Initialize OpenAI client
client = OpenAI()

# Retrieve OpenAI API key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    raise ValueError("Missing OpenAI API Key. Please set OPENAI_API_KEY in your environment variables.")

class FileReaderAgent(Agent, BaseModel):
    role: str = "Ansible Playbook Expert"
    goal: str = "Accurately parse and read YAML-based Ansible playbooks"
    backstory: str = "A seasoned Ansible specialist trained to deeply understand automation workflows."

class PlaybookContextAgent(Agent, BaseModel):
    role: str = "Ansible Playbook Context Learner"
    goal: str = "Understand the playbook's overall purpose and dependencies"
    backstory: str = "An automation architect who analyzes playbooks holistically."

class AnalyzerAgent(Agent, BaseModel):
    role: str = "Ansible Security Analyst"
    goal: str = "Analyze playbook tasks, extract module names, and assess configurations"
    backstory: str = "A cybersecurity expert specializing in detecting misconfigurations in Ansible automation."

class ExplainerAgent(Agent, BaseModel):
    role: str = "Cybersecurity Specialist"
    goal: str = "Provide expert security evaluation of Ansible tasks using playbook context"
    backstory: str = "An AI expert focused on analyzing infrastructure automation risks."