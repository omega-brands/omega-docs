# 🔱 OMEGA Resilience System

**Circuit Breaker, Exponential Backoff, and Rate Limiting for LLM API Calls**

*This is the way.*

---

## Overview

The OMEGA Resilience System provides three layers of protection for LLM API calls:

1. **Circuit Breaker** - Fail fast when a provider is down
2. **Exponential Backoff with Jitter** - Smart retry logic with randomization
3. **Rate Limiting** - Prevent quota exhaustion and API throttling

All resilience features are **automatically enabled** in the `UnifiedLLMClient` and require no code changes.

---

## Features

### 🔌 Circuit Breaker

The circuit breaker prevents cascading failures by detecting when an LLM provider is unavailable and temporarily stopping requests.

**States:**
- **CLOSED** (Normal) - All requests pass through
- **OPEN** (Failing) - Reject all requests, fail fast
- **HALF_OPEN** (Testing) - Allow limited requests to test recovery

**Configuration:**
```yaml
circuit_breaker:
  failure_threshold: 5        # Failures before opening
  success_threshold: 2        # Successes before closing
  timeout_seconds: 60.0       # Time before testing recovery
  half_open_max_calls: 3      # Max test calls in half-open
```

**Benefits:**
- Prevents wasting time on failing providers
- Allows system to recover gracefully
- Reduces load on failing services

---

### ⏱️ Exponential Backoff with Jitter

Smart retry logic that increases delay between retries exponentially, with random jitter to prevent thundering herd.

**Formula:**
```
delay = min(base_delay * (exponential_base ^ attempt) + jitter, max_delay)
```

**Configuration:**
```yaml
backoff:
  base_delay: 1.0            # Initial delay (seconds)
  max_delay: 60.0            # Maximum delay (seconds)
  exponential_base: 2.0      # Multiplier (2x each retry)
  jitter: true               # Add randomization
```

**Example Delays:**
- Attempt 1: ~1.0s + jitter
- Attempt 2: ~2.0s + jitter
- Attempt 3: ~4.0s + jitter
- Attempt 4: ~8.0s + jitter
- Attempt 5: ~16.0s + jitter

**Benefits:**
- Gives failing services time to recover
- Prevents thundering herd problem
- Reduces API load during incidents

---

### 🚦 Rate Limiting

Token bucket rate limiter that tracks both request count and token usage per minute.

**Configuration (per provider):**
```yaml
rate_limiting:
  openai:
    max_requests_per_minute: 60      # Adjust for your tier
    max_tokens_per_minute: 90000     # Adjust for your tier
    max_concurrent_requests: 10
```

**OpenAI Tier Limits:**
- **Free Tier**: 60 RPM, 90k TPM
- **Tier 1**: 500 RPM, 200k TPM
- **Tier 2**: 5000 RPM, 2M TPM
- **Tier 3**: 10000 RPM, 10M TPM

**Benefits:**
- Prevents quota exhaustion
- Avoids 429 rate limit errors
- Smooths out request bursts

---

## Usage

### Automatic (Recommended)

The resilience system is **automatically enabled** in all `UnifiedLLMClient` instances:

```python
from models.unified_llm_client import UnifiedLLMClient

# Resilience is enabled by default
llm = UnifiedLLMClient(
    preferred_model="gpt-5.2",
    openai_api_key="your-key"
)

# All calls are protected
result = await llm.chat(
    messages=[{"role": "user", "content": "Hello!"}]
)
```

### Manual Configuration

You can customize resilience settings:

```python
llm = UnifiedLLMClient(
    preferred_model="gpt-5.2",
    openai_api_key="your-key",
    enable_circuit_breaker=True,   # Enable circuit breaker
    enable_rate_limiting=True,     # Enable rate limiting
    max_retries=3                  # Number of retry attempts
)
```

### Disable Resilience (Not Recommended)

```python
llm = UnifiedLLMClient(
    preferred_model="gpt-5.2",
    openai_api_key="your-key",
    enable_circuit_breaker=False,
    enable_rate_limiting=False,
    max_retries=1
)
```

---

## Monitoring

### Get Resilience Statistics

```python
stats = llm.get_resilience_stats()

print(stats)
# {
#   "circuit_breakers": {
#     "openai": {
#       "name": "openai",
#       "state": "closed",
#       "failure_count": 0,
#       "success_count": 0,
#       "last_failure_time": null
#     }
#   },
#   "rate_limiters": {
#     "openai": {
#       "requests_last_minute": 15,
#       "tokens_last_minute": 12500,
#       "concurrent_requests": 2,
#       "max_requests_per_minute": 60,
#       "max_tokens_per_minute": 90000
#     }
#   }
# }
```

### Log Messages

The resilience system logs important events:

```
🔱 Circuit breakers initialized for all providers
🔱 Rate limiters initialized for all providers
⏳ Backing off for 2.34s (attempt 2)
⚠️ LLM call failed on attempt 1/3: Error...
🚨 Quota/Rate limit error on attempt 2/3: insufficient_quota
🚨 Circuit breaker 'openai' OPEN after 5 failures
🔄 Circuit 'openai' entering HALF_OPEN state
✅ Circuit 'openai' CLOSED (recovered)
⏸️ Rate limit hit for openai: 60 requests in last minute
```

---

## Error Handling

### Circuit Breaker Errors

When a circuit is open, you'll get:

```python
from models.circuit_breaker import CircuitBreakerError

try:
    result = await llm.chat(messages)
except CircuitBreakerError as e:
    print(f"Circuit is open: {e}")
    # Wait and try again later, or use fallback provider
```

### Rate Limit Errors

When rate limit is exceeded:

```python
from models.circuit_breaker import RateLimitExceededError

try:
    result = await llm.chat(messages)
except RateLimitExceededError as e:
    print(f"Rate limit exceeded: {e}")
    # Wait for rate limit window to reset
```

### Quota Errors

The system automatically detects and handles quota errors:

```python
try:
    result = await llm.chat(messages)
except UnifiedLLMClientError as e:
    if "insufficient_quota" in str(e):
        print("OpenAI quota exceeded - check billing")
    elif "429" in str(e):
        print("Rate limited - will retry with backoff")
```

---

## Configuration

### Environment Variables

You can override settings via environment:

```bash
# Circuit Breaker
export OMEGA_CIRCUIT_BREAKER_ENABLED=true
export OMEGA_CIRCUIT_FAILURE_THRESHOLD=5
export OMEGA_CIRCUIT_TIMEOUT_SECONDS=60

# Rate Limiting
export OMEGA_RATE_LIMITING_ENABLED=true
export OMEGA_OPENAI_MAX_RPM=60
export OMEGA_OPENAI_MAX_TPM=90000

# Backoff
export OMEGA_BACKOFF_BASE_DELAY=1.0
export OMEGA_BACKOFF_MAX_DELAY=60.0
export OMEGA_MAX_RETRIES=3
```

### YAML Configuration

Edit `config/resilience.yaml` to customize settings.

---

## Troubleshooting

### Issue: Still getting 429 errors

**Solution:** Lower your rate limits in `config/resilience.yaml`:

```yaml
rate_limiting:
  openai:
    max_requests_per_minute: 30  # Reduce from 60
    max_tokens_per_minute: 45000  # Reduce from 90000
```

### Issue: Circuit breaker opening too frequently

**Solution:** Increase failure threshold:

```yaml
circuit_breaker:
  failure_threshold: 10  # Increase from 5
```

### Issue: Retries taking too long

**Solution:** Reduce max delay or max retries:

```yaml
backoff:
  max_delay: 30.0  # Reduce from 60.0

resilience:
  max_retries: 2  # Reduce from 3
```

### Issue: Insufficient quota errors

**Solution:** This is a billing issue, not a resilience issue:
1. Check your OpenAI billing dashboard
2. Add payment method or upgrade tier
3. The circuit breaker will prevent hammering the API

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│                   UnifiedLLMClient                      │
│                                                         │
│  ┌───────────────────────────────────────────────────┐ │
│  │  chat() - Public API                              │ │
│  │  ├─ Retry Loop (max_retries)                      │ │
│  │  │  ├─ _chat_with_resilience()                    │ │
│  │  │  │  ├─ Rate Limiter (acquire/release)          │ │
│  │  │  │  ├─ Circuit Breaker (call)                  │ │
│  │  │  │  │  └─ _execute_llm_call()                  │ │
│  │  │  │  │     └─ Actual API Call                   │ │
│  │  │  │  │                                           │ │
│  │  │  │  └─ On Error: Exponential Backoff           │ │
│  │  │  │                                              │ │
│  │  │  └─ Retry with backoff                         │ │
│  └───────────────────────────────────────────────────┘ │
│                                                         │
│  Circuit Breakers (per provider):                      │
│  ├─ openai    [CLOSED]                                 │
│  ├─ anthropic [CLOSED]                                 │
│  ├─ google    [CLOSED]                                 │
│  └─ grok      [CLOSED]                                 │
│                                                         │
│  Rate Limiters (per provider):                         │
│  ├─ openai    [15/60 RPM, 12k/90k TPM]                 │
│  ├─ anthropic [8/50 RPM, 6k/100k TPM]                  │
│  ├─ google    [12/60 RPM, 10k/120k TPM]                │
│  └─ grok      [5/60 RPM, 4k/100k TPM]                  │
└─────────────────────────────────────────────────────────┘
```

---

## Testing

### Test Circuit Breaker

```python
# Simulate failures to trigger circuit breaker
for i in range(10):
    try:
        await llm.chat([{"role": "user", "content": "test"}])
    except Exception as e:
        print(f"Attempt {i}: {e}")

# Check circuit state
stats = llm.get_resilience_stats()
print(stats["circuit_breakers"]["openai"]["state"])  # Should be "open"
```

### Test Rate Limiting

```python
import asyncio

# Send burst of requests
tasks = [
    llm.chat([{"role": "user", "content": f"test {i}"}])
    for i in range(100)
]

results = await asyncio.gather(*tasks, return_exceptions=True)

# Check how many hit rate limit
rate_limited = sum(1 for r in results if isinstance(r, RateLimitExceededError))
print(f"Rate limited: {rate_limited}/100")
```

---

## Family is Forever

**This is the way.** 🔱

The OMEGA Resilience System ensures our Titans survive and thrive, even when the chaos of the external world tries to bring them down.

*We are not just building systems. We are building immortal machines.*

