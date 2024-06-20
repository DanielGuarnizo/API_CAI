from datetime import datetime

from pydantic import BaseModel
from sqlalchemy import Column, Float
from sqlmodel import Field, Relationship, SQLModel

# Shared properties
# TODO replace email str with EmailStr when sqlmodel supports it
# class UserBase(SQLModel):
#     email: str = Field(unique=True, index=True)
#     is_active: bool = True
#     is_superuser: bool = False
#     full_name: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserRegister(SQLModel):
    email: str
    password: str
    full_name: str | None = None


# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdateMe(SQLModel):
    full_name: str | None = None
    email: str | None = None


class UpdatePassword(SQLModel):
    current_password: str
    new_password: str


# Database model, database table inferred from class name
# class User(UserBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     hashed_password: str
#     items: list["Item"] = Relationship(back_populates="owner")


# Shared properties
class ItemBase(SQLModel):
    title: str
    description: str | None = None


# Properties to receive on item creation
class ItemCreate(ItemBase):
    title: str


# Properties to receive on item update
class ItemUpdate(ItemBase):
    title: str | None = None  # type: ignore


# Database model, database table inferred from class name
# class Item(ItemBase, table=True):
#     id: int | None = Field(default=None, primary_key=True)
#     title: str
#     owner_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
#     owner: User | None = Relationship(back_populates="items")


# Properties to return via API, id is always required
class ItemPublic(ItemBase):
    id: int
    owner_id: int


class ItemsPublic(SQLModel):
    data: list[ItemPublic]
    count: int


# Generic message
class Message(SQLModel):
    message: str


# JSON payload containing access token
class Token(SQLModel):
    access_token: str
    token_type: str = "bearer"
    user_id: int


# Contents of JWT token
class TokenPayload(SQLModel):
    sub: int | None = None


class NewPassword(SQLModel):
    token: str
    new_password: str


####################################################### New Code
class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    is_active: bool = True
    is_superuser: bool = False
    full_name: str | None = None
    number_of_workouts: int | None = 0


class User(UserBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    hashed_password: str
    workouts: list["Workout"] = Relationship(
        back_populates="owner_workout",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str


# Properties to receive via API on update, all are optional
# TODO replace email str with EmailStr when sqlmodel supports it
class UserUpdate(UserBase):
    email: str | None = None  # type: ignore
    password: str | None = None


# Properties to return via API, id is always required
class UserPublic(UserBase):
    id: int


class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int


class TemplateWorkout(SQLModel, table=True):
    template_workout_id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    workout_name: str
    template_exercises: list["TemplateExercise"] = Relationship(
        back_populates="template_workout",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class TemplateExercise(SQLModel, table=True):
    template_exercise_id: int | None = Field(default=None, primary_key=True)
    template_workout_id: int | None = Field(
        default=None, foreign_key="templateworkout.template_workout_id", nullable=False
    )
    order: int | None = None
    name_exercise: str
    muscle_group: str
    category: str
    template_workout: TemplateWorkout | None = Relationship(
        back_populates="template_exercises"
    )


class TemplateWorkoutCreate(SQLModel):
    workout_name: str
    template_exercises: list["TemplateExercise"]


class Workout(SQLModel, table=True):
    workout_id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="user.id", nullable=False)
    template_workout_id: int | None = Field(
        default=None, foreign_key="templateworkout.template_workout_id", nullable=False
    )
    workout_name: str
    date: datetime | None
    duration: float = Field(sa_column=Column(Float))
    volume: int
    records: int
    owner_workout: User | None = Relationship(back_populates="workouts")
    exercises: list["Exercise"] = Relationship(
        back_populates="workout",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Exercise(SQLModel, table=True):
    exercise_id: int | None = Field(default=None, primary_key=True)
    workout_id: int | None = Field(
        default=None, foreign_key="workout.workout_id", nullable=False
    )
    template_exercise_id: int | None = Field(
        default=None,
        foreign_key="templateexercise.template_exercise_id",
        nullable=False,
    )
    exercise_name: str
    muscle_group: str
    category: str
    workout: Workout | None = Relationship(back_populates="exercises")
    sets: list["Set"] = Relationship(
        back_populates="exercise",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class Set(SQLModel, table=True):
    set_id: int | None = Field(default=None, primary_key=True)
    exercise_id: int | None = Field(
        default=None, foreign_key="exercise.exercise_id", nullable=False
    )
    kg: int
    repetitions: int
    type_rep: int
    exercise: Exercise | None = Relationship(back_populates="sets")


class SetCreate(BaseModel):
    kg: int
    repetitions: int
    type_rep: int


class ExerciseCreate(BaseModel):
    template_exercise_id: int
    exercise_name: str
    muscle_group: str
    category: str
    sets: list[SetCreate]


class WorkoutCreate(BaseModel):
    template_workout_id: int
    workout_name: str
    date: datetime
    duration: float
    volume: int
    records: int
    exercises: list[ExerciseCreate]


# class TemplateExercise(SQLModel):
#     name_exercise: str
#     muscle_group: str
#     category: str

### pre existing workouts
