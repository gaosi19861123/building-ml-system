from datetime import datetime
from typing import List

from pydantic import BaseModel, Extra


class AnimalResponseBase(BaseModel):
    id: str
    animal_category_id: int
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_id: int
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    user_id: str
    user_handle_name: str
    name: str
    description: str
    photo_url: str
    likes: int
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime


class AnimalResponse(AnimalResponseBase):
    pass

    class Config:
        extra = Extra.forbid


class AnimalSearchResponse(BaseModel):
    score: float
    id: str
    name: str
    description: str
    photo_url: str
    animal_category_name_en: str
    animal_category_name_ja: str
    animal_subcategory_name_en: str
    animal_subcategory_name_ja: str
    user_handle_name: str
    likes: int
    created_at: datetime

    class Config:
        extra = Extra.forbid


class AnimalSearchResponses(BaseModel):
    hits: int
    max_score: float
    results: List[AnimalSearchResponse]

    class Config:
        extra = Extra.forbid
