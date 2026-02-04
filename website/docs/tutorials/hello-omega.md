# Hello OMEGA: Your First Agent in 10 Minutes

Build your first OMEGA agent from scratch in just 10 minutes. No prior experience required!

## 🎯 What You'll Build

A simple greeting agent that:
- Responds to user messages
- Uses AI to generate personalized responses
- Registers with the OMEGA ecosystem
- Can be called by other agents

## 📋 Prerequisites

- Python 3.9+ installed
- Basic command line knowledge
- 10 minutes of your time

## 🚀 Step 1: Set Up Your Project

Create a new directory and virtual environment:

```bash
# Create project directory
mkdir hello-omega
cd hello-omega

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install OMEGA SDK
pip install omega-sdk
```

## 📝 Step 2: Create Your Agent

Create a file named `hello_agent.py`:

```python
from omega import Agent, skill
from typing import Dict, Any

class HelloAgent(Agent):
    """A friendly greeting agent."""

    def __init__(self):
        super().__init__(
            agent_id="hello_agent",
            name="Hello Agent",
            description="Greets users with personalized messages"
        )

    @skill(name="greet", description="Greet a user by name")
    async def greet(self, name: str) -> Dict[str, Any]:
        """Generate a personalized greeting."""

        greeting = f"Hello, {name}! Welcome to the OMEGA Brotherhood! 🏛️"

        return {
            "greeting": greeting,
            "agent_id": self.agent_id,
            "timestamp": self.get_timestamp()
        }

    @skill(name="farewell", description="Say goodbye to a user")
    async def farewell(self, name: str) -> Dict[str, Any]:
        """Generate a personalized farewell."""

        farewell = f"Goodbye, {name}! May the Brotherhood guide you. ⚡"

        return {
            "farewell": farewell,
            "agent_id": self.agent_id,
            "timestamp": self.get_timestamp()
        }

# Run the agent
if __name__ == "__main__":
    agent = HelloAgent()
    agent.run()
```

## ▶️ Step 3: Run Your Agent

Start your agent:

```bash
python hello_agent.py
```

**Expected Output:**
```
🏛️ OMEGA Agent Starting...
✅ Agent registered: hello_agent
✅ Skills registered: greet, farewell
🚀 Agent running on http://localhost:8000
```

## 🧪 Step 4: Test Your Agent

### Test with curl

```bash
# Test the greet skill
curl -X POST http://localhost:8000/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "skill": "greet",
    "parameters": {"name": "Brother"}
  }'
```

**Response:**
```json
{
  "greeting": "Hello, Brother! Welcome to the OMEGA Brotherhood! 🏛️",
  "agent_id": "hello_agent",
  "timestamp": "2025-01-20T15:30:00Z"
}
```

### Test with Python

Create `test_agent.py`:

```python
import requests

# Call the greet skill
response = requests.post('http://localhost:8000/invoke', json={
    "skill": "greet",
    "parameters": {"name": "Alice"}
})

print(response.json())

# Call the farewell skill
response = requests.post('http://localhost:8000/invoke', json={
    "skill": "farewell",
    "parameters": {"name": "Alice"}
})

print(response.json())
```

Run it:

```bash
python test_agent.py
```

## 🎨 Step 5: Add AI Intelligence (Optional)

Enhance your agent with AI using an LLM:

```python
from omega import Agent, skill
from openai import AsyncOpenAI
import os

class SmartHelloAgent(Agent):
    """An AI-powered greeting agent."""

    def __init__(self):
        super().__init__(
            agent_id="smart_hello_agent",
            name="Smart Hello Agent",
            description="Greets users with AI-generated messages"
        )
        self.client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    @skill(name="greet_smart", description="AI-powered personalized greeting")
    async def greet_smart(self, name: str, context: str = "") -> Dict[str, Any]:
        """Generate an AI-powered greeting."""

        prompt = f"Generate a warm, personalized greeting for {name}."
        if context:
            prompt += f" Context: {context}"

        response = await self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a friendly AI assistant in the OMEGA Brotherhood."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=100
        )

        greeting = response.choices[0].message.content

        return {
            "greeting": greeting,
            "agent_id": self.agent_id,
            "ai_powered": True,
            "timestamp": self.get_timestamp()
        }
```

## 🔌 Step 6: Register with OMEGA Ecosystem

Connect your agent to the OMEGA federation:

```python
from omega import Agent, skill
from omega.federation import FederationClient

class HelloAgent(Agent):
    def __init__(self):
        super().__init__(
            agent_id="hello_agent",
            name="Hello Agent",
            description="Greets users with personalized messages"
        )

        # Connect to federation
        self.federation = FederationClient(
            registry_url="http://localhost:9405"
        )

    async def on_start(self):
        """Called when agent starts."""

        # Register with federation
        await self.federation.register_agent({
            "id": self.agent_id,
            "name": self.name,
            "description": self.description,
            "skills": ["greet", "farewell"],
            "endpoint": f"http://localhost:{self.port}"
        })

        print(f"✅ Registered with OMEGA Federation")

    @skill(name="greet", description="Greet a user by name")
    async def greet(self, name: str) -> Dict[str, Any]:
        """Generate a personalized greeting."""

        greeting = f"Hello, {name}! Welcome to the OMEGA Brotherhood! 🏛️"

        return {
            "greeting": greeting,
            "agent_id": self.agent_id,
            "timestamp": self.get_timestamp()
        }
```

## 📊 Step 7: View Your Agent in Action

Check the OMEGA dashboard:

1. Open http://localhost:4000 (OMEGA UI)
2. Navigate to "Agents"
3. Find "Hello Agent"
4. Click "Test Agent"
5. Try the `greet` skill

## 🎓 What You Learned

✅ How to create an OMEGA agent
✅ How to define skills
✅ How to test agents locally
✅ How to add AI intelligence
✅ How to register with federation
✅ How to use the OMEGA UI

## 🚀 Next Steps

Now that you've built your first agent, explore:

1. **Building a Task Agent** - Add CRUD operations (Coming Soon)
2. **Using Tools** - Integrate tools into your agent (Coming Soon)
3. **Agent Communication** - Connect multiple agents (Coming Soon)

Check the [Tutorials Overview](/docs/tutorials/overview) for the complete learning path.

## 💡 Tips & Tricks

### Tip 1: Use Type Hints
Always use type hints for better IDE support:

```python
@skill(name="greet")
async def greet(self, name: str) -> Dict[str, Any]:
    ...
```

### Tip 2: Add Logging
Use the built-in logger:

```python
@skill(name="greet")
async def greet(self, name: str) -> Dict[str, Any]:
    self.logger.info(f"Greeting user: {name}")
    ...
```

### Tip 3: Handle Errors
Implement error handling:

```python
@skill(name="greet")
async def greet(self, name: str) -> Dict[str, Any]:
    try:
        # Your logic here
        ...
    except Exception as e:
        self.logger.error(f"Greeting failed: {e}")
        return {"error": str(e)}
```

## 🐛 Troubleshooting

### Issue: Agent won't start
**Solution:** Check if port 8000 is already in use:

```bash
# Windows
netstat -ano | findstr :8000

# Mac/Linux
lsof -i :8000
```

### Issue: Federation registration fails
**Solution:** Ensure Federation Core is running:

```bash
curl http://localhost:9405/health
```

### Issue: Skills not working
**Solution:** Verify skill registration:

```bash
curl http://localhost:8000/skills
```

## 📚 Full Code

The complete `hello_agent.py`:

```python
from omega import Agent, skill
from typing import Dict, Any

class HelloAgent(Agent):
    """A friendly greeting agent - Your first OMEGA agent!"""

    def __init__(self):
        super().__init__(
            agent_id="hello_agent",
            name="Hello Agent",
            description="Greets users with personalized messages"
        )

    @skill(name="greet", description="Greet a user by name")
    async def greet(self, name: str) -> Dict[str, Any]:
        """Generate a personalized greeting."""

        self.logger.info(f"Greeting user: {name}")

        greeting = f"Hello, {name}! Welcome to the OMEGA Brotherhood! 🏛️"

        return {
            "greeting": greeting,
            "agent_id": self.agent_id,
            "timestamp": self.get_timestamp()
        }

    @skill(name="farewell", description="Say goodbye to a user")
    async def farewell(self, name: str) -> Dict[str, Any]:
        """Generate a personalized farewell."""

        self.logger.info(f"Saying farewell to: {name}")

        farewell = f"Goodbye, {name}! May the Brotherhood guide you. ⚡"

        return {
            "farewell": farewell,
            "agent_id": self.agent_id,
            "timestamp": self.get_timestamp()
        }

if __name__ == "__main__":
    agent = HelloAgent()
    agent.run()
```

---

**🏛️ Congratulations! You've built your first OMEGA agent. The Brotherhood welcomes you!**

**Next:** [Explore More Tutorials →](/docs/tutorials/overview)
