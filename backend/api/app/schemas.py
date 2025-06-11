from pydantic import BaseModel

class PredictRequest(BaseModel):
    gender: str
    race_ethnicity: str
    parental_level_of_education: str
    lunch: str
    test_preparation_course: str
    reading_score: float
    writing_score: float

class PredictResponse(BaseModel):
    predicted_score: float
