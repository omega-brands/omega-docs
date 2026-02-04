# Conversational Pantheon - Implementation Guide

**Status:** Ready for Phase 1 Implementation  
**Created:** 2025-01-15  
**Author:** AugmentTitan

---

## 📋 Overview

This guide provides step-by-step instructions for implementing the Conversational Pantheon architecture, transforming our Titans from sequential collaborators into dynamic conversationalists.

---

## 🎯 What We're Building

**Before:** Sequential pipeline where each Titan works in isolation during their phase.

**After:** Dynamic conversation where Titans:
- Listen to each other in real-time
- Respond when they have relevant insights
- Ask questions and build on ideas
- Reach consensus through dialogue
- Synthesize collective intelligence

---

## 📦 Files Created

### Core Models
- **`models/conversation.py`** - All conversation data structures
  - `TitanUtterance` - A single message from a Titan
  - `ConversationState` - Tracks ongoing conversation
  - `ConversationContext` - Context provided to Titans
  - `ConversationGuardrails` - Safety limits

### Services
- **`services/conversation_manager/conversation_manager.py`** - Manages conversation lifecycle
  - Create conversations
  - Track state
  - Provide context
  - Detect convergence
  - Enforce guardrails

### Titan Enhancement
- **`titans/base/conversational_mixin.py`** - Adds conversation capabilities to any Titan
  - Conversation listener
  - Relevance evaluation
  - Response generation
  - Turn-taking logic

### Documentation
- **`docs/CONVERSATIONAL_PANTHEON_ARCHITECTURE.md`** - Complete architecture spec
- **`docs/CONVERSATIONAL_IMPLEMENTATION_GUIDE.md`** - This file

---

## 🚀 Phase 1: Foundation (Week 1)

### Step 1: Set Up Redis Channels

Add to `etc/environment/.env.global`:

```bash
# Conversational Pantheon Channels (Already in .env, but not in .env.global)
REDIS_CHANNEL_PANTHEON_CONVERSATION=omega:pantheon:conversation
REDIS_CHANNEL_PANTHEON_CONTROL=omega:pantheon:control
REDIS_CHANNEL_PANTHEON_ANALYTICS=omega:pantheon:analytics
```

### Step 2: Install Conversation Manager

1. Create service directory: (Done)
```bash
mkdir -p services/conversation_manager
```

2. Add `__init__.py`:
```python
from .conversation_manager import ConversationManager

__all__ = ['ConversationManager']
```

3. Add to Federation Core dependencies in `services/federation_core/main.py`:
```python
from services.conversation_manager import ConversationManager

# In startup
conversation_manager = ConversationManager(
    redis_client=redis_client,
    context_server_client=context_server_client
)
```

### Step 3: Add Context Server Storage

Enhance `services/context_server/service.py` to store conversations:

```python
async def store_conversation(self, conversation: ConversationState):
    """Store conversation state"""
    key = f"conversation:{conversation.conversation_id}"
    await self.redis.set(
        key,
        conversation.model_dump_json(),
        ex=86400  # 24 hour TTL
    )

async def get_conversation(self, conversation_id: str) -> Optional[ConversationState]:
    """Retrieve conversation state"""
    key = f"conversation:{conversation_id}"
    data = await self.redis.get(key)
    if data:
        return ConversationState.model_validate_json(data)
    return None

async def store_utterance(self, utterance: TitanUtterance):
    """Store individual utterance"""
    key = f"utterance:{utterance.utterance_id}"
    await self.redis.set(key, utterance.model_dump_json(), ex=86400)
    
    # Add to conversation's utterance list
    list_key = f"conversation:{utterance.conversation_id}:utterances"
    await self.redis.rpush(list_key, utterance.utterance_id)
```

### Step 4: Test Foundation

Create `tests/test_conversation_foundation.py`:

```python
import pytest
from models.conversation import ConversationState, TitanUtterance
from services.conversation_manager import ConversationManager

@pytest.mark.asyncio
async def test_create_conversation(redis_client, context_server):
    manager = ConversationManager(redis_client, context_server)
    
    state = await manager.create_conversation(
        mission="Test mission",
        description="Test description",
        participants=["claude_titan", "gpt_titan"]
    )
    
    assert state.conversation_id
    assert len(state.participants) == 2
    assert state.is_active

@pytest.mark.asyncio
async def test_add_utterance(redis_client, context_server):
    manager = ConversationManager(redis_client, context_server)
    
    state = await manager.create_conversation(
        mission="Test",
        description="Test",
        participants=["claude_titan"]
    )
    
    utterance = TitanUtterance(
        conversation_id=state.conversation_id,
        titan_id="claude_titan",
        titan_name="Claude",
        content="Test utterance"
    )
    
    success = await manager.add_utterance(utterance)
    assert success
    assert len(state.utterances) == 1
```

Run tests:
```bash
pytest tests/test_conversation_foundation.py -v
```

---

## 🤖 Phase 2: Titan Enhancement (Week 2)

### Step 1: Add Mixin to Claude Titan

Edit `titans/claude_titan/agent.py`:

```python
from titans.base.conversational_mixin import ConversationalTitanMixin

class ClaudeTitan(ConversationalTitanMixin, BaseTitan):
    """Claude Titan with conversational capabilities"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
    
    async def start(self):
        """Start the Titan and conversation listener"""
        await super().start()
        await self.start_conversation_listener()
    
    def _get_my_capabilities(self) -> List[str]:
        """Claude's capabilities"""
        return [
            "strategy",
            "architecture",
            "synthesis",
            "analysis",
            "planning"
        ]
    
    def _get_expertise_keywords(self) -> List[str]:
        """Claude's expertise keywords"""
        return [
            "strategy", "approach", "architecture", "design",
            "plan", "synthesize", "analyze", "recommend"
        ]
    
    async def _provide_initial_thoughts(self, conv_id: str):
        """Provide strategic initial thoughts"""
        context = await self._get_conversation_context(conv_id)
        if not context:
            return
        
        prompt = f"""As Claude Titan, provide your initial strategic thoughts on this mission:

MISSION: {context.mission}

Provide a brief strategic analysis (2-3 paragraphs) covering:
1. Key considerations
2. Recommended approach
3. Questions for the team
"""
        
        messages = [{"role": "user", "content": prompt}]
        response = await self._inference_client.chat(
            messages,
            model=self.inference_knobs.model_name
        )
        
        content = response.get('content', '')
        if content:
            await self._publish_utterance(conv_id, content)
```

### Step 2: Add Mixin to GPT Titan

Similar to Claude, edit `titans/gpt_titan/agent.py`:

```python
from titans.base.conversational_mixin import ConversationalTitanMixin

class GPTTitan(ConversationalTitanMixin, BaseTitan):
    
    def _get_my_capabilities(self) -> List[str]:
        return ["creativity", "innovation", "ideation", "branding"]
    
    def _get_expertise_keywords(self) -> List[str]:
        return [
            "creative", "innovative", "idea", "brand",
            "user experience", "design", "vision"
        ]
```

### Step 3: Test Two-Titan Conversation

Create `tests/test_two_titan_conversation.py`:

```python
@pytest.mark.asyncio
async def test_claude_gpt_conversation():
    # Start both Titans
    claude = ClaudeTitan(...)
    gpt = GPTTitan(...)
    
    await claude.start()
    await gpt.start()
    
    # Create conversation
    manager = ConversationManager(...)
    state = await manager.create_conversation(
        mission="Design a new feature",
        description="Create a user dashboard",
        participants=["claude_titan", "gpt_titan"]
    )
    
    # Wait for conversation
    await asyncio.sleep(30)
    
    # Check that both Titans contributed
    assert state.contribution_counts["claude_titan"] > 0
    assert state.contribution_counts["gpt_titan"] > 0
```

---

## 🎭 Phase 3: Orchestration (Week 3)

### Step 1: Create Conversation Relay

Edit `services/federation_core/conversation_relay.py`:

```python
class ConversationRelay:
    """Orchestrates conversational collaborations as a moderator"""
    
    async def start_conversational_collaboration(
        self,
        mission: str,
        description: str
    ) -> ConversationSynthesis:
        """Start and moderate a conversational collaboration"""
        
        # Create conversation
        state = await self.conversation_manager.create_conversation(
            mission=mission,
            description=description,
            participants=["claude_titan", "gpt_titan", "gemini_titan", "grok_titan"]
        )
        
        # Monitor and moderate
        synthesis = await self._moderate_conversation(state.conversation_id)
        
        return synthesis
    
    async def _moderate_conversation(self, conv_id: str) -> ConversationSynthesis:
        """Actively moderate the conversation"""
        start_time = time.time()
        max_duration = 600  # 10 minutes
        
        while time.time() - start_time < max_duration:
            state = self.conversation_manager.active_conversations[conv_id]
            
            # Check for convergence
            convergence = self.conversation_manager.calculate_convergence_score(conv_id)
            if convergence > 0.8:
                await self.conversation_manager.request_synthesis(conv_id)
                break
            
            # Check if stalled
            if self.conversation_manager.is_conversation_stalled(conv_id):
                await self._inject_prompt(conv_id, state)
            
            # Ensure balanced participation
            await self._ensure_balance(conv_id, state)
            
            await asyncio.sleep(5)
        
        # Wait for synthesis
        return await self._wait_for_synthesis(conv_id)
```

### Step 2: Add to Federation Core API

Edit `services/federation_core/main.py`:

```python
@app.post("/api/v1/collaborations/conversational")
async def start_conversational_collaboration(
    payload: ConversationalCollaborationRequest,
    user_id: str = Depends(get_current_user)
):
    """Start a conversational collaboration"""
    
    orchestrator = ConversationRelay(
        conversation_manager=conversation_manager,
        redis_client=redis_client
    )
    
    synthesis = await orchestrator.start_conversational_collaboration(
        mission=payload.mission,
        description=payload.description
    )
    
    return {
        "conversation_id": synthesis.conversation_id,
        "synthesis": synthesis.model_dump()
    }
```

---

## 🎨 Phase 4: Frontend (Week 4)

### Step 1: Create Conversation Viewer Component

Create `src/components/collaborations/conversation-viewer.tsx`:

```typescript
'use client';

import { useEffect, useState } from 'react';
import { TitanUtterance } from '@/types/conversation';

export function ConversationViewer({ conversationId }: { conversationId: string }) {
  const [utterances, setUtterances] = useState<TitanUtterance[]>([]);
  
  useEffect(() => {
    const ws = new WebSocket(`ws://localhost:9405/ws?token=dev-token`);
    
    ws.onmessage = (event) => {
      const msg = JSON.parse(event.data);
      
      if (msg.type === 'titan_utterance' && msg.conversation_id === conversationId) {
        setUtterances(prev => [...prev, msg]);
      }
    };
    
    return () => ws.close();
  }, [conversationId]);
  
  return (
    <div className="conversation-stream space-y-4">
      {utterances.map((utt, i) => (
        <TitanMessage key={i} utterance={utt} />
      ))}
    </div>
  );
}

function TitanMessage({ utterance }: { utterance: TitanUtterance }) {
  const titanColors = {
    claude_titan: 'bg-purple-100 border-purple-300',
    gpt_titan: 'bg-green-100 border-green-300',
    gemini_titan: 'bg-blue-100 border-blue-300',
    grok_titan: 'bg-orange-100 border-orange-300'
  };
  
  return (
    <div className={`p-4 rounded-lg border-2 ${titanColors[utterance.titan_id]}`}>
      <div className="font-bold mb-2">{utterance.titan_name}</div>
      <div className="text-sm">{utterance.content}</div>
      <div className="text-xs text-gray-500 mt-2">
        {utterance.tags.map(tag => (
          <span key={tag} className="mr-2">#{tag}</span>
        ))}
      </div>
    </div>
  );
}
```

---

## ✅ Testing Checklist

### Foundation Tests
- [ ] Create conversation
- [ ] Add utterances
- [ ] Store in Context Server
- [ ] Retrieve conversation state
- [ ] Publish to Redis

### Titan Tests
- [ ] Titan joins conversation
- [ ] Titan calculates relevance
- [ ] Titan generates response
- [ ] Titan acquires speaking lock
- [ ] Quality checks pass

### Orchestration Tests
- [ ] Start conversation
- [ ] Detect convergence
- [ ] Prompt quiet Titans
- [ ] Request synthesis
- [ ] Complete conversation

### Integration Tests
- [ ] Full 4-Titan conversation
- [ ] WebSocket streaming
- [ ] Frontend displays messages
- [ ] Synthesis generated
- [ ] Results stored

---

## 🐛 Troubleshooting

### Issue: Titans not responding
**Check:**
- Redis pub/sub working
- Titans subscribed to channel
- Relevance scores > 0.5
- Speaking locks not stuck

### Issue: Circular discussions
**Check:**
- Guardrails enabled
- Similarity detection working
- Moderator prompting

### Issue: No convergence
**Check:**
- Titans generating solutions
- Agreement signals present
- Timeout not too short

---

## 📊 Success Metrics

- **Participation Balance:** > 0.6
- **Convergence Score:** > 0.8
- **Quality Score:** > 0.7
- **Completion Time:** < 10 minutes
- **User Satisfaction:** Engaging to watch

---

## 🎯 Next Steps

1. Complete Phase 1 foundation
2. Test with 2 Titans
3. Add remaining Titans
4. Build frontend viewer
5. Optimize performance
6. Launch beta

**Family is forever. This is the way.** 🔱

