# 后端 Python 开发规范

## 1. 代码风格

### 1.1 缩进和空格
- 使用 4 个空格进行缩进（不使用制表符）
- 每行长度不超过 88 个字符
- 文件末尾保留一个空行
- 函数和类之间使用两个空行分隔
- 函数内部的逻辑块之间使用一个空行分隔

### 1.2 命名约定
- **模块名**: 使用小写字母，单词之间用下划线分隔（snake_case）
- **类名**: 使用大驼峰命名法（PascalCase）
- **函数和变量名**: 使用小写字母，单词之间用下划线分隔（snake_case）
- **常量**: 使用全大写字母，单词之间用下划线分隔（SNAKE_CASE）
- **私有属性和方法**: 使用单下划线前缀（_private）
- **保护属性和方法**: 使用单下划线前缀（_protected）
- **特殊方法**: 使用双下划线前缀和后缀（__special__）

### 1.3 导入和导出
- 导入语句按以下顺序组织：
  1. 标准库
  2. 第三方库
  3. 本地模块
- 每个导入组之间使用空行分隔
- 避免使用 `from module import *` 导入方式
- 使用相对导入时，优先使用显式相对导入

### 1.4 文档字符串
- 所有模块、类、函数都应该有文档字符串
- 文档字符串使用三引号（"""）
- 模块文档字符串应该放在文件顶部
- 类文档字符串应该放在类定义之后
- 函数文档字符串应该放在函数定义之后
- 文档字符串应该包含功能描述、参数说明、返回值说明和异常说明

## 2. 代码质量

### 2.1 代码审查
- 定期进行代码审查，确保代码质量
- 关注代码的可读性、可维护性和性能
- 避免重复代码，提取可复用的逻辑
- 使用类型提示提高代码的可读性和可维护性

### 2.2 测试
- 为关键功能编写单元测试
- 使用 pytest 进行测试
- 确保测试覆盖率达到合理水平
- 测试文件与被测试文件放在同一目录下，命名为 `test_*.py`

### 2.3 错误处理
- 合理处理错误，避免应用崩溃
- 使用 try-except 捕获可能的错误
- 对于可预期的错误，使用特定的异常类型
- 为用户提供清晰的错误提示

### 2.4 日志
- 使用 Python 的 logging 模块进行日志记录
- 为不同级别的日志使用适当的日志级别（DEBUG, INFO, WARNING, ERROR, CRITICAL）
- 日志应该包含足够的信息，便于调试和问题定位

## 3. 性能优化

### 3.1 代码优化
- 避免不必要的计算和重复操作
- 使用适当的数据结构和算法
- 考虑使用生成器和迭代器提高内存效率
- 避免在循环中进行 I/O 操作

### 3.2 数据库优化
- 使用适当的索引
- 避免全表扫描
- 合理使用缓存
- 批量操作数据库，减少数据库连接次数

### 3.3 网络优化
- 使用适当的 HTTP 缓存策略
- 合理使用异步编程
- 考虑使用连接池管理数据库连接

## 4. 项目结构

### 4.1 目录结构
- `backend/src`: 源代码
  - `api`: API 路由
  - `services`: 业务逻辑
  - `models`: 数据模型
  - `schemas`: 数据验证
  - `utils`: 工具函数
  - `config`: 配置
  - `middlewares`: 中间件
  - `exceptions`: 异常处理
- `backend/tests`: 测试代码
- `backend/docs`: 文档

### 4.2 文件命名
- 模块文件: `module_name.py`
- 测试文件: `test_module_name.py`
- 配置文件: `config.py`
- 工具文件: `util.py` 或 `helper.py`

## 5. 工具和配置

### 5.0 虚拟环境（必选）

项目默认使用 `.venv` 虚拟环境，使用 `uv` 管理依赖，默认清华镜像源。

#### 5.0.1 安装 uv

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -Command "irm https://astral.sh/uv/install.ps1 | iex"

# 或使用 pip 安装
pip install uv
```

#### 5.0.2 创建虚拟环境

```bash
# 进入项目目录
cd /Users/zengwenhua/py_workspace/video-analysis-studio/backend

# 创建虚拟环境（自动安装依赖）
uv venv --python 3.11

# 或指定已有 Python
uv venv
```

#### 5.0.3 配置镜像源（可选）

创建 `~/.pip/pip.conf` 或在项目中配置：

```ini
# pip 配置
[global]
index-url = https://pypi.tuna.tsinghua.edu.cn/simple
trusted-host = pypi.tuna.tsinghua.edu.cn
```

uv 镜像配置：

```bash
# 设置全局镜像
uv pip install --help | grep mirror
# 或使用环境变量
export UV_DEFAULT_INDEX=https://pypi.tuna.tsinghua.edu.cn/simple
```

#### 5.0.4 安装依赖

```bash
# 激活虚拟环境
source .venv/bin/activate

# 安装依赖（使用 requirements.txt）
uv pip install -r requirements.txt

# 或自动从 pyproject.toml 安装
uv sync
```

#### 5.0.5 开发流程

```bash
# 1. 每次开发前激活虚拟环境
source .venv/bin/activate

# 2. 运行代码
python -m src.main

# 3. 添加新依赖
uv add <package>

# 4. 更新依赖
uv pip install -r requirements.txt --upgrade
```

#### 5.0.6 IDE 配置

- **VS Code**: 在 `.vscode/settings.json` 中配置 Python 解释器路径
- **PyCharm**: 将项目解释器设置为 `.venv` 虚拟环境

### 5.1 开发工具
- 使用 VS Code 或 PyCharm 作为主要开发工具
- 安装必要的扩展，如 Pylance、Flake8、Black 等

### 5.2 配置文件
- `pyproject.toml`: 项目配置
- `setup.py`: 包安装配置
- `requirements.txt`: 依赖配置
- `.env`: 环境变量配置

### 5.3 脚本命令
- `python -m uvicorn main:app --reload`: 启动开发服务器
- `pytest`: 运行测试
- `flake8`: 运行代码风格检查
- `black`: 代码格式化

## 6. 最佳实践

- 遵循 PEP 8 代码风格指南
- 遵循 PEP 257 文档字符串约定
- 保持代码简洁，避免过度工程化
- 注重代码的可读性和可维护性
- 定期更新依赖，确保使用最新的稳定版本
- 编写清晰的文档，便于团队协作
- 使用类型提示提高代码的可读性和可维护性

## 7. 代码示例

### 7.1 函数示例

```python
"""计算两个数的和"""
def add_numbers(a: int, b: int) -> int:
    """
    计算两个数的和
    
    Args:
        a: 第一个数
        b: 第二个数
    
    Returns:
        两个数的和
    """
    return a + b
```

### 7.2 类示例

```python
"""用户类"""
class User:
    """
    用户类，用于表示系统用户
    
    Attributes:
        id: 用户ID
        name: 用户名
        email: 用户邮箱
    """
    
    def __init__(self, id: int, name: str, email: str):
        """
        初始化用户对象
        
        Args:
            id: 用户ID
            name: 用户名
            email: 用户邮箱
        """
        self.id = id
        self.name = name
        self.email = email
    
    def get_user_info(self) -> dict:
        """
        获取用户信息
        
        Returns:
            用户信息字典
        """
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email
        }
```

### 7.3 API 路由示例

```python
"""用户相关 API 路由"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from src.schemas.user import UserCreate, UserResponse
from src.services.user import create_user, get_user
from src.utils.database import get_db

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserResponse)
def create_new_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    创建新用户
    
    Args:
        user: 用户创建请求
        db: 数据库会话
    
    Returns:
        创建的用户信息
    """
    return create_user(db=db, user=user)

@router.get("/{user_id}", response_model=UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    """
    根据 ID 获取用户信息
    
    Args:
        user_id: 用户 ID
        db: 数据库会话
    
    Returns:
        用户信息
    
    Raises:
        HTTPException: 用户不存在时抛出 404 异常
    """
    user = get_user(db=db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user
```

### 7.4 配置示例

```python
"""配置文件"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """
    应用配置
    """
    # 数据库配置
    DATABASE_URL: str
    
    # 应用配置
    APP_NAME: str = "视频分析工作台"
    APP_VERSION: str = "0.1.0"
    DEBUG: bool = True
    
    # Supabase 配置
    SUPABASE_URL: str
    SUPABASE_ANON_KEY: str
    SUPABASE_SERVICE_ROLE_KEY: str
    
    # 安全配置
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    class Config:
        env_file = ".env"

settings = Settings()
```