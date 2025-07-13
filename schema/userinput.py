
from typing import Literal, Annotated
from pydantic import BaseModel, Field, computed_field


#Pydantic Model to validate upcoming User Data 
class UserInput(BaseModel):
    Prev_Sem_Result : Annotated[float, Field(..., ge=5, le=10, description="Previous Semester's GPA")]
    IQ_group: Annotated[Literal['Low', 'Below Average', 'Average', 'Above Average', 'High'], Field(..., description="IQ/Critical-Thinking Skills")]
    CGPA: Annotated[float, Field(..., ge=5, le=10, description="Current CGPA of Student")]
    Academic_Performance: Annotated[int, Field(..., gt=0, le=10, description="Academic Performance Rating on a scale of 1-10")]
    Internship_Experience: Annotated[Literal['Yes', 'No'], Field(..., description="Does the student have internship experience")]
    Projects_Completed: Annotated[int, Field(..., ge=0, le=5, description="How many projects have the student completed?")]
    extra_curr_score: Annotated[Literal['None', 'Low', 'Moderate', 'High'], Field(..., description="Student's Involvement in Extra_Curricular Activities")]
    Comm_score: Annotated[Literal['Poor', 'Fair', 'Good', 'Excellent'], Field(..., description="Student's Communication/Soft Skill Rating")]