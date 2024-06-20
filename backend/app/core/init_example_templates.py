from sqlmodel import Session

from app import crud
from app.models import TemplateExercise


def create_example_template_workout(
    *,
    session: Session,
    template_workout_id: int,
    order: int,
    example_exercise: TemplateExercise,
):
    # copy and modify the template_workout_id of the existing exercise
    db_exercise = TemplateExercise(
        template_workout_id=template_workout_id,
        order=order,
        name_exercise=example_exercise.name_exercise,
        muscle_group=example_exercise.muscle_group,
        category=example_exercise.category,
    )

    print("THIS IS THE COPY OF THE EXERCISE")
    print(db_exercise)

    # save that exercise in the database
    _ = crud.create_template_exercise(session=session, db_exercise=db_exercise)
    return


def create_example_template_exercise(
    *,
    session: Session,
    template_workout_id: int,
    name_exercise: str,
    muscle_group: str,
    category: str,
) -> TemplateExercise:
    # Exercises legs
    db_exercise = TemplateExercise(
        template_workout_id=template_workout_id,
        order=0,
        name_exercise=name_exercise,
        muscle_group=muscle_group,
        category=category,
    )
    result = crud.create_template_exercise(session=session, db_exercise=db_exercise)
    return result
