import json
from cache import redis_client
from mysql.connector import IntegrityError
from database import get_connection
from schemas.employee import EmployeeCreate, EmployeeUpdate


def create_employee(data: EmployeeCreate):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        sql = """
            INSERT INTO employees (name, department, email)
            VALUES (%s, %s, %s)
        """

        cursor.execute(sql, (data.name, data.department, data.email))

        employee_id = cursor.lastrowid
        conn.commit()

        return {"id": employee_id, **data.model_dump()}

    except IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError("邮箱已存在") from e
        raise

    finally:
        cursor.close()
        conn.close()


def get_employees():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM employees ORDER BY id")
        return cursor.fetchall()

    finally:
        cursor.close()
        conn.close()


def get_employee(employee_id: int):
    cache_key = f"employee:{employee_id}"

    cached = redis_client.get(cache_key)

    if cached is not None:
        print("缓存命中")
        return json.loads(cached)

    print("缓存未命中，查询 MySQL")

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))

        employee = cursor.fetchone()

        if employee is not None:
            redis_client.set(cache_key, json.dumps(employee), ex=300)

        return employee

    finally:
        cursor.close()
        conn.close()


def update_employee(employee_id: int, data: EmployeeUpdate):
    updates = data.model_dump(exclude_none=True)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    try:
        cursor.execute(
            "SELECT * FROM employees WHERE id = %s FOR UPDATE", (employee_id,)
        )
        employee = cursor.fetchone()

        if employee is None:
            conn.rollback()
            return None

        if updates:
            fields = ", ".join(f"{key} = %s" for key in updates)

            sql = f"UPDATE employees SET {fields} WHERE id = %s"

            params = tuple(updates.values()) + (employee_id,)

            cursor.execute(sql, params)

        cursor.execute("SELECT * FROM employees WHERE id = %s", (employee_id,))
        employee = cursor.fetchone()
        conn.commit()

        redis_client.delete(f"employee:{employee_id}")

        return employee

    except IntegrityError as e:
        conn.rollback()
        if e.errno == 1062:
            raise ValueError("邮箱已存在") from e
        raise

    finally:
        cursor.close()
        conn.close()


def delete_employee(employee_id: int):
    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("DELETE FROM employees WHERE id = %s", (employee_id,))

        deleted = cursor.rowcount > 0
        conn.commit()

        if deleted:
            redis_client.delete(f"employee:{employee_id}")

        return deleted if deleted else None

    finally:
        cursor.close()
        conn.close()
