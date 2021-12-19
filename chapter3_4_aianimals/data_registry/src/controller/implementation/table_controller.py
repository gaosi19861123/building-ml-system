from typing import List

from sqlalchemy.engine import Engine
from src.controller.table_controller import AbstractTableController
from src.middleware.logger import configure_logger
from src.schema.animal import Animal
from src.schema.animal_category import AnimalCategory
from src.schema.animal_subcategory import AnimalSubcategory
from src.schema.base import Base
from src.schema.like import Like
from src.schema.user import User
from src.usecase.table_usecase import AbstractTableUsecase

logger = configure_logger(__name__)


class TableController(AbstractTableController):
    def __init__(
        self,
        table_usecase: AbstractTableUsecase,
        engine: Engine,
    ):
        super().__init__(
            table_usecase=table_usecase,
            engine=engine,
        )

    def create_table(self):
        tables: List[Base] = [AnimalCategory, AnimalSubcategory, User, Animal, Like]
        for table in tables:
            logger.info(f"create table: {table.__table__}")
            self.table_usecase.create_table(
                engine=self.engine,
                table=table,
                checkfirst=True,
            )
            logger.info(f"done create table: {table.__table__}")

    def create_index(self):
        animal_category_indices = [
            {"column": AnimalCategory.name_en, "unique": True},
            {"column": AnimalCategory.name_ja, "unique": True},
            {"column": AnimalCategory.is_deleted, "unique": False},
        ]
        animal_subcategory_indices = [
            {"column": AnimalSubcategory.name_en, "unique": True},
            {"column": AnimalSubcategory.name_ja, "unique": True},
            {"column": AnimalSubcategory.animal_category_id, "unique": False},
            {"column": AnimalSubcategory.is_deleted, "unique": False},
        ]
        user_indices = [
            {"column": User.handle_name, "unique": False},
            {"column": User.email_address, "unique": True},
            {"column": User.deactivated, "unique": False},
        ]
        animal_indices = [
            {"column": Animal.name, "unique": False},
            {"column": Animal.user_id, "unique": False},
            {"column": Animal.animal_category_id, "unique": False},
            {"column": Animal.animal_subcategory_id, "unique": False},
        ]
        like_indices = [
            {"column": Like.user_id, "unique": False},
            {"column": Like.animal_id, "unique": False},
        ]

        for index in animal_category_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=AnimalCategory,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in animal_subcategory_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=AnimalSubcategory,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in user_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=User,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in animal_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=Animal,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
        for index in like_indices:
            logger.info(f"create index: {index}")
            self.table_usecase.create_index(
                engine=self.engine,
                table=Like,
                column=index["column"],
                checkfirst=True,
                unique=index["unique"],
            )
            logger.info(f"done create index: {index}")
