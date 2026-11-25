
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from database import get_connection, create_table

app = FastAPI(title="Employee Management API")

# Create database table when application starts
create_table()


# Employee model
class Employee(BaseModel):
    id: int
    name: str
    department: str


# Model for partial updates
class EmployeeUpdate(BaseModel):
    name: str | None = None
    department: str | None = None


# Home endpoint
@app.get("/")
def home():
    return {
        "message": "Employee Management API is running!"
    }


# Get all employees
@app.get("/employees")
def get_employees():
    conn = get_connection()

    employees = conn.execute(
        "SELECT * FROM employees"
    ).fetchall()

    conn.close()

    return [dict(employee) for employee in employees]


# Get employee by ID
@app.get("/employees/{employee_id}")
def get_employee(employee_id: int):
    conn = get_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    conn.close()

    if employee is None:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return dict(employee)


# Add employee
@app.post("/employees", status_code=201)
def add_employee(employee: Employee):
    conn = get_connection()

    try:
        conn.execute(
            """
            INSERT INTO employees (id, name, department)
            VALUES (?, ?, ?)
            """,
            (employee.id, employee.name, employee.department)
        )

        conn.commit()

    except Exception:
        conn.close()

        raise HTTPException(
            status_code=400,
            detail="Employee ID already exists or invalid data"
        )

    conn.close()

    return {
        "message": "Employee added successfully",
        "employee": employee
    }


# Update complete employee record
@app.put("/employees/{employee_id}")
def update_employee(
    employee_id: int,
    updated_employee: Employee
):

    if updated_employee.id != employee_id:
        raise HTTPException(
            status_code=400,
            detail="Employee ID cannot be changed"
        )

    conn = get_connection()

    cursor = conn.execute(
        """
        UPDATE employees
        SET name = ?, department = ?
        WHERE id = ?
        """,
        (
            updated_employee.name,
            updated_employee.department,
            employee_id
        )
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee updated successfully"
    }


# Partially update employee record
@app.patch("/employees/{employee_id}")
def partial_update_employee(
    employee_id: int,
    updates: EmployeeUpdate
):

    update_data = updates.model_dump(exclude_unset=True)

    if not update_data:
        raise HTTPException(
            status_code=400,
            detail="No fields provided"
        )

    conn = get_connection()

    employee = conn.execute(
        "SELECT * FROM employees WHERE id = ?",
        (employee_id,)
    ).fetchone()

    if employee is None:
        conn.close()

        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    name = update_data.get(
        "name",
        employee["name"]
    )

    department = update_data.get(
        "department",
        employee["department"]
    )

    conn.execute(
        """
        UPDATE employees
        SET name = ?, department = ?
        WHERE id = ?
        """,
        (name, department, employee_id)
    )

    conn.commit()
    conn.close()

    return {
        "message": "Employee updated successfully"
    }


# Delete employee
@app.delete("/employees/{employee_id}")
def delete_employee(employee_id: int):

    conn = get_connection()

    cursor = conn.execute(
        "DELETE FROM employees WHERE id = ?",
        (employee_id,)
    )

    conn.commit()
    conn.close()

    if cursor.rowcount == 0:
        raise HTTPException(
            status_code=404,
            detail="Employee not found"
        )

    return {
        "message": "Employee deleted successfully"
    }


# Get employees with department details using SQL JOIN
@app.get("/employees-with-departments")
def get_employees_with_departments():

    conn = get_connection()

    query = """
    SELECT
        employees.name,
        departments.department_id,
        departments.department_name AS department
    FROM employees
    INNER JOIN departments
    ON employees.department = departments.department_name
    """

    result = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in result]


# Get highest-paid employee in each department
@app.get("/department-top-earners")
def get_department_top_earners():

    conn = get_connection()

    query = """
    WITH department_ranking AS (
        SELECT
            name,
            department,
            salary,
            DENSE_RANK() OVER (
                PARTITION BY department
                ORDER BY salary DESC
            ) AS department_rank
        FROM employee_salary_practice
    )
    SELECT
        name,
        department,
        salary
    FROM department_ranking
    WHERE department_rank = 1
    ORDER BY department
    """

    result = conn.execute(query).fetchall()

    conn.close()

    return [dict(row) for row in result]
