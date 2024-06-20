
################### da@gmail.com user
#Create User
# curl -X 'POST' \
#   'http://localhost/api/v1/login/register' \
#   -H 'accept: application/json' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "email": "da@gmail.com",
#   "is_active": true,
#   "is_superuser": false,
#   "full_name": "string",
#   "number_of_workouts": 0,
#   "password": "987654"
# }'

#################### create objects

# #Create TemplateWorkout
# curl -X 'POST' \
#   'http://localhost/api/v1/templates/workouts' \
#   -H 'accept: application/json' \
#   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNjkzNjgsInN1YiI6IjIifQ.Xo2UCW29V-_Mrq9JbK5xw7yte-xfI7IrvorrtbmJCxM' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "workout_name": "Full Body",
#   "last_date": "2024-05-25T08:28:15.523Z",
#   "template_exercises": [
#     {
#       "template_exercise_id": 0,
#       "template_workout_id": 0,
#       "order": 1,
#       "name_exercise": "Squat",
#       "muscle_group": "Legs",
#       "category": "Barbell"
#     },
#     {
#       "template_exercise_id": 0,
#       "template_workout_id": 0,
#       "order": 2,
#       "name_exercise": "Leg Extention",
#       "muscle_group": "Legs",
#       "category":"Machine"
#     },
#     {
#       "template_exercise_id": 0,
#       "template_workout_id": 0,
#       "order": 3,
#       "name_exercise": "PullUp Band",
#       "muscle_group": "Back",
#       "category": "Body Weight"
#     }
#   ]
# }'

# #Create TemplateExercise
# curl -X 'POST' \
#   'http://localhost/api/v1/templates/exercises' \
#   -H 'accept: application/json' \
#   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNjkzNjgsInN1YiI6IjIifQ.Xo2UCW29V-_Mrq9JbK5xw7yte-xfI7IrvorrtbmJCxM' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "name_exercise": "Lat Pull Down",
#   "muscle_group": "Back",
#   "category": "Barbell"
# }'


# #Create Workout
# curl -X 'POST' \
#   'http://localhost/api/v1/history/workouts' \
#   -H 'accept: application/json' \
#   -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNjkzNjgsInN1YiI6IjIifQ.Xo2UCW29V-_Mrq9JbK5xw7yte-xfI7IrvorrtbmJCxM' \
#   -H 'Content-Type: application/json' \
#   -d '{
#   "template_workout_id": 4,
#   "workout_name": "Full Body",
#   "date": "2023-05-27T00:00:00Z",
#   "duration": 5000.0,
#   "volume": 1000,
#   "records": 5,
#   "exercises": [
#     {
#       "template_exercise_id": 7,
#       "exercise_name": "Squat",
#       "muscle_group": "Legs",
#       "category": "Barbell",
#       "sets": [
#         {
#           "kg": 100,
#           "repetitions": 10,
#           "type_rep": 1
#         },
#         {
#           "kg": 100,
#           "repetitions": 8,
#           "type_rep": 1
#         }
#       ]
#     },
#     {
#       "template_exercise_id": 8,
#       "exercise_name": "Leg Extension",
#       "muscle_group": "Legs",
#       "category": "Machine",
#       "sets": [
#         {
#           "kg": 50,
#           "repetitions": 12,
#           "type_rep": 1
#         },
#         {
#           "kg": 50,
#           "repetitions": 10,
#           "type_rep": 1
#         }
#       ]
#     }
#   ]
# }'

#Create Workout
curl -X 'POST' \
  'http://localhost/api/v1/history/workouts' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNjkzNjgsInN1YiI6IjIifQ.Xo2UCW29V-_Mrq9JbK5xw7yte-xfI7IrvorrtbmJCxM' \
  -H 'Content-Type: application/json' \
  -d '{
  "template_workout_id": 2,
  "workout_name": "Example Legs Workout",
  "date": "2024-05-27T12:41:27.323Z",
  "duration": 5040,
  "volume": 1500,
  "records": 5,
  "exercises": [
    {
      "template_exercise_id": 4,
      "exercise_name": "Squat",
      "muscle_group": "Legs",
      "category": "Barbell",
      "sets": [
        {
          "kg": 100,
          "repetitions": 10,
          "type_rep": 1
        },
        {
          "kg": 90,
          "repetitions": 8,
          "type_rep": 1
        }
      ]
    },
    {
      "template_exercise_id": 5,
      "exercise_name": "Standing Calf Raise",
      "muscle_group": "Legs",
      "category": "Dumbbell",
      "sets": [
        {
          "kg": 50,
          "repetitions": 15,
          "type_rep": 1
        },
        {
          "kg": 45,
          "repetitions": 12,
          "type_rep": 1
        }
      ]
    },
    {
      "template_exercise_id": 6,
      "exercise_name": "Leg Extension",
      "muscle_group": "Legs",
      "category": "Machine",
      "sets": [
        {
          "kg": 70,
          "repetitions": 12,
          "type_rep": 1
        },
        {
          "kg": 65,
          "repetitions": 10,
          "type_rep": 1
        }
      ]
    }
  ]
}'

#Create Workout
curl -X 'POST' \
  'http://localhost/api/v1/history/workouts' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNjkzNjgsInN1YiI6IjIifQ.Xo2UCW29V-_Mrq9JbK5xw7yte-xfI7IrvorrtbmJCxM' \
  -H 'Content-Type: application/json' \
  -d '{
  "template_workout_id": 4,
  "workout_name": "Full Body Workout",
  "date": "2024-05-27T12:41:27.323Z",
  "duration": 4080,
  "volume": 2000,
  "records": 6,
  "exercises": [
    {
      "template_exercise_id": 7,
      "exercise_name": "Squat",
      "muscle_group": "Legs",
      "category": "Barbell",
      "sets": [
        {
          "kg": 100,
          "repetitions": 10,
          "type_rep": 1
        },
        {
          "kg": 90,
          "repetitions": 8,
          "type_rep": 1
        }
      ]
    },
    {
      "template_exercise_id": 8,
      "exercise_name": "Leg Extension",
      "muscle_group": "Legs",
      "category": "Machine",
      "sets": [
        {
          "kg": 70,
          "repetitions": 12,
          "type_rep": 1
        },
        {
          "kg": 65,
          "repetitions": 10,
          "type_rep": 1
        }
      ]
    }
  ]
}
'

#Create TemplateWorkout
curl -X 'POST' \
  'http://localhost/api/v1/templates/workouts' \
  -H 'accept: application/json' \
  -H 'Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MTgzNjkzNjgsInN1YiI6IjIifQ.Xo2UCW29V-_Mrq9JbK5xw7yte-xfI7IrvorrtbmJCxM' \
  -H 'Content-Type: application/json' \
  -d '{
  "workout_name": "Push 2",
  "template_exercises": [
    {
      "template_exercise_id": 1,
      "template_workout_id": 1,
      "order": 1,
      "name_exercise": "Bench Press2",
      "muscle_group": "Chest",
      "category": "Barbell"
    },
    {
      "template_exercise_id": 2,
      "template_workout_id": 1,
      "order": 2,
      "name_exercise": "Overhead Press2",
      "muscle_group": "Shoulders",
      "category": "Barbell"
    },
    {
      "template_exercise_id": 3,
      "template_workout_id": 1,
      "order": 3,
      "name_exercise": "Tricep Dips2",
      "muscle_group": "Triceps",
      "category": "Bodyweight"
    }
  ]
}'
