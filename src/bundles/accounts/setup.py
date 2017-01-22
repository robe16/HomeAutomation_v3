from bundles.accounts.nest.setup import setup_nest
from bundles.accounts.icloud.setup import setup_icloud


def add_account(data):
    while True:
        #
        print("Add account\n" +
              "1 - Nest\n" +
              "2 - iCloud\n" +
              "e - Exit to previous menu\n")
        #
        input_acc = raw_input("Type the required option number followed by the return key: ")
        print("\n****************************************************************\n")
        #
        if input_acc == 'e':
            #
            return
            #
        elif input_acc == '1' or input_acc == '2':
            #
            if input_acc == '1':
                new_acc = setup_nest()
            elif input_acc == '2':
                new_acc = setup_icloud()
            #
            if new_acc:
                data['accounts'][new_acc['account_id']] = new_acc
                #
                print("\n****************************************************************\n")
                return data
            #
        else:
            #
            print("Invalid entry, please try again!!")
            print("\n****************************************************************\n")
            return data
