from crewai import Crew
from agents import FileReaderAgent, PlaybookContextAgent, AnalyzerAgent, ExplainerAgent

# Initialize agents
reader = FileReaderAgent()
context_learner = PlaybookContextAgent()
analyzer = AnalyzerAgent()
explainer = ExplainerAgent()

# Define the team of experts working together
security_analysis_crew = Crew(agents=[reader, context_learner, analyzer, explainer])