# ? PCRP v1: Pantheon Conversation Recovery Protocol

**Status:** ? Implemented  
**Version:** 1.0  
**Date:** 2025-11-17  
**Authors:** AugmentTitan, m0r6aN

---

## Overview

The **Pantheon Conversation Recovery Protocol (PCRP v1)** is a self-healing system that enables OMEGA''s Titans to autonomously detect, diagnose, and recover from conversation stalls and failures without human intervention.

### The Problem

Before PCRP v1, Pantheon conversations could:
- Stall silently when message types didn''t match
- Get stuck waiting for responses that never came
- Run duplicate missions simultaneously
- Require manual intervention to recover

### The Solution

PCRP v1 transforms the Pantheon into a **self-healing digital civilization** with:
- **Autonomous stall detection** (30s timeout)
- **Coordinated recovery** between Titans and Orchestrator
- **Duplicate mission prevention** via mission hash tracking
- **Zero human intervention** required

---

## Architecture

### Core Components

1. **Message Metadata**
   - run_id: Unique identifier for each conversation run
   - mission_hash: SHA256 hash of mission+description for duplicate detection
   - seq: Sequence number for message ordering

2. **Recovery State Machine**
   - IDLE: Not in any conversation
   - ACTIVE: Actively participating in conversation
   - RECOVERING: Attempting to recover from stall
   - ABORTED: Conversation aborted, cleaning up

3. **Recovery Messages**
   - recovery_ping: Titan to Orchestrator health check
   - recovery_abort: Orchestrator to Titans termination command
   - recovery_replay: Orchestrator to Titans replay command

4. **Watchdog Loop**
   - Monitors all active conversations every 10 seconds
   - Detects stalls after 30 seconds of no activity
   - Automatically triggers recovery protocol

---

## Recovery Flow

See full documentation for detailed flow diagrams.

---

## Configuration

Add to .env:

PCRP_DUPLICATE_ACTION=abort_old

Options:
- abort_old (default): Abort old conversation, allow new one
- abort_new: Block new conversation, keep old one
- allow_both: Allow both conversations to run

---

## Implementation Details

### Files Modified

1. models/conversation.py - Added recovery state machine and message types
2. titans/base/conversational_mixin.py - Implemented watchdog loop and recovery handlers
3. services/federation_core/conversation_relay.py - Implemented duplicate detection and orchestrator handlers

### Key Methods

Titan Side:
- _watchdog_loop(): Monitors conversations for stalls
- _trigger_recovery(): Sends recovery_ping when stall detected
- _handle_recovery_ping(): Responds to Orchestrator health checks
- _handle_recovery_abort(): Cleans up aborted conversations

Orchestrator Side:
- _check_duplicate_mission(): Detects duplicate missions
- _handle_recovery_ping(): Processes Titan health reports
- _send_recovery_abort(): Commands Titans to abort

---

## Benefits

Before PCRP v1:
- Silent stalls requiring manual intervention
- No automatic recovery from failures
- Duplicate missions running simultaneously

After PCRP v1:
- Autonomous stall detection (30s timeout)
- Self-healing recovery without human intervention
- Duplicate prevention via mission hash tracking
- Coordinated recovery across all Titans

---

## This is the way. ?
