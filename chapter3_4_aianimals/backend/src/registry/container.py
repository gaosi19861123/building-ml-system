from logging import getLogger

from src.configurations import Configurations
from src.constants import RUN_ENVIRONMENT
from src.infrastructure.client.elastic_search import Elasticsearch
from src.infrastructure.client.google_cloud_storage import GoogleCloudStorage
from src.infrastructure.client.local_storage import LocalStorage
from src.infrastructure.client.postgresql_database import PostgreSQLDatabase
from src.infrastructure.client.redis_queue import RedisQueue
from src.infrastructure.database import AbstractDatabase
from src.infrastructure.queue import AbstractQueue
from src.infrastructure.search import AbstractSearch
from src.infrastructure.storage import AbstractStorage
from src.middleware.crypt import AbstractCrypt, Crypt
from src.repository.animal_category_repository import AbstractAnimalCategoryRepository
from src.repository.animal_repository import AbstractAnimalRepository
from src.repository.animal_search_repository import AbstractAnimalSearchRepository
from src.repository.animal_subcategory_repository import AbstractAnimalSubcategoryRepository
from src.repository.implementation.animal_category_repository import AnimalCategoryRepository
from src.repository.implementation.animal_repository import AnimalRepository
from src.repository.implementation.animal_search_repository import AnimalSearchRepository
from src.repository.implementation.animal_subcategory_repository import AnimalSubcategoryRepository
from src.repository.implementation.like_repository import LikeRepository
from src.repository.implementation.user_repository import UserRepository
from src.repository.like_repository import AbstractLikeRepository
from src.repository.user_repository import AbstractUserRepository
from src.usecase.animal_category_usecase import AbstractAnimalCategoryUsecase
from src.usecase.animal_subcategory_usecase import AbstractAnimalSubcategoryUsecase
from src.usecase.animal_usecase import AbstractAnimalUsecase
from src.usecase.implementation.animal_category_usecase import AnimalCategoryUsecase
from src.usecase.implementation.animal_subcategory_usecase import AnimalSubcategoryUsecase
from src.usecase.implementation.animal_usecase import AnimalUsecase
from src.usecase.implementation.like_usecase import LikeUsecase
from src.usecase.implementation.metadata_usecase import MetadataUsecase
from src.usecase.implementation.user_usecase import UserUsecase
from src.usecase.like_usecase import AbstractLikeUsecase
from src.usecase.metadata_usecase import AbstractMetadataUsecase
from src.usecase.user_usecase import AbstractUserUsecase

logger = getLogger(__name__)


class Container(object):
    def __init__(
        self,
        storage_client: AbstractStorage,
        database: AbstractDatabase,
        queue: AbstractQueue,
        search_client: AbstractSearch,
        crypt: AbstractCrypt,
    ):
        self.database = database
        self.storage_client = storage_client
        self.queue = queue
        self.search_client = search_client
        self.crypt = crypt

        self.animal_category_repository: AbstractAnimalCategoryRepository = AnimalCategoryRepository()
        self.animal_subcategory_repository: AbstractAnimalSubcategoryRepository = AnimalSubcategoryRepository()
        self.animal_reposigory: AbstractAnimalRepository = AnimalRepository()
        self.user_repository: AbstractUserRepository = UserRepository()
        self.like_repository: AbstractLikeRepository = LikeRepository()
        self.animal_search_repository: AbstractAnimalSearchRepository = AnimalSearchRepository(
            search_client=self.search_client
        )

        self.animal_category_usecase: AbstractAnimalCategoryUsecase = AnimalCategoryUsecase(
            animal_category_repository=self.animal_category_repository,
        )
        self.animal_subcategory_usecase: AbstractAnimalSubcategoryUsecase = AnimalSubcategoryUsecase(
            animal_category_repository=self.animal_category_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
        )
        self.user_usecase: AbstractUserUsecase = UserUsecase(
            user_repository=self.user_repository,
            crypt=self.crypt,
        )
        self.animal_usecase: AbstractAnimalUsecase = AnimalUsecase(
            animal_repository=self.animal_reposigory,
            animal_search_repository=self.animal_search_repository,
            storage_client=self.storage_client,
            queue=self.queue,
        )
        self.like_usecase: AbstractLikeUsecase = LikeUsecase(
            like_repository=self.like_repository,
        )
        self.metadata_usecase: AbstractMetadataUsecase = MetadataUsecase(
            animal_category_repository=self.animal_category_repository,
            animal_subcategory_repository=self.animal_subcategory_repository,
        )


if Configurations.run_environment == RUN_ENVIRONMENT.LOCAL.value:
    storage_client: AbstractStorage = LocalStorage()
elif Configurations.run_environment == RUN_ENVIRONMENT.CLOUD.value:
    storage_client = GoogleCloudStorage()

container = Container(
    storage_client=storage_client,
    database=PostgreSQLDatabase(),
    queue=RedisQueue(),
    search_client=Elasticsearch(),
    crypt=Crypt(key_file_path=Configurations.key_file_path),
)
