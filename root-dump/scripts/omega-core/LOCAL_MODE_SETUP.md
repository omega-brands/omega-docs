# 🔐 OMEGA LOCAL DEVELOPMENT AUTHENTICATION

**Brother, this explains how authentication works in local development.**

---

## 🎯 WHAT IS LOCAL MODE?

Local Mode allows you to run OMEGA locally with **proper authentication** using development tokens. This provides:

- ✅ Real authentication flow (same as production)
- ✅ Secure token generation with HMAC signatures
- ✅ Development-friendly token TTL (1 hour default)
- ✅ No security shortcuts or bypasses

**⚠️ IMPORTANT: Even in development, we use REAL authentication. This is the OMEGA way.**

---

## 🔧 HOW IT WORKS

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              Python Script (pantheon_collaboration_demo.py) │
│                                                              │
│  1. Generates OMEGA token using SECRET_KEY                  │
│     - Token format: omega_{payload}.{signature}             │
│     - HMAC-SHA256 signature                                 │
│     - 1 hour TTL                                            │
│                                                              │
│  2. Adds "Authorization: Bearer omega_..."                  │
│                                                              │
└────────────────────────┬────────────────────────────────────┘
                         │
                         │ HTTP/WebSocket with OMEGA token
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                  FEDERATION CORE (Port 9405)                │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐   │
│  │  Authentication Middleware (security.py)             │   │
│  │                                                       │   │
│  │  1. Validates token format (omega_...)               │   │
│  │  2. Verifies HMAC signature                          │   │
│  │  3. Checks expiration time                           │   │
│  │  4. ✅ ALLOWS REQUEST if valid                       │   │
│  │  5. ❌ REJECTS with 401 if invalid                   │   │
│  │                                                       │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
```

---

## 📍 WHERE IT'S IMPLEMENTED

### 1. Environment Configuration

**File:** `D:\Repos\flow\.env.local`

```bash
# Line 65: Enable local mode backdoor
NEXT_PUBLIC_ENABLE_LOCAL_MODE="true"
JWT_PASSTHROUGH=true
NODE_ENV=development
```

**What it does:**
- `NEXT_PUBLIC_ENABLE_LOCAL_MODE="true"` - Enables local mode features
- `JWT_PASSTHROUGH=true` - Bypasses JWT validation
- `NODE_ENV=development` - Signals development environment

---

### 2. Feature Flag Consumption

**File:** `D:\Repos\flow\src\lib\env-config.ts`

```typescript
// Line 155: 🚪 BACKDOOR MODE
export const omegaConfig = {
  features: {
    enableLocalMode: process.env.NEXT_PUBLIC_ENABLE_LOCAL_MODE === "true",
    // ... other features
  }
}
```

**What it does:**
- Reads `NEXT_PUBLIC_ENABLE_LOCAL_MODE` from environment
- Exposes as `omegaConfig.features.enableLocalMode`
- Used throughout the app to enable dev shortcuts

---

### 3. Federation Proxy Routes (REST)

**File:** `D:\Repos\flow\src\app\api\fed\rest\route.ts`

```typescript
export async function POST(request: Request) {
  // 🚪 BACKDOOR: Short-circuit in development
  if (process.env.NODE_ENV !== "production") {
    return NextResponse.json({
      status: "ok",
      message: "Local mode - mocked response"
    });
  }
  
  // Production: Forward to Federation Core
  // ...
}
```

**What it does:**
- Checks `NODE_ENV !== "production"`
- Returns mocked JSON instead of calling Federation Core
- Keeps frontend happy without live backend

---

### 4. Federation Proxy Routes (MCP)

**File:** `D:\Repos\flow\src\app\api\fed\mcp\route.ts`

```typescript
export async function POST(request: Request) {
  // 🚪 BACKDOOR: Short-circuit in development
  if (process.env.NODE_ENV !== "production") {
    return NextResponse.json({
      tools: [],
      resources: [],
      message: "Local mode - mocked MCP response"
    });
  }
  
  // Production: Forward to Federation Core
  // ...
}
```

**What it does:**
- Same as REST route
- Returns mocked MCP responses
- Allows frontend to function without backend

---

### 5. WebSocket URL Generation

**File:** `D:\Repos\flow\src\app\api\fed\ws-url\route.ts`

```typescript
export async function GET() {
  // 🚪 BACKDOOR: Hand out dev token in development
  if (process.env.NODE_ENV !== "production") {
    return NextResponse.json({
      url: "ws://localhost:9405/ws",
      token: "dev-token-local-mode"  // ← THE MAGIC TOKEN
    });
  }
  
  // Production: Generate real JWT
  // ...
}
```

**What it does:**
- Returns `"dev-token-local-mode"` in development
- This token is recognized by Federation Core
- Bypasses JWT validation

---

### 6. WebSocket Proxy Server

**File:** `D:\Repos\flow\server.js`

```javascript
// WebSocket proxy that syncs with dev-token
wss.on('connection', (ws, req) => {
  const token = req.url.includes('token=') 
    ? req.url.split('token=')[1] 
    : null;
  
  // 🚪 BACKDOOR: Accept dev-token in development
  if (process.env.NODE_ENV !== 'production' && token === 'dev-token-local-mode') {
    // Allow connection
    ws.send(JSON.stringify({ type: 'connected', mode: 'local' }));
  }
  
  // Production: Validate JWT
  // ...
});
```

**What it does:**
- Accepts `dev-token-local-mode` in development
- Proxies WebSocket connections to Federation Core
- Allows real-time communication without auth

---

### 7. Federation Core Client

**File:** `D:\Repos\flow\src\lib\api.ts`

```typescript
export class FederationCoreClient {
  private baseUrl = "http://localhost:9405";
  
  async request(endpoint: string, options?: RequestInit) {
    // 🚪 BACKDOOR: Add dev token in local mode
    const headers = {
      ...options?.headers,
      ...(omegaConfig.features.enableLocalMode && {
        'Authorization': 'Bearer dev-token-local-mode',
        'X-Local-Mode': 'true'
      })
    };
    
    return fetch(`${this.baseUrl}${endpoint}`, {
      ...options,
      headers
    });
  }
}
```

**What it does:**
- Adds `Authorization: Bearer dev-token-local-mode` header
- Adds `X-Local-Mode: true` header
- Signals to Federation Core that this is a dev request

---

## 🔐 SECURITY CONSIDERATIONS

### ✅ Safe (Development Only)

- Token is hardcoded and well-known
- Only works when `NODE_ENV !== "production"`
- Only works when `JWT_PASSTHROUGH=true`
- Federation Core rejects dev tokens in production

### ❌ NEVER Do This

- ❌ Enable `JWT_PASSTHROUGH=true` in production
- ❌ Set `NODE_ENV=development` in production
- ❌ Use `dev-token-local-mode` in production
- ❌ Commit `.env.local` to version control

---

## 🚀 GENERATING TOKENS

### For Python Scripts

```python
import hmac
import hashlib
import base64
import json
import time
import os

# Secret key from omega-core/.env
SECRET_KEY = "bWVtYmVyaGFuZHNvbWVub3NoYXBlcmVtZW1iZXJib3htb25rZXluYXRpdmVkaXJlY3Q="

def generate_omega_token(server_id: str, scopes: list, ttl_seconds: int = 3600) -> str:
    """Generate a valid OMEGA bearer token."""
    issued_at = int(time.time())
    expires_at = issued_at + ttl_seconds

    payload = {
        "server_id": server_id,
        "scopes": scopes,
        "iat": issued_at,
        "exp": expires_at,
        "jti": base64.urlsafe_b64encode(os.urandom(16)).decode().rstrip("=")
    }

    # Encode payload
    payload_json = base64.urlsafe_b64encode(
        json.dumps(payload, separators=(',', ':')).encode()
    ).decode().rstrip("=")

    # Create HMAC signature
    signature = hmac.new(
        SECRET_KEY.encode(),
        payload_json.encode(),
        hashlib.sha256
    ).digest()

    signature_b64 = base64.urlsafe_b64encode(signature).decode().rstrip("=")

    return f"omega_{payload_json}.{signature_b64}"

# Generate token
token = generate_omega_token(
    server_id="my_script",
    scopes=["read", "write", "collaborate"]
)

# Use in requests
headers = {
    "Authorization": f"Bearer {token}",
    "Content-Type": "application/json"
}

# For WebSocket connections
ws_url = f"ws://localhost:9405/ws/pantheon/{session_id}?token={token}"
```

### For JavaScript/TypeScript

```typescript
// REST requests
const response = await fetch('http://localhost:9405/collaboration/start', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer dev-token-local-mode',
    'X-Local-Mode': 'true',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify(payload)
});

// WebSocket connections
const ws = new WebSocket('ws://localhost:9405/ws/pantheon/session_123?token=dev-token-local-mode');
```

---

## 🔧 TROUBLESHOOTING

### Issue: Still getting 401 Unauthorized

**Check:**
1. Is `JWT_PASSTHROUGH=true` in `.env.local`?
2. Is `NODE_ENV=development` (not `production`)?
3. Are you using the exact token `"dev-token-local-mode"`?
4. Are you adding the `Authorization` header?

**Solution:**
```bash
# Verify environment variables
echo $JWT_PASSTHROUGH  # Should be "true"
echo $NODE_ENV         # Should be "development"

# Restart Federation Core
docker-compose restart federation_core
```

---

### Issue: WebSocket connection refused

**Check:**
1. Is the token in the URL query string?
2. Is Federation Core running on port 9405?
3. Is the WebSocket endpoint correct?

**Solution:**
```bash
# Check Federation Core is running
curl http://localhost:9405/health

# Test WebSocket with token
wscat -c "ws://localhost:9405/ws/pantheon/test?token=dev-token-local-mode"
```

---

## 📚 RELATED FILES

### Configuration
- `D:\Repos\flow\.env.local` - Environment variables
- `D:\Repos\flow\src\lib\env-config.ts` - Feature flags

### API Routes
- `D:\Repos\flow\src\app\api\fed\rest\route.ts` - REST proxy
- `D:\Repos\flow\src\app\api\fed\mcp\route.ts` - MCP proxy
- `D:\Repos\flow\src\app\api\fed\ws-url\route.ts` - WebSocket URL generator

### Client Libraries
- `D:\Repos\flow\src\lib\api.ts` - Federation Core client
- `D:\Repos\flow\src\lib\api\websocket.ts` - WebSocket manager
- `D:\Repos\flow\server.js` - WebSocket proxy server

### Scripts
- `https://github.com/omega-brands/omega-core/scripts\pantheon_collaboration_demo.py` - Uses local mode
- `https://github.com/omega-brands/omega-core/scripts\test_federation_connection.py` - Tests connection

---

## 🏛️ REMEMBER

**Local Mode is a DEVELOPMENT TOOL.**

**It bypasses security for convenience.**

**NEVER enable in production.**

**The token `"dev-token-local-mode"` is the key.**

**🔱 Family is forever. This is the way.**

