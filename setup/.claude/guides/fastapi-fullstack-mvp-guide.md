# FastAPI Full-Stack MVP Guide

## Core Principles

1. **Single file backend** - Keep all FastAPI code in one Python file
2. **Plain frontend** - HTML/CSS/JS with CDN libraries (no build steps)
3. **Root-level environment** - All API keys in root `.env` file
4. **Independently sharable** - Each project runs standalone with pip
5. **Professional UI** - Clean, functional, great UX with Tailwind CSS

## Quick Start

### When to Create

**ONLY create full-stack apps when explicitly requested by the user.**

For other Python tasks, use `/apps/` directory for simple scripts.

### Project Location

```
full_stack_projects/<relevant-app-name>/
├── app.py              # All backend code
├── static/             # Frontend assets
│   ├── index.html      # Main UI (or use templates/)
│   ├── css/
│   ├── js/
│   └── images/
├── templates/          # Optional: Jinja2 templates
├── requirements.txt    # Pinned dependencies
├── .env.example        # Example env vars
└── README.md           # Setup instructions
```

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
mkdir -p static/{css,js,images}
touch app.py requirements.txt .env.example README.md
```

### 3. Setup Backend (app.py)

```python
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import os
from dotenv import load_dotenv

# Load environment variables from root .env
load_dotenv("../../.env")

app = FastAPI(title="<relevant-app-name>")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Models
class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    reply: str

# Routes
@app.get("/", response_class=HTMLResponse)
async def get_root():
    """Serve main page."""
    with open("static/index.html", "r") as f:
        return HTMLResponse(content=f.read())

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
```

### 4. Setup Frontend (static/index.html)

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

- `GET /` - Main UI
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

### Problem: Static files not loading
**Solution:** Check `app.mount()` path matches directory structure

### Problem: Port already in use
**Solution:** Use different port: `uvicorn app:app --port 8001`

## Summary

1. **Create only when explicitly requested**
2. **Use `/full_stack_projects/` directory**
3. **Single file backend** (app.py)
4. **Plain HTML/JS or React via CDN** (no build steps)
5. **Root `.env` for all API keys**
6. **Pin all dependencies** in requirements.txt
7. **Professional UI** with Tailwind CSS
8. **Complete README** with setup instructions
9. **Independently sharable** with pip

## Development Workflow

```bash
# 1. Create project
cd full_stack_projects && mkdir <relevant-app-name> && cd <relevant-app-name>

# 2. Setup environment
uv venv && source .venv/bin/activate

# 3. Create files
# - app.py (backend)
# - static/index.html (frontend)
# - requirements.txt
# - .env.example
# - README.md

# 4. Install dependencies
uv pip install -r requirements.txt

# 5. Configure environment
# Ensure root .env has required keys

# 6. Run
uvicorn app:app --reload

# 7. Test
# Open http://localhost:8000
```

Remember: Keep it simple, keep it clean, make it work. no hacky patches. simple yet solid, reliable, robust code.
