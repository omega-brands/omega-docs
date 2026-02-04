# Federation Core Changelog

## 08/29/2025

### Summary of Changes

1. **Consolidated Duplicated Code & Established Patterns**
    * Unified the two similar MCP adapters into a single, reusable `OmegaMCPAdapter` located at `core/utils/fastmcp_adapter.py`.
    * Eliminated duplicate Pydantic models and the `sign_manifest` security function by centralizing them in `models.py` and `security.py` respectively.

2. **Centralized Configuration**
    * Removed hardcoded URLs for the `health_manager`, `agent_registry`, and `llm_tool_server` from the service's code.
    * The service now pulls these values from the central `ConfigManager`, making it more portable and easier to configure.

3. **Improved Persistence & Scalability**
    * Replaced the volatile, in-memory server directory with a persistent, Redis-backed implementation. This makes the federation's service discovery mechanism robust and production-ready.
    * Moved the LLM server's auto-registration into the main application's startup sequence, ensuring database connections are ready before they are used.

4. Simplified Architecture & Clarified Routing**
    * Removed the unused `APIRouter` from the `FederationCore` class.
    * This cleanup establishes `main.py` as the single source of truth for all API routes, making the service's architecture easier to understand and maintain.
