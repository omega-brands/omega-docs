# Flow Demo Pages

This directory contains demonstration pages for various Flow features.

## Available Demos

### WebSocket Collaboration Demo
**Path:** `/demo/websocket-collaboration`

Demonstrates real-time collaboration updates via WebSocket connection to OMEGA Federation Core.

**Features:**
- Start a Four Titans collaboration
- Real-time WebSocket message streaming
- Message type handling (connected, started, completed, failed)
- Connection status monitoring
- Live code example

**What You'll Learn:**
- How to start collaborations
- How to connect to WebSocket
- How to handle real-time updates
- Message types and formats

**Related Files:**
- Component: `src/components/collaborations/collaboration-websocket-example.tsx`
- Quick Reference: `conversational/websocket-quick-reference.md`

## Running the Demos

1. **Start the development server:**
   ```bash
   npm run dev
   ```

2. **Ensure Federation Core is running:**
   ```bash
   cd /path/to/omega-core
   docker-compose up federation_core
   ```

3. **Navigate to a demo:**
   ```
   http://localhost:3000/demo/websocket-collaboration
   ```

## Creating New Demos

To add a new demo page:

1. Create a new directory under `src/app/demo/`:
   ```
   src/app/demo/my-feature/page.tsx
   ```

2. Create the demo component:
   ```typescript
   'use client';
   
   export default function MyFeatureDemoPage() {
     return (
       <div className="container mx-auto py-8">
         <h1>My Feature Demo</h1>
         {/* Demo content */}
       </div>
     );
   }
   ```

3. Update this README with the new demo information

## Demo Best Practices

- **Keep demos simple** - Focus on one feature at a time
- **Add documentation** - Include inline comments and links to guides
- **Show code examples** - Display the code being demonstrated
- **Handle errors gracefully** - Show what happens when things go wrong
- **Make it interactive** - Let users try the feature themselves
- **Link to production** - Show where the feature is used in the app

## Related Documentation

- [WebSocket Quick Reference](../../../conversational/websocket-quick-reference.md)

## Feedback

If you have suggestions for new demos or improvements to existing ones, please create an issue or submit a PR.
