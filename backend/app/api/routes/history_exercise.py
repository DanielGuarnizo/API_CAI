from typing import Any

from fastapi import APIRouter
from sqlalchemy.orm import joinedload
from sqlmodel import select

from app.api.deps import (
    CurrentUser,
    SessionDep,
)
from app.models import Exercise, Set, TemplateExercise, Workout

router = APIRouter()


@router.get("/history/exercises/{template_exercise_id}")
def get_history_exercise_by_template_exercise_id(
    session: SessionDep, current_user: CurrentUser, template_exercise_id: int
) -> Any:
    print("THIS IS THE ID OF THE CURRENT USER: history/exericise/")
    print(current_user.id)
    statement = select(Exercise).where(
        Exercise.template_exercise_id == template_exercise_id
    )

    history_exercises = session.exec(statement).all()

    exercises = []
    for exe in history_exercises:
        statement = select(Set).where(Set.exercise_id == exe.exercise_id)
        history_sets = session.exec(statement).all()
        history_sets_dict = exe.dict()
        history_sets_dict["sets"] = history_sets
        exercises.append(history_sets_dict)

    print(exercises)
    return exercises


@router.get("/history/last-exercise/{template_exercise_id}")
def get_last_exercise_by_template_exercise_id(
    session: SessionDep, _: CurrentUser, template_exercise_id: int
) -> Any:
    statement = (
        select(Exercise)
        .join(Workout, Workout.workout_id == Exercise.workout_id)
        .where(Exercise.template_exercise_id == template_exercise_id)
        .order_by(Workout.date.desc())
        .options(joinedload(Exercise.workout))
        .limit(1)
    )

    last_exercise_result = session.exec(statement)
    last_exercise = last_exercise_result.first()  # Get the first result or None

    if not last_exercise:
        print("THERE ISN'T AT LEAST ONE EXERCISE FOR THE GIVEN TEMPLATE EXERCISE ID")
        statement = select(TemplateExercise).where(
            TemplateExercise.template_exercise_id == template_exercise_id
        )
        template_exercise = session.exec(statement).first()
        print(template_exercise)
        return {
            "exercise_id": 0,
            "workout_id": 0,
            "template_exercise_id": template_exercise.template_exercise_id,
            "exercise_name": template_exercise.name_exercise,
            "muscle_group": template_exercise.muscle_group,
            "category": template_exercise.category,
            "sets": [
                {
                    "set_id": 0,
                    "exercise_id": 0,
                    "kg": 0,
                    "repetitions": 0,
                    "type_rep": 0,
                }
            ],
        }

    statement_set = select(Set).where(Set.exercise_id == last_exercise.exercise_id)
    history_sets = session.exec(statement_set).all()
    history_sets_dict = last_exercise.dict()
    history_sets_dict["sets"] = history_sets

    print("THIS IS HISTORY_SETS")
    print(history_sets_dict)
    return history_sets_dict

    # return last_exercise
