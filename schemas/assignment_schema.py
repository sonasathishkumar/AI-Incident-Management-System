from pydantic import BaseModel


class AssignIncident(BaseModel):
    user_id: int