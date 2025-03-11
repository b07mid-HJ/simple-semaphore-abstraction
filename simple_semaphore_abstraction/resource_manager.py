from typing import Dict, Optional
from simple_semaphore_abstraction.resource_pool import ResourcePool
import threading

class ResourceManager:
    """
    A singleton class that manages named resource pools.
    
    This class implements the singleton pattern to ensure only one instance exists.
    It provides thread-safe registration and access to resource pools.
    """

    # Class variables for singleton implementation
    _instance = None  # Holds the single instance
    _lock = threading.Lock()  # Lock for thread-safe instance creation

    def __new__(cls):
        """
        Ensures only one instance of ResourceManager is created (singleton pattern).
        Uses a lock for thread-safe instance creation.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
            return cls._instance

    def __init__(self):
        # Only initialize once
        if not hasattr(self, 'initialized'):
            self.pools: Dict[str, ResourcePool] = {}  # Maps pool names to ResourcePool instances
            self.pools_lock = threading.RLock()  # Lock for thread-safe pool operations
            self.initialized = True  # Flag to prevent re-initialization

    def register_pool(self, name: str, pool: ResourcePool) -> None:
        """Register a resource pool with a name."""
        with self.pools_lock:
            self.pools[name] = pool
            
    def get_pool(self, name: str) -> Optional[ResourcePool]:
        """Get a resource pool by name."""
        with self.pools_lock:
            return self.pools.get(name)
            
    def unregister_pool(self, name: str) -> None:
        """Unregister a resource pool."""
        with self.pools_lock:
            if name in self.pools:
                del self.pools[name] 

# Create a global instance that can be imported and used across the application
global_resource_manager = ResourceManager()