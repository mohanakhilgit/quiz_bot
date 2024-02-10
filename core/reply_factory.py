
from .constants import BOT_WELCOME_MESSAGE, PYTHON_QUESTION_LIST


def generate_bot_responses(message, session):
    bot_responses = []

    current_question_id = session.get("current_question_id")
    if not current_question_id and current_question_id != 0:
        bot_responses.append(BOT_WELCOME_MESSAGE)

    success, error = record_current_answer(message, current_question_id, session)

    if not success:
        return [error]

    next_question, next_question_id = get_next_question(current_question_id)

    if next_question:
        bot_responses.append(next_question)
    else:
        final_response = generate_final_response(session)
        bot_responses.append(final_response)

    session["current_question_id"] = next_question_id
    session.save()

    return bot_responses


def record_current_answer(answer, current_question_id, session):
    '''
    Validates and stores the answer for the current question to django session.
    '''
    if current_question_id or current_question_id == 0:
        if answer == PYTHON_QUESTION_LIST[current_question_id]["answer"]:
            answer = 'correct'
        else:
            answer = 'wrong'
        session["message_history"].append({"answer_dict": {"question_id": current_question_id, "answer": answer}})
        
    return True, ""


def get_next_question(current_question_id):
    '''
    Fetches the next question from the PYTHON_QUESTION_LIST based on the current_question_id.
    '''
    if current_question_id or current_question_id == 0:
        next_question_id = current_question_id + 1
        if next_question_id < len(PYTHON_QUESTION_LIST):
            question = PYTHON_QUESTION_LIST[next_question_id]['question_text']
            options = PYTHON_QUESTION_LIST[next_question_id]['options']
            return f"Question: {question}\nOptions: \n{options}", next_question_id
        else:
            return None, None
    else:
        question = PYTHON_QUESTION_LIST[0]['question_text'], 
        options = PYTHON_QUESTION_LIST[0]['options']
        return f"Question: {question}\nOptions: \n{options}", 0


def generate_final_response(session):
    '''
    Creates a final result message including a score based on the answers
    by the user for questions in the PYTHON_QUESTION_LIST.
    '''
    score = 0
    for message_dict in session["message_history"]:
        if message_dict.get("answer_dict"):
            if message_dict["answer_dict"]["answer"] == "correct":
                score += 1
    return f"You scored {score} out of {len(PYTHON_QUESTION_LIST)}."
