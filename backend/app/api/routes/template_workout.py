from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import and_, or_, select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
)
from app.models import Message, TemplateExercise, TemplateWorkout, TemplateWorkoutCreate

router = APIRouter()


@router.post("/templates/workouts")
def create_template_workout(
    *,
    session: SessionDep,
    current_user: CurrentUser,
    template_workout_in: TemplateWorkoutCreate,
) -> Any:
    "Create new Template"
    print("ENTER IN THE CREATE TEMPLATE FUNCTION")

    # Validate template to send model to database
    db_template_workout = TemplateWorkout(
        user_id=current_user.id,
        workout_name=template_workout_in.workout_name,
        template_exercises=[],
    )

    # Save model into the database and refresh to get the template_id
    template = crud.create_template_workout(
        session=session, db_template_workout=db_template_workout
    )

    print(template)

    # validate exercises for template
    for exe in template_workout_in.template_exercises:
        if exe.template_workout_id == crud.get_base_template_workout_id_by_user_id(
            session=session, user_id=current_user.id
        ):
            # We need to create a TemplaeExercise given that in the new TemplateWorkout the user add a new Exercises that is not present in the list
            db_exercise = TemplateExercise(
                template_workout_id=exe.template_workout_id,
                order=exe.order,
                name_exercise=exe.name_exercise,
                muscle_group=exe.muscle_group,
                category=exe.category,
            )
            _ = crud.create_template_exercise(session=session, db_exercise=db_exercise)

        else:
            db_exercise = TemplateExercise(
                template_workout_id=template.template_workout_id,
                order=exe.order,
                name_exercise=exe.name_exercise,
                muscle_group=exe.muscle_group,
                category=exe.category,
            )
            _ = crud.create_template_exercise(session=session, db_exercise=db_exercise)
            # print(exercise)

    return Message(message="Template created succesfuly")


@router.delete("/templates/workouts/{template_workout_id}")
def delete_template_workout(
    session: SessionDep, current_user: CurrentUser, template_workout_id: int
) -> Message:
    template_workout = session.get(TemplateWorkout, template_workout_id)
    print(template_workout)

    if not template_workout:
        raise HTTPException(status_code=404, detail="Template Workout not found")
    elif template_workout.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permitions")
    session.delete(template_workout)
    session.commit()
    return {"message": "Template Workout was deleted succesfully"}


@router.get("/templates/workouts")
def get_templates_workouts(session: SessionDep, current_user: CurrentUser) -> Any:
    # Select template_workout_id of base workouts or custume workouts of the user
    print("THIS IS THE ID OF THE CURRENT USER: /templates/workouts")
    print(current_user.id)
    statement = select(TemplateWorkout).where(
        or_(
            and_(TemplateWorkout.user_id == 1, TemplateWorkout.workout_name != "Base"),
            and_(
                TemplateWorkout.user_id == current_user.id,
                TemplateWorkout.workout_name != "Base",
            ),
        )
    )
    workouts = session.exec(statement).all()
    # print(workouts)

    result = []
    # Select TemplatesExercises that has template_workout_id in the previosu result values
    for workout in workouts:
        statement = select(TemplateExercise).where(
            TemplateExercise.template_workout_id == workout.template_workout_id
        )
        exercises = session.exec(statement).all()
        workout_dict = workout.dict()
        workout_dict["template_exercises"] = exercises
        result.append(workout_dict)

    print(result)
    return result
