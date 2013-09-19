from neopapi.core import Time, Paths
from neopapi.core.browse.Redirecter import Redirecter
from configparser import ConfigParser
from io import BytesIO
from datetime import timedelta
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from random import uniform
import os, urllib, logging, re, time, gzip
from neopapi.core.browse import find_path
from http import cookiejar
from neopapi.core.Exceptions import LoginRequiredException


class Browser(object):
    """
    This is the browser used by the API to browse around on Neopets.com.
    
    To seem humanlike, the browser has the following features:
        * Random waiting time between requests
        * Automatic pathfinding between last-visited page, and the given url to browse to
        * Mozilla Firefox Headers
        * Referer Header is filled in automatically according to last visited page
    
    When a page is requested that requires a logged-in user, and no user is currently logged
    in, the Browser will raise a 'LoginRequiredException'.
    
    """
    
    HEADER =  {'Host' : 'www.neopets.com',
               'User-agent' : 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)',
               'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
               'Accept-Language' : 'en-us;q=0.7,en;q=0.3',
               'Accept-Encoding' : 'gzip, deflate',
               'Accept-Charset' : 'utf-8;q=0.7,*;q=0.7'}
    
    
    def __init__(self):
        self.time_of_last_get = Time.NST_epoch()
        
        self.cj = cookiejar.LWPCookieJar()
        
        if os.path.isfile(Paths.COOKIES_FILE):
            self.cj.load(Paths.COOKIES_FILE)
            
        cookieHandler = urllib.request.HTTPCookieProcessor(self.cj)
        redirectHandler = Redirecter()
         
        self.opener = urllib.request.build_opener(redirectHandler, cookieHandler)
        
        self.last_visited_url = None
        self.last_visited_page = None
        
        core_config = ConfigParser()
        core_config.read(Paths.CORE_CONFIG_FILE)
        if 'Browser' in core_config:
            self._load_config(core_config['Browser'])
        else:
            self._load_config({})
    
    def _load_config(self, config):
        self.min_wait = int(config.get('delay_time_min', 0))
        if self.min_wait < 0:
            logging.warn('Browser configuration: delay_time_min should not be less than 0, using default.')
            self.min_wait = 0
        self.max_wait = int(config.get('delay_time_max', 0))
        if self.max_wait < 0:
            logging.warn('Browser configuration: delay_time_max should not be less than 0, using default.')
            self.max_wait = 0
        not_connected_action = config.get('not_connected_handling', 'exit')
        if not_connected_action.lower() == 'exit':
            self.not_connected_handler = 0
        elif not_connected_action.lower() == 'retry':
            self.not_connected_handler = 1
        elif re.match('retry\ \d*', not_connected_action.lower()):
            self.not_connected_handler = int(re.sub('[^\d]', '', not_connected_action))
        else:
            logging.warn('Browser configuration: unrecognized option for not_connected_handling setting, using default.')
            self.not_connected_handler = 0

    def _get_wait_time(self):
        '''
        Returns a uniformly distributed wait time between to boundaries defined in the
        main preferences of the program in seconds
        '''
        return timedelta(milliseconds=uniform(self.min_wait, self.max_wait))

    def _get(self, url, base_url, post_dict=None, referer=None, delay_ms=0):
        '''
        This is an internal method used by the get and post methods
        '''
        current_time = Time.NST_time()
        wait_time = self._get_wait_time()
        delay = timedelta(milliseconds=delay_ms)
        while (self.time_of_last_get+delay+wait_time > current_time):
            current_time = Time.NST_time()
        
        # Construct the url
        full_url = 'http://www.' + base_url + '/' + url
        logging.debug('Browsing to ' + full_url)
        
        # Construct the post data if it is available
        data = None
        if post_dict:
            data = urllib.parse.urlencode(post_dict)
            data = data.encode('utf_8')
        
        # Construct the request header
        header = Browser.HEADER
        if referer is None:
            # Default value: use previously visited page
            if self.last_visited_url:
                if self.last_visited_url == 'http://www.neopets.com/useobject.phtml':
                    # If the user has just used an object, we do not want to browse with this
                    # page as referer, because a user would normally browse from the inventory
                    # window
                    header['Referer'] = 'http://www.neopets.com/objects.phtml?type=inventory'
                else:
                    header['Referer'] = self.last_visited_url
        elif referer:
            # Given value: is this value
            header['Referer'] = referer
            
        # Make the request
        while True:
            try:
                req = urllib.request.Request(full_url, data, header)            
                handle = self.opener.open(req)
                self.last_visited_url = handle.geturl().replace('http://www.' + base_url + '/', '')
                self.retries = 0
                break
            except (HTTPError, URLError):
                logging.error("Couldn't connect to " + full_url)
                if self.not_connected_handler > 1 and self.retries < self.not_connected_handler:
                    time.sleep(1)
                    self.retries += 1
                    logging.error('Retry connection: ' + self.retries)
                    continue
                logging.error('Exiting')
                raise Exception()
        
        # Save the cookies
        self.cj.save(Paths.COOKIES_FILE)
        
        if 'http://www.neopets.com/login/index.phtml' in self.last_visited_url and not url == self.last_visited_url:
            raise LoginRequiredException(url)
        
        # Get the request html; decode if necessary
        data = handle.read()        
        if handle.info().get('Content-Encoding') == 'gzip':
            buf = BytesIO(data)
            f = gzip.GzipFile(fileobj=buf)
            page = f.read()
        # Maybe add more encoding types in the future?
        page = BeautifulSoup(page)
        
        self.time_of_last_get = current_time
        self.last_visited_page = page
        
        return page

    def goto(self, url, base_url='neopets.com', delay=0):
        """
        Send the browser to the given url.
        To emulate human behaviour, the browser will find the shortest path from the
        last visited page to the given url, and browse each page of this path in turn.
        Returns a beautifulsoup of the requested page.
        
        """
        if self.last_visited_url is None:
            self._get('', base_url, delay_ms=delay)
        
        if url == self.last_visited_url:
            return self.last_visited_page
            
        url_chain = find_path(self.last_visited_url, url)
        for url in url_chain[:-1]:
            self._get(url, base_url, delay_ms=0)
        return self._get(url_chain[-1], base_url, delay_ms=delay)
    
    def post(self, url, post_dict, base_url='neopets.com', delay=0):
        """
        Posts the given data to the given url.
        The browser will not automatically browse to the given page before posting, so 
        make sure this has been taken care of if you want to look human.
        
        """
        return self._get(url, base_url, post_dict, delay_ms=delay)
    
    def back(self):
        # Go back one page
        # TODO: implement
        raise NotImplementedError
    
    def refresh(self):
        # TODO: implement
        raise NotImplementedError

BROWSER = Browser()
