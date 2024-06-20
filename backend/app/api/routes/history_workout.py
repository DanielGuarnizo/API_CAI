from typing import Any

from fastapi import APIRouter, HTTPException
from sqlmodel import select

from app import crud
from app.api.deps import (
    CurrentUser,
    SessionDep,
)
from app.models import Exercise, Message, Set, Workout, WorkoutCreate

router = APIRouter()


@router.post("/history/workouts")
def create_history_workout(
    session: SessionDep, current_user: CurrentUser, workout_in: WorkoutCreate
) -> int:
    # Validate workout to send model to the database
    #! THIS VALIDATE PROCES IS DONE BECAUSE WE ARE RECEIVING A JSON OBJECT AND
    #! TO SAVE A DATAMODEL IN THE DATABASE IT SHOULD BE EXACTLY AS THAT DATAMODEL
    #! NOT AS A JSON OBJECT , SO WE HAVE TO CONVERT THE RECEIVING DATA IN THE SPECIFIC DATA MODEL
    db_workout = Workout(
        user_id=current_user.id,
        template_workout_id=workout_in.template_workout_id,
        workout_name=workout_in.workout_name,
        date=workout_in.date,
        duration=workout_in.duration,
        volume=workout_in.volume,
        records=workout_in.records,
    )
    workout = crud.create_workout(session=session, db_workout=db_workout)

    # Validate exercises in the workout to send model on the database
    for exe in workout_in.exercises:
        db_exercise = Exercise(
            workout_id=workout.workout_id,
            template_exercise_id=exe.template_exercise_id,
            exercise_name=exe.exercise_name,
            muscle_group=exe.muscle_group,
            category=exe.category,
        )
        exercise = crud.create_exercise(session=session, db_exercise=db_exercise)

        # Validate sets for exercise
        for set in exe.sets:
            db_set = Set(
                exercise_id=exercise.exercise_id,
                kg=set.kg,
                repetitions=set.repetitions,
                type_rep=set.type_rep,
            )

            set = crud.create_set(session=session, db_set=db_set)

    session.refresh(workout)
    print("THIS IS THE NWE CREATED WORKOUT")
    print(workout.dict())
    return workout.workout_id


@router.delete("/history/workouts/{workout_id}")
def delete_history_workout(
    session: SessionDep, current_user: CurrentUser, workout_id: int
) -> Message:
    "Delete Workout"
    workout = session.get(Workout, workout_id)

    if not workout:
        raise HTTPException(status_code=404, detail="Template Workout not found")
    elif workout.user_id != current_user.id:
        raise HTTPException(status_code=400, detail="Not enough permitions")
    session.delete(workout)
    session.commit()
    return {"message": "Workout was deleted succesfully"}


@router.get("/history/workouts/{user_id}")
def get_history_workouts_by_user_id(
    session: SessionDep, _: CurrentUser, user_id: int
) -> Any:
    # Select history workouts of the user by user_id
    statement = (
        select(Workout).where(Workout.user_id == user_id).order_by(Workout.date.desc())
    )
    history_workouts = session.exec(statement).all()

    # Convert datetime values to ISO 8601 strings
    for workout in history_workouts:
        workout.date = workout.date.isoformat() if workout.date else None

    workouts = []

    # Select History Exercise that has workout_id as the previous workout
    for workout in history_workouts:
        statement = select(Exercise).where(Exercise.workout_id == workout.workout_id)
        history_exercises = session.exec(statement).all()
        history_workout_dict = workout.dict()

        exercises = []
        # Select History Set that has exercise_id as the previous exercise
        for exercise in history_exercises:
            statement = select(Set).where(Set.exercise_id == exercise.exercise_id)
            history_sets = session.exec(statement).all()
            history_sets_dict = exercise.dict()
            history_sets_dict["sets"] = history_sets
            exercises.append(history_sets_dict)

        history_workout_dict["exercises"] = exercises
        workouts.append(history_workout_dict)

    print(workouts)
    return workouts
