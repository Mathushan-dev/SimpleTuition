class booking:
    def __init__ (self, booking_id, user_id, teacher_id, subject_id, date, time, booking_status, admin_notes):
        self.booking_id = booking_id
        self.user_id = user_id
        self.teacher_id = teacher_id
        self.subject_id = subject_id
        self.date = date
        self.time = time
        self.booking_status = booking_status
        self.admin_notes = admin_notes

    def display_info(self):
        print('Booking Information:')
        print('Booking ID: ' + str(self.booking_id))
        print('User ID: ' + str(self.user_id))
        print('Teacher ID: ' + str(self.teacher_id))
        print('Subject ID: ' + str(self.subject_id))
        print('Date: ' + self.date)
        print('Time: ' + self.time)
        print('Booking Status: ' + self.booking_status)
        print('Admin Notes: ' + self.admin_notes)
    
    def get_booking_id(self):
        return self.booking_id
    
    def get_user_id(self):
        return self.user_id
    
    def get_teacher_id(self):
        return self.teacher_id
    
    def get_subject_id(self):
        return self.subject_id
    
    def get_date(self):
        return self.date
    
    def get_time(self):
        return self.time
    
    def get_booking_status(self):
        return self.booking_status
    
    def get_admin_notes(self):
        return self.admin_notes
    
    def set_booking_status(self, new_status):
        self.booking_status = new_status
        print('Booking status updated to: ' + self.booking_status)

    def set_admin_notes(self, new_notes):
        self.admin_notes = new_notes
        print('Admin notes updated to: ' + self.admin_notes)

    def change_date(self, new_date):
        self.date = new_date
        print('Booking date changed to: ' + self.date)

    def change_time(self, new_time):
        self.time = new_time
        print('Booking time changed to: ' + self.time)
    
    def change_teacher(self, new_teacher_id):
        self.teacher_id = new_teacher_id
        print('Booking teacher changed to: ' + str(self.teacher_id))
    
    def change_subject(self, new_subject_id):
        self.subject_id = new_subject_id
        print('Booking subject changed to: ' + str(self.subject_id))
    
    def change_user(self, new_user_id):
        self.user_id = new_user_id
        print('Booking user changed to: ' + str(self.user_id))

    def cancel_booking(self):
        self.booking_status = 'Cancelled'
        print('Booking cancelled successfully.')

    def confirm_booking(self):
        self.booking_status = 'Confirmed'
        print('Booking confirmed successfully.')
    
    def reschedule_booking(self, new_date, new_time):
        self.date = new_date
        self.time = new_time
        print('Booking rescheduled to: ' + self.date + ' at ' + self.time)
    
    def add_admin_notes(self, notes):
        self.admin_notes = self.admin_notes + ' | ' + notes
        print('Admin notes added: ' + self.admin_notes)

    def remove_admin_notes(self):
        self.admin_notes = ''
        print('Admin notes removed.')

    