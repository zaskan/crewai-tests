import os
from crewai import Agent, Task, Crew, Process
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables.")

researcher = Agent(
    role='Senior Research Analyst',
    goal='Gather information about the latest AI trends.',
    backstory="You are a seasoned analyst with expertise in AI.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key) # Correct way to define llm
)

writer = Agent(
    role='Technical Writer',
    goal='Write a concise report based on the research.',
    backstory="You are skilled in simplifying complex data.",
    verbose=True,
    allow_delegation=False,
    llm=ChatOpenAI(model_name="gpt-3.5-turbo", openai_api_key=openai_api_key) # Correct way to define llm
)

research_task = Task(
    description="Conduct thorough research on the most recent advancements in large language models. Focus on key developments and their potential impact.",
    agent=researcher
)

write_report_task = Task(
    description="Using the research provided, write a short report summarizing the key findings. Keep the report under 200 words.",
    agent=writer
)

crew = Crew(
    agents=[researcher, writer],
    tasks=[research_task, write_report_task],
    verbose=2,
    process=Process.sequential
)

result = crew.kickoff()

print("\n\nResult:")
print(result)