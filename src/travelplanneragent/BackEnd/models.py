from datetime import date
from pydantic import BaseModel, Field


class TravelRequest(BaseModel):
    destination: str
    origin: str
    start_date: str
    end_date: str
    trip_type: str = Field(default="Solo")
    mode_of_transport: str = Field(default="Flight")
    budget_total: float
    budget_currency: str
    num_travelers: int = Field(default=1, ge=1)


class TravelResponse(BaseModel):
    status: str
    report_file: str | None = None
    detail: str | None = None
