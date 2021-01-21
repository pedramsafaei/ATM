class Bank:
    def __init__(self):
        self.bank_data = {}

    def add_card(self, card_num, PIN, account, money):
        self.bank_data[card_num] = {"pin": PIN, "account": {account: money}}

    def account_exist(self, card_num, account):
        if account not in self.bank_data[card_num]["account"]:
            return False
        return True

    def add_account(self, card_num, account, money):
        if card_num in self.bank_data:
            self.bank_data[card_num]["account"][account] = money

    def update_account(self, card_num, account, money):
        if (
            self.bank_data[card_num]["account"][account]
            in self.bank_data[card_num]["account"]
        ):
            self.bank_data[card_num]["account"][account] = money
        else:
            self.add_account(card_num, account, money)

    def check_pin(self, card_num, entered_pin):
        if (
            card_num in self.bank_data
            and self.bank_data[card_num]["pin"] == entered_pin
        ):
            return self.bank_data[card_num]["account"]
        else:
            return None


class Controller:
    def __init__(self, bank, cash):
        self.Bank = bank
        self.accounts = None
        self.cash_bin = cash

    def insert_card(self, card_num, pin):
        self.accounts = self.Bank.check_pin(card_num, pin)
        if not self.accounts:
            return False, "Please re-enter the PIN"
        else:
            return True, "welcome Customer"

    def account_actions(self, card_num, acc, action, amt=0):
        if action == "Check Balance":
            return self.accounts[acc], 1
        elif action == "Withdraw":
            if self.accounts[acc] >= amt and self.cash_bin >= amt:
                self.accounts[acc] = self.accounts[acc] - amt
                self.Bank.update_account(card_num, acc, self.accounts[acc])
                return self.accounts[acc], 1
            else:
                return self.accounts[acc], 0
        elif action == "Deposit":
            self.cash_bin += amt
            self.accounts[acc] = self.accounts[acc] + amt
            self.Bank.update_account(card_num, acc, self.accounts[acc])
            return self.accounts[acc], 1
        else:
            return self.accounts[acc], 2

    def __call__(self, card_num, pin, acc, action_list):
        customer_leave = False
        while not customer_leave:

            valid, notif = self.insert_card(card_num, pin)
            if not valid:
                return notif

            check = self.Bank.account_exist(card_num, acc)
            if not check:
                return "Not a valid Account!"

            for action in action_list:
                if action[0] == "Leave":
                    break
                balance, msg = self.account_actions(card_num, acc, action[0], action[1])
                if msg == 2:
                    return "Invalid"
            return "Successful"


if __name__ == "__main__":

    test_bank = Bank()
    test_bank.add_card(439967, 1234, "checking", 1000)
    test_bank.add_account(222444, "saving", 223)
    test_bank.add_card(95555, 7321, "checking", 24889)
    atm = Controller(test_bank, 100)
    action_list1 = [
        ("Check Balance", 0),
        ("Withdraw", 40),
        ("Withdraw", 1000),
        ("Deposit", 100),
    ]
    print("Test")
    print(atm(95555, 7321, "checking", action_list1))