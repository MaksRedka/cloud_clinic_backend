"""Schemas to represent languages application models."""

from pydantic import BaseModel, Json

"""Schemas to represent languages application models."""

class TreatmentPlanBase(BaseModel):
    user_uuid: str
    title: str
    description: str
    is_open: bool
    data: Json

class TreatmentPlanCreate(TreatmentPlanBase):
    pass

class TreatmentPlanUpdate(BaseModel):
    data: Json 