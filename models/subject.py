class subject:
    def __init__ (self, subject_id, name, duration, fee):
        self.subject_id = subject_id
        self.name = name
        self.duration = duration
        self.fee = fee

    def display_info(self):
        print('Subject Information:')
        print('Subject ID: ' + str(self.subject_id))
        print('Name: ' + self.name)
        print('Duration: ' + str(self.duration) + ' hours')
        print('Fee: $' + str(self.fee))

    def get_subject_id(self):
        return self.subject_id 
    
    def get_name(self):
        return self.name
    
    def get_duration(self):
        return self.duration
    
    def get_fee(self):
        return self.fee
    
    def set_duration(self, new_duration):
        self.duration = new_duration
        print('Duration updated successfully.')

    def set_fee(self, new_fee):
        self.fee = new_fee
        print('Fee updated successfully.')
    
    def set_name(self, new_name):
        self.name = new_name
        print('Name updated successfully.')
    
    def add_fee(self, additional_fee):
        self.fee = self.fee + additional_fee
        print('Fee increased by £' + str(additional_fee) + '. New fee is £' + str(self.fee) + '.')

    def remove_fee(self, fee_to_remove):
        if fee_to_remove <= self.fee:
            self.fee = self.fee - fee_to_remove
            print('Fee reduced by £' + str(fee_to_remove) + '. New fee is £' + str(self.fee) + '.')
        else:
            print('Cannot remove fee, as it is greater than current fee.')
    
    def change_fee(self, new_fee):
        self.fee = new_fee
        print('Fee changed to £' + str(self.fee) + '.')
   
    def change_duration(self, new_duration):
        self.duration = new_duration
        print('Duration changed to ' + str(self.duration) + ' hours.')


    