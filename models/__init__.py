import os
import glob

# Get all Python files in the current directory
modules = glob.glob(os.path.dirname(__file__) + "/*.py")

# Import all modules except __init__.py
__all__ = [os.path.basename(f)[:-3] for f in modules if not f.endswith("__init__.py")]

# Import all models
from . import *
