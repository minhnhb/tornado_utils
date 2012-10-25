import tornado.gen
from urlparse import urlparse, parse_qs, urlunparse
from urllib import urlencode
from tornado.httpclient import AsyncHTTPClient
from tornado.web import HTTPError
import xml.etree.ElementTree as ET

CAS_SERVER = "https://id.mwork.vn"

class MworkMixin(object):

    @tornado.gen.engine
    def authenticate_redirect(self, callback=None, http_client=None):

        ticket = self.get_argument("ticket", None)

        url = self.request.full_url()
        u = urlparse(url)
        q = parse_qs(u.query)
        q.pop("ticket", None)
        u = u._replace(query=urlencode(q, True))

        callback_uri = urlunparse(u)

        if not ticket:
            self.redirect(CAS_SERVER + "/login?service=" + callback_uri)
            return

        if http_client is None:
            http_client = AsyncHTTPClient()

        response = yield tornado.gen.Task(http_client.fetch, CAS_SERVER+"/serviceValidate?ticket=%s&service=%s" % (ticket, callback_uri), validate_cert=False)
        if response.error:
            raise HTTPError(401, 'Unable to authenticate: trouble retrieving assertion from CAS to validate ticket.')

        xml = ET.fromstring(response.body)

        if xml is None:
            raise HTTPError(401, 'Unable to authenticate: trouble parsing XML assertion.')

        usernameElem = xml.find(".//{http://www.yale.edu/tp/cas}user")
        if usernameElem is None:
            self.redirect(CAS_SERVER + "/login?service=" + callback_uri)
            return

        user = {"username": usernameElem.text}

        for attrElem in xml.findall(".//{http://www.yale.edu/tp/cas}attribute"):
            nameElem = attrElem.find(".//{http://www.yale.edu/tp/cas}name")
            valElem = attrElem.find(".//{http://www.yale.edu/tp/cas}value")
            if nameElem is not None and valElem is not None:
                user[nameElem.text] = valElem.text

        if callback is not None:
            callback(user)

    def logout(self, callback=None):
        callback = urllib.urlencode(callback)
        self.redirect(CAS_SERVER + "/logout?service=" + callback)
