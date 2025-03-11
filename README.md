<!-- create a simple init readme for this project about sempaphore abstraction library in python -->

# Semaphore Abstraction Library in Python

This project is a simple abstraction library for resource pooling and synchronization in Python. It provides thread-safe resource management with semaphore-based access control.

## Features

- **Thread-Safe Resource Pool**: Manage shared resources with thread-safe access control
- **Resource Manager**: Global resource pool management with named pools
- **Decorator Support**: Easy resource acquisition through decorators

## Installation

You can install the package using pip:

```bash
pip install semaphore-abstraction
```

Or install from source:

```bash
git clone https://github.com/b07mid-HJ/simple-semaphore-abstraction.git
cd simple-semaphore-abstraction
pip install -e .
```

## Usage Examples

### Resource Pool Example

```python
from semaphore_abstraction import ResourcePool

# Create a pool of database connections
connections = [create_connection() for _ in range(3)]
pool = ResourcePool(resources=connections, max_call=2)

# Use a connection from the pool
resource = pool.acquire(timeout=5.0)
try:
    # Use the resource
    result = resource.execute("SELECT * FROM table")
finally:
    pool.release(resource)

# Or use the context manager
with pool:
    resource = pool.acquire()
    # Use the resource
    result = resource.execute("SELECT * FROM table")
```

### Using Resource Manager and Decorator

```python
from semaphore_abstraction import ResourceManager, with_resource

# Get the global resource manager
manager = ResourceManager()

# Register a pool
manager.register_pool("db_pool", pool)

# Use the decorator to automatically acquire and release resources
@with_resource("db_pool", timeout=5.0)
def query_database(connection, query):
    return connection.execute(query)

# The connection is automatically managed
result = query_database("SELECT * FROM table")
```

## API Documentation

### ResourcePool[T]

- `ResourcePool(resources: List[T], max_call: int = 1)`
  - `resources`: List of resources to manage
  - `max_call`: Maximum number of concurrent accesses
- `acquire(timeout: Optional[float] = None) -> Optional[T]`: Get a resource from the pool
- `release(resource: T) -> bool`: Return a resource to the pool
- Context manager support with `__enter__` and `__exit__`

### ResourceManager

- Singleton class for global resource pool management
- `register_pool(name: str, pool: ResourcePool)`: Register a named resource pool
- `get_pool(name: str) -> Optional[ResourcePool]`: Get a pool by name
- `unregister_pool(name: str)`: Remove a pool registration

### Decorators

- `@with_resource(pool_name: str, timeout: Optional[float] = None)`: 
  - Decorator for automatic resource acquisition
  - Acquires resource from named pool and passes it as first argument to function
  - Optional timeout for acquisition attempts


## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
