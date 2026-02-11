class payment:
    def __init__ (self, payment_id, booking_id, amount, method, status, timestamp):
        self.payment_id = payment_id
        self.booking_id = booking_id
        self.amount = amount
        self.method = method
        self.status = status
        self.timestamp = timestamp

    def display_info(self):
        print('Payment Information:')
        print('Payment ID: ' + str(self.payment_id))
        print('Booking ID: ' + str(self.booking_id))
        print('Amount: $' + str(self.amount))
        print('Method: ' + self.method)
        print('Status: ' + self.status)
        print('Timestamp: ' + self.timestamp)
    
    def get_payment_id(self):
        return self.payment_id
    
    def get_booking_id(self):
        return self.booking_id
    
    def get_amount(self):
        return self.amount
    
    def get_method(self):
        return self.method
    
    def get_status(self):
        return self.status
    
    def get_timestamp(self):
        return self.timestamp
    
    def set_status(self, new_status):
        self.status = new_status
        print('Payment status updated to: ' + self.status)

    def set_method(self, new_method):
        self.method = new_method
        print('Payment method updated to: ' + self.method)
    
    def change_amount(self, new_amount):
        self.amount = new_amount
        print('Payment amount changed to: £' + str(self.amount))
    
    def change_timestamp(self, new_timestamp):
        self.timestamp = new_timestamp
        print('Payment timestamp changed to: ' + self.timestamp)
    
    def add_fee(self, additional_fee):
        self.amount = self.amount + additional_fee
        print('Payment amount increased by £' + str(additional_fee) + '. New amount is £' + str(self.amount) + '.')

    def remove_fee(self, fee_to_remove):
        if fee_to_remove <= self.amount:
            self.amount = self.amount - fee_to_remove
            print('Payment amount reduced by £' + str(fee_to_remove) + '. New amount is £' + str(self.amount) + '.')
        else:
            print('Cannot remove fee, as it is greater than current amount.')
    
    