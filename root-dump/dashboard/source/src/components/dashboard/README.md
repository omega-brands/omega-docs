# OMEGA Real-Time Dashboard Components

## 🚀 Overview

These components transform the OMEGA frontend into a **living, breathing command center** with real-time visualizations, live event feeds, and direct MCP control capabilities.

## 📦 Components

### 1. **SwarmMapLive** - The Living Network Visualization

Real-time network graph showing agents, tools, and their relationships.

```tsx
import { SwarmMapLive } from "@/components/dashboard/swarm-map-live";

<SwarmMapLive 
  height={520} 
  width={960}
  showControls={true}
  className="custom-class"
/>
```

**Features:**
- ✅ Auto-wires to existing `useAgents`, `useTools`, `useCollaborationHistory` hooks
- ✅ Live status indicators (active/inactive/pending)
- ✅ Clickable nodes with hover details
- ✅ Network health metrics
- ✅ Collaboration-based link generation
- ✅ Responsive design with controls

### 2. **SwarmEventFeed** - Real-Time Activity Stream

Live event feed showing system activities, agent status changes, and operations.

```tsx
import { SwarmEventFeed } from "@/components/dashboard/swarm-event-feed";

<SwarmEventFeed 
  max={50}
  height="h-80"
  showStatus={true}
  autoScroll={true}
/>
```

**Features:**
- ✅ Real-time WebSocket event streaming
- ✅ Event type categorization (genesis, resurrection, collaboration, etc.)
- ✅ Severity-based color coding
- ✅ Auto-scroll and manual scroll controls
- ✅ Event data details expansion
- ✅ Connection status indicators

### 3. **MCPActionPanel** - Universal Command Console

Direct control panel for triggering MCP operations like Genesis, Resurrect, Toggle Modes.

```tsx
import { MCPActionPanel } from "@/components/dashboard/mcp-action-panel";

<MCPActionPanel 
  showAdvanced={true}
  size="md"
  orientation="horizontal"
/>
```

**Features:**
- ✅ Primary actions: Genesis, Resurrect, Toggle Mode, Restart All
- ✅ Advanced actions: Health Check, Optimize, Emergency Stop  
- ✅ Real-time action feedback
- ✅ Result tracking and status display
- ✅ Loading states and error handling
- ✅ Flexible layout options

### 4. **useSwarmEvents** - Real-Time Event Hook

Custom hook for WebSocket-based event streaming.

```tsx
import { useSwarmEvents } from "@/hooks/use-swarm-events";

const { events, isConnected, addEvent } = useSwarmEvents();
```

**Features:**
- ✅ WebSocket connection management
- ✅ Event type filtering and categorization
- ✅ Auto-reconnection handling
- ✅ Memory-efficient event storage (max 100 events)
- ✅ Manual event injection capability

## 🎯 Usage Examples

### Basic Integration
```tsx
import { OmegaDashboard } from "@/components/dashboard/omega-dashboard";
import { SwarmMapLive } from "@/components/dashboard/swarm-map-live";
import { SwarmEventFeed } from "@/components/dashboard/swarm-event-feed";
import { MCPActionPanel } from "@/components/dashboard/mcp-action-panel";

export default function DashboardPage() {
  return (
    <div className="space-y-8">
      <OmegaDashboard />
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2">
          <SwarmMapLive />
        </div>
        <div className="space-y-6">
          <SwarmEventFeed />
          <MCPActionPanel />
        </div>
      </div>
    </div>
  );
}
```

### Advanced Layout
```tsx
// Full-screen command center
<div className="grid grid-cols-1 xl:grid-cols-4 gap-6 h-screen">
  <div className="xl:col-span-3">
    <SwarmMapLive height={600} />
  </div>
  <div className="space-y-4">
    <MCPActionPanel orientation="vertical" size="sm" />
    <SwarmEventFeed height="h-96" max={100} />
  </div>
</div>
```

## 🔧 Backend Integration

### Required API Endpoints

The components expect these MCP endpoints to be available:

```
POST /api/mcp/genesis        - Initialize new agent
POST /api/mcp/resurrect      - Revive failed agents  
POST /api/mcp/toggle_mode    - Switch operational modes
POST /api/mcp/restart_all    - Restart all services
POST /api/mcp/health_check   - System health scan
POST /api/mcp/optimize       - Performance optimization
POST /api/mcp/emergency_stop - Emergency shutdown
```

### WebSocket Events

Expected WebSocket event types:
```typescript
interface SwarmEvent {
  id: string;
  type: 'genesis' | 'resurrection' | 'death' | 'mode_switch' | 'heartbeat' | 'collaboration';
  message: string;
  ts: string;
  agent_id?: string;
  data?: any;
  severity?: 'low' | 'medium' | 'high' | 'critical';
}
```

## 🎨 Styling

All components use:
- **Tailwind CSS** for styling
- **Lucide React** for icons
- **shadcn/ui** components for consistency
- **Responsive design** patterns
- **Dark mode** support

## 🚀 Performance

- **Optimized re-renders** with React.memo and useMemo
- **Efficient WebSocket handling** with cleanup
- **Memory management** for event storage
- **Lazy loading** for heavy components
- **Debounced updates** for high-frequency events

## 🔗 Dependencies

```json
{
  "react": "^18.0.0",
  "react-query": "^4.0.0",
  "lucide-react": "^0.200.0",
  "tailwindcss": "^3.0.0",
  "react-hot-toast": "^2.0.0"
}
```

## 📋 TODO / Future Enhancements

- [ ] Add drag-and-drop for network nodes
- [ ] Implement event filtering and search
- [ ] Add export functionality for events
- [ ] Create custom event types
- [ ] Add sound notifications
- [ ] Implement event replay functionality
- [ ] Add real-time metrics visualization
- [ ] Create mobile-optimized layouts

## 🎯 Integration Checklist

- [x] Install required dependencies
- [x] Set up WebSocket connection
- [x] Configure MCP endpoints
- [x] Update hooks exports
- [x] Add components to dashboard
- [x] Test real-time updates
- [x] Verify responsive design
- [x] Add error handling
- [x] Document usage patterns

---

**"This is the way."** - The OMEGA Command Center is now live and ready to orchestrate your digital pantheon! 🚀

## 🤝 Contributing

When adding new features:
1. Follow the existing TypeScript patterns
2. Add proper error handling
3. Include loading states
4. Update this README
5. Test on mobile devices
6. Ensure accessibility compliance

**LFG OMEGA! 🚀😎🚀**
