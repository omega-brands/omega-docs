# Advanced Tool Patterns

Master advanced tool development techniques including lifecycle hooks, context-aware execution, and specialized tool patterns.

## 🪝 Lifecycle Hooks

OMEGA tools can integrate with the agent lifecycle through **hook execution** - allowing tools to participate in critical workflow stages.

### What are Lifecycle Hooks?

Hooks are execution points in the agent lifecycle where tools can inject custom logic:

- **`oracle`** - Pre-task intelligence gathering
- **`on_task`** - During task execution
- **`post_task`** - After task completion
- **`absorb`** - Learning and memory integration

### The Hook Executor Pattern

```python
from tools.base import OmegaTool
from typing import Any, Dict

class HookExecutorTool(OmegaTool):
    """Context-aware lifecycle hook execution."""

    def __init__(self):
        super().__init__(
            name="hook_executor",
            description="Executes lifecycle hooks based on context and priority"
        )

    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a lifecycle hook."""

        operation = payload.get("operation")

        if operation == "execute_hook":
            return await self._execute_hook(payload)
        else:
            return {"error": f"Unknown operation: {operation}"}

    async def _execute_hook(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        """Execute specific hook type with context."""

        hook_type = payload.get("hook_type")
        context = payload.get("context", {})

        # Route to appropriate hook handler
        if hook_type == "oracle":
            return await self._oracle_hook(context)
        elif hook_type == "post_task":
            return await self._post_task_hook(context)
        elif hook_type == "absorb":
            return await self._absorb_hook(context)
        else:
            return {"error": f"Unknown hook type: {hook_type}"}
```

### Example: Oracle Hook

The Oracle hook gathers intelligence before task execution:

```python
async def _oracle_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
    """Pre-task intelligence gathering."""

    task_id = context.get("task_id")
    payload = context.get("payload", {})

    # Gather contextual intelligence
    intel = {
        "task_id": task_id,
        "timestamp": datetime.utcnow().isoformat(),
        "intelligence": {
            "similar_tasks": await self._find_similar_tasks(payload),
            "recommended_approach": await self._analyze_approach(payload),
            "potential_risks": await self._identify_risks(payload)
        }
    }

    return {
        "hook_type": "oracle",
        "status": "complete",
        "intel": intel
    }

async def _find_similar_tasks(self, payload: Dict) -> List[Dict]:
    """Find similar historical tasks."""
    # Query vector store for semantic similarity
    return [
        {"task_id": "xyz789", "similarity": 0.92},
        {"task_id": "abc456", "similarity": 0.87}
    ]
```

### Example: Post-Task Hook

The Post-Task hook processes results after execution:

```python
async def _post_task_hook(self, context: Dict[str, Any]) -> Dict[str, Any]:
    """Post-task result processing."""

    task_id = context.get("task_id")
    result = context.get("result")
    success = context.get("success", False)

    # Process the result
    processed = {
        "task_id": task_id,
        "timestamp": datetime.utcnow().isoformat(),
        "result_analysis": {
            "success": success,
            "quality_score": await self._score_result(result),
            "lessons_learned": await self._extract_lessons(result),
            "next_actions": await self._suggest_next_actions(result)
        }
    }

    return {
        "hook_type": "post_task",
        "status": "complete",
        "analysis": processed
    }
```

### Invocation Example

```http
POST /invoke
Content-Type: application/json

{
  "operation": "execute_hook",
  "hook_type": "oracle",
  "context": {
    "task_id": "abc123",
    "payload": {
      "question": "What is the next best action?",
      "domain": "code_generation"
    }
  }
}
```

**Response:**
```json
{
  "hook_type": "oracle",
  "status": "complete",
  "intel": {
    "task_id": "abc123",
    "timestamp": "2025-05-25T14:30:00Z",
    "intelligence": {
      "similar_tasks": [
        {"task_id": "xyz789", "similarity": 0.92}
      ],
      "recommended_approach": "Use code_generator agent with validation",
      "potential_risks": ["Complex dependencies", "API rate limits"]
    }
  }
}
```

---

## 🔄 Context-Aware Tools

Build tools that adapt behavior based on execution context.

### Context7 Compliance

Context-aware tools follow the **Context7** pattern - self-weaving based on environmental signals:

```python
class ContextAwareTool(OmegaTool):
    """Tool that adapts to execution context."""

    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        # Extract context signals
        context = payload.get("context", {})

        # Adapt behavior based on context
        if context.get("environment") == "production":
            return await self._production_mode(payload)
        elif context.get("environment") == "development":
            return await self._development_mode(payload)
        else:
            return await self._default_mode(payload)

    async def _production_mode(self, payload: Dict) -> Dict:
        """Production: strict validation, error handling."""
        # Validate thoroughly
        errors = await self._strict_validation(payload)
        if errors:
            return {"error": "Validation failed", "details": errors}

        # Execute with safety checks
        return await self._execute_safely(payload)

    async def _development_mode(self, payload: Dict) -> Dict:
        """Development: verbose output, debug info."""
        result = await self._execute(payload)
        result["debug"] = {
            "execution_time": "...",
            "memory_usage": "...",
            "trace": "..."
        }
        return result
```

### Priority-Based Execution

Handle operations based on priority levels:

```python
async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
    priority = payload.get("priority", "normal")

    # Route based on priority
    if priority == "critical":
        return await self._critical_execution(payload)
    elif priority == "high":
        return await self._high_priority_execution(payload)
    else:
        return await self._normal_execution(payload)

async def _critical_execution(self, payload: Dict) -> Dict:
    """Critical: immediate execution, bypass queues."""
    # Execute immediately without queuing
    result = await self._execute_immediate(payload)

    # Send alerts if failed
    if not result.get("success"):
        await self._send_critical_alert(result)

    return result
```

---

## 🎨 Specialized Tool Patterns

### Pattern 1: Multi-Stage Processing

Tools that execute operations in stages:

```python
class MultiStageTool(OmegaTool):
    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        stages = payload.get("stages", ["validate", "process", "finalize"])
        data = payload.get("data")

        results = []
        for stage in stages:
            result = await self._execute_stage(stage, data)
            results.append(result)

            # Use output as input for next stage
            data = result.get("output", data)

            # Stop on failure
            if not result.get("success"):
                break

        return {
            "stages_completed": len(results),
            "results": results,
            "final_output": data
        }

    async def _execute_stage(self, stage: str, data: Any) -> Dict:
        handlers = {
            "validate": self._validate_stage,
            "process": self._process_stage,
            "finalize": self._finalize_stage
        }

        handler = handlers.get(stage)
        if not handler:
            return {"success": False, "error": f"Unknown stage: {stage}"}

        return await handler(data)
```

### Pattern 2: Batch Processing

Process multiple items efficiently:

```python
class BatchProcessorTool(OmegaTool):
    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        items = payload.get("items", [])
        batch_size = payload.get("batch_size", 10)
        parallel = payload.get("parallel", False)

        results = []

        # Process in batches
        for i in range(0, len(items), batch_size):
            batch = items[i:i+batch_size]

            if parallel:
                batch_results = await self._process_parallel(batch)
            else:
                batch_results = await self._process_sequential(batch)

            results.extend(batch_results)

        return {
            "total_items": len(items),
            "processed": len(results),
            "results": results
        }

    async def _process_parallel(self, batch: List) -> List:
        """Process batch items in parallel."""
        tasks = [self._process_item(item) for item in batch]
        return await asyncio.gather(*tasks)

    async def _process_sequential(self, batch: List) -> List:
        """Process batch items sequentially."""
        results = []
        for item in batch:
            result = await self._process_item(item)
            results.append(result)
        return results
```

### Pattern 3: Validation Chains

Chain multiple validators:

```python
class ValidationChainTool(OmegaTool):
    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        data = payload.get("data")
        validators = payload.get("validators", [
            "schema", "business_rules", "security"
        ])

        validation_results = []
        all_valid = True

        for validator_name in validators:
            result = await self._run_validator(validator_name, data)
            validation_results.append(result)

            if not result["valid"]:
                all_valid = False
                # Stop on first failure if strict mode
                if payload.get("strict", False):
                    break

        return {
            "valid": all_valid,
            "validators_run": len(validation_results),
            "results": validation_results
        }

    async def _run_validator(self, name: str, data: Any) -> Dict:
        validators = {
            "schema": self._validate_schema,
            "business_rules": self._validate_business_rules,
            "security": self._validate_security
        }

        validator = validators.get(name)
        if not validator:
            return {"valid": False, "error": f"Unknown validator: {name}"}

        return await validator(data)
```

---

## 🔐 Security Patterns

### Input Sanitization

Always sanitize inputs before processing:

```python
async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
    # Sanitize before processing
    sanitized = await self._sanitize_input(payload)

    # Validate after sanitization
    if not await self._validate_input(sanitized):
        return {"error": "Invalid input after sanitization"}

    return await self._process(sanitized)

async def _sanitize_input(self, payload: Dict) -> Dict:
    """Remove dangerous characters and patterns."""
    sanitized = {}

    for key, value in payload.items():
        if isinstance(value, str):
            # Remove SQL injection patterns
            value = value.replace("';", "").replace("--", "")
            # Remove XSS patterns
            value = value.replace("<script>", "")

        sanitized[key] = value

    return sanitized
```

### Rate Limiting

Implement tool-level rate limiting:

```python
from collections import defaultdict
from datetime import datetime, timedelta

class RateLimitedTool(OmegaTool):
    def __init__(self):
        super().__init__(name="rate_limited", description="...")
        self.request_counts = defaultdict(list)

    async def invoke(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        client_id = payload.get("client_id", "anonymous")

        # Check rate limit
        if not await self._check_rate_limit(client_id):
            return {
                "error": "Rate limit exceeded",
                "retry_after": 60
            }

        # Process request
        return await self._process(payload)

    async def _check_rate_limit(self, client_id: str) -> bool:
        now = datetime.utcnow()
        window = timedelta(minutes=1)
        max_requests = 100

        # Clean old requests
        self.request_counts[client_id] = [
            ts for ts in self.request_counts[client_id]
            if now - ts < window
        ]

        # Check limit
        if len(self.request_counts[client_id]) >= max_requests:
            return False

        # Record request
        self.request_counts[client_id].append(now)
        return True
```

---

## 🧪 Testing Advanced Patterns

### Testing Hooks

```python
@pytest.mark.asyncio
async def test_oracle_hook():
    tool = HookExecutorTool()

    result = await tool.invoke({
        "operation": "execute_hook",
        "hook_type": "oracle",
        "context": {
            "task_id": "test123",
            "payload": {"question": "Test question"}
        }
    })

    assert result["hook_type"] == "oracle"
    assert result["status"] == "complete"
    assert "intel" in result
```

### Testing Context Awareness

```python
@pytest.mark.asyncio
async def test_context_adaptation():
    tool = ContextAwareTool()

    # Production context
    prod_result = await tool.invoke({
        "context": {"environment": "production"},
        "data": "test"
    })

    # Development context
    dev_result = await tool.invoke({
        "context": {"environment": "development"},
        "data": "test"
    })

    # Development should have debug info
    assert "debug" in dev_result
    assert "debug" not in prod_result
```

---

## 📚 Next Steps

- [Tool Testing](/docs/intro) - Comprehensive testing strategies
- [Integration Patterns](/docs/intro) - Connect tools to ecosystem
- [Neural Architecture](/docs/developer/agents/architecture) - Understanding hook lifecycle

**🏛️ Master advanced patterns. Build intelligent, context-aware tools.**
