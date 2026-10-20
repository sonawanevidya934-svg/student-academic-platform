from dataclasses import dataclass
from typing import Optional
@dataclass
class Enrollment:
    student_id: str
    course_code: str
    semester: int
    enrollment_id: Optional[int] = None
    marks: Optional[float] = None

