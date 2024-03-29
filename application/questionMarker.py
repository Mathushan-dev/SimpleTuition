def analyse_answers(user_answer, mark_scheme):
    """
    [[["small cells", "tiny cells"], ["cell wall", "cell membrane"]], [["nucleus"], ["DNA", "genetic material"]]]

    In correctPhrases and orderRequired is FALSE:
    ("small cells" OR "tiny cells") AND ("cell wall" OR "cell membrane") IN ONE SENTENCE
    ("nucleus") AND ("DNA" OR "genetic material") IN ONE SENTENCE

    CASE WILL NOT BE ACCOUNTED FOR
    """
    maximum_marks = len(mark_scheme)
    actual_marks, correct_answers = mark_answer(user_answer, mark_scheme)

    return actual_marks, maximum_marks, correct_answers


def mark_answer(user_answer, mark_scheme):
    actual_marks = 0
    correct_answers = []

    user_answer_sentences = user_answer.split(".")

    found_sentence_set = None

    for sentence_to_check in user_answer_sentences:
        progress = True
        if found_sentence_set is not None:
            mark_scheme.remove(found_sentence_set)
        for sentence_set in mark_scheme:
            actual_keyword_set_marks = 0
            maximum_keyword_set_marks = len(sentence_set)

            for keyword_set in sentence_set:
                for keyword in keyword_set:
                    if keyword in sentence_to_check:
                        actual_keyword_set_marks += 1
                        break

            if actual_keyword_set_marks == maximum_keyword_set_marks:
                actual_marks += 1
                correct_answers.append(sentence_to_check)
                found_sentence_set = sentence_set
                progress = False
                break

        if progress:
            found_sentence_set = None

    return actual_marks, correct_answers
