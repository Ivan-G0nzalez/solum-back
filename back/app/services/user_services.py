from app.repositories.unit_of_work import UnitOfWork
from app.data_acess.models import User as UserModel
from app.domain.user_models import User as UserDomain, UserCreate, UserUpdate
from app.utils.logger import logger
from app.utils.pagination import CustomPagination
from app.utils.auth import get_password_hash, verify_password
from datetime import datetime
from typing import List, Optional

class UserService:
    def __init__(self, unit_of_work_factory=UnitOfWork) -> None:
        self._unit_of_work_factory = unit_of_work_factory



    def authenticate_user(self, username_or_email: str, password: str):
        logger.info(f"Authenticating user: {username_or_email}")
        try:
            with self._unit_of_work_factory() as uow:
                user_model = uow.users.get_by_username_or_email(username_or_email)
                if not user_model or not verify_password(password, user_model.password):
                    logger.warning(f"Authentication failed for user: {username_or_email}")
                    return None
                if not user_model.is_active:
                    logger.warning(f"Inactive user: {username_or_email}")
                    return None

                uow.users.update_last_login(user_model.id)
                uow._UnitOfWork__session.commit()
                logger.info(f"Authenticated user: {username_or_email}")
                # Convert to domain model before returning to avoid detached instance error
                return UserDomain.model_validate(user_model)
        except Exception as e:
            logger.error(f"Error authenticating user: {e}")
            raise

    def get_users(self) -> List[UserDomain]:
        logger.info("Fetching all users")
        try:
            with self._unit_of_work_factory() as uow:
                users_models = uow.users.list()
                users = [UserDomain.model_validate(user) for user in users_models]
                return users
        except Exception as e:
            logger.error(f"Error fetching users: {e}")
            raise

    def get_users_paginated(self, pagination: CustomPagination):
        logger.info(f"Fetching paginated users: page={pagination.page}, items={pagination.items_per_page}")
        try:
            with self._unit_of_work_factory() as uow:
                total = uow.users.count()
                users = uow.users.list_paginated(pagination.offset, pagination.items_per_page)
                domain_users = [UserDomain.model_validate(user) for user in users]
                return pagination.paginate(domain_users, total)
        except Exception as e:
            logger.error(f"Error paginating users: {e}")
            raise

    def get_user(self, user_id: int) -> Optional[UserDomain]:
        logger.info(f"Fetching user by ID: {user_id}")
        try:
            with self._unit_of_work_factory() as uow:
                user = uow.users.get(user_id)
                return UserDomain.model_validate(user) if user else None
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {e}")
            raise

    def get_user_by_username(self, username: str) -> Optional[UserDomain]:
        logger.info(f"Fetching user by username: {username}")
        try:
            with self._unit_of_work_factory() as uow:
                user = uow.users.get_by_username(username)
                return UserDomain.model_validate(user) if user else None
        except Exception as e:
            logger.error(f"Error fetching user {username}: {e}")
            raise

    def create_user(self, user_data: UserCreate) -> UserDomain:
        logger.info(f"Creating user: {user_data.username}")
        try:
            with self._unit_of_work_factory() as uow:
                if uow.users.get_by_username(user_data.username):
                    raise ValueError("Username already exists")
                if uow.users.get_by_email(user_data.email):
                    raise ValueError("Email already exists")

                hashed_password = get_password_hash(user_data.password)
                user_model = UserModel(**user_data.model_dump(exclude={"password"}), password=hashed_password)
                new_user = uow.users.add(user_model)
                uow._UnitOfWork__session.commit()
                return UserDomain.model_validate(new_user)
        except Exception as e:
            logger.error(f"Error creating user: {e}")
            raise

    def update_user(self, user_id: int, user_data: UserUpdate) -> Optional[UserDomain]:
        logger.info(f"Updating user ID: {user_id}")
        try:
            with self._unit_of_work_factory() as uow:
                update_data = user_data.model_dump(exclude_unset=True)
                if 'email' in update_data:
                    existing = uow.users.get_by_email(update_data['email'])
                    if existing and existing.id != user_id:
                        raise ValueError("Email already exists")
                updated = uow.users.update(user_id, update_data)
                if updated:
                    uow._UnitOfWork__session.commit()
                    return UserDomain.model_validate(updated)
                return None
        except Exception as e:
            logger.error(f"Error updating user {user_id}: {e}")
            raise

    def delete_user(self, user_id: int) -> bool:
        logger.info(f"Deleting user ID: {user_id}")
        try:
            with self._unit_of_work_factory() as uow:
                success = uow.users.delete(user_id)
                if success:
                    uow._UnitOfWork__session.commit()
                return success
        except Exception as e:
            logger.error(f"Error deleting user {user_id}: {e}")
            raise


