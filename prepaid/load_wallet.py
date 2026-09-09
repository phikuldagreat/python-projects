class LoadWallet:
    def __init__(self, owner_name, mobile_number, starting_balance):
        self.owner_name = owner_name
        self.mobile_number = mobile_number
        self.starting_balance = starting_balance
    
    def top_up(self):
        self.amount = float(input("Enter Amount to Top Up: "))
        self.starting_balance += self.amount
        print(f"New Balance: {self.starting_balance}")
        
    def send_load(self):
        pass
    
    def show_balance(self):
        pass
        
    def send_with_fee(self):
        pass
        