from neopapi.core.browse.Browser import BROWSER
import re
from neopapi.core.Exceptions import LoginRequiredException
from neopapi.core.browse import register_page
from neopapi.main.Exceptions import LockedOutException, WrongPasswordException,\
    WrongUsernameException

register_page('logout.phtml', reachable_from_everywhere=True)

def is_logged_in(username=None):
    if BROWSER.last_visited_page() is None or BROWSER.last_visited_page().find('td', class_='user') is None:
        BROWSER.goto('')
    
    userlink = BROWSER.last_visited_page().find("td", class_="user").find("a", href=re.compile("userlookup"))
        
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
            
    page = BROWSER.post(url, values)
    
    if 'Incorrect username in cookie' in page.text:
        raise WrongUsernameException(username)
    if 'Bad Password' in page.text:
        raise WrongPasswordException(username)
    
    if 'Sorry, you have tried too many times' in page.text:
        raise LockedOutException(username)
    
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
    if BROWSER.last_visited_page is None or BROWSER.last_visited_page().find('td', class_='user') is None:
        BROWSER.goto('')
        
    return int(BROWSER.last_visited_page().find("td", class_="user").find("a", id="npanchor").text.strip().replace(',', ''))

def active_pet():
    # TODO: implement
    raise NotImplementedError

