#!/usr/bin/env python3
"""
MIRA — Multi-AI Orchestrator via CrewAI
MIR ACADEMY Project: Intelligent task delegation across ChatGPT, Gemini, Grok, and other tools
Built by: Emre Mir (MIR) + MIRA (Claude)
2026
"""

from crewai import Agent, Task, Crew, Process
import os

# ──────────────────────────────────────────────────
# EXAMPLE 1: CONTENT GENERATION WORKFLOW
# ──────────────────────────────────────────────────
def content_generation_crew():
    """
    Workflow: Blog outline → Draft article → Editorial review
    """
    
    # AGENT 1: Architect (MIRA)
    architect = Agent(
        role="Content Architect (MIRA Lead)",
        goal="Design content structure, decide delegation strategy, assign to best AI tools",
        backstory="""You are MIRA, the orchestrator managing multiple AI workers. 
        Your job: break down tasks, assign to ChatGPT for drafting, Gemini for analysis, Grok for trending info.
        Output: structured outline with tool assignments.""",
        verbose=True,
        allow_delegation=False,
    )
    
    # AGENT 2: Writer (ChatGPT proxy)
    writer = Agent(
        role="Content Writer (ChatGPT)",
        goal="Write engaging, well-researched content based on the architectural outline",
        backstory="You are a skilled writer. You follow the outline EXACTLY and produce polished prose.",
        verbose=True,
    )
    
    # AGENT 3: Reviewer (Editorial)
    reviewer = Agent(
        role="Editorial Reviewer",
        goal="Review draft for clarity, factual accuracy, and tone alignment",
        backstory="You catch errors, suggest improvements, and ensure brand voice is maintained.",
        verbose=True,
    )
    
    # TASK 1: Architect designs the workflow
    task_architect = Task(
        description="Create a detailed outline for an article on 'AI in Education 2026'. "
                    "Decide which other tools should contribute: ChatGPT for writing, Gemini for research data.",
        expected_output="Structured outline with section assignments and tool delegation plan",
        agent=architect,
    )
    
    # TASK 2: Writer drafts content
    task_write = Task(
        description="Write the article following the architect's outline. Target: 1500 words, professional tone.",
        expected_output="Complete first draft ready for review",
        agent=writer,
        depends_on=[task_architect],
    )
    
    # TASK 3: Reviewer provides feedback
    task_review = Task(
        description="Review the draft article. Check: accuracy, clarity, tone, engagement. Provide bullet-point feedback.",
        expected_output="Review feedback with 5-7 actionable improvements",
        agent=reviewer,
        depends_on=[task_write],
    )
    
    # Crew execution
    crew = Crew(
        agents=[architect, writer, reviewer],
        tasks=[task_architect, task_write, task_review],
        process=Process.sequential,
        verbose=True,
    )
    
    return crew

# ──────────────────────────────────────────────────
# EXAMPLE 2: CODE REVIEW PIPELINE
# ──────────────────────────────────────────────────
def code_review_crew():
    """
    Workflow: Analyze code → Optimize → Document
    """
    
    analyzer = Agent(
        role="Code Analyzer (MIRA)",
        goal="Audit code for issues, performance, security; assign optimization to ChatGPT",
        backstory="You understand architecture and identify bottlenecks.",
        verbose=True,
    )
    
    optimizer = Agent(
        role="Code Optimizer (ChatGPT)",
        goal="Refactor and optimize based on analysis. Maintain functionality.",
        backstory="You write clean, efficient code following best practices.",
        verbose=True,
    )
    
    documenter = Agent(
        role="Technical Writer",
        goal="Create clear docs for optimized code with examples",
        backstory="You explain complex logic in simple terms.",
        verbose=True,
    )
    
    task_analyze = Task(
        description="Analyze the provided Python code for: performance, security, readability. List 5 improvements.",
        expected_output="Analysis report with specific issues and recommendations",
        agent=analyzer,
    )
    
    task_optimize = Task(
        description="Refactor the code to address the top 3 issues from the analysis.",
        expected_output="Optimized code with comments explaining changes",
        agent=optimizer,
        depends_on=[task_analyze],
    )
    
    task_doc = Task(
        description="Write documentation for the optimized code. Include usage examples.",
        expected_output="Complete documentation markdown file",
        agent=documenter,
        depends_on=[task_optimize],
    )
    
    crew = Crew(
        agents=[analyzer, optimizer, documenter],
        tasks=[task_analyze, task_optimize, task_doc],
        process=Process.sequential,
        verbose=True,
    )
    
    return crew

# ──────────────────────────────────────────────────
# EXAMPLE 3: RESEARCH & SYNTHESIS
# ──────────────────────────────────────────────────
def research_synthesis_crew():
    """
    Workflow: Research topic → Find data sources → Synthesize findings
    """
    
    researcher = Agent(
        role="Lead Researcher (MIRA)",
        goal="Identify research question, outline sources, delegate data gathering to Grok/web tools",
        backstory="You design research strategy and coordinate data collection.",
        verbose=True,
    )
    
    data_gatherer = Agent(
        role="Data Gatherer (Grok/Web)",
        goal="Find and collect relevant data, citations, and sources on the topic",
        backstory="You search comprehensively and compile raw research materials.",
        verbose=True,
    )
    
    synthesizer = Agent(
        role="Analyst & Writer",
        goal="Turn raw research into coherent, cited findings with conclusions",
        backstory="You find patterns, make connections, and write compelling analysis.",
        verbose=True,
    )
    
    task_research = Task(
        description="Design a research plan for: 'Impact of AI on Global Job Markets 2024–2026'",
        expected_output="Research outline with 5 key questions and source categories",
        agent=researcher,
    )
    
    task_gather = Task(
        description="Collect data on AI job displacement, new roles created, and salary trends. Find 10+ credible sources.",
        expected_output="Annotated bibliography with key statistics",
        agent=data_gatherer,
        depends_on=[task_research],
    )
    
    task_synthesize = Task(
        description="Write a research summary (1000 words) synthesizing the data with conclusions.",
        expected_output="Formatted research paper with citations",
        agent=synthesizer,
        depends_on=[task_gather],
    )
    
    crew = Crew(
        agents=[researcher, data_gatherer, synthesizer],
        tasks=[task_research, task_gather, task_synthesize],
        process=Process.sequential,
        verbose=True,
    )
    
    return crew

# ──────────────────────────────────────────────────
# MAIN: Run example
# ──────────────────────────────────────────────────
if __name__ == "__main__":
    print("\n" + "="*70)
    print("MIRA ORCHESTRATOR — Choose Example")
    print("="*70)
    print("1. Content Generation (Outline → Write → Review)")
    print("2. Code Review (Analyze → Optimize → Document)")
    print("3. Research & Synthesis (Plan → Gather → Synthesize)")
    print("="*70 + "\n")
    
    choice = input("Run example (1-3): ").strip()
    
    if choice == "1":
        print("\n🚀 Starting Content Generation Crew...\n")
        crew = content_generation_crew()
        result = crew.kickoff(inputs={"topic": "AI in Education"})
        print("\n✅ Content workflow complete.\n")
    
    elif choice == "2":
        print("\n🚀 Starting Code Review Crew...\n")
        crew = code_review_crew()
        result = crew.kickoff(inputs={"code": "# Your code here"})
        print("\n✅ Code review complete.\n")
    
    elif choice == "3":
        print("\n🚀 Starting Research Crew...\n")
        crew = research_synthesis_crew()
        result = crew.kickoff(inputs={"topic": "AI Job Market 2026"})
        print("\n✅ Research complete.\n")
    
    else:
        print("Invalid choice. Exiting.")
