import json
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class PersonalInfo(BaseModel):
    name: str
    email: EmailStr
    phone: Optional[str] = None

class ExperienceItem(BaseModel):
    role: str
    company: str
    start_date: str
    end_date: Optional[str] = None  # made optional with default
    description: str

class Resume(BaseModel):
    personal_info: PersonalInfo
    summary: str
    skills: List[str]
    experience: Optional[List[ExperienceItem]] = None  # optional list


def parse_resume(raw_json_str: str) -> Resume:
    data = json.loads(raw_json_str)
    return Resume(**data)