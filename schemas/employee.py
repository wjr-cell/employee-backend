from pydantic import BaseModel, Field


class EmployeeCreate(BaseModel):
    name: str = Field(min_length=1)
    department: str = Field(min_length=1)
    email: str = Field(min_length=1)


class EmployeeUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    department: str | None = Field(default=None, min_length=1)
    email: str | None = Field(default=None, min_length=1)


class Employee(EmployeeCreate):
    id: int
