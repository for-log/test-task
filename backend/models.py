from utils import generate_random_string
from typing import List
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    token: Mapped[str] = mapped_column(default=lambda: generate_random_string(16))

    records: Mapped[List["Record"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<User {self.email}>'
    

class Record(Base):
    __tablename__ = "record"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id = mapped_column(ForeignKey("user.id"))
    user: Mapped[User] = relationship(back_populates="records")

    datas: Mapped[List["Data"]] = relationship(
        back_populates="record", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f'<Record {self.id}>'
    

class Data(Base):
    __tablename__ = "data"

    id: Mapped[int] = mapped_column(primary_key=True)
    value: Mapped[int] = mapped_column(nullable=False)
    record_id = mapped_column(ForeignKey("record.id"))
    record: Mapped[Record] = relationship(back_populates="datas")

    def __repr__(self):
        return f'<Data {self.id=} {self.value=} {self.record_id=}>'