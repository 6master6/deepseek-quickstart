from fastapi import HTTPException, status, Request
from typing import List, Optional
from .models import get_user, User

async def get_current_user(request: Request) -> Optional[User]:
    """从请求头提取用户名并查询用户"""
    # 从请求头获取 "username" 字段
    username = request.headers.get("username")
    if not username:
        return None
    # 调用 models 中的 get_user 查询用户
    return get_user(username)

# 权限检查装饰器：接收权限列表和 require_all 参数（是否需要所有权限）
def permission_required(permission_names: List[str], require_all: bool = False):
    # 装饰器内层：接收被装饰的路由函数
    def decorator(func):
        # 包装函数：实现权限检查逻辑
        async def wrapper(request: Request):  
            # 获取当前用户
            current_user = await get_current_user(request)
            # 未认证用户：返回 401
            if not current_user:
                raise HTTPException( 
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="未认证用户"
                )
            
            # 检查用户是否有权限
            if require_all:
                has_perm = all(
                    current_user.has_permission(perm)
                    for perm in permission_names
                )
            else:
                has_perm = any(
                    current_user.has_permission(perm)
                    for perm in permission_names
                )
            # 权限不足：返回 403
            if not has_perm:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="权限不足"
                )
            # 3. 权限通过：调用原路由函数
            return await func()  # 不传递任何参数给路由函数
        return wrapper
    return decorator



