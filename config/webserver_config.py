import os
import base64
from airflow import configuration as conf
from flask_appbuilder.security.manager import AUTH_DB, AUTH_OAUTH, AUTH_OID
from flask_appbuilder.security.sqla.manager import SecurityManager

# from flask_appbuilder.security.manager import AUTH_REMOTE_USER
basedir = os.path.abspath(os.path.dirname(__file__))

# The SQLAlchemy connection string.
SQLALCHEMY_DATABASE_URI = conf.get('core', 'SQL_ALCHEMY_CONN')

# Flask-WTF flag for CSRF
CSRF_ENABLED = True

#----------------------
# AUTHENTICATION CONFIG
#----------------------
# For details on how to set up each of the following authentication, see
# http://flask-appbuilder.readthedocs.io/en/latest/security.html# authentication-methods
# for details.

# The authentication type
# AUTH_OID : Is for OpenID
# AUTH_DB : Is for database
# AUTH_LDAP : Is for LDAP
# AUTH_REMOTE_USER : Is for using REMOTE_USER from web server
# AUTH_OAUTH : Is for OAuth
AUTH_TYPE = AUTH_OAUTH

# When using AUTH_DB you will need to run airflow create_user to create an
# admin user:
# airflow create_user -f FIRSTNAME -e EMAIL -l LASTNAME -u USERNAME -r Admin -p PASSWORD

# Uncomment to setup Full admin role name
# AUTH_ROLE_ADMIN = 'Admin'

# Uncomment to setup Public role name, no authentication needed
# AUTH_ROLE_PUBLIC = 'Public'

# Will allow user self registration
AUTH_USER_REGISTRATION = True

# The default user self registration role
AUTH_USER_REGISTRATION_ROLE = "Admin" # @Update: this should be changed to viewer (only use for testing)

# Required for Okta OAuth
state_param = base64.b64encode(b'xyzabc123').decode('utf-8')

# Examples for oauth: https://github.com/dpgaspar/Flask-AppBuilder/tree/master/examples/oauth

# OAuth provider config setup
OAUTH_PROVIDERS = [{
        'name':'okta',
        'whitelist': ['@<COMPANY1>.com', '@<COMPANY2>.com'], # optional
        'token_key':'access_token',
        'icon':'fa-circle-o',
        'remote_app': {
            'base_url': 'https://<COMPANY>.okta.com/oauth2/v1/',
            'request_token_params': {
                'scope': 'email openid profile',
                'state': state_param,
            },
            'access_token_url': 'https://<COMPANY>.okta.com/oauth2/v1/token',
            'authorize_url': 'https://<COMPANY>.okta.com/oauth2/v1/authorize',
            'request_token_url': None,
            'consumer_key': 'CONSUMER_KEY',
            'consumer_secret': 'CONSUMER_SECRET',
        }
    },
    {
        'name':'google',
        'whitelist': ['@<COMPANY1>.com', '@<COMPANY2>.com'], # optional
        'token_key': 'access_token',
        'icon': 'fa-google',
        'remote_app': {
            'base_url': 'https://www.googleapis.com/oauth2/v2/',
            'request_token_params': {
                'scope': 'email profile'
            },
            'access_token_url': 'https://accounts.google.com/o/oauth2/token',
            'authorize_url': 'https://accounts.google.com/o/oauth2/auth',
            'request_token_url': None,
            'consumer_key': 'CONSUMER_KEY',
            'consumer_secret': 'CONSUMER_SECRET',
        }
    }
]

# Example of custom SecurityManager class. This is needed for unsupported OAuth
# providers (ie Okta) or for customizing existing OAuth providers (ie google)
class CustomSecurityManager(SecurityManager):
    def oauth_user_info(self, provider, resp):
        if provider == 'okta':
            me = self.appbuilder.sm.oauth_remotes[provider].get('userinfo')
            return {'username': me.data.get('email', '').split('@')[0],
                    'first_name': me.data.get('given_name', ''),
                    'last_name': me.data.get('family_name', ''),
                    'email': me.data.get('email', '')}
        if provider == 'google':
            me = self.appbuilder.sm.oauth_remotes[provider].get('userinfo')
            return {'username': me.data.get('email', '').split('@')[0],
                    'first_name': me.data.get('given_name', ''),
                    'last_name': me.data.get('family_name', ''),
                    'email': me.data.get('email', '')}
        return {}

SECURITY_MANAGER_CLASS = CustomSecurityManager

# When using LDAP Auth, setup the ldap server
# AUTH_LDAP_SERVER = "ldap://ldapserver.new"

# When using OpenID Auth, uncomment to setup OpenID providers.
# example for OpenID authentication
# OPENID_PROVIDERS = [
#    { 'name': 'Yahoo', 'url': 'https://me.yahoo.com' },
#    { 'name': 'AOL', 'url': 'http://openid.aol.com/<username>' },
#    { 'name': 'Flickr', 'url': 'http://www.flickr.com/<username>' },
#    { 'name': 'MyOpenID', 'url': 'https://www.myopenid.com' }]

