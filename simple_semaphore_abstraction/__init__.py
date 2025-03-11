from .resource_pool import ResourcePool
from .resource_manager import ResourceManager, global_resource_manager
from .decorators import with_resource

__version__ = "0.1.0"

__all__ = [
    "ResourcePool",
    "ResourceManager",
    "with_resource",
    "global_resource_manager",
]