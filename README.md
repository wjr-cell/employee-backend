# Employee Backend

基于 FastAPI 的员工管理后端系统，实现员工信息管理、数据持久化、缓存优化、批量数据导入及第三方系统对接。

## 技术栈

- Python 3.12
- FastAPI / Uvicorn
- MySQL
- Redis
- Pydantic
- HTTPX
- Pytest
- Docker

## 核心功能

- RESTful API 与员工 CRUD
- MySQL 数据持久化与邮箱唯一性校验
- Redis Cache Aside 查询缓存及缓存失效
- CSV 文件批量导入与数据清洗
- 第三方 REST API 数据获取与字段映射
- 接口异常处理与基础自动化测试

## API 接口

| Method | Endpoint | Description |
|---|---|---|
| GET | /health | 健康检查 |
| GET | /employees | 查询员工列表 |
| GET | /employees/{id} | 查询指定员工 |
| POST | /employees | 新增员工 |
| PATCH | /employees/{id} | 修改员工 |
| DELETE | /employees/{id} | 删除员工 |
| POST | /employees/import | CSV 批量导入 |
| POST | /employees/sync | 第三方数据同步 |

## 本地运行

1. 安装 requirements.txt 中的 Python 依赖。
2. 启动 MySQL 和 Redis 服务。
3. 创建 employee_db 数据库及 employees 表。
4. 参考 .env.example 创建并配置 .env 文件。
5. 执行 `python -m uvicorn main:app --reload` 启动项目。

Swagger API 文档：http://127.0.0.1:8000/docs

## 自动化测试

执行 `python -m pytest -v` 运行基础接口测试。