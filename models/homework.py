class homework:
    def __init__ (self, homework_id, teacher_id, subject_id, assigned_date, due_date, questions, answer_key):
        self.homework_id = homework_id
        self.teacher_id = teacher_id
        self.subject_id = subject_id
        self.assigned_date = assigned_date
        self.due_date = due_date
        self.questions = questions
        self.answer_key = answer_key

    def display_info(self):
        print('Homework Information:')
        print('Homework ID: ' + str(self.homework_id))
        print('Teacher ID: ' + str(self.teacher_id))
        print('Subject ID: ' + str(self.subject_id))
        print('Assigned Date: ' + self.assigned_date)
        print('Due Date: ' + self.due_date)
        print('Questions: ' + ', '.join(self.questions))
        print('Answer Key: ' + ', '.join(self.answer_key))
    
    def get_homework_id(self):
        return self.homework_id
    
    def get_teacher_id(self):
        return self.teacher_id
    
    def get_subject_id(self):
        return self.subject_id
    
    def get_assigned_date(self):
        return self.assigned_date
    
    def get_due_date(self):
        return self.due_date
    
    def get_questions(self):
        return self.questions
    
    def get_answer_key(self):
        return self.answer_key
    
    def set_due_date(self, new_due_date):
        self.due_date = new_due_date
        print('Due date updated to: ' + self.due_date)
    
    def add_question(self, question):
        if question not in self.questions:
            self.questions.append(question)
            print('Question added successfully.')
        else:
            print('Question already exists.')

    def remove_question(self, question):
        if question in self.questions:
            self.questions.remove(question)
            print('Question removed successfully.')
        else:
            print('Question does not exist.')

    def update_answer_key(self, question, answer):
        if question in self.questions:
            index = self.questions.index(question)
            self.answer_key[index] = answer
            print('Answer key updated successfully.')
        else:
            print('Question not found in homework.')
    
    def display_answer_key(self):
        print('Answer Key:')
        for question, answer in zip(self.questions, self.answer_key):
            print(f'Question: {question} - Answer: {answer}')

    def change_questions(self, new_questions):
        self.questions = new_questions
        print('Questions updated successfully.')

    def change_answer_key(self, new_answer_key):
        if len(new_answer_key) == len(self.questions):
            self.answer_key = new_answer_key
            print('Answer key updated successfully.')
        else:
            print('Error: Answer key length does not match number of questions.')

    def change_assigned_date(self, new_assigned_date):
        self.assigned_date = new_assigned_date
        print('Assigned date changed to: ' + self.assigned_date)

    def change_teacher(self, new_teacher_id):
        self.teacher_id = new_teacher_id
        print('Teacher ID changed to: ' + str(self.teacher_id))
    
    def change_subject(self, new_subject_id):
        self.subject_id = new_subject_id
        print('Subject ID changed to: ' + str(self.subject_id))
    
    def change_homework_id(self, new_homework_id):
        self.homework_id = new_homework_id
        print('Homework ID changed to: ' + str(self.homework_id))

    def cancel_homework(self):
        print('Homework cancelled successfully.')
        self.questions = []
        self.answer_key = []
        self.due_date = ''
        self.assigned_date = ''
        print('All homework details cleared.')
    
    