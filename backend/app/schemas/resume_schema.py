from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    filename: str
    score: int
    skills: list[str]
    education: list[str]
    experience: list[str]
    suggestions: list[str]


class ResumeMatchRequest(BaseModel):
    job_description: str


class ResumeMatchResponse(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]