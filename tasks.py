from cloud_env.graders import grade_easy, grade_medium, grade_hard


TASKS = [
    {
        "name": "easy",
        "grader": grade_easy
    },
    {
        "name": "medium",
        "grader": grade_medium
    },
    {
        "name": "hard",
        "grader": grade_hard
    }
]