from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import or_, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
)
from app.models import Message, TemplateExercise

router = APIRouter()


@router.post("/templates/exercises")
def create_template_exercise(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    template_exercise_in: TemplateExercise,
) -> Any:
    "Create New Template Exercise"

    # Validated template exercise to send to the database
    template_workout_id = crud.get_base_template_workout_id_by_user_id(
        session=session, user_id=current_user.id
    )

    db_template_exercise = TemplateExercise(
        template_workout_id=template_workout_id,
        order=0,
        name_exercise=template_exercise_in.name_exercise,
        muscle_group=template_exercise_in.muscle_group,
        category=template_exercise_in.category,
    )

    template_exercise = crud.create_template_exercise(
        session=session, db_exercise=db_template_exercise
    )
    return template_exercise


@router.delete("/templates/exercises/{template_exercise_id}")
def delete_template_exercise(
    *, session: SessionDep, current_user: CurrentUser, template_exercise_id: int
) -> Message:
    "Delete Template Exercise by id"

    template_exercise = session.get(TemplateExercise, template_exercise_id)

    if not template_exercise:
        raise HTTPException(status_code=404, detail="Template Workout not found")
    elif not crud.get_base_template_workout_id_by_user_id(
        session=session, user_id=current_user.id
    ):
        raise HTTPException(status_code=400, detail="Not enough permitions")
    session.delete(template_exercise)
    session.commit()
    return {"message": "Template Exercise was deleted succesfully"}


@router.get("/template/exercises")
def get_templates_exericise_user(
    *, session: SessionDep, current_user: CurrentUser
) -> Any:
    "Get list of pre existing or custom exercises of the given user"
    statement = select(TemplateExercise).where(
        or_(
            TemplateExercise.template_workout_id == 1,
            TemplateExercise.template_workout_id
            == crud.get_base_template_workout_id_by_user_id(
                session=session, user_id=current_user.id
            ),
        )
    )

    exercises = session.exec(statement).all()
    return exercises
