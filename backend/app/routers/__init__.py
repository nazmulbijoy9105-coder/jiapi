"""
JIAPI - Router exports
"""
from .post2023 import router as post2023
from .pre2023 import router as pre2023
from .caselaw import router as caselaw
from .search import router as search
from .amendments import router as amendments
from .dtaa import router as dtaa
from .sros import router as sros
from .circulars import router as circulars
from .auth import router as auth
from .admin import router as admin
from .health import router as health

__all__ = [
    "post2023", "pre2023", "caselaw", "search", 
    "amendments", "dtaa", "sros", "circulars",
    "auth", "admin", "health"
]
