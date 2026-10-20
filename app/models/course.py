from dataclasses import dataclass
from typing import Optional
@dataclass
class Course:
    course_code: str
    title: str
    credits: int
    semester: int
    faculty_id: Optional[str] = None

