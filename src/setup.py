from config.bindings.config_bindings import get_cfg_bindings_json, write_config_bindings


def console_setup():
    while True:
        print("1 - Display current setup summary\n" +
              "2 - Amend structure details\n" +
              "3 - Amend groups and devices\n" +
              "e - Exit to main menu\n")
        #
        input_var = raw_input("Type the required option number followed by the return key: ")
        print("\n****************************************************************\n")
        #
        if input_var == 'e':
            #
            return
            #
        if input_var == '1' or input_var == '2' or input_var == '3':
            #
            if input_var=='1':
                print_current_setup()
            elif input_var=='2':
                structure_menu()
            elif input_var=='3':
                pass
            #
            print("\n****************************************************************\n")
            #
        else:
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
        print("1 - Amend name\n" +
              "2 - Amend postcode\n" +
              "3 - Amend town (must be as per metoffice town names)\n" +
              "e - Exit to previous menu\n")
        #
        input_var = raw_input("Type the required option number followed by the return key: ")
        print("\n****************************************************************\n")
        #
        if input_var == 'e':
            return
        elif input_var == '1' or input_var == '2' or input_var == '3':
            #
            if input_var == '1':
                new_val = raw_input("Enter new value for Structure Name")
                data['structure']['structure_name'] = new_val
                data['structure']['structure_id'] = new_val.lower().replace(' ', '')
            elif input_var == '2':
                raw_input("Enter new value for Structure Postcode")
                data['structure']['structure_postcode'] = new_val
            elif input_var == '3':
                #TODO: get list of towns from metoffice and display as numbered list to select from
                raw_input("Enter new value for Structure Town")
                data['structure']['structure_town'] = new_val
            #
            write_config_bindings(data)
            print("\nThe amendment has been saved to the configuration file")
            print("\n****************************************************************\n")
            #
        else:
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
    print('Groups & devices:')
    for r_key, r_value in data['groups'].iteritems():
        print('\_ {room_name}:'.format(room_name=data['groups'][r_key]['room_name']))
        for d_key, d_value in data['groups'][r_key]['devices'].iteritems():
            print('  \_ {device_name} ({device_type})'.format(device_name=data['groups'][r_key]['devices'][d_key]['device_name'],
                                                              device_type=data['groups'][r_key]['devices'][d_key]['device_type']))