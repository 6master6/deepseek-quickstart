import pytest
from fastapi import FastAPI, status
from fastapi.testclient import TestClient


import sys
import os
# 将项目根目录添加到 sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from rbac.models import create_user, create_role, create_permission
from rbac.decorators import permission_required

app = FastAPI()  # 测试用 FastAPI 实例
client = TestClient(app)  # 测试客户端

# 创建测试数据
@pytest.fixture(scope="module")
def setup_data():
    # 清空数据库以确保测试独立性
    from rbac.models import roles_db, users_db, permissions_db
    roles_db.clear()
    users_db.clear()
    permissions_db.clear()
    
    # 创建权限
    read_perm = create_permission("read", "读取权限")
    write_perm = create_permission("write", "写入权限")
    
    # 创建角色并分配权限
    admin_role = create_role("admin")
    admin_role.add_permission(read_perm)
    admin_role.add_permission(write_perm)
    
    reader_role = create_role("reader")
    reader_role.add_permission(read_perm)
    
    # 创建用户并分配角色
    admin_user = create_user("admin")
    admin_user.add_role(admin_role)
    
    reader_user = create_user("reader")
    reader_user.add_role(reader_role)
    
    # 创建一个没有权限的用户
    no_perm_user = create_user("no_permission_user")
    
    return admin_user, reader_user

# 测试路由
@app.get("/read-data")
@permission_required(["read"])
async def read_data():
    return {"message": "数据读取成功"}

@app.post("/write-data")
@permission_required(["write"])
async def write_data():
    return {"message": "数据写入成功"}



def test_read_with_permission(setup_data):
    # 有read权限的用户
    response = client.get("/read-data", headers={"username": "reader"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "数据读取成功"}

def test_read_without_permission(setup_data):
    # 无read权限的用户
    response = client.get("/read-data", headers={"username": "no_permission_user"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_write_with_permission(setup_data):
    # 有write权限的用户
    response = client.post("/write-data", headers={"username": "admin"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"message": "数据写入成功"}

def test_write_without_permission(setup_data):
    # 无write权限的用户
    response = client.post("/write-data", headers={"username": "reader"})
    assert response.status_code == status.HTTP_403_FORBIDDEN

def test_unauthenticated_access():
    # 未认证用户
    response = client.get("/read-data")
    assert response.status_code == status.HTTP_401_UNAUTHORIZED
