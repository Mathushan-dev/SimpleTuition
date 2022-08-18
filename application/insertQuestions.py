#INSERT INTO questions (id, question, keywords, exam_id)
#VALUES (1, 'What is a cell?', '[[["small cells", "tiny cells"], ["cell wall", "cell membrane"]], [["nucleus"], ["DNA", "genetic material"]]]', 1);

with open("/Users/mathushanmathiyalagan/Downloads/niru.tsv") as file:
    lines = file.readlines()
    lines = [line.rstrip() for line in lines]

sqlQuery = "INSERT INTO questions (id, question, keywords, exam_id)\nVALUES\n"
questionId = 0
for line in lines:
    if questionId != 0: #To exclude column names
        lineSplit = line.split("\t")
        exam_id = lineSplit[0]
        question = lineSplit[1]
        markScheme = lineSplit[2]
        sqlQuery += "(" + str(questionId) + ", \'" + question + "\', \'" + markScheme + "\', \'" + exam_id + "\'),\n"
    questionId += 1

print(sqlQuery)
