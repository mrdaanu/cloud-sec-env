from cloud_env.graders import grade_easy, grade_medium, grade_hard


TASKS = [
    {
        "id": "easy",
        "grader": grade_easy
    },
    {
        "id": "medium",
        "grader": grade_medium
    },
    {
        "id": "hard",
        "grader": grade_hard
    }
]