---
sidebar_position: 4
title: Build Your First Agent
description: Comprehensive tutorial for building a production-ready OMEGA agent
---

# Build Your First Agent

In this tutorial, you'll build a **Task Management Agent** that demonstrates the full power of the OMEGA platform. This agent will:

- ✅ Accept task creation requests
- 🔄 Coordinate with multiple tools
- 📊 Manage state across requests
- 🎯 Route to specialized sub-agents
- 📝 Generate comprehensive reports

## What You'll Learn

- Agent architecture and patterns
- Tool integration and development
- State management
- Error handling and retry logic
- Agent-to-Agent communication
- Testing and deployment

## Prerequisites

Ensure you've completed the [Quick Start](/docs/getting-started/quick-start) guide and have:
- OMEGA SDK installed
- A working project initialized
- Basic understanding of the [Core Concepts](/docs/getting-started/core-concepts)

## Step 1: Define the Agent Structure

Create a file `src/agents/task-agent.ts`:

```typescript
import { Agent, Context, Tool } from '@omega/sdk';

interface Task {
  id: string;
  title: string;
  description: string;
  priority: 'low' | 'medium' | 'high';
  status: 'pending' | 'in-progress' | 'completed';
  assignee?: string;
  createdAt: Date;
  updatedAt: Date;
}

export const taskAgent = new Agent({
  name: 'TaskManagementAgent',
  description: 'Manages tasks with intelligent prioritization and routing',
  version: '1.0.0',

  // We'll implement this in the next steps
  async process(context: Context) {
    // Processing logic here
  }
});
```

## Step 2: Create Supporting Tools

Define tools that the agent will use:

```typescript
// Tool 1: Create Task
const createTaskTool: Tool = {
  name: 'createTask',
  description: 'Creates a new task in the system',

  parameters: {
    title: { type: 'string', required: true },
    description: { type: 'string', required: true },
    priority: {
      type: 'string',
      enum: ['low', 'medium', 'high'],
      default: 'medium'
    },
    assignee: { type: 'string', required: false }
  },

  async execute({ title, description, priority, assignee }) {
    const task: Task = {
      id: generateId(),
      title,
      description,
      priority,
      status: 'pending',
      assignee,
      createdAt: new Date(),
      updatedAt: new Date()
    };

    await database.tasks.insert(task);

    return {
      success: true,
      task
    };
  }
};

// Tool 2: Update Task Status
const updateTaskTool: Tool = {
  name: 'updateTaskStatus',
  description: 'Updates the status of an existing task',

  parameters: {
    taskId: { type: 'string', required: true },
    status: {
      type: 'string',
      enum: ['pending', 'in-progress', 'completed'],
      required: true
    }
  },

  async execute({ taskId, status }) {
    const task = await database.tasks.findById(taskId);

    if (!task) {
      throw new Error(`Task ${taskId} not found`);
    }

    task.status = status;
    task.updatedAt = new Date();

    await database.tasks.update(taskId, task);

    return {
      success: true,
      task
    };
  }
};

// Tool 3: Prioritize Tasks
const prioritizeTasksTool: Tool = {
  name: 'prioritizeTasks',
  description: 'Intelligently prioritizes tasks based on criteria',

  parameters: {
    tasks: { type: 'array', required: true },
    criteria: {
      type: 'string',
      enum: ['deadline', 'priority', 'assignee'],
      default: 'priority'
    }
  },

  async execute({ tasks, criteria }) {
    // Prioritization logic
    const prioritized = tasks.sort((a, b) => {
      if (criteria === 'priority') {
        const priorityOrder = { high: 3, medium: 2, low: 1 };
        return priorityOrder[b.priority] - priorityOrder[a.priority];
      }
      // Add more criteria...
      return 0;
    });

    return {
      success: true,
      prioritizedTasks: prioritized
    };
  }
};
```

## Step 3: Implement the Agent Logic

Now implement the main processing logic:

```typescript
export const taskAgent = new Agent({
  name: 'TaskManagementAgent',
  description: 'Manages tasks with intelligent prioritization and routing',
  version: '1.0.0',

  tools: [createTaskTool, updateTaskTool, prioritizeTasksTool],

  async process(context: Context) {
    const { action, data } = context.input;

    switch (action) {
      case 'create':
        return await this.handleCreate(context, data);

      case 'update':
        return await this.handleUpdate(context, data);

      case 'list':
        return await this.handleList(context, data);

      case 'prioritize':
        return await this.handlePrioritize(context, data);

      default:
        throw new Error(`Unknown action: ${action}`);
    }
  },

  async handleCreate(context: Context, data: any) {
    // Use the create task tool
    const result = await this.useTool('createTask', data);

    // Check if high priority - route to notification agent
    if (data.priority === 'high') {
      await this.routeTo('NotificationAgent', {
        type: 'task_created',
        task: result.task
      });
    }

    return {
      success: true,
      message: 'Task created successfully',
      task: result.task
    };
  },

  async handleUpdate(context: Context, data: any) {
    const result = await this.useTool('updateTaskStatus', data);

    // If completed, trigger reporting
    if (data.status === 'completed') {
      await this.routeTo('ReportingAgent', {
        type: 'task_completed',
        task: result.task
      });
    }

    return {
      success: true,
      message: 'Task updated successfully',
      task: result.task
    };
  },

  async handleList(context: Context, data: any) {
    const tasks = await database.tasks.findAll(data.filters);

    return {
      success: true,
      tasks,
      count: tasks.length
    };
  },

  async handlePrioritize(context: Context, data: any) {
    const tasks = await database.tasks.findAll();
    const result = await this.useTool('prioritizeTasks', {
      tasks,
      criteria: data.criteria
    });

    return {
      success: true,
      prioritizedTasks: result.prioritizedTasks
    };
  }
});
```

## Step 4: Add Error Handling

Implement robust error handling:

```typescript
export const taskAgent = new Agent({
  // ... previous configuration

  errorStrategy: {
    retry: {
      maxAttempts: 3,
      backoff: 'exponential',
      retryOn: ['network', 'timeout', 'database']
    },
    fallback: ['BackupTaskAgent'],
    circuitBreaker: {
      threshold: 5,
      timeout: 30000
    }
  },

  async onError(error: Error, context: Context) {
    // Log error
    this.logger.error(`Task agent error: ${error.message}`, {
      requestId: context.requestId,
      input: context.input,
      stack: error.stack
    });

    // Send to monitoring
    await monitoring.trackError(error, {
      agent: this.name,
      context
    });

    // Return user-friendly error
    return {
      success: false,
      error: 'Failed to process task request',
      requestId: context.requestId
    };
  }
});
```

## Step 5: Add Observability

Instrument your agent for monitoring:

```typescript
export const taskAgent = new Agent({
  // ... previous configuration

  async beforeProcess(context: Context) {
    // Start tracing
    const span = tracer.startSpan('task-agent-process', {
      requestId: context.requestId,
      action: context.input.action
    });

    context.metadata.span = span;

    // Log request
    this.logger.info('Processing task request', {
      requestId: context.requestId,
      action: context.input.action
    });
  },

  async afterProcess(context: Context, result: any) {
    // End tracing
    const span = context.metadata.span;
    span.end();

    // Log result
    this.logger.info('Task request completed', {
      requestId: context.requestId,
      success: result.success
    });

    // Track metrics
    metrics.increment('task_agent.requests', {
      action: context.input.action,
      status: result.success ? 'success' : 'failure'
    });
  }
});
```

## Step 6: Write Tests

Create comprehensive tests in `tests/agents/task-agent.test.ts`:

```typescript
import { describe, it, expect, beforeEach } from 'vitest';
import { taskAgent } from '@/agents/task-agent';
import { createContext } from '@omega/sdk/testing';

describe('TaskManagementAgent', () => {
  beforeEach(async () => {
    await database.tasks.clear();
  });

  it('creates a task successfully', async () => {
    const context = createContext({
      input: {
        action: 'create',
        data: {
          title: 'Test Task',
          description: 'Test Description',
          priority: 'high'
        }
      }
    });

    const result = await taskAgent.process(context);

    expect(result.success).toBe(true);
    expect(result.task.title).toBe('Test Task');
    expect(result.task.priority).toBe('high');
  });

  it('updates task status', async () => {
    // Create task first
    const task = await createTestTask();

    const context = createContext({
      input: {
        action: 'update',
        data: {
          taskId: task.id,
          status: 'in-progress'
        }
      }
    });

    const result = await taskAgent.process(context);

    expect(result.success).toBe(true);
    expect(result.task.status).toBe('in-progress');
  });

  it('handles errors gracefully', async () => {
    const context = createContext({
      input: {
        action: 'update',
        data: {
          taskId: 'non-existent',
          status: 'completed'
        }
      }
    });

    const result = await taskAgent.process(context);

    expect(result.success).toBe(false);
    expect(result.error).toBeDefined();
  });
});
```

## Step 7: Deploy Your Agent

Deploy to production:

```bash
# Build the agent
omega build

# Run tests
omega test

# Deploy to staging
omega deploy --env staging

# Deploy to production (after validation)
omega deploy --env production
```

## Testing Your Agent

Invoke your agent locally:

```bash
# Create a task
omega invoke TaskManagementAgent --input '{
  "action": "create",
  "data": {
    "title": "Implement user authentication",
    "description": "Add JWT-based auth to the API",
    "priority": "high",
    "assignee": "alice@example.com"
  }
}'

# Update task status
omega invoke TaskManagementAgent --input '{
  "action": "update",
  "data": {
    "taskId": "task-123",
    "status": "completed"
  }
}'

# List and prioritize tasks
omega invoke TaskManagementAgent --input '{
  "action": "prioritize",
  "data": {
    "criteria": "priority"
  }
}'
```

## What You've Built

Congratulations! You've built a production-ready OMEGA agent with:

- ✅ **Multi-tool integration** - Create, update, and prioritize tasks
- ✅ **Agent routing** - Coordinate with notification and reporting agents
- ✅ **Error handling** - Retry logic and fallback strategies
- ✅ **Observability** - Logging, tracing, and metrics
- ✅ **Testing** - Comprehensive test coverage
- ✅ **Deployment** - Production-ready configuration

## Next Steps

Continue your OMEGA journey:

1. **[Agent Patterns →](/docs/intro)** - Learn advanced agent patterns
2. **[Tool Development →](/docs/intro)** - Build custom tools
3. **[Router Design →](/docs/intro)** - Create intelligent routers
4. **[Production Deployment →](/docs/intro)** - Deploy to production

<div className="brotherhood-signature">
  For the Brotherhood. For the Pantheon. For OMEGA.
</div>
