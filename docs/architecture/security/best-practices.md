# Security Best Practices

Actionable security recommendations to ensure OMEGA components meet DoD standards (NIST SP 800-53, DISA STIGs).

## 🔒 Core Security Principles

### 1. Fail-Fast Validation
- ✅ **Validate at startup** - Never use fallback values
- ✅ **Type checking** - Enforce schemas for all config
- ✅ **URL validation** - Parse and verify all endpoints
- ✅ **Range checks** - Validate numeric bounds

### 2. Zero Trust Architecture
- ✅ **Authenticate everything** - No unauthenticated endpoints
- ✅ **Verify signatures** - Cryptographically sign all messages
- ✅ **Audit trails** - Log every security-relevant action
- ✅ **Least privilege** - Grant minimum necessary permissions

### 3. Defense in Depth
- ✅ **Multiple layers** - Security at every level
- ✅ **Redundant controls** - Backup security measures
- ✅ **Monitoring** - Continuous threat detection
- ✅ **Incident response** - Automated remediation

---

## 🛡️ Component-Specific Recommendations

### Tools (base_tool.py)

#### ❌ Current Issues
- Auto-certification lacks revocation checks
- Broad exception handling masks failures
- No input validation on capabilities

#### ✅ Recommended Changes

```python
from enum import Enum
from pydantic import BaseModel, validator
from typing import List

class SecurityLevel(str, Enum):
    """Tool security classification."""
    STANDARD = "standard"
    HIGH = "high"
    CRITICAL = "critical"

class ToolCapability(BaseModel):
    """Validated tool capability schema."""
    name: str
    description: str
    parameters: dict

    @validator('name')
    def name_must_be_valid(cls, v):
        if not v or len(v) > 100:
            raise ValueError('Name must be 1-100 characters')
        return v

    class Config:
        extra = "forbid"  # Reject unknown fields

class OmegaTool:
    async def certify(self):
        """Certify tool with CRL check."""
        try:
            # Check certificate revocation list
            if await self.ca.check_crl(self.tool_id):
                raise ValueError("Certificate revoked")

            # Certify tool
            cert = await self.ca.certify_omega_tool(
                self.tool_id,
                security_level=SecurityLevel.HIGH
            )
            return cert

        except httpx.HTTPError as e:  # Specific exception
            self.logger.error(f"Certification failed: {e}")
            raise
```

**Security Improvements:**
- ✅ CRL (Certificate Revocation List) checking
- ✅ Specific exception handling
- ✅ Pydantic validation for capabilities
- ✅ Security level enforcement
- ✅ Sensitive file exclusion in bundles

---

### Resources (base_resource.py)

#### ❌ Current Issues
- No authentication on endpoints
- Single-attempt registration (no retries)
- No access level validation

#### ✅ Recommended Changes

```python
from fastapi import Depends
from core.security import require_bearer
from enum import Enum
import asyncio

class AccessLevel(str, Enum):
    """Resource access levels."""
    PUBLIC = "public"
    OPERATOR = "operator"
    PANTHEON = "pantheon"

class BaseResource:
    @app.post("/register", dependencies=[Depends(require_bearer)])
    async def register(self, data: ResourceData):
        """Protected registration endpoint."""

        # Validate access level
        if data.access_level not in AccessLevel.__members__.values():
            raise ValueError(f"Invalid access level: {data.access_level}")

        # Retry with exponential backoff
        for attempt in range(3):
            try:
                response = await self.http_client.post(
                    f"{self.registry_url}/resources/register",
                    json=data.dict(),
                    timeout=30.0
                )
                return response.json()

            except httpx.HTTPError as e:
                if attempt == 2:  # Last attempt
                    raise
                wait_time = 2 ** attempt  # 1s, 2s, 4s
                await asyncio.sleep(wait_time)
```

**Security Improvements:**
- ✅ Bearer token authentication
- ✅ Exponential backoff retries
- ✅ Access level enum validation
- ✅ Timeout enforcement

---

### Configuration (manager.py)

#### ❌ Current Issues
- HMAC key without rotation
- Broad exception handling
- No JSON validation

#### ✅ Recommended Changes

```python
from pydantic import BaseModel
from datetime import datetime

class ConfigMessage(BaseModel):
    """Validated config update message."""
    event: str
    version: str
    changed: List[str]
    signature: str
    timestamp: str

    class Config:
        extra = "forbid"

class ConfigManager:
    async def _verify_signature(self, msg: dict) -> bool:
        """Verify signature with key rotation support."""

        # Check key version
        current_version = await self.redis.get("omega:config:key_version")
        msg_version = msg.get("key_version")

        if msg_version != current_version:
            # Try previous key for grace period
            if not await self._verify_with_old_key(msg):
                raise ValueError("Signature verification failed - key mismatch")

        # Verify with current key
        hmac_key = self.config.get_secret(ConfigKey.CONFIG_MSG_HMAC_KEY)
        return self._compute_hmac(msg, hmac_key) == msg.get("signature")

    async def _handle_message(self, msg: str):
        """Handle config update with validation."""
        try:
            # Parse and validate
            data = ConfigMessage(**json.loads(msg))

            # Process update
            await self._apply_update(data)

        except ValidationError as e:
            self.logger.error(f"Invalid config message: {e}")
        except ConnectionError as e:
            self.logger.error(f"Redis connection error: {e}")
            raise
```

**Security Improvements:**
- ✅ Key rotation support
- ✅ Pydantic message validation
- ✅ Specific exception handling
- ✅ Grace period for key rotation

---

### Certificate Authority (tool_certification.py)

#### ❌ Current Issues
- No passphrase on private keys
- No CRL enforcement
- Hardcoded expiration

#### ✅ Recommended Changes

```python
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa

class OmegaToolCertificationAuthority:
    def __init__(self):
        self.config = create_config_manager()
        self.passphrase = self.config.get_secret(
            ConfigKey.CA_PASSPHRASE
        ).encode()

    def _generate_private_key(self) -> rsa.RSAPrivateKey:
        """Generate passphrase-protected private key."""

        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048
        )

        # Encrypt with passphrase
        pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.BestAvailableEncryption(
                self.passphrase
            )
        )

        return private_key

    async def check_crl(self, tool_id: str) -> bool:
        """Check if certificate is revoked."""

        revoked = await self.redis.sismember(
            "omega:crl",
            tool_id
        )
        return revoked

    async def verify_certificate(self, cert: dict) -> bool:
        """Verify certificate with CRL check."""

        tool_id = cert.get("tool_id")

        # Check CRL first
        if await self.check_crl(tool_id):
            self.logger.warning(
                f"Certificate revoked: {tool_id}",
                extra={"security_context": True}
            )
            return False

        # Verify signature
        is_valid = self._verify_cert_signature(cert)

        # Check expiration
        expiry_days = self.config.get_int(
            ConfigKey.CERT_EXPIRY_DAYS,
            default=365
        )
        is_expired = self._check_expiration(cert, expiry_days)

        return is_valid and not is_expired

    async def revoke_certificate(self, tool_id: str, reason: str):
        """Revoke certificate and add to CRL."""

        await self.redis.sadd("omega:crl", tool_id)

        # Log revocation
        self.logger.warning(
            f"Certificate revoked: {tool_id}",
            extra={
                "security_context": True,
                "tool_id": tool_id,
                "reason": reason,
                "timestamp": datetime.utcnow().isoformat()
            }
        )
```

**Security Improvements:**
- ✅ Passphrase-protected keys
- ✅ CRL (Certificate Revocation List)
- ✅ Configurable expiration
- ✅ Revocation audit logging

---

## 📊 General Recommendations

### Logging & Observability

```python
import uuid
from structlog import get_logger

class AuditLogger:
    """Structured logging with correlation IDs."""

    def __init__(self):
        self.logger = get_logger()

    def log_security_event(self, event: str, **kwargs):
        """Log security event with full context."""

        correlation_id = kwargs.get("correlation_id") or str(uuid.uuid4())

        self.logger.info(
            event,
            extra={
                "security_context": True,
                "correlation_id": correlation_id,
                "timestamp": datetime.utcnow().isoformat(),
                **kwargs
            }
        )
```

**Benefits:**
- ✅ Correlation IDs for traceability (AU-2/AU-3)
- ✅ JSON-structured logging for SIEM
- ✅ Tamper-proof audit trails

### Input Validation

```python
from pydantic import BaseModel, validator, HttpUrl

class ServiceConfig(BaseModel):
    """Validated service configuration."""

    redis_url: HttpUrl
    max_connections: int
    timeout: int

    @validator('max_connections')
    def validate_connections(cls, v):
        if not 1 <= v <= 1000:
            raise ValueError('Connections must be 1-1000')
        return v

    @validator('timeout')
    def validate_timeout(cls, v):
        if not 1 <= v <= 300:
            raise ValueError('Timeout must be 1-300 seconds')
        return v

    class Config:
        extra = "forbid"
```

**Benefits:**
- ✅ Schema validation at startup
- ✅ Range checks for numeric values
- ✅ URL parsing and verification
- ✅ Reject unknown fields

### Error Handling

```python
# ❌ Bad - Broad exception masks issues
try:
    await process_task()
except Exception as e:
    logger.error(f"Error: {e}")

# ✅ Good - Specific exceptions
try:
    await process_task()
except ValidationError as e:
    logger.error(f"Validation failed: {e}")
    raise
except ConnectionError as e:
    logger.error(f"Connection failed: {e}")
    await self.retry_with_backoff()
except httpx.HTTPError as e:
    logger.error(f"HTTP error: {e}")
    raise
```

---

## 🔐 JWT & Authentication

### Asymmetric JWT Signing

```python
from jose import jwt, JWTError
from datetime import datetime, timedelta

class JWTManager:
    """RS256 JWT with key rotation."""

    def __init__(self):
        self.private_key = self._load_private_key()
        self.public_key = self._load_public_key()

    def create_token(self, payload: dict, expires_delta: timedelta) -> str:
        """Create signed JWT token."""

        to_encode = payload.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})

        # Sign with RS256
        token = jwt.encode(
            to_encode,
            self.private_key,
            algorithm="RS256"
        )

        return token

    def verify_token(self, token: str) -> dict:
        """Verify JWT signature."""

        try:
            payload = jwt.decode(
                token,
                self.public_key,
                algorithms=["RS256"]
            )
            return payload

        except JWTError as e:
            logger.error(f"JWT verification failed: {e}")
            raise ValueError("Invalid token")
```

---

## 📚 Compliance Checklist

### NIST SP 800-53 Controls

- [ ] **AC-2** - Account Management
- [ ] **AC-3** - Access Enforcement
- [ ] **AU-2** - Audit Events
- [ ] **AU-3** - Content of Audit Records
- [ ] **IA-2** - Identification and Authentication
- [ ] **SC-8** - Transmission Confidentiality
- [ ] **SC-13** - Cryptographic Protection

### DISA STIG Requirements

- [ ] **V-222391** - Encryption of sensitive data
- [ ] **V-222392** - Authentication mechanisms
- [ ] **V-222393** - Audit logging
- [ ] **V-222394** - Secure communications
- [ ] **V-222395** - Access control

---

## 📚 Next Steps

- [Security Fortress](/docs/security/fortress) - Implementation guide
- [Security Doctrine](/docs/doctrine/security-doctrine) - Security principles
- [Compliance](/docs/intro) - Regulatory compliance

**🔱 Security is not optional. It's the foundation of the Brotherhood.**
