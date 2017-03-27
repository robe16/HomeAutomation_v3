import datetime
import json
import webbrowser
import requests
from time import sleep
from lists.bindings.list_bindings import get_binding_detail
from auth import get_accesstoken


def setup_nest():
    #
    name = raw_input("Enter the name: ")
    #
    try:
        #
        print('The web browser will open to the Nest website.')
        print('Please sign in and grant permissions for the HomeControl-server to interact with the Nest account.')
        sleep(5)
        #
        client_id = get_binding_detail('nest_account', 'client_id')
        client_secret = get_binding_detail('nest_account', 'client_secret')
        state = 'STATE'
        #
        url_auth = 'https://home.nest.com/login/oauth2?client_id={client_id}&state={state}'.format(client_id=client_id,
                                                                                                   state=state)
        webbrowser.open(url_auth, new=1)
        #
        pincode = raw_input("Enter pincode: ")
        #
        token_response = get_accesstoken(client_id, client_secret, pincode)
        #
        ################################
        #
    except:
        print("\n!! An error has ocurred - please try again !!")
        print("\n****************************************************************\n")
        return
    #
    new_acc = {}
    new_acc['type'] = 'nest_account'
    new_acc['name'] = name
    new_acc['details_private'] = {'tokenexpiry': token_response['tokenexpiry'],
                                  'token': token_response['token'],
                                  'state': state,
                                  'redirect_url': ''}
    new_acc['details_public'] = {}
    #
    return new_acc
