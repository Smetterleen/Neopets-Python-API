from urllib.request import HTTPRedirectHandler
from urllib.request import urlparse, urlunparse, urljoin, HTTPError

class Redirecter(HTTPRedirectHandler):
    '''
    classdocs
    '''

    def http_error_302(self, req, fp, code, msg, headers):
        # Some servers (incorrectly) return multiple Location headers
        # (so probably same goes for URI).  Use first header.
        if "location" in headers:
            newurl = headers["location"]
        elif "uri" in headers:
            newurl = headers["uri"]
        else:
            return

        if newurl.startswith('training.phtml'):
            newurl = '/island/' + newurl
        elif not newurl.startswith('/'):
            newurl = '/' + newurl
            
        # fix relative URL
        newurl = 'http://www.neopets.com' + newurl

        # fix a possible malformed URL
        urlparts = urlparse(newurl)

        # For security reasons we don't allow redirection to anything other
        # than http, https or ftp.

        if not urlparts.scheme in ('http', 'https', 'ftp'):
            raise HTTPError(newurl, code,
                            msg +
                            " - Redirection to url '%s' is not allowed" %
                            newurl,
                            headers, fp)

        if not urlparts.path:
            urlparts = list(urlparts)
            urlparts[2] = "/"
        newurl = urlunparse(urlparts)

        newurl = urljoin(req.full_url, newurl)

        # XXX Probably want to forget about the state of the current
        # request, although that might interact poorly with other
        # handlers that also use handler-specific request attributes
        new = self.redirect_request(req, fp, code, msg, headers, newurl)
        if new is None:
            return

        # loop detection
        # .redirect_dict has a key url if url was previously visited.
        if hasattr(req, 'redirect_dict'):
            visited = new.redirect_dict = req.redirect_dict
            if (visited.get(newurl, 0) >= self.max_repeats or
                len(visited) >= self.max_redirections):
                raise HTTPError(req.full_url, code,
                                self.inf_msg + msg, headers, fp)
        else:
            visited = new.redirect_dict = req.redirect_dict = {}
        visited[newurl] = visited.get(newurl, 0) + 1

        # Don't close the fp until we are sure that we won't use it
        # with HTTPError.
        fp.read()
        fp.close()

        return self.parent.open(new, timeout=req.timeout)