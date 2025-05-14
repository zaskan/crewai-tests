from crewai import Agent, Task, Crew, Process
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import BaseTool

# Define a proper BaseTool for read_playbook
class ReadPlaybookTool(BaseTool):
    name: str = "read_playbook"
    description: str = "Reads an Ansible playbook file"

    def _run(self, playbook_path: str) -> str:
        with open(playbook_path, 'r') as f:
            return f.read()

    async def _arun(self, playbook_path: str) -> str:
        # Async version if needed
        return self._run(playbook_path)

@CrewBase
class AnsibleAnalysisCrew:
    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    @agent
    def filereader(self) -> Agent:
        return Agent(
            config=self.agents_config['filereader'],
            tools=[ReadPlaybookTool()],  # Use the properly defined tool
            verbose=True
        )

    @agent
    def ansible_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['ansible_expert'],
            verbose=True
        )

    @agent
    def security_expert(self) -> Agent:
        return Agent(
            config=self.agents_config['security_expert'],
            verbose=True
        )

    @task
    def file_reading_task(self) -> Task:
        return Task(
            config=self.tasks_config['file_reading'],
            agent=self.filereader()
        )

    @task
    def purpose_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['purpose_analysis'],
            agent=self.ansible_expert()
        )

    @task
    def security_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['security_analysis'],
            agent=self.security_expert()
        )

    @task
    def task_analysis_task(self) -> Task:
        return Task(
            config=self.tasks_config['task_analysis'],
            agent=self.ansible_expert()
        )

    @crew
    def crew(self) -> Crew:
        return Crew(
            agents=[
                self.filereader(),
                self.ansible_expert(),
                self.security_expert()
            ],
            tasks=[
                self.file_reading_task(),
                self.purpose_analysis_task(),
                self.security_analysis_task(),
                self.task_analysis_task()
            ],
            process=Process.sequential,
            verbose=True
        )
