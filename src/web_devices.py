# from urllib import urlopen
# from console_messages import print_error
# from web_tvlistings import html_listings_user_and_all
#
#
# def _create_device_page(user, tvlistings, device, structure_id, room_id, device_id):
#     #
#     if not device:
#         return ''
#     #
#     html_body = ''
#     try:
#         html_body = device.getHtml(listings=tvlistings, user=user)
#     except Exception as e:
#         print_error('Attempting to create HTML for {structure_id} - {room_id} - {device_id}: {err}'.format(structure_id=structure_id,
#                                                                                                            room_id=room_id,
#                                                                                                            device_id=device_id,
#                                                                                                            err=e))
#         #
#         html_body += urlopen('web/comp_alert.html').read().encode('utf-8').format(type='alert-danger',
#                                                                                   visible='visible',
#                                                                                   body='<strong>An error has occurred!!</strong> Please try again and if the issue persists check the server setup.')
#     return html_body
#
#
# def _create_account_page(user, tvlistings, device, structure_id, account_id):
#     #
#     if not device:
#         return ''
#     #
#     html_body = ''
#     try:
#         html_body = device.getHtml(listings=tvlistings, user=user)
#     except Exception as e:
#         print_error('Attempting to create HTML for {structure_id} - {account_id}: {err}'.format(structure_id=structure_id,
#                                                                                                 account_id=account_id,
#                                                                                                 err=e))
#         #
#         html_body += urlopen('web/comp_alert.html').read().encode('utf-8').format(type='alert-danger',
#                                                                                   visible='visible',
#                                                                                   body='<strong>An error has occurred!!</strong> Please try again and if the issue persists check the server setup.')
#     return html_body
#
#
# def refresh_tvguide(tvlistings, device=None, structure_id=False, room_id=False, device_id=False, user=False):
#     # Attempt getting current channel from device
#     try:
#         chan_current = device.getChan()
#     except:
#         chan_current = False
#     #
#     return True
#     #return html_listings_user_and_all(tvlistings, group_name=group_name, device_name=device_name, chan_current=chan_current, user=user)