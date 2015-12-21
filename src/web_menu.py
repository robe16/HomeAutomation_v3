from urllib import urlopen

def _menu(user, arr_objects):
    return urlopen('web/menu.html').read().encode('utf-8').format(menus=_menudrops(arr_objects),
                                                                  user=user)


def _menudrops(arr_objects):
    x = 0
    STRhtml = ""
    while x < len(arr_objects):
        room = arr_objects[x][0].lower()
        items = ""
        y = 0
        while y < len(arr_objects[x][1]):
            group = arr_objects[x][1][y][0].lower()
            items += urlopen('web/header_dropdown_items.html').read().encode('utf-8').format(room + group,
                                                                                             room + '/' + group,
                                                                                             group.upper())
            y += 1
        STRhtml += urlopen('web/header_dropdown.html').read().encode('utf-8').format(room, room.capitalize(), items)
        x += 1
    return STRhtml