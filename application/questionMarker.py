def analyse_answers(user_answer, correct_phrases):
    """
    [["small cells", "tiny cells"], ["cell wall", "cell membrane"]]

    In correctPhrases:
    ("small cells" OR "tiny cells") AND ("cell wall" OR "cell membrane")

    CASE WILL NOT BE ACCOUNTED FOR
    """
    maximum_marks = len(correct_phrases)
    actual_marks = check_keyword_exists(user_answer, correct_phrases)

    print("Marks:", actual_marks, " out of ", maximum_marks)
    return actual_marks, maximum_marks


def check_keyword_exists(user_answer, keyword_list):
    marks = 0

    for phrase_set in keyword_list:
        for phrase in phrase_set:
            if phrase.strip().casefold() in user_answer.casefold():
                marks += 1
                break

    return marks


def test_analyse_answers():
    answer = [["small cells", "tiny cells"], ["cell wall", "cell membrane"]]
    assert (analyse_answers("The small cells have Small Cell walls", answer) == (2, 2))
    assert (analyse_answers("The large cells have Small Cell walls", answer) == (1, 2))
