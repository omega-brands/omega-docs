# DEPRECATED: Old Orchestrator Hooks

**⚠️ This directory is now OBSOLETE**

The orchestrator now uses the new unified OMEGA hook system at:
```
core.hooks
```

## What Changed:
- ❌ **OLD**: Broken, individual hook files with missing dependencies
- ✅ **NEW**: Unified hook system with proper Pantheon evaluation 

## Migration Completed:
- All hook functionality moved to `core.hooks.genesis_council_hook`
- Orchestrator now uses `execute_hooks()` and `HookType` enums
- Proper lifecycle hooks added for startup, shutdown, task delegation
- Full Genesis Protocol integration with pre/post hooks

## Files:
- `council_hook.py.old` - Backup of old broken implementation 
- This directory can be safely deleted

**This is the way.** 🛡️
