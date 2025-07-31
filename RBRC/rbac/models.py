from typing import Dict, List, Optional

class Permission:
    def __init__(self, name: str, description: str = ""):
        self.name = name
        self.description = description

class Role:
    def __init__(self, name: str):
        self.name = name
        self.permissions: List[Permission] = []
    
    def add_permission(self, permission: Permission):
        if permission not in self.permissions:
            self.permissions.append(permission)
    
    def has_permission(self, permission_name: str) -> bool:
        return any(p.name == permission_name for p in self.permissions)

class User:
    def __init__(self, username: str):
        self.username = username
        self.roles: List[Role] = []
    
    def add_role(self, role: Role):
        if role not in self.roles:
            self.roles.append(role)
    
    def has_permission(self, permission_name: str) -> bool:
        return any(role.has_permission(permission_name) for role in self.roles)

# 内存存储
roles_db: Dict[str, Role] = {}
users_db: Dict[str, User] = {}
permissions_db: Dict[str, Permission] = {}

def get_user(username: str) -> Optional[User]:
    return users_db.get(username)

def create_user(username: str) -> User:
    if username in users_db:
        raise ValueError(f"User {username} already exists")
    user = User(username)
    users_db[username] = user
    return user

def create_role(role_name: str) -> Role:
    if role_name in roles_db:
        raise ValueError(f"Role {role_name} already exists")
    role = Role(role_name)
    roles_db[role_name] = role
    return role

def create_permission(permission_name: str, description: str = "") -> Permission:
    if permission_name in permissions_db:
        raise ValueError(f"Permission {permission_name} already exists")
    permission = Permission(permission_name, description)
    permissions_db[permission_name] = permission
    return permission
