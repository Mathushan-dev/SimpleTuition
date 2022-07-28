import csv
import ast

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
                        print("Keyword Found: ", keyword)
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
    answer = [[["cell wall"],["cell membrane"],["cytoplasm"]]]
    assert (analyse_answers("cell wall", answer, False) == (0, 1))

# test_analyse_answers()

def automateTest():
    with open('/Users/mathushanmathiyalagan/Downloads/niru.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                print(row[1])
                user_answer = input("Enter your answer below: \n")
                print("***", row[2])
                print(analyse_answers(user_answer, ast.literal_eval(row[2]), False))
                print(row[3], "\n\n\n")
                line_count += 1
        print(f'Processed {line_count} lines.')

automateTest()