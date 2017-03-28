from config.bindings.config_bindings import get_cfg_bindings_json, write_config_bindings
from setup_bindings import thing_menu


def console_setup():
    while True:
        #
        options = {"1": "Display current setup summary",
                   "2": "Amend structure details",
                   "3": "Amend groups and Things",
                   "4": "Amend Info Services"}
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
                if input_var == 1:
                    print_current_setup()
                elif input_var == 2:
                    structure_menu()
                elif input_var == 3:
                    thing_menu()
                elif input_var == 4:
                    pass
                #
                print("\n****************************************************************\n")
                #
            else:
                raise Exception
            #
        except Exception as e:
            #
            print("Invalid entry, please try again!!")
            print("\n****************************************************************\n")


def structure_menu():
    while True:
        #
        data = get_cfg_bindings_json()
        #
        print('Current structure details:')
        print(' + Name: {name}'.format(name=data['structure']['structure_name']))
        print(' + Postcode: {postcode}'.format(postcode=data['structure']['structure_postcode']))
        print(' + Town: {town}'.format(town=data['structure']['structure_town']))
        print('')
        #
        options = {"1": "Amend name",
                   "2": "Amend postcode",
                   "3": "Amend town"}
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
                if input_var == 1:
                    new_val = raw_input("Enter new value for Structure Name")
                    data['structure']['structure_name'] = new_val
                    data['structure']['structure_id'] = new_val.lower().replace(' ', '')
                elif input_var == 2:
                    new_val = raw_input("Enter new value for Structure Postcode")
                    data['structure']['structure_postcode'] = new_val
                elif input_var == 3:
                    new_val = raw_input("Enter new value for Structure Town")
                    data['structure']['structure_town'] = new_val
                #
                write_config_bindings(data)
                print("\nThe amendment has been saved to the configuration file")
                print("\n****************************************************************\n")
                #
            else:
                raise Exception
            #
        except Exception as e:
            #
            print("Invalid entry, please try again!!")
            print("\n****************************************************************\n")


def print_current_setup():
    #
    data = get_cfg_bindings_json()
    #
    print('Structure')
    print(' + Name: {name}'.format(name=data['structure']['structure_name']))
    print(' + Location: {town}, {postcode}'.format(town=data['structure']['structure_town'],
                                                   postcode=data['structure']['structure_postcode']))
    #
    print('Groups & Things:')
    for group in data['bindings']['groups']:
        print("\_ {seq}: {name}".format(seq=group['sequence'], name=group['name']))
        for thing in group['things']:
            print("  \_ {seq}: {name} ({type})".format(seq=thing['sequence'],
                                                       name=thing['name'],
                                                       type=thing['type']))
    #
    print('Info_Services:')
    for info in data['bindings']['groups']:
        print("\_ {seq}: {name} ({type})".format(seq=info['sequence'],
                                                 name=info['name'],
                                                 type=info['type']))
    #
    print("\n****************************************************************\n")
