# FastAPI Full-Stack MVP Guide

## Core Principles

1. **Single file backend** - Keep all FastAPI code in one Python file that serves frontend at root (/)
2. **Single file frontend** - HTML/CSS/JS in `frontend/index.html` with CDN libraries (no build steps)
3. **Single port deployment** - Backend serves frontend, everything runs on one port (default: 8000, auto-selects if busy)
4. **Root-level environment** - All API keys in root `.env` file
5. **Independently sharable** - Each project runs standalone with pip
6. **Professional UI** - Clean, functional, great UX with Tailwind CSS

**Key Architecture:** The backend uses `FileResponse` to serve the frontend HTML from the root endpoint (/), eliminating the need for separate static file servers or template directories. This means one command (`python app.py`) runs everything. Use automatic port selection (see Advanced Patterns) to avoid port conflicts when running multiple apps.

## Quick Start

### When to Create

**ONLY create full-stack apps when explicitly requested by the user.**

For other Python tasks, use `/apps/` directory for simple scripts.

### Project Location

```
full_stack_projects/<relevant-app-name>/
├── app.py              # All backend code (serves frontend at root)
├── frontend/           # Frontend directory
│   └── index.html      # Main UI (single file)
├── requirements.txt    # Pinned dependencies
├── .env.example        # Example env vars
└── README.md           # Setup instructions
```

**Note:** The backend serves the frontend directly from the root endpoint (/), eliminating the need for a separate static file server or template directory.

## Step-by-Step Workflow

### 1. Gather Requirements

Ask for details if not provided:

```xml
<requirements>
- What does the app do?
- What API integrations needed?
- User authentication required?
- Database needed? defaults to tinydb
- Key features 
</requirements>
```

### 2. Create Project Structure

```bash
cd full_stack_projects
mkdir <relevant-app-name> && cd <relevant-app-name>
mkdir -p frontend
touch app.py requirements.txt .env.example README.md frontend/index.html
```

### 3. Setup Backend (app.py)

```python
from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path
import os
from dotenv import load_dotenv

# Load environment variables from root .env
load_dotenv("../../.env")

app = FastAPI(title="<relevant-app-name>")

# Paths
FRONTEND_DIR = Path("frontend")
FRONTEND_HTML = FRONTEND_DIR / "index.html"

# Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Serve Frontend
@app.get("/")
async def serve_frontend():
    """Serve the frontend HTML file."""
    if FRONTEND_HTML.exists():
        return FileResponse(str(FRONTEND_HTML))
    raise HTTPException(status_code=404, detail="Frontend not found")

# API Routes
@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """Main API endpoint."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise HTTPException(status_code=500, detail="API key not configured")

    # Your logic here
    return ChatResponse(reply=f"Echo: {request.message}")

@app.get("/api/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}

# Automatic port selection (avoids conflicts when running multiple apps)
def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

if __name__ == "__main__":
    import uvicorn
    port = find_available_port(8000)
    print(f"🚀 Starting server on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Key Features:**
- Frontend served directly from root endpoint (/) using `FileResponse`
- No need for `StaticFiles` mount or templates directory
- Frontend in `frontend/index.html` (single file)
- Automatic port selection (tries 8000-8009, shows which port is used)
- Single command to run: `python app.py`

### 4. Setup Frontend (frontend/index.html)

**Option A: Plain HTML/JS**

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My App</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100 min-h-screen">
    <div class="container mx-auto p-4 max-w-2xl">
        <h1 class="text-3xl font-bold mb-6">My App</h1>

        <div id="messages" class="bg-white rounded-lg p-4 mb-4 h-96 overflow-y-auto">
        </div>

        <form id="chatForm" class="flex gap-2">
            <input
                type="text"
                id="messageInput"
                class="flex-1 px-4 py-2 border rounded-lg"
                placeholder="Type a message..."
            >
            <button
                type="submit"
                class="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700"
            >
                Send
            </button>
        </form>
    </div>

    <script>
        const form = document.getElementById('chatForm');
        const input = document.getElementById('messageInput');
        const messages = document.getElementById('messages');

        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = input.value.trim();
            if (!message) return;

            // Add user message
            addMessage('user', message);
            input.value = '';

            // Call API
            try {
                const response = await fetch('/api/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({ message })
                });
                const data = await response.json();
                addMessage('assistant', data.reply);
            } catch (error) {
                addMessage('error', 'Failed to get response');
            }
        });

        function addMessage(type, text) {
            const div = document.createElement('div');
            div.className = `mb-2 p-3 rounded ${
                type === 'user' ? 'bg-blue-100 text-right' : 'bg-gray-100'
            }`;
            div.textContent = text;
            messages.appendChild(div);
            messages.scrollTop = messages.scrollHeight;
        }
    </script>
</body>
</html>
```

**Option B: React with CDN** (for complex UIs, or if user explicitly requests)

```html
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My App</title>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body>
    <div id="root"></div>

    <script crossorigin src="https://unpkg.com/react@18/umd/react.development.js"></script>
    <script crossorigin src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
    <script src="https://unpkg.com/@babel/standalone@7.8.3/babel.js"></script>

    <script type="text/babel">
        // Components
        function UserMessage({ text }) {
            return (
                <div className="mb-2 p-3 bg-blue-100 rounded text-right">
                    {text}
                </div>
            );
        }

        function AssistantMessage({ text }) {
            return (
                <div className="mb-2 p-3 bg-gray-100 rounded">
                    {text}
                </div>
            );
        }

        // Main App
        function App() {
            const [messages, setMessages] = React.useState([]);
            const [input, setInput] = React.useState('');
            const [loading, setLoading] = React.useState(false);

            const handleSubmit = async (e) => {
                e.preventDefault();
                if (!input.trim()) return;

                const userMsg = { type: 'user', text: input };
                setMessages(prev => [...prev, userMsg]);
                setInput('');
                setLoading(true);

                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: { 'Content-Type': 'application/json' },
                        body: JSON.stringify({ message: input })
                    });
                    const data = await response.json();
                    setMessages(prev => [...prev, { type: 'assistant', text: data.reply }]);
                } catch (error) {
                    setMessages(prev => [...prev, { type: 'error', text: 'Error' }]);
                } finally {
                    setLoading(false);
                }
            };

            return (
                <div className="container mx-auto p-4 max-w-2xl min-h-screen bg-gray-100">
                    <h1 className="text-3xl font-bold mb-6">My App</h1>

                    <div className="bg-white rounded-lg p-4 mb-4 h-96 overflow-y-auto">
                        {messages.map((msg, idx) => (
                            msg.type === 'user'
                                ? <UserMessage key={idx} text={msg.text} />
                                : <AssistantMessage key={idx} text={msg.text} />
                        ))}
                    </div>

                    <form onSubmit={handleSubmit} className="flex gap-2">
                        <input
                            type="text"
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            className="flex-1 px-4 py-2 border rounded-lg"
                            placeholder="Type a message..."
                            disabled={loading}
                        />
                        <button
                            type="submit"
                            disabled={loading}
                            className="px-6 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
                        >
                            {loading ? 'Sending...' : 'Send'}
                        </button>
                    </form>
                </div>
            );
        }

        const root = ReactDOM.createRoot(document.getElementById('root'));
        root.render(<App />);
    </script>
</body>
</html>
```

### 5. Create Requirements File

```txt
# requirements.txt
fastapi==0.115.0
uvicorn==0.30.0
python-dotenv==1.0.0
pydantic==2.9.0
# Add project-specific dependencies
```

### 6. Create .env.example

```bash
# .env.example
# Copy to ../../.env (.env at the root of the project)  and fill in your values

OPENAI_API_KEY=your_key_here
ANTHROPIC_API_KEY=your_key_here
# Add other required keys
```

### 7. Create README.md

```markdown
# My App

Brief description of what the app does.

## Setup

### Using UV (Recommended)

1. Create virtual environment:
   ```bash
   uv venv
   source .venv/bin/activate  # Unix/MacOS
   # or: .venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Configure environment:
   - Ensure API keys are in root `.env` file (../../.env)
   - Or copy `.env.example` to `.env` and configure

4. Run the app:
   ```bash
   uvicorn app:app --reload
   ```

5. Open browser: http://localhost:8000

### Using pip

1. Create virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Unix/MacOS
   # or: venv\Scripts\activate  # Windows
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Configure environment (same as above)

4. Run the app (same as above)

## Features

- Feature 1
- Feature 2
- Feature 3

## API Endpoints

- `GET /` - Serves frontend HTML (single endpoint for UI)
- `POST /api/chat` - Chat endpoint
- `GET /api/health` - Health check

## Tech Stack

- Backend: FastAPI
- Frontend: HTML/CSS/JS with Tailwind CSS
- (or) Frontend: React (CDN)
```

## Common Patterns

### Database Integration (SQLite)

```python
import sqlite3
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup
    conn = sqlite3.connect("app.db")
    conn.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY,
            content TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.close()
    yield
    # Shutdown
    pass

app = FastAPI(lifespan=lifespan)

def get_db():
    conn = sqlite3.connect("app.db")
    conn.row_factory = sqlite3.Row
    return conn

@app.post("/api/save")
async def save_message(request: ChatRequest):
    conn = get_db()
    conn.execute("INSERT INTO messages (content) VALUES (?)", (request.message,))
    conn.commit()
    conn.close()
    return {"status": "saved"}
```

### API Integration (OpenAI)

```python
from openai import OpenAI

@app.post("/api/chat")
async def chat(request: ChatRequest):
    client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": request.message}]
    )

    return ChatResponse(reply=response.choices[0].message.content)
```

### File Upload

```python
from fastapi import UploadFile, File

@app.post("/api/upload")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    # Process file
    return {"filename": file.filename, "size": len(contents)}
```

### WebSocket (Real-time)

```python
from fastapi import WebSocket

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        # Process data
        await websocket.send_text(f"Echo: {data}")
```

## Quick Templates

### Minimal Chat App

```xml
<task>Create a chat app with OpenAI</task>

<features>
- Text input and send button
- Display conversation history
- Call OpenAI API for responses
- Clean UI with Tailwind CSS
</features>

<api_keys>
OPENAI_API_KEY (from root .env)
</api_keys>
```

### Todo App with Database

```xml
<task>Create a todo list app</task>

<features>
- Add/delete/complete todos
- Persist to SQLite
- Filter: all/active/completed
- Clean UI with animations
</features>

<tech>
- FastAPI backend
- Plain HTML/JS frontend
- SQLite database
</tech>
```

### Image Generator

```xml
<task>Create an image generator</task>

<features>
- Text prompt input
- Generate with DALL-E
- Display generated image
- Download button
</features>

<api_keys>
OPENAI_API_KEY (from root .env)
</api_keys>
```

## Component-Based React Pattern

For complex UIs, organize React components in a single file:

```javascript
// Constants
const MESSAGE_TYPES = {
  USER: 'user',
  ASSISTANT: 'assistant'
};

// Components
function MessageList({ messages }) {
  return (
    <div className="space-y-2">
      {messages.map((msg, idx) => (
        <Message key={idx} message={msg} />
      ))}
    </div>
  );
}

function Message({ message }) {
  return (
    <div className={`p-3 rounded ${
      message.type === MESSAGE_TYPES.USER
        ? 'bg-blue-100 text-right'
        : 'bg-gray-100'
    }`}>
      {message.text}
    </div>
  );
}

function InputForm({ onSubmit, disabled }) {
  const [input, setInput] = React.useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(input);
    setInput('');
  };

  return (
    <form onSubmit={handleSubmit} className="flex gap-2">
      <input
        value={input}
        onChange={(e) => setInput(e.target.value)}
        disabled={disabled}
        className="flex-1 px-4 py-2 border rounded-lg"
      />
      <button
        type="submit"
        disabled={disabled}
        className="px-6 py-2 bg-blue-600 text-white rounded-lg"
      >
        Send
      </button>
    </form>
  );
}

// Main App
function App() {
  const [messages, setMessages] = React.useState([]);
  const [loading, setLoading] = React.useState(false);

  const handleSend = async (text) => {
    // API logic
  };

  return (
    <div className="container mx-auto p-4">
      <MessageList messages={messages} />
      <InputForm onSubmit={handleSend} disabled={loading} />
    </div>
  );
}
```

## Best Practices

### Security

```python
# CORS for production
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://yourdomain.com"],  # keep "*" in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input validation
from pydantic import BaseModel, Field, validator

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=1000)

    @validator('message')
    def message_not_empty(cls, v):
        if not v.strip():
            raise ValueError('Message cannot be empty')
        return v
```

### Error Handling

```python
from fastapi import HTTPException

@app.post("/api/chat")
async def chat(request: ChatRequest):
    try:
        # Your logic
        return response
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="Internal server error")
```

### Environment Variables

```python
# Always load from root .env
load_dotenv("../../.env")

# Validate required keys on startup
REQUIRED_KEYS = ["OPENAI_API_KEY"]
missing_keys = [key for key in REQUIRED_KEYS if not os.getenv(key)]
if missing_keys:
    raise RuntimeError(f"Missing required environment variables: {missing_keys}")
```

## Troubleshooting

### Problem: Module not found
**Solution:** Install dependencies: `uv pip install -r requirements.txt`

### Problem: API key not found
**Solution:** Ensure `.env` exists at project root with required keys

### Problem: CORS errors
**Solution:** Add CORS middleware (see Security section)

### Problem: Frontend not loading
**Solution:** Ensure `frontend/index.html` exists and path in app.py is correct

### Problem: Port already in use
**Solution:** Add automatic port selection (see Advanced Patterns section below)

## Advanced Patterns

### Automatic Port Selection

When running multiple apps simultaneously, automatically find available ports:

```python
def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    import socket
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('0.0.0.0', port))
                return port
        except OSError:
            continue
    raise RuntimeError(f"Could not find available port in range {start_port}-{start_port + max_attempts}")

if __name__ == "__main__":
    import uvicorn
    port = find_available_port(8000)
    print(f"🚀 Starting server on http://localhost:{port}")
    uvicorn.run(app, host="0.0.0.0", port=port)
```

**Benefits:**
- No port conflicts when running multiple apps
- Automatically tries ports 8000-8009 (configurable)
- Shows which port was selected

### Dynamic API URLs (Multi-Port Frontend)

Always use dynamic API URLs in frontend to support different ports:

```javascript
// ❌ Bad - Hardcoded port
const API_BASE_URL = 'http://localhost:8000/api';

// ✅ Good - Dynamic based on current page
const API_BASE_URL = `${window.location.origin}/api`;
```

**Why this matters:**
- Works on any port (8000, 8001, 8002...)
- Works in production (different domains)
- No CORS issues
- No frontend code changes needed when port changes

### Custom Loading Animations

For better user feedback, implement custom CSS animations when Tailwind utilities aren't sufficient:

```html
<style>
    /* Circular pulsing animation for icons */
    @keyframes circularPulse {
        0% { transform: scale(1) translate(0, 0); }
        25% { transform: scale(1.2) translate(2px, -2px); }
        50% { transform: scale(1) translate(2px, 2px); }
        75% { transform: scale(1.2) translate(-2px, 2px); }
        100% { transform: scale(1) translate(0, 0); }
    }

    .search-icon-animated {
        display: inline-block;
        animation: circularPulse 1s ease-in-out infinite;
    }
</style>

<!-- Usage -->
<div class="search-icon-animated">🔍</div>
```

**JavaScript-based animation** (when CSS doesn't work):

```javascript
// Animated dots: Searching → Searching. → Searching.. → Searching...
let dots = '';
const loadingInterval = setInterval(() => {
    dots = dots.length >= 3 ? '' : dots + '.';
    button.textContent = 'Searching' + dots;
}, 400);

// Clear when done
clearInterval(loadingInterval);
```

**Best practices:**
- Use CSS animations for visual effects (rotating, pulsing)
- Use JavaScript for text/content updates
- Always provide visual feedback during async operations
- Test animations work across browsers

### Student-Friendly Free APIs

Prioritize APIs with generous free tiers for educational projects:

```python
# ✅ Free tier options

# Google Gemini (Free: 15 RPM, 1M TPM, 1500 RPD)
import google.generativeai as genai
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-2.0-flash-exp')

# Groq (Free: 30 RPM, 6K TPM, 1K RPD)
from langchain_groq import ChatGroq
llm = ChatGroq(model="llama-3.3-70b-versatile")

# Tavily Search (Free: 1000 searches/month)
from tavily import AsyncTavilyClient
client = AsyncTavilyClient(api_key=TAVILY_API_KEY)
```

**Cost tracking in documentation:**

```markdown
## API Costs

**💰 Total Cost: $0 (Free tier)**

APIs used:
- Tavily: 1000 searches/month free
- Google Gemini Flash: 15 RPM, 1M TPM, 1500 RPD free
- Groq: 30 RPM, 6K TPM, 1K RPD free

Perfect for students and learning!
```

### Testing with chrome-devtools MCP

Add comprehensive testing using chrome-devtools MCP server:

```python
# Test with chrome-devtools MCP
# 1. Navigate to app
await mcp__chrome-devtools__browser_navigate(url="http://localhost:8000")

# 2. Fill form
await mcp__chrome-devtools__browser_type(
    element="search input",
    ref="e18",
    text="test query"
)

# 3. Click button
await mcp__chrome-devtools__browser_click(
    element="search button",
    ref="e19"
)

# 4. Verify results loaded
# Check page snapshot for expected content
```

**Testing checklist:**
- ✅ Page loads without errors
- ✅ Forms accept input
- ✅ Buttons trigger actions
- ✅ Loading states show correctly
- ✅ Results display properly
- ✅ Error handling works

### Async API Patterns

Use parallel API calls for better performance:

```python
import asyncio

async def search_restaurants(query: str):
    # Search multiple APIs in parallel
    tavily_task = search_tavily(query)
    gemini_task = search_gemini(query)

    # Wait for all to complete
    tavily_results, gemini_results = await asyncio.gather(
        tavily_task,
        gemini_task,
        return_exceptions=True
    )

    # Handle errors gracefully
    if isinstance(tavily_results, Exception):
        tavily_results = []
    if isinstance(gemini_results, Exception):
        gemini_results = []

    # Merge and return
    return merge_results(tavily_results, gemini_results)
```

**Benefits:**
- Faster response times (parallel vs sequential)
- Graceful error handling
- Better user experience

## Summary

1. **Create only when explicitly requested**
2. **Use `/full_stack_projects/` directory**
3. **Single file backend** (app.py) - serves frontend at root (/)
4. **Single file frontend** (frontend/index.html) - served by backend
5. **Plain HTML/JS or React via CDN** (no build steps)
6. **Root `.env` for all API keys**
7. **Pin all dependencies** in requirements.txt
8. **Professional UI** with Tailwind CSS
9. **Complete README** with setup instructions
10. **Independently sharable** with pip
11. **Single port deployment** - defaults to port 8000, auto-selects if busy (see Advanced Patterns)

## Development Workflow

```bash
# 1. Create project
cd full_stack_projects && mkdir <relevant-app-name> && cd <relevant-app-name>

# 2. Setup environment
uv venv && source .venv/bin/activate

# 3. Create files
mkdir -p frontend
touch app.py requirements.txt .env.example README.md frontend/index.html

# 4. Write code
# - app.py: Backend with FileResponse at root (/)
# - frontend/index.html: Single-file UI with CDN libraries

# 5. Install dependencies
uv pip install -r requirements.txt

# 6. Configure environment
# Ensure root .env has required keys

# 7. Run (single command, single port)
python app.py
# Or: uvicorn app:app --reload

# 8. Test
# Open http://localhost:8000 (frontend served from root)
```

**Key Benefits:**
- ✅ No separate frontend server needed
- ✅ Simple deployment (just run app.py)
- ✅ Clean project structure

Remember: Keep it simple, keep it clean, make it work. no hacky patches. simple yet solid, reliable, robust code.
