from neopapi.core.browse.Browser import BROWSER
import re
from neopapi.core.Exceptions import LoginRequiredException
from neopapi.core.browse import register_page

register_page('logout.phtml', reachable_from_everywhere=True)

def is_logged_in(username=None):
    if BROWSER.last_visited_page is None or BROWSER.last_visited_page.find('td', class_='user') is None:
        BROWSER.goto('')
    
    userlink = BROWSER.last_visited_page.find("td", class_="user").find("a", href=re.compile("userlookup"))
        
    if userlink is not None:
        if username is None or username.lower() == userlink.text.lower():
            return True
    return False    

def login(username, password):
    if is_logged_in(username):
        return True
    if is_logged_in():
        logout()
    url = "login.phtml"
    
    values = {'destination' : '/index.phtml',
              'password' : password,
              'username' : username}
            
    index = BROWSER.post(url, values)
            
    # TODO: do error handling
    if is_logged_in(username):
        return True
    return False
        

def logout():
    if is_logged_in():
        BROWSER.goto('logout.phtml')
        return True
    return False

def cash_on_hand():
    if not is_logged_in():
        raise LoginRequiredException(msg='Login required for checking Cash on Hand')
    if BROWSER.last_visited_page is None or BROWSER.last_visited_page.find('td', class_='user') is None:
        BROWSER.goto('')
        
    return int(BROWSER.last_visited_page.find("td", class_="user").find("a", id="npanchor").text.strip().replace(',', ''))

def active_pet():
    # TODO: implement
    raise NotImplementedError

