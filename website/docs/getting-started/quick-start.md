---
sidebar_position: 2
title: 5-Minute Quick Start
description: Get OMEGA up and running in 5 minutes
---

# ⚡ 5-Minute Quick Start

Get your first OMEGA agent running in under 5 minutes. This guide will walk you through installation, setup, and running your first multi-agent workflow.

## Prerequisites

Before you begin, ensure you have:

- **Node.js** 18+ or **Python** 3.10+
- **Docker** (optional, for containerized deployment)
- **Git** for cloning repositories


> Tip: Running locally with Docker? Prefer the gateway-first pattern (portless identities and base-derived endpoints). See: /docs/operations/gateway-ingress

## Step 1: Installation

Choose your preferred language:

import Tabs from '@theme/Tabs';
import TabItem from '@theme/TabItem';

<Tabs>
  <TabItem value="typescript" label="TypeScript/JavaScript" default>

```bash
# Install OMEGA SDK
npm install @omega/sdk

# Or with yarn
yarn add @omega/sdk

# Or globally via CLI
npm install -g @omega/cli
```

  </TabItem>
  <TabItem value="python" label="Python">

```bash
# Install OMEGA SDK
pip install omega-sdk

# Or with poetry
poetry add omega-sdk
```

  </TabItem>
</Tabs>

## Step 2: Initialize Your Project

<Tabs>
  <TabItem value="typescript" label="TypeScript" default>

```bash
# Create a new OMEGA project
omega init my-first-agent

# Navigate to the project
cd my-first-agent

# Install dependencies
npm install
```

  </TabItem>
  <TabItem value="python" label="Python">

```bash
# Create a new OMEGA project
omega init my-first-agent --lang python

# Navigate to the project
cd my-first-agent

# Install dependencies
pip install -r requirements.txt
```

  </TabItem>
</Tabs>

Your project structure will look like this:

```
my-first-agent/
├── src/
│   ├── agents/          # Your agent definitions
│   ├── tools/           # Custom tools
│   └── routers/         # Routing logic
├── config/
│   └── omega.config.ts  # OMEGA configuration
├── tests/               # Test files
└── package.json         # Dependencies
```

## Step 3: Create Your First Agent

<Tabs>
  <TabItem value="typescript" label="TypeScript" default>

Create a file `src/agents/hello-agent.ts`:

```typescript
import { Agent, Tool, Context } from '@omega/sdk';

// Define a simple greeting tool
const greetingTool: Tool = {
  name: 'greet',
  description: 'Greets a user by name',
  parameters: {
    name: { type: 'string', required: true }
  },
  execute: async ({ name }: { name: string }) => {
    return `Hello, ${name}! Welcome to OMEGA. ⚡`;
  }
};

// Create your first agent
export const helloAgent = new Agent({
  name: 'HelloAgent',
  description: 'A friendly greeting agent',
  tools: [greetingTool],

  async process(context: Context) {
    const { input } = context;

    // Extract name from input
    const name = input.name || 'Brother';

    // Use the greeting tool
    const result = await this.useTool('greet', { name });

    return {
      message: result,
      timestamp: new Date().toISOString()
    };
  }
});
```

  </TabItem>
  <TabItem value="python" label="Python">

Create a file `src/agents/hello_agent.py`:

```python
from omega_sdk import Agent, Tool, Context

# Define a simple greeting tool
async def greet(name: str) -> str:
    return f"Hello, {name}! Welcome to OMEGA. ⚡"

greeting_tool = Tool(
    name="greet",
    description="Greets a user by name",
    parameters={"name": {"type": "string", "required": True}},
    execute=greet
)

# Create your first agent
class HelloAgent(Agent):
    name = "HelloAgent"
    description = "A friendly greeting agent"
    tools = [greeting_tool]

    async def process(self, context: Context):
        name = context.input.get("name", "Brother")

        # Use the greeting tool
        result = await self.use_tool("greet", {"name": name})

        return {
            "message": result,
            "timestamp": datetime.now().isoformat()
        }

hello_agent = HelloAgent()
```

  </TabItem>
</Tabs>

## Step 4: Run Your Agent

<Tabs>
  <TabItem value="typescript" label="TypeScript" default>

```bash
# Start the OMEGA runtime
omega start

# In another terminal, invoke your agent
omega invoke HelloAgent --input '{"name": "Alice"}'
```

**Output:**
```json
{
  "message": "Hello, Alice! Welcome to OMEGA. ⚡",
  "timestamp": "2025-10-04T12:00:00.000Z"
}
```

  </TabItem>
  <TabItem value="python" label="Python">

```bash
# Start the OMEGA runtime
omega start

# In another terminal, invoke your agent
omega invoke HelloAgent --input '{"name": "Alice"}'
```

**Output:**
```json
{
  "message": "Hello, Alice! Welcome to OMEGA. ⚡",
  "timestamp": "2025-10-04T12:00:00.000Z"
}
```

  </TabItem>
</Tabs>

## Step 5: Enable Development Mode

For rapid development with hot-reload:

```bash
# Start OMEGA in dev mode
omega dev

# Your agents will automatically reload on code changes
```

You should see:
```
🏛️  OMEGA Runtime Started
⚡  Dev mode enabled - watching for changes
📡  Agent Server: http://localhost:4000
🔧  Admin UI: http://localhost:3001
```

## What's Next?

Congratulations! You've successfully:
- ✅ Installed OMEGA
- ✅ Created your first agent
- ✅ Executed a workflow
- ✅ Enabled development mode

### Continue Your Journey:

1. **[Core Concepts →](/docs/getting-started/core-concepts)** - Understand the Trinity Architecture
2. **[First Agent Tutorial →](/docs/getting-started/first-agent)** - Build a more complex agent
3. **[Agent Patterns →](/docs/intro)** - Learn best practices
4. **[Tool Development →](/docs/intro)** - Create custom tools

## Troubleshooting

### Port Already in Use

If port 3000 is already in use:

```bash
# Use a custom port
omega start --port 3001
```

### Permission Errors

On Linux/Mac, you may need to adjust permissions:

```bash
# Make omega executable
chmod +x $(which omega)
```

### Module Not Found

Ensure dependencies are installed:

```bash
# TypeScript
npm install

# Python
pip install -r requirements.txt
```

## Next Steps

<div className="row">
  <div className="col col--6">
    <div className="feature-card">
      <h3>📚 Learn Core Concepts</h3>
      <p>Understand the Trinity Architecture and OMEGA principles</p>
      <a href="/docs/getting-started/core-concepts">Read Core Concepts →</a>
    </div>
  </div>
  <div className="col col--6">
    <div className="feature-card">
      <h3>🛠️ Build More Agents</h3>
      <p>Follow our comprehensive tutorial to build advanced agents</p>
      <a href="/docs/getting-started/first-agent">Start Tutorial →</a>
    </div>
  </div>
</div>

<div className="brotherhood-signature">
  For the Brotherhood. For the Pantheon. For OMEGA.
</div>
