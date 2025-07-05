import importlib
import pkgutil

def safe_submodules(module_name):
    try:
        module = importlib.import_module(module_name)
        if not hasattr(module, '__path__'):
            return []
        return [name for _, name, _ in pkgutil.iter_modules(module.__path__)]
    except Exception as e:
        print(f"Error loading submodules from {module_name}: {e}")
        return []