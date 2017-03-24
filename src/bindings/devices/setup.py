from config.bindings.config_bindings import get_cfg_bindings_json, write_config_bindings
from bindings.devices.nest.setup import setup_nest
from bindings.devices.icloud.setup import setup_icloud


def account_menu():
    while True:
        #
        data = get_cfg_bindings_json()
        #
        print("Accounts:")
        for a_key, a_value in data['accounts'].iteritems():
            print("\_ {account_name} ({account_type})".format(account_name=data['accounts'][a_key]['account_name'],
                                                              account_type=data['accounts'][a_key]['account_type']))
        print('')
        #
        print("1 - Add account\n" +
              "2 - Amend account\n" +
              "3 - Delete account\n" +
              "e - Exit to previous menu\n")
        #
        input_var = raw_input("Type the required option number followed by the return key: ")
        print("\n****************************************************************\n")
        #
        if input_var == 'e':
            return
        elif input_var == '1' or input_var == '2' or input_var == '3':
            #
            new_data = None
            #
            if input_var == '1':
                # Add account
                new_data = add_account(data)
                #
            elif input_var == '2':
                # Amend account
                # TODO
                pass
            elif input_var == '3':
                # Delete account
                # TODO
                pass
            #
            if new_data:
                write_config_bindings(data)
                print("\nThe changes have been saved to the configuration file")
                print("\n****************************************************************\n")
            #
        else:
            #
            print("Invalid entry, please try again!!")
            print("\n****************************************************************\n")


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
            new_acc = None
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


#TODO
def amend_account(data):
    while True:
        #
        data = get_cfg_bindings_json()
        #
        print("Accounts:")
        key_count = 0
        for a_key, a_value in data['accounts'].iteritems():
            print("{key} - {account_name} ({account_type})".format(key=str(key_count),
                                                                   account_name=data['accounts'][a_key]['account_name'],
                                                                   account_type=data['accounts'][a_key]['account_type']))
        print('')
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
            new_acc = None
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
