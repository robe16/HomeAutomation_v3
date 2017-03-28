from config.bindings.config_bindings import get_cfg_bindings_json, write_config_bindings
from bindings.nest.setup import setup_nest
from bindings.icloud.setup import setup_icloud


def thing_menu():
    while True:
        #
        data = get_cfg_bindings_json()
        #
        print("Things:")
        #
        for group in data['bindings']['groups']:
            print("\_ {seq}: {name}".format(seq=group['sequence'], name=group['name']))
            for thing in group['things']:
                print("  \_ {seq}: {name}".format(seq=thing['sequence'], name=thing['name']))
        #
        print("")
        #
        options = {"1": "Add group",
                   "2": "Rename group",
                   "3": "Amend group",
                   "4": "Delete group"}
        #
        for k,v in options:
            print("{key} - {desc}".format(key=k, desc=v))
        print("e - Exit to previous menu\n")
        #
        input_var = raw_input("Type the required option number followed by the return key: ")
        print("\n****************************************************************\n")
        #
        if input_var == 'e':
            return
        #
        try:
            input_var = int(input_var)
            #
            if 0 < input_var <= len(options):
                #
                new_data = None
                #
                if input_var == 1:
                    new_data = add_group(data)
                elif input_var == 2:
                    new_data = rename_group(data)
                elif input_var == 3:
                    new_data = amend_group(data)
                elif input_var == 4:
                    new_data = delete_group(data)
                #
                if new_data:
                    write_config_bindings(new_data)
                    print("\nThe changes have been saved to the configuration file")
                    print("\n****************************************************************\n")
                    return
                #
            else:
                raise Exception
            #
        except Exception as e:
            #
            print("Invalid entry, please try again!!")
            print("\n****************************************************************\n")


def add_group(data):
    while True:
        #
        print("** Add Group **")
        input_response = raw_input("Enter the name for new group: ")
        print("\n****************************************************************\n")
        #
        seq = len(data['bindings']['groups'])
        #
        new_group = {"sequence": seq,
                     "name": input_response,
                     "things": []}
        #
        data['bindings']['groups'].append(new_group)
        #
        return data


def rename_group(data):
    while True:
        #
        print("** Rename Group **")
        try:
            seq = _select_group(data)
            #
            for group in data['bindings']['groups']:
                if group['sequence'] == seq:
                    #
                    print("\_ {seq}: {name}".format(seq=group['sequence'], name=group['name']))
                    #
                    input_response = raw_input("Enter the name for the group: ")
                    print("\n****************************************************************\n")
                    group['name'] = input_response
                    return data
            #
            raise Exception
            #
        except Exception as e:
            print("Error - Returning to previous screen")
            print("\n****************************************************************\n")
            return


def amend_group(data):
    while True:
        #
        print("** Amend Group **")
        try:
            group_seq = _select_group(data)
            #
            for group in data['bindings']['groups']:
                if group['sequence'] == group_seq:
                    #
                    print("\_ {seq}: {name}".format(seq=group['sequence'], name=group['name']))
                    _print_things(group)
                    print("")
                    #
                    options = {"1": "Add Thing'",
                               "2": "Amend Thing",
                               "3": "Delete Thing"}
                    #
                    for k,v in options:
                        print("{key} - {desc}".format(key=k, desc=v))
                    print("e - Exit to previous menu\n")
                    #
                    input_var = raw_input("Type the required option number followed by the return key: ")
                    print("\n****************************************************************\n")
                    #
                    if input_var == 'e':
                        return
                    #
                    try:
                        input_var = int(input_var)
                        #
                        if 0 < input_var <= len(options):
                            #
                            new_data = None
                            #
                            if input_var == 1:
                                new_data = add_thing(data, group_seq)
                            elif input_var == 2:
                                new_data = amend_thing(data, group_seq)
                            elif input_var == 3:
                                new_data = delete_thing(data, group_seq)
                            #
                            if new_data:
                                write_config_bindings(new_data)
                                print("\nThe changes have been saved to the configuration file")
                                print("\n****************************************************************\n")
                                return
                            #
                        else:
                            #
                            print("Invalid entry, please try again!!")
                            print("\n****************************************************************\n")
                        #
                    except Exception as e:
                        raise Exception
            #
            raise Exception
            #
        except Exception as e:
            print("Error - Returning to previous screen")
            print("\n****************************************************************\n")
            return


def delete_group(data):
    while True:
        #
        print("** Delete Group **")
        try:
            seq = _select_group(data)
            #
            for group in data['bindings']['groups']:
                if group['sequence'] == seq:
                    #
                    print("\_ {seq}: {name}".format(seq=group['sequence'], name=group['name']))
                    _print_things(group)
                    print("")
                    #
                    input_response = raw_input("Are you sure you want to delete this group (this action cannot be undone): (y/n) ")
                    print("\n****************************************************************\n")
                    #
                    if input_response.lower() == 'y':
                        data['bindings']['groups'].remove(group)
                        return data
                    elif input_response.lower() == 'n':
                        print("Cancelling operation - Returning to previous screen")
                        print("\n****************************************************************\n")
                        return
                    else:
                        print("Invalid entry - Returning to previous screen")
                        print("\n****************************************************************\n")
                        return
            #
            raise Exception
            #
        except Exception as e:
            print("Error - Returning to previous screen")
            print("\n****************************************************************\n")
            return


def add_thing(data, group_seq):
    #
    print("** Add Thing **")
    #
    try:
        for group in data['bindings']['groups']:
            if group['sequence'] == group_seq:
                #
                # "1": "[Info Service] News",
                # "2": "[Info Service] Weather",
                # "3": "[Info Service] TV Listings",
                #
                options = {"1": "[Device] LG TV (Netcast)",
                           "2": "[Device] Virgin Media (TiVo)",
                           "3": "[Account] iCloud",
                           "4": "[Account] Nest"}
                #
                for k,v in options:
                    print("{key} - {desc}".format(key=k, desc=v))
                print("e - Exit to previous menu\n")
                #
                input_var = raw_input("Type the required option number followed by the return key: ")
                print("\n****************************************************************\n")
                #
                if input_var == 'e':
                    return
                #
                try:
                    input_var = int(input_var)
                    #
                    if 0 < input_var <= len(options):
                        #
                        new_acc = None
                        #
                        if input_var == 1:
                            pass
                        elif input_var == 2:
                            pass
                        elif input_var == 3:
                            new_acc = setup_icloud()
                        elif input_var == 4:
                            new_acc = setup_nest()
                        #
                        if new_acc:
                            group.append(new_acc)
                            return data
                        #
                    else:
                        #
                        print("Invalid entry, please try again!!")
                        print("\n****************************************************************\n")
                    #
                except Exception as e:
                    raise Exception
        #
        raise Exception
        #
    except Exception as e:
        print("Error - Returning to previous screen")
        print("\n****************************************************************\n")
        return


def amend_thing(data, group_seq):
    #
    print("** Amend Thing **")
    print("***********************************")
    print("** FUNCTION NOT YET IN OPERATION **")
    print("***********************************")
    #
    return


def delete_thing(data, group_seq):
    #
    print("** Delete Thing **")
    #
    try:
        for group in data['bindings']['groups']:
            if group['sequence'] == group_seq:
                #
                thing_seq = _select_thing(group)
                #
                for thing in group['things']:
                    if thing['sequence'] == thing_seq:
                        #
                        print("  \_ {seq}: {name} ({type})".format(seq=thing['sequence'],
                                                                   name=thing['name'],
                                                                   type=thing['type']))
                        #
                        input_response = raw_input("Are you sure you want to delete this Thing (this action cannot be undone): (y/n) ")
                        print("\n****************************************************************\n")
                        #
                        if input_response.lower() == 'y':
                            group.remove(thing)
                            return data
                        elif input_response.lower() == 'n':
                            print("Cancelling operation - Returning to previous screen")
                            print("\n****************************************************************\n")
                            return
                        else:
                            print("Invalid entry - Returning to previous screen")
                            print("\n****************************************************************\n")
                            return
                        pass
        #
        raise Exception
        #
    except Exception as e:
        print("Error - Returning to previous screen")
        print("\n****************************************************************\n")
        return


# #TODO
# def amend_account(data):
#     while True:
#         #
#         data = get_cfg_bindings_json()
#         #
#         print("Accounts:")
#         key_count = 0
#         for a_key, a_value in data['accounts'].iteritems():
#             print("{key} - {account_name} ({account_type})".format(key=str(key_count),
#                                                                    account_name=data['accounts'][a_key]['account_name'],
#                                                                    account_type=data['accounts'][a_key]['account_type']))
#         print('')
#         #
#         input_acc = raw_input("Type the required option number followed by the return key: ")
#         print("\n****************************************************************\n")
#         #
#         if input_acc == 'e':
#             #
#             return
#             #
#         elif input_acc == '1' or input_acc == '2':
#             #
#             new_acc = None
#             #
#             if input_acc == '1':
#                 new_acc = setup_nest()
#             elif input_acc == '2':
#                 new_acc = setup_icloud()
#             #
#             if new_acc:
#                 data['accounts'][new_acc['account_id']] = new_acc
#                 #
#                 print("\n****************************************************************\n")
#                 return data
#             #
#         else:
#             #
#             print("Invalid entry, please try again!!")
#             print("\n****************************************************************\n")
#             return data


def _select_group(data):
    while True:
        #
        _print_groups(data)
        input_response = raw_input("Type the group sequence number that you wish to amend: ")
        #
        try:
            return int(input_response)
        except:
            raise Exception


def _select_thing(group):
    while True:
        #
        _print_groups(group)
        input_response = raw_input("Type the Thing sequence number that you wish to amend: ")
        #
        try:
            return int(input_response)
        except:
            raise Exception


def _print_groups(data):
    for group in data['bindings']['groups']:
        print("\_ {seq}: {name}".format(seq=group['sequence'], name=group['name']))


def _print_things(group):
    for thing in group['things']:
        print("  \_ {seq}: {name} ({type})".format(seq=thing['sequence'],
                                                   name=thing['name'],
                                                   type=thing['type']))


def _print_infoservices(data):
    for info in data['bindings']['info_services']:
        print("\_ {seq}: {name} ({type})".format(seq=info['sequence'],
                                                 name=info['name'],
                                                 type=info['type']))