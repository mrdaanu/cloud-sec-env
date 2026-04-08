def grade_action(action, expected):

    if action == expected:
        return 1.0

    elif action != "unknown":
        return 0.5

    return 0.0