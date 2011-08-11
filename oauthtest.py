import urlparse
import httplib2
import datetime
import oauth2 as oauth
import Cookie
from django.utils import simplejson as json
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app

#consumer_key = 'DK2jcYzQztQqkGLHEk'
#consumer_secret = 'VDvU32gg46DRaq24FmSXy9zNg9s7WCWC'

consumer_key = 'MGueyfX4ZYdghpyMqU'
consumer_secret = 'VQ3r83KRafzqjx7fbdeQb2SKLj9jpSmD'

#request_token_url = 'http://internplease.frontend-ivan1.office.loggly.net/api/oauth/request_token/'
#access_token_url = 'http://internplease.frontend-ivan1.office.loggly.net/api/oauth/access_token/'
#authorize_url = 'http://internplease.frontend-ivan1.office.loggly.net/api/oauth/authorize/'

request_token_url = 'http://internplease.loggly.com/api/oauth/request_token/'
access_token_url = 'http://internplease.loggly.com/api/oauth/access_token/'
authorize_url = 'https://internplease.loggly.com/api/oauth/authorize/'


def get_data():
    import Cookie
    consumer = oauth.Consumer(consumer_key, consumer_secret)
    signature_method = oauth.SignatureMethod_HMAC_SHA1()

#    client = oauth.Client(consumer)
#    resp, content = client.request(request_token_url, "GET")
#    request_token = dict(urlparse.parse_qsl(content))
    h = httplib2.Http()

    # get request token
    parameters = {}
    # We dont have a callback server, we're going to use the browser to
    # authorize.

    #TODO: Add check for 401 etc
    parameters['oauth_callback'] = 'http://localhost:8082/oauthreturned/'
    oauth_req1 = oauth.Request.from_consumer_and_token(
        consumer, http_url=request_token_url, parameters=parameters)
    oauth_req1.sign_request(signature_method, consumer, None)
    #print 'Request headers: %s' % str(oauth_req1.to_header())
    response, content = h.request(oauth_req1.to_url(), 'GET')
    token = oauth.Token.from_string(content)
    
    expiration = datetime.datetime.now() + datetime.timedelta(days=30)
    c = Cookie.SimpleCookie()
    c['secret'] = str(token.secret)
    c['secret']["expires"] = expiration.strftime("%a, %d-%b-%Y %H:%M:%S PST")
    print c
    
    #print 'GOT key: %s  secret:%s' % (str(token.key), str(token.secret))

    #print '* Authorize the request token ...'
    oauth_req2 = oauth.Request.from_token_and_callback(
        token=token, callback='http://localhost:8082/oauthreturned/', http_url=authorize_url)
    #print 'Please run this URL in a browser and paste the token back here'
    return oauth_req2.to_url()
    
    
    
    
#    print request_token
#
#    print "Request Token:"
#    print "    - oauth_token        = %s" % request_token['oauth_token']
#    print "    - oauth_token_secret = %s" % request_token['oauth_token_secret']
#    print 
# Step 2: Redirect to the provider. Since this is a CLI script we do not 
# redirect. In a web application you would redirect the user to the URL
# below.

#    print "Go to the following link in your browser:"
#    print "%s?oauth_token=%s&oauth_callback=http://localhost:8083/oauthreturned" % (authorize_url, request_token['oauth_token'])
    
#    return token 
#"%s?oauth_token=%s&oauth_callback=http://localhost:8082/oauthreturned/" % (authorize_url, request_token['oauth_token'])

class redirect(webapp.RequestHandler):
        def get(self):
                self.response.out.write(open ('redirect.html').read())

class auth(webapp.RequestHandler):

      def get(self):
                #print "BLAH", content
                self.response.out.write(get_data())
                #print "%s?oauth_token=%s&oauth_callback=http://localhost:8082/oauthreturned/" % (authorize_url, request_token['oauth_token'])
            

app = webapp.WSGIApplication([('/oauthtest', auth),('/redirect', redirect)], debug = True)


def main():
    run_wsgi_app(app)

if __name__ == "__main__":
    main()


# Step 3: Once the consumer has redirected the user back to the oauth_callback
# URL you can request the access token the user has approved. You use the 
# request token to sign this request. After this is done you throw away the
# request token and use the access token returned. You should store this 
# access token somewhere safe, like a database, for future use.
#token = oauth.Token(request_token['oauth_token'],
#    request_token['oauth_token_secret'])
#token.set_verifier(oauth_verifier)
#print "Token:", token
#client = oauth.Client(consumer, token)
#
#resp, content = client.request(access_token_url, "POST")
#access_token = dict(urlparse.parse_qsl(content))
#
#print "Access Token:", access_token
#print "    - oauth_token        = %s" % access_token['oauth_token']
#print "    - oauth_token_secret = %s" % access_token['oauth_token_secret']
#print
#print "You may now access protected resources using the access tokens above." 
#print
