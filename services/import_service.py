import csv
import io

from schemas.employee import EmployeeCreate
from services.employee_service import create_employee


def import_employees(content: bytes):
    text = content.decode("utf-8-sig")

    reader = csv.DictReader(io.StringIO(text))

    required_fields = {"name", "department", "email"}

    if not required_fields.issubset(reader.fieldnames or []):
        raise ValueError("CSV 文件缺少必要字段")

    success = 0
    errors = []

    for row_number, row in enumerate(reader, start=2):
        try:
            data = EmployeeCreate(
                name=(row.get("name") or "").strip(),
                department=(row.get("department") or "").strip(),
                email=(row.get("email") or "").strip(),
            )

            create_employee(data)

            success += 1

        except ValueError as e:
            errors.append({"row": row_number, "reason": str(e)})

    return {
        "total": success + len(errors),
        "success": success,
        "failed": len(errors),
        "errors": errors,
    }
