import httpx

from schemas.employee import EmployeeCreate
from services.employee_service import create_employee


API_URL = "https://jsonplaceholder.typicode.com/users"


def sync_employees():
    response = httpx.get(API_URL, timeout=10.0)

    response.raise_for_status()

    users = response.json()

    success = 0
    errors = []

    for user in users:
        try:
            data = EmployeeCreate(
                name=user["name"].strip(),
                email=user["email"].strip(),
                department=user["company"]["name"].strip(),
            )

            create_employee(data)

            success += 1

        except (ValueError, KeyError, TypeError, AttributeError) as e:
            errors.append({"external_id": user.get("id"), "reason": str(e)})

    return {
        "total": len(users),
        "success": success,
        "failed": len(errors),
        "errors": errors,
    }
