"""
Resume analysis request/response schemas.
"""
from pydantic import BaseModel


class ResumeAnalysisResponse(BaseModel):
    analysis_id: str
    filename: str
    analysis_result: dict


class ResumeMatchRequest(BaseModel):
    job_description: str


class ResumeMatchResponse(BaseModel):
    score: float
    strengths: list[str]
    weaknesses: list[str]
    recommendations: list[str]