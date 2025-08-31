import warnings
print("Welcome to Bunian jail! Can you escape?")
payload = input("> ")
_exec = exec
__builtins__.__dict__.clear()
__builtins__ = None
_exec(payload)
