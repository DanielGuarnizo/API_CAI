from sqlmodel import Session, create_engine, select

from app import crud
from app.core.config import settings
from app.core.init_example_templates import (
    create_example_template_exercise,
    create_example_template_workout,
)
from app.models import TemplateWorkout, User, UserCreate

# handcraft url
# URL_DATABASE = "postgresql://1605@localhost:5432/app"
# engine = create_engine(URL_DATABASE)

engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))


# make sure all SQLModel models are imported (app.models) before initializing DB
# otherwise, SQLModel might fail to initialize relationships properly
# for more details: https://github.com/tiangolo/full-stack-fastapi-template/issues/28


def init_db(session: Session) -> None:
    # Tables should be created with Alembic migrations
    # But if you don't want to use migrations, create
    # the tables un-commenting the next lines
    # from sqlmodel import SQLModel

    # from app.core.engine import engine
    # This works because the models are already imported and registered from app.models
    # SQLModel.metadata.create_all(engine)

    user = session.exec(
        select(User).where(User.email == settings.FIRST_SUPERUSER)
    ).first()

    if not user:
        user_in = UserCreate(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )
        user = crud.create_user(session=session, user_create=user_in)

        # % Initilize base workout which will containt all the existing exercises of the application
        db_base = TemplateWorkout(user_id=user.id, workout_name="Base")
        base = crud.create_template_workout(
            session=session, db_template_workout=db_base
        )

        # % All the existing exercises
        # Exercises legs
        squat_legs_barbell = create_example_template_exercise(
            session=session,
            template_workout_id=base.template_workout_id,
            name_exercise="Squat",
            muscle_group="Legs",
            category="Barbell",
        )
        legExtention_legs_barbell = create_example_template_exercise(
            session=session,
            template_workout_id=base.template_workout_id,
            name_exercise="Leg Extention",
            muscle_group="Legs",
            category="Machine",
        )
        StandingCalfRaise_legs_barbell = create_example_template_exercise(
            session=session,
            template_workout_id=base.template_workout_id,
            name_exercise="Standing Calf Raise",
            muscle_group="Legs",
            category="Dumbell",
        )

        # @ Initialise Example Workouts

        # Example workout Legs
        db_example_workout = TemplateWorkout(
            user_id=user.id,
            workout_name="Example Legs",
        )
        example_legs = crud.create_template_workout(
            session=session, db_template_workout=db_example_workout
        )
        create_example_template_workout(
            session=session,
            template_workout_id=example_legs.template_workout_id,
            order=1,
            example_exercise=squat_legs_barbell,
        )
        create_example_template_workout(
            session=session,
            template_workout_id=example_legs.template_workout_id,
            order=2,
            example_exercise=StandingCalfRaise_legs_barbell,
        )
        create_example_template_workout(
            session=session,
            template_workout_id=example_legs.template_workout_id,
            order=3,
            example_exercise=legExtention_legs_barbell,
        )
