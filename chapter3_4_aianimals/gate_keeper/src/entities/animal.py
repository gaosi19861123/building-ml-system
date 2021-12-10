from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Extra

ANIMAL_MAPPING_NAME = "animal"

ANIMAL_MAPPING = {
    "settings": {
        "analysis": {
            "analyzer": {
                "kuromoji_analyzer": {
                    "type": "custom",
                    "char_filter": [
                        "icu_normalizer",
                    ],
                    "tokenizer": "kuromoji_tokenizer",
                    "filter": [
                        "kuromoji_baseform",
                        "kuromoji_part_of_speech",
                        "ja_stop",
                        "kuromoji_number",
                        "kuromoji_stemmer",
                    ],
                }
            }
        }
    },
    "mappings": {
        "properties": {
            "name": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            },
            "description": {
                "type": "text",
                "analyzer": "kuromoji_analyzer",
            },
            "animal_category": {
                "type": "text",
            },
            "animal_subcategory": {
                "type": "text",
            },
        }
    },
}


class AnimalDocument(BaseModel):
    name: str
    description: str
    animal_category: str
    animal_subcategory: str

    class Config:
        extra = Extra.forbid


class AnimalQuery(BaseModel):
    id: Optional[str]
    name: Optional[str]
    animal_category_id: Optional[int]
    animal_subcategory_id: Optional[int]
    user_id: Optional[str]
    deactivated: Optional[bool] = False

    class Config:
        extra = Extra.forbid


class AnimalModel(BaseModel):
    id: str
    animal_category_id: int
    animal_category_name: str
    animal_subcategory_id: int
    animal_subcategory_name: str
    user_id: str
    name: str
    description: str
    photo_url: str
    deactivated: bool = False
    created_at: datetime
    updated_at: datetime
