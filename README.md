# Multi-Agentic RAG with MCP
Multi-Agentic Retreival Augmented Generation (RAG) system built with Planner - Executor - Synthesizer agentic architecture, combining local document retrieval and live web search with complete backend wrapped by a MCP client-server model.

## 💻 Tech Stack
### AI/LLM Layer
 - Groq LLM (model: llama-3.3-70b-versatile)
 - Used for Planner and Synthesizer agent

### LangChain
 - Prompt templating
 - LLM abstractions

### LangGraph
 - Agent Orchestration 
 - State management (Planner - Executor - Synthesizer)

### LangSmith
 - LLM tracing
 - Tool execution monitoring
 - Latency and Token metrics

### Model Context Protocol (MCP)
 - FastMCP for MCP server implementation
 - Streamlit UI as MCP client

## 🧱 High-level Application Architecture
<img width="840" height="1088" alt="Architecture" src="https://github.com/user-attachments/assets/2befd011-2ba7-46c9-97c6-612bc03dc046" />

## 🤖 Agent Architecture
  ### 📋 Planner
   - LLM-based intent and tool planning.
   - Behaves like an autonomous reasoning agent.
   - Decides on how to solve user-query.

 ### ▶️ Executor
  - Deterministic tool execution.
  - Executes the steps from the Planner.
  - Calls tools (Local Rag or Google Search) one-by-one
  - Each step is an independent agent action.

### 📝 Synthesizer
 - LLM-based final output generator.
 - Uses user query, full conversation history, planner output and exectuor output.
 - Does summarization, reasoning, fusion of results, removes hallucinations.
 - Produces human-level natural language as final output to user. 


