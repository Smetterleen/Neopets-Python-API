from neopapi.core.browse import register_page
from neopapi.core.browse.Browser import BROWSER
import re

register_page('inventory.phtml',
              ['quickstock.phtml'],
              True)
register_page('quickstock.phtml')



class Item(object):
    
    def __init__(self, item_id, name):
        self.item_id = item_id
        self.name = name

    # TODO: functies om andere acties op items te exporteren, bv. 'feed to', 'put
    #       up for auction' en 'read to'
    

def items():
    """
    Returns a list containing the items in the users inventory
    
    """
    inv_page = BROWSER.goto('inventory.phtml')
    item_link_tags = inv_page.find_all('a', onclick=re.compile('openwin'))
    items = []
    for item_link_tag in item_link_tags:
        item_id = re.sub('\D', '', item_link_tag.attrs['onclick'])
        name = item_link_tag.next_element.next_element.next_element
        items.append(Item(item_id, name))
    
    return items

def amount_of_items():
    """
    Returns the amount of items currently in the users inventory
    
    """
    inv_page = BROWSER.goto('inventory.phtml')
    item_link_tags = inv_page.find_all('a', onclick=re.compile('openwin'))
    return len(item_link_tags)
    
    return items

def contains(item_list):
    """
    Returns a list of Booleans, whose value depends on wether or
    not they corresponding item is present in the users inventory.
    If the argument is a string instead of a list, a boolean will be
    returned.
    
    """
    inv_page = BROWSER.goto('inventory.phtml')
    
    is_string = isinstance(item_list, str)
    if is_string:
        item_list = [item_list]
    item_list = item_list.copy()
    item_link_tags = inv_page.find_all('a', onclick=re.compile('openwin'))
    items_in_inventory = [False] * len(item_list)
    items_found = 0
    for item_link_tag in item_link_tags:
        name = item_link_tag.next_element.next_element.next_element
        if name in item_list:
            item_index = item_list.index(name)
            items_in_inventory[item_index] = True
            item_list[item_index] = None
            items_found += 1
            if items_found >= len(item_list):
                break
    if is_string:
        return items_in_inventory[0]
    return items_in_inventory

def put_in_SDB(item_list):
    """
    Attempts to put every item in the given list into the users Safety
    Deposit Box. If a given item is not present in the users inventory,
    it will be ignored.
    
    """
    return _put_in(item_list, 'deposit')

def put_in_shop(item_list):
    """
    Attempts to put every item in the given list into the users Shop. 
    If a given item is not present in the users inventory,
    it will be ignored.
    
    """
    return _put_in(item_list, 'stock')

def donate(item_list):
    """
    Attempts to donate every item in the given list. If a given item 
    is not present in the users inventory, it will be ignored.
    
    """
    return _put_in(item_list, 'donate')

def discard(item_list):
    """
    Attempts to discard every item in the given list. If a given item 
    is not present in the users inventory, it will be ignored.
    
    """
    return _put_in(item_list, 'discard')

def put_in_gallery(item_list):
    """
    Attempts to put every item in the given list into the users Gallery. 
    If a given item is not present in the users inventory, it will be ignored.
    
    """
    return _put_in(item_list, 'gallery')

def put_in_closet(item_list):
    """
    Attempts to put every item in the given list into the users Closet. 
    If a given item is not present in the users inventory, it will be ignored.
    
    """
    return _put_in(item_list, 'closet')

def put_in_shed(item_list):
    """
    Attempts to put every item in the given list into the users Shed. 
    If a given item is not present in the users inventory, it will be ignored.
    
    """
    return _put_in(item_list, 'shed')

def _put_in(item_list, place):
    """
    Puts the items in the given item list in the given place. Place can be:
        deposit, stock, donate, discard, gallery, closet, shed
    Returns a list of items that were not put in the given place, because the
    needed action is not available for those items.
    
    """
    ignored_items = []
    page = BROWSER.goto('quickstock.phtml')
    item_trs = page.find('form', {'name': 'quickstock'}).find_all('tr')[1:]
    item_num = 1
    post_dict = {'buyitem': 0}
    for item_tr in item_trs:
        item_id = item_tr.find('input')['value']
        item_name = item_tr.find('td').text
        post_dict['id_arr[' + str(item_num) + ']'] = item_id
        if item_name in item_list:
            if not item_tr.find('input', {'value': place}):
                ignored_items.append(item_name)
                continue
            post_dict['radio_arr[' + str(item_num) + ']'] = place
    return ignored_items
    
