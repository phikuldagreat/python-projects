from load_wallet import LoadWallet

class PrepaidService:
    def main(self):
        self.owner_name = input("Enter owner name: ")
        self.mobile_number = input("Enter mobile number: ")
        self.starting_balance = float(input("Enter starting balance: "))
        
        print("\n---- MENU -----")
        print("1. Top up Load")
        print("2. Send Load (same network)")
        print("3. Send Load (other network, with fee)")
        print("4. Show Balance")
        print("5. Exit")
        
        wallet = LoadWallet(self.owner_name, self.mobile_number, self.starting_balance)
        
        while True:
            user_choice = int(input("\nEnter your choice (1-5): "))
            
            if user_choice == 1:
                wallet.top_up()
            elif user_choice == 2:
                wallet.send_load()
            elif user_choice == 3:
                wallet.send_with_fee()
            elif user_choice == 4:
                wallet.show_balance()
            elif user_choice == 5:
                print("Thank you. Goodbye.")
                break
            else:
                print("Please enter a number from 1-5.")

if __name__ == "__main__":
    PrepaidService = PrepaidService()
    PrepaidService.main()