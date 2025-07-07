from app.data_acess.models import User
from app.repositories.repository import AbtractRepository
from app.utils.logger import logger
from datetime import datetime

class UserRepository(AbtractRepository):
    def __init__(self, session):
        self.__session = session
    
    def list(self):
        logger.info("Start getting users from database")
        try:
            users = self.__session.query(User).all()
            logger.info("Successful operation to get all users")
            return users
        except Exception as e:
            logger.error(f'Failed Operation to get all users: {e}')
            raise

    def list_paginated(self, offset: int, limit: int):
        """Get paginated list of users"""
        logger.info(f"Start getting paginated users: offset={offset}, limit={limit}")
        try:
            users = self.__session.query(User).offset(offset).limit(limit).all()
            logger.info(f"Successful operation to get paginated users: {len(users)} items")
            return users
        except Exception as e:
            logger.error(f'Failed Operation to get paginated users: {e}')
            raise

    def count(self) -> int:
        """Get total count of users"""
        logger.info("Start counting users")
        try:
            count = self.__session.query(User).count()
            logger.info(f"Successful count operation: {count} users")
            return count
        except Exception as e:
            logger.error(f'Failed Operation to count users: {e}')
            raise
    
    def get(self, user_id):
        logger.info(f"Starting to get a user from database with id: {user_id}")
        try:
            user = self.__session.query(User).filter(User.id == user_id).first()
            if user is None:
                logger.info(f'User not found with id: {user_id}')
                return None
            
            logger.info(f'Found the user: {user.id} username: {user.username}')
            return user
        except Exception as e:
            logger.error(f'Failed Operation to get user: {e}')
            raise

    def get_by_username(self, username: str):
        """Get user by username"""
        logger.info(f"Starting to get a user from database with username: {username}")
        try:
            user = self.__session.query(User).filter(User.username == username).first()
            if user is None:
                logger.info(f'User not found with username: {username}')
                return None
            
            logger.info(f'Found the user: {user.id} username: {user.username}')
            return user
        except Exception as e:
            logger.error(f'Failed Operation to get user by username: {e}')
            raise

    def get_by_email(self, email: str):
        """Get user by email"""
        logger.info(f"Starting to get a user from database with email: {email}")
        try:
            user = self.__session.query(User).filter(User.email == email).first()
            if user is None:
                logger.info(f'User not found with email: {email}')
                return None
            
            logger.info(f'Found the user: {user.id} email: {user.email}')
            return user
        except Exception as e:
            logger.error(f'Failed Operation to get user by email: {e}')
            raise

    def get_by_username_or_email(self, username_or_email: str):
        """Get user by username or email"""
        logger.info(f"Starting to get a user from database with username or email: {username_or_email}")
        try:
            user = self.__session.query(User).filter(
                (User.username == username_or_email) | (User.email == username_or_email)
            ).first()
            if user is None:
                logger.info(f'User not found with username or email: {username_or_email}')
                return None
            
            logger.info(f'Found the user: {user.id} username: {user.username}')
            return user
        except Exception as e:
            logger.error(f'Failed Operation to get user by username or email: {e}')
            raise

    def add(self, user: User):
        logger.info("Starting to add a user to database")
        try:
            self.__session.add(user)
            self.__session.flush()  # Flush to get the ID
            self.__session.refresh(user)
            logger.info(f"Successfully added user: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Failed to add user: {e}")
            raise

    def update(self, user_id: int, user_data: dict):
        logger.info(f"Starting to update user with id: {user_id}")
        try:
            user = self.get(user_id)
            if user is None:
                logger.error(f"User with id {user_id} not found")
                return None
            
            for key, value in user_data.items():
                setattr(user, key, value)
            
            self.__session.flush()
            self.__session.refresh(user)
            logger.info(f"Successfully updated user: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Failed to update user: {e}")
            raise

    def update_last_login(self, user_id: int):
        """Update user's last login timestamp"""
        logger.info(f"Starting to update last login for user with id: {user_id}")
        try:
            user = self.get(user_id)
            if user is None:
                logger.error(f"User with id {user_id} not found")
                return None
            
            user.last_login = datetime.utcnow()
            self.__session.flush()
            self.__session.refresh(user)
            logger.info(f"Successfully updated last login for user: {user.username}")
            return user
        except Exception as e:
            logger.error(f"Failed to update last login: {e}")
            raise

    def delete(self, user_id: int):
        logger.info(f"Starting to delete user with id: {user_id}")
        try:
            user = self.get(user_id)
            if user is None:
                logger.error(f"User with id {user_id} not found")
                return False
            
            self.__session.delete(user)
            self.__session.flush()
            logger.info(f"Successfully deleted user: {user.username}")
            return True
        except Exception as e:
            logger.error(f"Failed to delete user: {e}")
            raise 