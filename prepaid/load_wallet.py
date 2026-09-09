<<<<<<< HEAD
class LoadWallet:
    def __init__(self, owner_name, mobile_number, balance):
        self.owner_name = owner_name
        self.mobile_number = mobile_number
        self.balance = balance
    
    def top_up(self):
        amount = float(input("\nEnter Amount to Top Up: "))
        self.balance += amount
        print(f"New Balance: {self.balance}")
        
    def send_load(self):
        amount = float(input("Enter amount to send: "))
        if self.balance >= amount:
            self.balance -= amount
            print(f"\nLoad sent. New balance: {self.balance}")
        else:
            print("Insufficient balance, please top up.")
    
    def show_balance(self):
        print(f"Owner: {self.owner_name}")
        print(f"Mobile Number: {self.mobile_number}")
        print(f"Balance: {self.balance}")
        
    def send_with_fee(self):
        fee = 12.2
        amount = float(input("Enter amount to send: "))
        total_amount = amount + fee
        if self.balance >= total_amount:
            self.balance -= total_amount
            print(f"Load sent with PHP{fee} fee. New balance: {self.balance}")
        else:
            print("Insufficient balance, please top up.")
        
        
=======
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
>>>>>>> bec3e1203d79792b0cab7ca30db02df78adc8fda
        