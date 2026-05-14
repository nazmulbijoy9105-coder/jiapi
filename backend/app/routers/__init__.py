from .post2023 import router as post2023_router
from .pre2023 import router as pre2023_router
from .caselaw import router as caselaw_router
from .search import router as search_router
from .amendments import router as amendments_router
from .dtaa import router as dtaa_router
from .sros import router as sros_router
from .circulars import router as circulars_router
from .auth import router as auth_router
from .admin import router as admin_router
from .health import router as health_router

post2023 = post2023_router
pre2023 = pre2023_router
caselaw = caselaw_router
search = search_router
amendments = amendments_router
dtaa = dtaa_router
sros = sros_router
circulars = circulars_router
auth = auth_router
admin = admin_router
health = health_router
