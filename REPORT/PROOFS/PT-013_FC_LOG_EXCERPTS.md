# PT-013 Federation Core Log Excerpts

**Purpose:** Corroborate PT-013 bundle artifacts with live FC container logs  
**Container:** `omega-federation-core-prod`  
**Image:** `omega-core-federation_core`  
**Image Digest:** `sha256:81ea24a2a35cfe1aa58c748ef3bf27ff4223749e3d83f2426816edbca57c3aa1`  
**Container Created:** `2026-02-06T12:18:40.738Z`  
**Log Extraction Date:** 2026-02-07  
**Command:** `docker logs omega-federation-core-prod 2>&1 | findstr "<run_id>"`

---

## Run A: Happy Path — `bea9e0e1-989c-4e54-84c4-48cdec9a577d`

### 1. Workflow Run Created
```json
{"event": "Creating workflow run: workflow_id=pt013_collab, tenant=tenant_omega, actor=pt013_test_harness", "logger": "FCRunsAPI", "level": "info"}
{"event": "Created workflow run: bea9e0e1-989c-4e54-84c4-48cdec9a577d (workflow=pt013_collab, tenant=tenant_omega)", "logger": "RunStore", "level": "info"}
```

### 2. Status: pending → running
```json
{"event": "Updating run: bea9e0e1-989c-4e54-84c4-48cdec9a577d, tenant=tenant_omega", "logger": "FCRunsAPI", "level": "info"}
{"event": "Updated run status: bea9e0e1-989c-4e54-84c4-48cdec9a577d (pending -> running)", "logger": "RunStore", "level": "info"}
```
**HTTP:** `PATCH /api/fc/runs/bea9e0e1-989c-4e54-84c4-48cdec9a577d HTTP/1.1 200 OK` @ `2026-02-07T13:43:03.295029+00:00`

### 3. Gate Created (Multi-Titan Collaboration Gate)
```json
{"event": "Creating gate for run: bea9e0e1-989c-4e54-84c4-48cdec9a577d, gate=Multi-Titan Collaboration Gate", "logger": "FCRunsAPI", "level": "info"}
{"event": "Updated run status: bea9e0e1-989c-4e54-84c4-48cdec9a577d (running -> paused)", "logger": "RunStore", "level": "info"}
{"event": "Created gate: d8ea741c-2d53-4f4d-b9d7-8de8cc079378 for run bea9e0e1-989c-4e54-84c4-48cdec9a577d", "logger": "RunStore", "level": "info"}
```
**HTTP:** `POST /api/fc/runs/bea9e0e1-989c-4e54-84c4-48cdec9a577d/gate HTTP/1.1 201 Created` @ `2026-02-07T13:43:03.340602+00:00`

### 4. Gate Resolved (approved)
```json
{"event": "Resolving gate: d8ea741c-2d53-4f4d-b9d7-8de8cc079378, status=approved", "logger": "FCRunsAPI", "level": "info"}
{"event": "Resolved gate: d8ea741c-2d53-4f4d-b9d7-8de8cc079378 with status approved", "logger": "RunStore", "level": "info"}
{"event": "Updated run status: bea9e0e1-989c-4e54-84c4-48cdec9a577d (paused -> running)", "logger": "RunStore", "level": "info"}
```
**HTTP:** `POST /api/fc/gates/d8ea741c-2d53-4f4d-b9d7-8de8cc079378 HTTP/1.1 200 OK` @ `2026-02-07T13:43:03.910072+00:00` (28.22ms)

### 5. Status: running → completed (SEAL)
```json
{"event": "Updating run: bea9e0e1-989c-4e54-84c4-48cdec9a577d, tenant=tenant_omega", "logger": "FCRunsAPI", "level": "info"}
{"event": "Updated run status: bea9e0e1-989c-4e54-84c4-48cdec9a577d (running -> completed)", "logger": "RunStore", "level": "info"}
```
**HTTP:** `PATCH /api/fc/runs/bea9e0e1-989c-4e54-84c4-48cdec9a577d HTTP/1.1 200 OK` @ `2026-02-07T13:43:03.950271+00:00`

**Full lifecycle:** `pending → running → paused → running → completed` ✅

---

## Run B: Gate Deny — `f57650b0-1efd-44f2-b344-d2eb44ddf031`

### 1. Workflow Run Created
```json
{"event": "Creating workflow run: workflow_id=pt013_collab, tenant=tenant_omega, actor=pt013_test_harness", "logger": "FCRunsAPI", "level": "info"}
{"event": "Created workflow run: f57650b0-1efd-44f2-b344-d2eb44ddf031 (workflow=pt013_collab, tenant=tenant_omega)", "logger": "RunStore", "level": "info"}
```

### 2. Status: pending → running
```json
{"event": "Updating run: f57650b0-1efd-44f2-b344-d2eb44ddf031, tenant=tenant_omega", "logger": "FCRunsAPI", "level": "info"}
{"event": "Updated run status: f57650b0-1efd-44f2-b344-d2eb44ddf031 (pending -> running)", "logger": "RunStore", "level": "info"}
```
**HTTP:** `PATCH /api/fc/runs/f57650b0-1efd-44f2-b344-d2eb44ddf031 HTTP/1.1 200 OK` @ `2026-02-07T13:43:04.019256+00:00`

### 3. Gate Created (Security Gate)
```json
{"event": "Creating gate for run: f57650b0-1efd-44f2-b344-d2eb44ddf031, gate=Security Gate", "logger": "FCRunsAPI", "level": "info"}
{"event": "Updated run status: f57650b0-1efd-44f2-b344-d2eb44ddf031 (running -> paused)", "logger": "RunStore", "level": "info"}
{"event": "Created gate: 967c9432-80b3-4c4e-b9ba-264d7249933a for run f57650b0-1efd-44f2-b344-d2eb44ddf031", "logger": "RunStore", "level": "info"}
```
**HTTP:** `POST /api/fc/runs/f57650b0-1efd-44f2-b344-d2eb44ddf031/gate HTTP/1.1 201 Created` @ `2026-02-07T13:43:04.066803+00:00`

### 4. Gate Resolved (REJECTED — fail-closed)
```json
{"event": "Resolving gate: 967c9432-80b3-4c4e-b9ba-264d7249933a, status=rejected", "logger": "FCRunsAPI", "level": "info"}
{"event": "Resolved gate: 967c9432-80b3-4c4e-b9ba-264d7249933a with status rejected", "logger": "RunStore", "level": "info"}
{"event": "Updated run status: f57650b0-1efd-44f2-b344-d2eb44ddf031 (paused -> failed)", "logger": "RunStore", "level": "info"}
```
**HTTP:** `POST /api/fc/gates/967c9432-80b3-4c4e-b9ba-264d7249933a HTTP/1.1 200 OK` @ `2026-02-07T13:43:04.690528+00:00` (42.87ms)

**Full lifecycle:** `pending → running → paused → failed` ✅ (fail-closed on rejection)

---

## Run C: Titan Failure — `3cf293c9-f704-4a42-b701-7cd3dd09a2f5`

### 1. Workflow Run Created
```json
{"event": "Creating workflow run: workflow_id=pt013_collab, tenant=tenant_omega, actor=pt013_test_harness", "logger": "FCRunsAPI", "level": "info"}
{"event": "Created workflow run: 3cf293c9-f704-4a42-b701-7cd3dd09a2f5 (workflow=pt013_collab, tenant=tenant_omega)", "logger": "RunStore", "level": "info"}
```

### 2. Status: pending → running
```json
{"event": "Updating run: 3cf293c9-f704-4a42-b701-7cd3dd09a2f5, tenant=tenant_omega", "logger": "FCRunsAPI", "level": "info"}
{"event": "Updated run status: 3cf293c9-f704-4a42-b701-7cd3dd09a2f5 (pending -> running)", "logger": "RunStore", "level": "info"}
```
**HTTP:** `PATCH /api/fc/runs/3cf293c9-f704-4a42-b701-7cd3dd09a2f5 HTTP/1.1 200 OK` @ `2026-02-07T13:43:04.825176+00:00`

### 3. No Gate — Titan Failure Halts Execution
No further FC lifecycle events. Harness recorded Titan failure (Gemini timeout) in ledger.  
Workflow remained in `running` state — no completion, no seal. **Fail-closed at harness level.** ✅

---

## Verification Summary

| Run ID | Lifecycle | Gate | Terminal State | FC Confirmed |
|--------|-----------|------|----------------|--------------|
| `bea9e0e1...` | pending→running→paused→running→completed | `d8ea741c...` approved | COMPLETED | ✅ |
| `f57650b0...` | pending→running→paused→failed | `967c9432...` rejected | FAILED | ✅ |
| `3cf293c9...` | pending→running (halted) | N/A (Titan failure) | RUNNING (halted) | ✅ |

**All 3 run_ids confirmed in live FC container logs.**  
**Gate create + resolve confirmed for Tests A and B.**  
**Status transitions match ledger claims.**

---

*Extracted from: `omega-federation-core-prod` (`sha256:81ea24a2a35c...`)*  
*This is the way.* 🔱

