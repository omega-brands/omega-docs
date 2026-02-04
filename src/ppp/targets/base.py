"""Base target abstraction."""

from abc import ABC, abstractmethod
from typing import List, Dict, Any


class TargetBase(ABC):
    """Abstract base class for targets."""

    @abstractmethod
    def discover(self) -> List[Dict[str, Any]]:
        """
        Discover targets.
        
        Returns list of target objects with id, title, url, etc.
        """
        pass

    @abstractmethod
    def observe(self, target_id: str) -> Dict[str, Any]:
        """
        Observe a specific target.
        
        Returns target details including content, threads, comments, etc.
        """
        pass

    @abstractmethod
    def participate(self, target_id: str, thread_id: str, draft_text: str) -> Dict[str, Any]:
        """
        Generate a draft participation artifact.
        
        Must NOT post or publish. Returns draft reply/comment structure.
        """
        pass
