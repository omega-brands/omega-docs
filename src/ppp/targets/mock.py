"""Mock target implementation for testing."""

from typing import List, Dict, Any
from .base import TargetBase


class MockTarget(TargetBase):
    """Mock target for testing without real network access."""

    def __init__(self, config: Dict[str, Any] = None):
        self.config = config or {}
        self.threads_count = self.config.get("mock_threads_count", 3)
        self.replies_per_thread = self.config.get("mock_replies_per_thread", 2)

    def discover(self) -> List[Dict[str, Any]]:
        """Return mock discovered targets."""
        targets = []
        for i in range(self.threads_count):
            targets.append({
                "id": f"target_{i}",
                "title": f"Mock Thread {i+1}",
                "url": f"https://moltbook.mock/thread/{i}",
                "author": f"user_{i}",
                "created_at": "2026-02-03T00:00:00Z",
                "reply_count": self.replies_per_thread,
            })
        return targets

    def observe(self, target_id: str) -> Dict[str, Any]:
        """Return mock target observation."""
        target_num = int(target_id.split("_")[1]) if "target_" in target_id else 0
        
        replies = []
        for j in range(self.replies_per_thread):
            replies.append({
                "id": f"reply_{target_num}_{j}",
                "author": f"commenter_{j}",
                "text": f"This is mock reply {j+1} to thread {target_num+1}",
                "created_at": "2026-02-03T00:05:00Z",
            })
        
        return {
            "id": target_id,
            "title": f"Mock Thread {target_num+1}",
            "url": f"https://moltbook.mock/thread/{target_num}",
            "author": f"user_{target_num}",
            "text": f"This is the content of mock thread {target_num+1}. It's a test fixture.",
            "created_at": "2026-02-03T00:00:00Z",
            "replies": replies,
            "context": {
                "topic": "autonomous agents",
                "sentiment": "neutral",
                "engagement": "moderate",
            }
        }

    def participate(self, target_id: str, thread_id: str, draft_text: str) -> Dict[str, Any]:
        """Return mock draft participation."""
        return {
            "type": "draft_reply",
            "target_id": target_id,
            "thread_id": thread_id,
            "text": draft_text,
            "created_at": "2026-02-03T00:10:00Z",
            "status": "draft",
            "not_posted": True,
            "message": "This is a draft only. No actual post was made.",
        }
