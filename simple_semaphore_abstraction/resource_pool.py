import threading
from typing import Dict, List, Optional, TypeVar, Generic

T = TypeVar('T')  # Generic type variable for the resource type


class ResourcePool (Generic[T]):
    """
    A thread-safe pool of resources that can be acquired and released.
    
    Uses a semaphore to limit concurrent access and tracks resource usage per thread.
    Generic type T represents the resource type being managed.
    """
    
    def __init__(self, resources: List[T], max_call: int=1):
        """
        Initialize the resource pool.
        
        Args:
            resources: List of resources to manage in the pool
            max_call: Maximum number of concurrent resource acquisitions allowed
        """
        self.resources=resources
        self.available_resources= resources.copy()  # Track available resources
        self.semaphore= threading.Semaphore(value= max_call)  # Control concurrent access
        self.resource_lock= threading.RLock()  # Lock for thread-safe resource management
        self.in_use: Dict[T, threading.Thread]={}  # Track which thread is using each resource

    def acquire (self, timeout : Optional[float]=None) -> Optional[T]:
        """
        Acquire a resource from the pool.
        
        Args:
            timeout: Maximum time to wait for resource. None means wait indefinitely.
            
        Returns:
            A resource of type T if successful, None if timeout or no resources available
        """
        if not self.semaphore.acquire(blocking=True, timeout=timeout):
            return None

        with self.resource_lock:
            if not self.available_resources:
                self.semaphore.release()
                return None
            res=self.available_resources.pop(0)
            self.in_use[res]=threading.current_thread()
            return res
    
    def release (self,resource: T) -> bool:
        """
        Release a resource back to the pool.
        
        Args:
            resource: The resource to release
            
        Returns:
            True if resource was released, False if resource wasn't in use
        """
        with self.resource_lock:
            if resource not in self.in_use:
                return False
            del self.in_use[resource]
            self.available_resources.append(resource)
            self.semaphore.release()
            return True
    
    def __enter__(self) -> 'ResourcePool[T]':
        """Context manager entry - returns self for use in with statements"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Context manager exit - automatically releases all resources held by current thread.
        Ensures resources are released even if an exception occurs.
        """
        thread = threading.current_thread()
        with self.resource_lock:
            resources_to_release = [r for r, t in self.in_use.items() if t == thread]
            
        for resource in resources_to_release:
            self.release(resource)
    
            
     


