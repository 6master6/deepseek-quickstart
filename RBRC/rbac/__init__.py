from .decorators import permission_required
from .models import Role, Permission, User

__all__ = ["permission_required", "Role", "Permission", "User"]

__version__ = "0.1.0"

# 依赖配置
__dependencies__ = [
    "fastapi>=0.68.0",
    "pytest>=6.2.4",
    "python-multipart>=0.0.5",
    "uvicorn>=0.15.0"
]
