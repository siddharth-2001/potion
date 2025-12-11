from sqlalchemy.orm import Session
from app.models.user import User

class UserRepository:

    def __init__(self, session: Session):
        self.session = session

    def create_user(self, first_name: str, last_name: str, email: str, hashed_password: str) -> User:

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            email=email,
            hashed_password=hashed_password
        )
        self.session.add(new_user)
        self.session.commit()
        self.session.refresh(new_user)
        return new_user
    
    def get_user_by_email(self, email: str) -> User | None:
        return self.session.query(User).filter(User.email == email).first()

    def get_user_by_id(self, user_id: str) -> User | None:
        return self.session.query(User).filter(User.id == user_id).first()
    
    def change_password(self, user: User, new_password: str) -> None:
        user.hashed_password = new_password
        self.session.commit()
