from fastapi import UploadFile, File
from services.import_service import import_employees
from fastapi import APIRouter, HTTPException, Response
from schemas.employee import EmployeeCreate, EmployeeUpdate, Employee
from services import employee_service
import httpx
from services.sync_service import sync_employees

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("", response_model=Employee, status_code=201)
def create(data: EmployeeCreate):
    try:
        return employee_service.create_employee(data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@router.get("", response_model=list[Employee])
def get_all():
    return employee_service.get_employees()


@router.post("/import")
def import_csv(file: UploadFile = File(...)):
    if not file.filename or not file.filename.lower().endswith(".csv"):
        raise HTTPException(status_code=400, detail="仅支持 CSV 文件")

    content = file.file.read()

    try:
        return import_employees(content)

    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="文件必须使用 UTF-8 编码")

    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/sync")
def sync():
    try:
        return sync_employees()

    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="第三方系统请求超时")

    except httpx.HTTPError:
        raise HTTPException(status_code=502, detail="第三方系统请求失败")

    except ValueError:
        raise HTTPException(status_code=502, detail="第三方系统返回的数据格式错误")


@router.get("/{employee_id}", response_model=Employee)
def get_one(employee_id: int):
    employee = employee_service.get_employee(employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="员工不存在")

    return employee


@router.patch("/{employee_id}", response_model=Employee)
def update(employee_id: int, data: EmployeeUpdate):
    try:
        employee = employee_service.update_employee(employee_id, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))

    if employee is None:
        raise HTTPException(status_code=404, detail="员工不存在")

    return employee


@router.delete("/{employee_id}", status_code=204)
def delete(employee_id: int):
    employee = employee_service.delete_employee(employee_id)

    if employee is None:
        raise HTTPException(status_code=404, detail="员工不存在")

    return Response(status_code=204)
