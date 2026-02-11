class teacher:  # Defines a class named 'teacher'
    def __init__ (self, teacher_id, name, subjects, availiability):  # Constructor to initialize teacher attributes
        self.teacher_id = teacher_id  # Assigns teacher ID
        self.name = name  # Assigns teacher name
        self.subjects = subjects  # Assigns list of subjects the teacher can teach
        self.availability = availiability  # Assigns teacher availability

    def display_info(self):  # Displays teacher's information
        print('Teacher Information:')  # Prints heading
        print('Teacher ID: ' + str(self.teacher_id))  # Prints teacher ID
        print('Name: ' + str(self.name))  # Prints teacher name
        print('Subjects: ' + ', '.join(self.subjects))  # Prints subjects taught
        print('Availability: ' + ', '.join(self.availability))  # Prints availability times
    
    def get_teacher_id(self):  # Returns teacher ID
        return self.teacher_id
    
    def get_name(self):  # Returns teacher name
        return self.name
    
    def get_subjects(self):  # Returns list of subjects
        return self.subjects
    
    def get_availability(self):  # Returns teacher availability
        return self.availability
    
    def set_availability(self, new_availability):  # Updates teacher availability
        self.availability = new_availability  # Sets new availability
        print('Availability updated successfully.') # Confirm availability update

    def add_subject(self, subject):  # Adds a new subject to the teacher's list
        if subject not in self.subjects:  # Checks if the subject is not already present
            self.subjects.append(subject)  # Adds the new subject
            print('Subject ' + subject + ' added successfully.')  # Confirmation message
        else:
            print('Subject ' + subject + ' already exists.')  # Message if subject already exists
    
    def remove_subject(self, subject):  # Removes a subject from the teacher's list
        if subject in self.subjects:  # Checks if the subject exists
            self.subjects.remove(subject)  # Removes the subject
            print('Subject ' + subject + ' removed successfully.')  # Confirmation message
        else:
            print('Subject ' + subject + ' does not exist.')  # Message if subject doesn't exist