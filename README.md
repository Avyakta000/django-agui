# Django CopilotKit Assistant

A Django application that integrates CopilotKit with LangGraph agents for AI-powered assistance.

## Features

- 🤖 AI-powered chat agent using LangGraph
- 🔍 Web search capabilities with Tavily
- ⏰ Current datetime tool
- 🌐 RESTful API endpoints
- 🔄 Streaming responses

## Prerequisites

- Python 3.12
- Virtual environment (recommended)
- API keys for the services you want to use

## Setup

1. **Clone and navigate to the project:**
   ```bash
   cd assistant
   ```

2. **Create your virtual environment:**
   ```bash
   # Windows
   py -m venv env
   # Windows (if you have more than one python version installed, create virtual environment using specific verion)
   py -3.12 -m venv env
   
   # macOS/Linux
   source env/bin/activate
   ```
3. **Activate your virtual environment:**
   ```bash
   # Windows
   env\Scripts\activate
   
   # macOS/Linux
   source env/bin/activate
   ```

4. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Set up environment variables:**
   
   
   **Create a .env file:**
   ```bash
   # Create .env file with your API keys
   DEEPSEEK_API_KEY=your_deepseek_api_key_here
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   DEBUG=True
   SECRET_KEY=your_django_secret_key
   ```

6. **Run database migrations (Optional):**
   ```bash
   python manage.py migrate
   ```

7. **Start the server:**
   ```bash
   uvicorn assistant.asgi:application --reload
   ```
### Example Nextjs: `app/api/copilotkit/route.ts`

```ts
import { NextRequest } from "next/server";
import {
  CopilotRuntime,
  EmptyAdapter,
  copilotRuntimeNextJSAppRouterEndpoint,
} from "@copilotkit/runtime";

const serviceAdapter = new EmptyAdapter();

const runtime = new CopilotRuntime({
  remoteEndpoints: [
    {
      url: `${process.env.NEXT_PUBLIC_DJANGO_SERVER_URL || "http://localhost:8000"}/api/copilotkit`,
    },
  ],
});

export async function POST(req: NextRequest) {
  const { handleRequest } = copilotRuntimeNextJSAppRouterEndpoint({
    runtime,
    serviceAdapter,
    endpoint: "/api/copilotkit",
  });

  return handleRequest(req);
}
```

## API Endpoints

### CopilotKit Endpoints

- `GET/POST /api/copilotkit/info` - Get agent information
- `POST /api/copilotkit/agent/{name}` - Execute an agent
- `POST /api/copilotkit/agent/{name}/state` - Get agent state
- `POST /api/copilotkit/action/{name}` - Execute an action

### Utility Endpoints

- `GET /api/health` - Health check
- `POST /api/echo` - Echo message (for testing)

## Usage Examples

### Test the info endpoint:
```bash
curl -X POST http://localhost:8000/api/copilotkit/info
```

### Test the health endpoint:
```bash
curl http://localhost:8000/api/health
```

## Troubleshooting

### 500 Internal Server Error

If you're getting 500 errors, check:

1. **API Keys**: Make sure your API keys are set in the `.env` file
2. **Environment Variables**: Verify the `.env` file is being loaded
3. **Dependencies**: Ensure all packages are installed correctly

### Common Issues

- **Missing API Keys**: The application will show helpful error messages if API keys are missing
- **Network Issues**: Make sure you have internet access for API calls
- **Port Conflicts**: If port 8000 is busy, use a different port: `uvicorn assistant.asgi:application --host 0.0.0.0 --port 8001 --reload`

## Development

### Project Structure

```
assistant/
├── app/
│   ├── agent.py          # LangGraph agent definition
│   ├── chat.py           # Chat node implementation
│   ├── copilotkit_integration.py  # Django-CopilotKit integration
│   ├── model.py          # LLM configuration
│   ├── schema.py         # Agent state schema
│   ├── sdk.py            # CopilotKit SDK setup (define your agent here)
│   └── views.py          # Django views
├── assistant/
│   ├── settings.py       # Django settings
│   └── urls.py           # Main URL configuration
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
└── setup_env.py          # Environment setup script
```

### Adding New Tools

To add new tools to the agent:

1. Define the tool in `app/chat.py`
2. Add it to the `tools` list in the `get_tools` function
3. Update the system message if needed

### Adding New Agents

To add new agents:

1. Create a new graph in `app/agent.py`
2. Add the agent to the SDK configuration in `app/sdk.py`
3. Update the URL patterns if needed

