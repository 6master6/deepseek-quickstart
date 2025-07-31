from fastapi import FastAPI
from rbac.models import create_user, create_role, create_permission
from rbac.decorators import permission_required
from contextlib import asynccontextmanager

# 定义生命周期事件处理器
@asynccontextmanager
async def lifespan(app: FastAPI):
    # 应用启动时执行
    init_data()
    yield  # 应用运行中
    # # 应用关闭时可添加清理逻辑（如关闭数据库连接）
    

# 使用lifespan参数初始化应用
app = FastAPI(lifespan=lifespan)

# 初始化测试数据
def init_data():
    # 清空数据库
    from rbac.models import roles_db, users_db, permissions_db
    roles_db.clear()
    users_db.clear()
    permissions_db.clear()
    
    # 创建权限
    read_perm = create_permission("read", "读取权限")
    write_perm = create_permission("write", "写入权限")
    
    # 创建角色
    admin_role = create_role("admin")
    admin_role.add_permission(read_perm)
    admin_role.add_permission(write_perm)
    
    reader_role = create_role("reader")
    reader_role.add_permission(read_perm)
    
    # 创建用户
    admin = create_user("admin")
    admin.add_role(admin_role)
    
    reader = create_user("reader")
    reader.add_role(reader_role)

    # 添加调试信息，确认用户已创建
    print(f"已创建用户: {[user.username for user in users_db.values()]}")


# 路由定义：按权限级别划分接口
@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/public")
async def public():
    return {"message": "公开接口，无需权限"}

@app.get("/protected-read")
@permission_required(["read"])
async def protected_read():
    return {"message": "需要read权限"}

@app.post("/protected-write")
@permission_required(["write"])
async def protected_write():
    return {"message": "需要write权限"}

# 需要所有权限
@app.post("/sensitive-operation")
# require_all=True 表示需所有权限
@permission_required(["read", "write", "admin"], require_all=True)
async def sensitive_operation():
    return {"message": "需要read、write和admin权限"}



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
