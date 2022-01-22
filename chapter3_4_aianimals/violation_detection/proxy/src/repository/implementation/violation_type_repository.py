from logging import getLogger
from typing import List, Optional

from sqlalchemy import and_
from src.entities.violation_type import ViolationTypeCreate, ViolationTypeModel, ViolationTypeQuery
from src.infrastructure.database import AbstractDatabase
from src.repository.violation_type_repository import AbstractViolationTypeRepository
from src.schema.table import TABLES
from src.schema.violation_type import ViolationType

logger = getLogger(__name__)


class ViolationTypeRepository(AbstractViolationTypeRepository):
    def __init__(
        self,
        database: AbstractDatabase,
    ) -> None:
        super().__init__(database=database)
        self.table_name = TABLES.VIOLATION_TYPE.value

    def select(
        self,
        query: Optional[ViolationTypeQuery],
    ) -> List[ViolationTypeModel]:
        session = self.database.get_session().__next__()
        try:
            filters = []
            if query is not None:
                if query.id is not None:
                    filters.append(ViolationType.id == query.id)
                if query.name is not None:
                    filters.append(ViolationType.name == query.name)
            results = session.query(ViolationType).filter(and_(*filters)).order_by(ViolationType.id).all()
            data = [
                ViolationTypeModel(
                    id=d.id,
                    name=d.name,
                    created_at=d.created_at,
                    updated_at=d.updated_at,
                )
                for d in results
            ]
            return data
        except Exception as e:
            raise e
        finally:
            session.close()

    def insert(
        self,
        record: ViolationTypeCreate,
        commit: bool = True,
    ) -> Optional[ViolationTypeModel]:
        session = self.database.get_session().__next__()
        try:
            data = ViolationType(**record.dict())
            session.add(data)
            if commit:
                session.commit()
                session.refresh(data)
                result = self.select(
                    query=ViolationTypeQuery(id=data.id),
                )
                return result[0]
            return None
        except Exception as e:
            raise e
        finally:
            session.close()
