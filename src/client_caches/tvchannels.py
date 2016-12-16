import ast
from src.lists.channels.list_channels import read_list_channels


def compile_tvchannels():
    #
    data = read_list_channels()
    #
    # remove fields that are not required by client
    catCount = 0
    while catCount < len(data['channels']):
        chanCount = 0
        while chanCount < len(data['channels'][str(catCount)]['channels']):
            del data['channels'][str(catCount)]['channels'][str(chanCount)]['listingsrc']
            chanCount += 1
        catCount += 1
    #
    try:
        return ast.literal_eval(data)
    except:
        return data