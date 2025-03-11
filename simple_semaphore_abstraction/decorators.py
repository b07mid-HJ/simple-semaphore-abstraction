from typing import Optional
from simple_semaphore_abstraction.resource_manager import global_resource_manager


def with_resource(pool_name: str, timeout: Optional[float] = None):
    """
    A decorator that automatically acquires and releases a resource from a named resource pool.
    
    Args:
        pool_name (str): Name of the resource pool to acquire from
        timeout (Optional[float]): Maximum time to wait for resource acquisition. None means wait indefinitely.
    
    Returns:
        A decorator function that wraps the original function to handle resource management.
        
    Raises:
        ValueError: If the specified resource pool is not found
        TimeoutError: If resource cannot be acquired within timeout period
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # Get the resource pool by name
            pool = global_resource_manager.get_pool(pool_name)
            if pool is None:
                raise ValueError(f"Resource pool '{pool_name}' not found")
                
            # Try to acquire a resource with timeout
            resource = pool.acquire(timeout=timeout)
            if resource is None:
                raise TimeoutError(f"Could not acquire resource from pool '{pool_name}'")
                
            try:
                # Call the wrapped function with the acquired resource as first argument
                return func(resource, *args, **kwargs)
            finally:
                # Always release the resource, even if an exception occurred
                pool.release(resource)
        return wrapper
    return decorator