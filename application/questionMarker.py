def analyse_answers(user_answer, mark_scheme, orderRequired):
    """
    [[["small cells", "tiny cells"], ["cell wall", "cell membrane"]], [["nucleus"], ["DNA", "genetic material"]]]

    In correctPhrases and orderRequired is FALSE:
    ("small cells" OR "tiny cells") AND ("cell wall" OR "cell membrane") IN ONE SENTENCE
    ("nucleus") AND ("DNA" OR "genetic material") IN ONE SENTENCE

    CASE WILL NOT BE ACCOUNTED FOR
    """
    maximum_marks = len(mark_scheme)
    print(maximum_marks)
    actual_marks = mark_answer(user_answer, mark_scheme)

    print("Marks:", actual_marks, " out of ", maximum_marks)
    return actual_marks, maximum_marks


def mark_answer(user_answer, mark_scheme):
    actual_marks = 0

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
                found_sentence_set = sentence_set
                progress = False
                break

        if progress:
            found_sentence_set = None

    return actual_marks


def test_analyse_answers():
    answer = [[["bacteria cell is smaller", "bacteria cells are smaller","plant cell is larger", "plant cells are larger"]],[["plant cells have chloroplasts","plant cell has chloroplast"]],[["plant cells have vacuole","plant cell has vacuole"]],[["bacteria cells have slime capsules","bacteria cell has slime capsule"]],[["bacteria cells have flagella","bacteria cell has flagellum"]],[["plant cells have nucleus","plant cell has nucleus","bacteria cells have no nucleus","bacteria cell has no nucleus"]],[["cell wall"],["plant"],["cellulose"]],[["bacteria cells have plasmid DNA","bacteria cell has plasmid DNA"]]]
    assert (analyse_answers("They are small cells with a cell membrane. They have a nucleus with DNA in it.", answer, False) == (0, 8))
    answer = [[["stores","contains"],["DNA","genetic material"]],[["controls"],["activities","what the cell does"]]]
    assert (analyse_answers("The nucleus controls the cell's activities. It contains DNA.", answer, False) == (1, 2))
    answer = [[["small", "tiny"], ["cell wall", "cell membrane"]], [["nucleus"], ["DNA", "genetic material"]]]
    assert (analyse_answers("The cells are small and have cell membrane. The cells are small. The cell's nucleus contain DNA.", answer, False) == (2, 2))
    answer = [[["small", "tiny"], ["cell wall", "cell membrane"]], [["nucleus"], ["DNA", "genetic material"]]]
    assert (analyse_answers("The cells are small and have cell membrane. The cells are small and have cell membrane.", answer, False) == (1, 2))
