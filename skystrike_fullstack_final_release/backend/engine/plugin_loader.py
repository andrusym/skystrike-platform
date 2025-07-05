import importlib

def run_hook(path, *args, **kwargs):
    """
    Dynamically load and run a function from a full module path.
    Example: run_hook("engine.drawdown_guardrails.check_equity_guardrail")
    """
    try:
        module_path, func_name = path.rsplit(".", 1)
        module = importlib.import_module(module_path)
        func = getattr(module, func_name)
        return func(*args, **kwargs)
    except Exception as e:
        return {"error": f"hook failed: {e}", "path": path}