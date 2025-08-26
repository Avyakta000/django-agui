# Django CopilotKit Multi-Agent Assistant

A Django application that integrates CopilotKit with multiple specialized LangGraph agents for AI-powered assistance across different domains.

## 🏗️ **Project Architecture**

### **Clear Separation of Concerns:**
- **`config/`** = Django core configuration (not assistant functionality)
- **`apps/rest_api/copilotkit/`** = Endpoint infrastructure for different agents
- **`apps/rest_api/copilotkit/agents/`** = Different specialized agent types
- **`apps/rest_api/copilotkit/runtime/`** = Shared components used by all agents

## 📁 **Project Structure**

```
django-agui/
├── config/                           # Django core configuration
│   ├── __init__.py                   # Makes config a Python package
│   ├── settings.py                   # Django settings, apps, middleware
│   ├── urls.py                       # Root URL routing configuration
│   ├── asgi.py                       # ASGI entry point for async servers (uvicorn)
│   └── wsgi.py                       # WSGI entry point for traditional servers
├── apps/                             # Application modules
│   ├── __init__.py                   # Makes apps a Python package
│   ├── rest_api/                     # REST API endpoints
│   │   ├── __init__.py               # Makes rest_api a Python package
│   │   ├── apps.py                   # Django app configuration
│   │   ├── urls.py                   # REST API URL routing (includes CopilotKit)
│   │   ├── views/                    # REST API view implementations
│   │   │   ├── health.py             # Health check endpoint
│   │   │   └── echo.py               # Echo endpoint for testing
│   │   └── copilotkit/               # CopilotKit endpoint infrastructure
│   │       ├── __init__.py           # Makes copilotkit a Python package
│   │       ├── endpoints.py          # Main endpoint handlers for all agents
│   │       ├── sdk.py                # CopilotKit SDK setup with multiple agents
│   │       ├── runtime/              # Shared runtime components
│   │       │   ├── __init__.py       # Runtime package marker
│   │       │   ├── schema.py         # AgentState schema for all agents
│   │       │   ├── model.py          # LLM configuration (OpenAI, DeepSeek)
│   │       │   └── tools/            # Shared tools used by all agents
│   │       │       ├── __init__.py   # Tools package marker
│   │       │       ├── datetime_tool.py  # Current date/time tool
│   │       │       └── web_search.py     # Web search tool (Tavily)
│   │       └── agents/               # Different specialized agent implementations
│   │           ├── __init__.py       # Exports all agent graphs
│   │           ├── general.py        # General-purpose assistant
│   │           ├── research.py       # Research assistant
│   │           └── medical.py        # Medical information assistant
│   └── graphql_api/                  # GraphQL API endpoints
├── manage.py                         # Django management script
├── requirements.txt                  # Python dependencies
├── env.example                       # Environment variables template
├── db.sqlite3                        # SQLite database
└── README.md                         # This file
```

## 🚀 **Features**

- 🤖 **Multiple Specialized Agents:**
  - **General Assistant** - Everyday tasks and information queries
  - **Research Assistant** - Research tasks with web search and analysis
  - **Medical Assistant** - Health information (with medical disclaimers)
- 🔍 **Web Search Capabilities** with Tavily API
- ⏰ **Current DateTime Tool** for context
- 🌐 **RESTful API Endpoints** for each agent type
- 🔄 **Async Streaming Responses** for real-time interaction
- 🏗️ **Modular Architecture** - Easy to add new agent types

## 📋 **Prerequisites**

- Python 3.12+
- Virtual environment (recommended)
- API keys for the services you want to use

## ⚙️ **Setup**

1. **Clone and navigate to the project:**
   ```bash
   cd django-agui
   ```

2. **Create your virtual environment:**
   ```bash
   # Windows
   py -m venv venv
   
   # macOS/Linux
   python3 -m venv venv
   ```

3. **Activate your virtual environment:**
   ```bash
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   
   **Create a .env file based on env.example:**
   ```bash
   # API Keys for Language Models
   OPENAI_API_KEY=your_openai_api_key_here
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   
   # Web Search API Key
   TAVILY_API_KEY=your_tavily_api_key_here
   
   # Django Settings
   SECRET_KEY=your_django_secret_key_here
   DEBUG=True
   ```

6. **Run database migrations (Optional):**
   ```bash
   python manage.py migrate
   ```

7. **Start the server:**
   ```bash
   uvicorn config.asgi:application --host 0.0.0.0 --port 8000 --reload --lifespan off
   ```

## 🌐 **API Endpoints**

### **CopilotKit Agent Endpoints**

- `GET/POST /api/copilotkit/info` - Get information about all available agents
- `POST /api/copilotkit/agent/general_assistant` - Execute general assistant
- `POST /api/copilotkit/agent/research_assistant` - Execute research assistant
- `POST /api/copilotkit/agent/medical_assistant` - Execute medical assistant
- `POST /api/copilotkit/agent/{name}/state` - Get agent state
- `POST /api/copilotkit/action/{name}` - Execute an action

### **Utility Endpoints**

- `GET /api/health` - Health check
- `POST /api/echo` - Echo message (for testing)

## 📖 **Usage Examples**

### **Test the info endpoint:**
```bash
curl -X POST http://localhost:8000/api/copilotkit/info
```

### **Test the health endpoint:**
```bash
curl http://localhost:8000/api/health
```

### **Execute the research assistant:**
```bash
curl -X POST http://localhost:8000/api/copilotkit/agent/research_assistant \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What are the latest developments in AI?"}],
    "state": {},
    "config": {}
  }'
```

### **Execute the medical assistant:**
```bash
curl -X POST http://localhost:8000/api/copilotkit/agent/medical_assistant \
  -H "Content-Type: application/json" \
  -d '{
    "messages": [{"role": "user", "content": "What are the benefits of exercise?"}],
    "state": {},
    "config": {}
  }'
```

## 🔧 **Development**

### **Adding New Agent Types**

To add a new agent (e.g., `legal_assistant`):

1. **Create the agent file:**
   ```python
   # apps/rest_api/copilotkit/agents/legal.py
   from ..runtime.model import get_llm
   from ..runtime.schema import AgentState
   # ... rest of agent implementation
   ```

2. **Add to the agents package:**
   ```python
   # apps/rest_api/copilotkit/agents/__init__.py
   from .legal import legal_graph
   
   __all__ = [
       "general_graph",
       "research_graph", 
       "medical_graph",
       "legal_graph"  # ← Add new agent
   ]
   ```

3. **Add to the SDK:**
   ```python
   # apps/rest_api/copilotkit/sdk.py
   from .agents import legal_graph
   
   sdk = CopilotKitRemoteEndpoint(
       agents=lambda context: [
           # ... existing agents
           LangGraphAgent(
               name="legal_assistant",
               description="Legal information assistant.",
               graph=legal_graph,
           ),
       ],
   )
   ```

### **Adding New Tools**

To add a new tool:

1. **Create the tool file:**
   ```python
   # apps/rest_api/copilotkit/runtime/tools/calculator.py
   from langchain_core.tools import tool
   
   @tool
   def calculate(expression: str) -> str:
       """Calculate mathematical expressions."""
       return eval(expression)  # Note: Use safer alternatives in production
   ```

2. **Import in your agent:**
   ```python
   from ..runtime.tools.calculator import calculate
   
   def get_agent_tools():
       return [get_current_datetime, search_web, calculate]
   ```

## 🚨 **Troubleshooting**

### **500 Internal Server Error**

If you're getting 500 errors, check:

1. **API Keys**: Make sure your API keys are set in the `.env` file
2. **Environment Variables**: Verify the `.env` file is being loaded
3. **Dependencies**: Ensure all packages are installed correctly

### **Common Issues**

- **Missing API Keys**: The application will show helpful error messages if API keys are missing
- **Network Issues**: Make sure you have internet access for API calls
- **Port Conflicts**: If port 8000 is busy, use a different port: `uvicorn config.asgi:application --host 0.0.0.0 --port 8001 --reload`

### **Import Errors**

If you get import errors after restructuring:

1. **Clear Python cache:**
   ```bash
   # Remove all __pycache__ directories
   find . -type d -name "__pycache__" -exec rm -rf {} +
   ```

2. **Restart your development server**

## 📚 **Key Components Explained**

### **`config/` Folder**
- **Purpose**: Django's core project configuration
- **Contains**: Settings, URL routing, ASGI/WSGI entry points
- **Why this name**: Industry standard for Django projects (was `assistant`)

### **`apps/rest_api/copilotkit/` Folder**
- **Purpose**: CopilotKit endpoint infrastructure
- **Contains**: Endpoint handlers, SDK configuration, runtime components
- **Why this location**: CopilotKit is an endpoint, not an agent type

### **`apps/rest_api/copilotkit/agents/` Folder**
- **Purpose**: Different specialized agent implementations
- **Contains**: General, research, medical, and future agent types
- **Why this structure**: Each agent uses shared runtime as a base

### **`apps/rest_api/copilotkit/runtime/` Folder**
- **Purpose**: Shared components used by all agents
- **Contains**: Schema, models, tools that agents inherit from
- **Why this design**: DRY principle - don't repeat code across agents

## 🎯 **Architecture Benefits**

1. **Clear Separation**: Configuration vs. functionality vs. endpoints
2. **Easy Extension**: Add new agents without touching existing code
3. **Shared Resources**: Tools and models reused across agents
4. **Industry Standards**: Follows Django and Python best practices
5. **Maintainable**: Logical organization makes code easier to understand

---

**Ready to build amazing AI assistants! 🚀**

