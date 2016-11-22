from parsing.States import States


def shit_happens(state):
    give_reply = False

    if state == States.STARTED:
        give_reply = True

    state = States.LISTENING

    return "I feel for you man! Lemme see what I can do.\nSend me a frontal view of the scene.", give_reply, state


def do_nothing(state):
    return "Nothing to do" , False, state


def give_feedback(message, current_state):
    """

    :param message:
    :param current_state:
    :return: [feedback_message_str, should_respond_to_user_bool, new_state ]
    """
    if message == "shit_happens":
        return shit_happens((current_state))
    else:
        return do_nothing(current_state)