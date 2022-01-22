from abc import ABC, abstractmethod
from logging import getLogger
from typing import List, Optional

from src.entities.violation_type import ViolationTypeModel, ViolationTypeQuery
from src.infrastructure.database import AbstractDatabase

logger = getLogger(__name__)


class AbstractViolationTypeRepository(ABC):
    def __init__(
        self,
        database: AbstractDatabase,
    ):
        self.database = database

    @abstractmethod
    def select(
        self,
        query: Optional[ViolationTypeQuery],
    ) -> List[ViolationTypeModel]:
        raise NotImplementedError
