# User Tables

### User

id
email (unique)
username
password
is_active
date_joined

### User Profile

user_id (FK)
age
gender
height (cm)
weight (kg)
fitness_goal (lose_weight / gain_muscle / maintain)
activity_level

# Workout Tables

### Exercise

id
name
muscle_group (chest, legs, etc.)
equipment (optional)
description

### Workout plan

id
user_id (FK)
name
goal
is_active
created_at

### Workout Session

id
user_id (FK)
date
duration
notes

### Workout Exercise

id
session_id (FK)
exercise_id (FK)
order

### Log

id
workout_exercise_id (FK)
reps
weight
duration (optional)
rest_time

# Biometrics

### Body Stats

id
user_id
weight
body_fat %
date
