# Multi-Agentic RAG with MCP
Multi-Agentic Retreival Augmented Generation (RAG) system built with Planner - Executor - Synthesizer agentic architecture, combining local document retrieval and live web search with complete backend wrapped by a MCP client-server model.

## 💻 Tech Stack
### 🔹AI/LLM Layer
 - Groq LLM (model: llama-3.3-70b-versatile)
 - Used for Planner and Synthesizer agent

### 🔹LangChain
 - Prompt templating
 - LLM abstractions

### 🔹LangGraph
 - Agent Orchestration 
 - State management (Planner - Executor - Synthesizer)

### 🔹LangSmith
 - LLM tracing
 - Tool execution monitoring
 - Latency and Token metrics

### 🔹Model Context Protocol (MCP)
 - FastMCP for MCP server implementation
 - Streamlit UI as MCP client

## 🧱 High-level Application Architecture
<img width="840" height="1088" alt="Architecture" src="https://github.com/user-attachments/assets/2befd011-2ba7-46c9-97c6-612bc03dc046" />

## 🤖 Agent Architecture
  ### 📋 Planner
   - Decides on how to solve user-query.
   - LLM-based intent and tool planning.
   - Discovers available tools by querying the MCP server.
   - Formulates an execution plan by selecting most appropriate tools.
   - Behaves like an autonomous reasoning agent.
   - Planner output format:
```json
      {
        "steps": [
        {
            "action": "<tool_name | no_tool>",
            "input": "<input query as string>",
            "description": "<short explanation of why this step is needed>"
          },
          ...
        ]
      }
```

 ### ▶️ Executor
  - Deterministic tool execution.
  - Executes the steps from the Planner.
  - Calls tools (**Local Rag or Google Search**) one-by-one.
  - Each step is an independent agent action.

### 📝 Synthesizer
 - LLM-based final output generator.
 - Uses user query, full conversation history, planner output and exectuor output.
 - Does summarization, reasoning, fusion of results, removes hallucinations.
 - Produces human-level natural language as final output to user.

## 📚 RAG Data Ingestion Pipeline
<img width="693" height="409" alt="RAG_Data_Ingestion" src="https://github.com/user-attachments/assets/2604bd0b-9015-497c-8769-37ef71aa4373" />

## ⚙️ Tools
 ### 📚 Local RAG
  - Queries ChromaDB (vectorStore) for Movie knowledge and technical documents related to AI, Computer science and Software engineering.
### 🌐 Google Search 
 - Search google web for queries related to general information or if the information is not present in local documents.

## 📸Application
<img width="1920" height="1020" alt="main_page" src="https://github.com/user-attachments/assets/340c60a4-7918-4391-898c-d909583765e9" />
<img width="1920" height="1020" alt="personal_preference_chat_history" src="https://github.com/user-attachments/assets/257ce5da-b017-482d-9327-39d1010ae4d2" />

## 📊Observability
<img width="1920" height="965" alt="langsmith_homepage" src="https://github.com/user-attachments/assets/b85f4fd2-76fd-4453-a9bd-81ae3c6f16bc" />









