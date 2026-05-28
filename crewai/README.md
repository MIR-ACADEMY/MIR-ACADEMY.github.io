# MIRA — Multi-AI Orchestrator  
**CrewAI Framework for Intelligent Task Delegation**

MIR ACADEMY's intelligent orchestration system where Claude acts as the lead architect, delegating specialized tasks to ChatGPT, Gemini, Grok, and other AI tools based on cost optimization and capability matching.

## Overview

**Problem:** Managing multiple AI tools, choosing the right one for each task, minimizing API costs, maximizing output quality.

**Solution:** MIRA (Claude) as the orchestrator. Rules-based delegation:
- **Cost First** → Free/cheaper options preferred
- **Capability Match** → Right tool for right task  
- **Quality** → No compromises on output
- **Transparency** → Clear workflow, auditable decisions

## Framework Components

### 1. **Agent Roles**
- **MIRA** (Claude): System architect, workflow designer, final QA
- **ChatGPT**: Code generation, technical writing, prototypes
- **Gemini**: Data analysis, visualization, image generation
- **Grok**: Real-time research, trending data, current events
- **Editor**: Quality assurance, brand alignment, accuracy checks

### 2. **Workflow Examples**

#### Content Generation
```
Outline → Draft → Review → Publish
MIRA   → ChatGPT → Editor → MIRA
```

#### Code Review & Optimization
```
Analyze → Optimize → Document → QA
MIRA   → ChatGPT  → ChatGPT  → Editor
```

#### Research & Intelligence
```
Plan → Gather → Analyze → Synthesize → Publish
MIRA → Grok  → Gemini  → ChatGPT   → Editor
```

## Getting Started

### Installation

```bash
pip install crewai anthropic openai google-genai x-api
```

### Environment Variables
```bash
export ANTHROPIC_API_KEY="your_claude_key"
export OPENAI_API_KEY="your_chatgpt_key"
export GOOGLE_API_KEY="your_gemini_key"
export X_API_KEY="your_grok_key"
```

### Run Example

```bash
python orchestrator.py
# Choose workflow: 1 (content), 2 (code), 3 (research)
```

## Configuration

Edit `config.yaml` to:
- Add new agent roles
- Define custom workflows
- Adjust cost optimization rules
- Configure API endpoints

## Cost Optimization Rules

The framework prioritizes cost while maintaining quality:

1. **Use free tools first** (web search, local processing)
2. **Delegate to ChatGPT for coding** (cheaper than Claude)
3. **Use Gemini for images** (free tier available)
4. **Use Grok for real-time data** (X API integration)
5. **Reserve Claude for complex reasoning & final QA**
6. **Batch similar tasks** to reduce API calls
7. **Cache results** when possible

## Files

- `orchestrator.py` — Main framework with 3 example workflows
- `config.yaml` — Agent and workflow configuration
- `README.md` — This guide

## MIR ACADEMY Integration

This framework is the flagship technology demonstrating:
- **Intelligent delegation** across multiple AI tools
- **Cost-first optimization** without sacrificing quality
- **Transparent workflows** auditable at every step
- **Production-ready** multi-agent systems

Used for:
- Educational content creation
- Code review & optimization
- Market research & analysis
- Document generation
- Quality assurance

## Next Steps

1. **Configure your API keys** (see Installation)
2. **Run an example workflow** (content, code, or research)
3. **Customize agents & workflows** in config.yaml
4. **Integrate into your projects** — import CrewAI crew functions

## Questions?

This framework demonstrates MIR ACADEMY's capability to orchestrate complex AI workflows. For custom setups, reach out to Emre Mir.

---

**Built by:** Emre Mir (MIR) + MIRA (Claude)  
**2026** — MIR ACADEMY
