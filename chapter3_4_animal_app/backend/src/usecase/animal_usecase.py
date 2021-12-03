from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from sqlalchemy.orm import Session
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.request_object.animal import AnimalCreateRequest, AnimalRequest
from src.response_object.animal import AnimalResponse, AnimalResponseWithLike
from src.response_object.user import UserResponse

logger = getLogger(__name__)


class AbstractAnimalUsecase(ABC):
    def __init__(
        self,
        like_repository: AbstractLikeRepository,
        user_repository: AbstractUserRepository,
        animal_category_repository: AbstractAnimalCategoryRepository,
        animal_subcategory_repository: AbstractAnimalSubcategoryRepository,
        animal_repository: AbstractAnimalRepository,
    ):
        self.like_repository = like_repository
        self.user_repository = user_repository
        self.animal_category_repository = animal_category_repository
        self.animal_subcategory_repository = animal_subcategory_repository
        self.animal_repository = animal_repository

    @abstractmethod
    def retrieve(
        self,
        session: Session,
        request: Optional[AnimalRequest] = None,
        limit: Optional[int] = 100,
        offset: Optional[int] = 0,
    ) -> List[AnimalResponseWithLike]:
        raise NotImplementedError

    @abstractmethod
    def liked_by(
        self,
        session: Session,
        animal_id: str,
    ) -> List[UserResponse]:
        raise NotImplementedError

    @abstractmethod
    def register(
        self,
        session: Session,
        record: AnimalCreateRequest,
    ) -> Optional[AnimalResponse]:
        raise NotImplementedError
