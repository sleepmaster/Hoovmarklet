import time
import httplib2
import os
import urllib
import urllib2
import Cookie
import oauth2 as oauth
import gdata.docs.service
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app


# Set the API endpoint 
#url = "http://internplease.frontend-ivan1.office.loggly.net/api/inputs/"
url = "http://internplease.loggly.com/api/inputs/"
#consumer_key = 'DK2jcYzQztQqkGLHEk'
#consumer_secret = 'VDvU32gg46DRaq24FmSXy9zNg9s7WCWC'
consumer_key = 'MGueyfX4ZYdghpyMqU'
consumer_secret = 'VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD'
#access_token_url = 'http://internplease.frontend-ivan1.office.loggly.net/api/oauth/access_token/'
access_token_url = 'http://internplease.loggly.com/api/oauth/access_token/'

# Set the base oauth_* parameters along with any other parameters required
# for the API call.
cookie_string = os.environ.get('HTTP_COOKIE')
#print "My cookie", cookie_string

#c.load(cookie_string)
#print c['secret']

# Set up instances of our Token and Consumer. The Consumer.key and 
# Consumer.secret are given to you by the API provider. The Token.key and
# Token.secret is given to you after a three-legged authentication.
#def get_access_token():
#    token = oauth.Token(key="swHm3Eeza9zHQ8YE62", secret="bVPEAczQzkGxnPSfb2rFPdPf6getCGb7")
#consumer = oauth.Consumer(key="DK2jcYzQztQqkGLHEk", secret="VDvU32gg46DRaq24FmSXy9zNg9s7WCWC")
consumer = oauth.Consumer(key="MGueyfX4ZYdghpyMqU", secret=" VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD")
# Set our token/key parameters

# Create our request. Change method, etc. accordingly.
#req = oauth.Request(method="GET", url=url, parameters=params)
#print "req", req
# Sign the request.
#signature_method = oauth.SignatureMethod_HMAC_SHA1()
#content = req.sign_request(signature_method, consumer, token)

#auth = urllib2.Request( url, req.to_postdata() )
#form_data = urllib.urlencode(params)
#print "xxx", req.to_postdata()
#print "end post data"
#auth = urlfetch.fetch(url=url, payload= form_data, method=urlfetch.GET)
#print "auth", auth.content

def get_access_token(req_t, verif, secret):
    import urlparse
    import Cookie
    import oauth2 as oauth
    
    h = httplib2.Http()
    signature_method = oauth.SignatureMethod_HMAC_SHA1()

#    params = {
#    'oauth_version': "1.0",
#    'oauth_nonce': oauth.generate_nonce(),
#    'oauth_timestamp': int(time.time())
#    }
#    params['oauth_token'] = req_t
#    params['oauth_consumer_key'] = consumer_key
#    params['oauth_verifier'] = verif
    #print "SECRET", secret
    token = oauth.Token(key = req_t, secret = secret)
    token.set_verifier(verif)
    #    client = oauth.Client(consumer, token)
    #
    #    resp, content = client.request(access_token_url, "POST")
    #    print resp
    #    print content
    #    access_token = dict(urlparse.parse_qsl(content))
    #access_token = oauth.Request(method="POST", url = access_token_url, parameters = params)
    #access_token.sign_request(signature_method, consumer, token)
    
    oauth_req3 = oauth.Request.from_consumer_and_token(
        consumer, token=token, http_url=access_token_url)
    
    oauth_req3.sign_request(signature_method, consumer, token)
    
    sign = oauth_req3.get_parameter('oauth_signature')
    #print "signature", sign 
    
    #print "Oauth_req",oauth_req3
    
    #print 'Request headers: %s' % str(oauth_req3.to_header())
    response, content = h.request(oauth_req3.to_url(), 'GET')
    access_token = oauth.Token.from_string(content)
    #print 'WAHOO', str( access_token.key), str(access_token.secret)
    #access_token = oauth.Token.from_string(content)
    #print 'Access Token key: %s  secret:%s' % (str(access_token.key),
    #                                           str(access_token.secret))
#    client = gdata.docs.service.ContactsService() 
#    client.SetOAuthInputParameters(signature_method, 
#    consumer_key,consumer_secret=consumer_secret) 
#    oauth_input_params = 
#    gdata.auth.OAuthInputParams(gdata.auth.OAuthSignatureMethod.HMAC_SHA1, 
#    consumer_key, consumer_secret=consumer_key) 
#    # the token key and secret should be recalled from your database 
#    oauth_token = gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret, 
#    scopes=OAUTH_SCOPES, oauth_input_params=oauth_input_params) 
#    client.SetOAuthToken(oauth_token)
    client = gdata.docs.service.DocsService()
    client.SetOAuthInputParameters(signature_method,consumer_key,consumer_secret=consumer_secret)

# the token key and secret should be recalled from your database
    client.SetOAuthToken(gdata.auth.OAuthToken(key=access_token.key, secret=access_token.secret))

    #print "muahhaha", client
    return access_token
    


def get_inputs(access_t):
    import urlparse
    import Cookie
    import oauth2 as oauth
    
    h = httplib2.Http()
    signature_method = oauth.SignatureMethod_HMAC_SHA1()
#    params = {
#    'oauth_version': "1.0",
#    'oauth_nonce': oauth.generate_nonce(),
#    'oauth_timestamp': int(time.time())
#    }
#    params['oauth_token'] = access_t
#    params['oauth_consumer_key'] = consumer_key
#    params['oauth_signature_method'] = oauth.SignatureMethod_HMAC_SHA1()
#    
#    print "access_token", access_t
#    print "params", params
#    print params['oauth_token']
    oauth_req4 = oauth.Request.from_consumer_and_token(consumer,
                                                       token=access_t,
                                                       http_url=url)
    oauth_req4.sign_request(signature_method, consumer, access_t)
    resp, content = h.request(url, "GET", headers=oauth_req4.to_header())
    #print resp
    content_dict = json.loads(content)
    #print content_dict
    num = len(content_dict)
    input_key = []
    input_name = []
    for i in range(num):
        if(content_dict[i]['service']['name'] =='HTTP'):
            input_key.append(content_dict[i]['input_token'])
            input_name.append(content_dict[i]['name'])
            
            
    print "<h1> %s </h1> " % 'YOU SUCK'
    for i in range(len(input_key)):
        print "<a href=\"javascript:(function(){newsrc=document.location.protocol+'//d3eyf2cx8mbems.cloudfront.net/js/loggly-0.1.0.js';document.body.appendChild(document.createElement('script')).src=newsrc;var logglykey='"+input_key[i]+"';var%20host=document.location.protocol+'//logs.loggly.com';function%20sendlog(host,logglykey){castor=new%20loggly({url:host+'/inputs/'+logglykey+'?rt=1',level:'log'});castor.log('url='+location.href);}function racecond(){try{loggly==null;sendlog(host,logglykey);}catch(err){setTimeout(racecond,100);}}setTimeout(racecond,100);})();\">Send to "+input_name[i]+"@loggly >></a><br>"

    #print "<H1>%s</H1>" % len(content_dict)
    
    
    
    
#    req = oauth.Request(method="GET", url=url, parameters=params)
#    print "req", req
#    content = req.sign_request(signature_method, consumer, access_t)
#    print "content", content
    
    
    
class oauth(webapp.RequestHandler):
    def get(self):
        url = self.request.arguments()
        #print url
        oauth_v = self.request.get('oauth_verifier')
        req_token = self.request.get('oauth_token')
        #self.response.out.write(req_token)
        #print req_token
        #print oath_v
        #print str(self.request.cookies)
        req_secret = self.request.cookies['secret']
        #signature_method = self.request.cookies['signature']
        
        #print "req",req_secret
        access_token = get_access_token(req_token, oauth_v, req_secret)
        #print "ACCESS TOKEN", access_token
        
        json = (get_inputs(access_token))
        return json
#        self.response.out.write(get_inputs(access_token))
#        self.response.out.write(get_access_token(req_token, req_secret, oath_v ))
        
        #oauth_verifier = self.request.get_all()
                
            

app = webapp.WSGIApplication([('/oauthreturned/', oauth)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()

#print "OMG THIS SUCKS"

#Need to make it into OOP. so make a class that handles GET and POST methods. In GET, make the request and 
#call the website, grab the url and access it i think?. something like that
#when they return the callback to u, handle it and use get_all method, hopefully that gets me oauth_verifier
#next call the POST method, in order to handle the request token + oauth_verifier
# and hopefully get back the access token
#from access token, then do a GET using access token and then grab the last URL. i think thats what i gotta do tmrw. ***i think**** 