from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User)
    oauth_token = models.CharField(max_length=200)
    oauth_secret = models.CharField(max_length=200)

#Basado en: http://djangosnippets.org/snippets/2065/
# 16 June 2010 Added missing imports. Cleaned up the template.
#Shouts out to @obeattie and @whalesalad
#Author: barnardo
#Posted: June 15, 2010

class FacebookSessionError(Exception):
    def __init__(self, error_type, message):
        self.message = message
        self.type = error_type
    def get_message(self):
        return self.message
    def get_type(self):
        return self.type
    def __unicode__(self):
        return u'%s: "%s"' % (self.type, self.message)

class FacebookSession(models.Model):
    access_token = models.CharField(max_length=200, unique=True)
    expires = models.IntegerField(null=True)

    user = models.ForeignKey(User, null=True)
    uid = models.BigIntegerField(unique=True, null=True)

    class Meta:
        unique_together = (('user', 'uid'), ('access_token', 'expires'))

    def query(self, object_id, connection_type=None, fields=None, metadata=False):
        import urllib
        import simplejson

        url = 'https://graph.facebook.com/%s' % (object_id)
        if connection_type:
            url += '/%s' % (connection_type)

        params = {'access_token': self.access_token}
        if metadata:
            params['metadata'] = 1
        if fields:
            params['fields'] = fields

        url += '?' + urllib.urlencode(params)
        response = simplejson.load(urllib.urlopen(url))
        if 'error' in response:
            error = response['error']
            raise FacebookSessionError(error['type'], error['message'])
        return response


# CRH models here.
class Collection(models.Model):
    V_TYPE = (
        (u'PR', u'Private'),
        (u'PU', u'Public'),
        )

    name = models.CharField(max_length=50)
    description = models.CharField(max_length=50)
    creation_date = models.DateTimeField()
    visibility = models.CharField(max_length=45, choices=V_TYPE)
    users = models.ManyToManyField(User, through='User_Collection')

    def __unicode__(self):
        return u'%s %s' % (self.name, self.description)

class User_Collection(models.Model):
    STATUS_TYPE= (
        (u'PR', u'Private'),
        (u'PU', u'Public')
        )
    ROLE_TYPE=(
        (u'O', u'Owner'),
        (u'C', u'Collaborator'),
        (u'A', u'Anonymous')
        )
    user = models.ForeignKey(User)
    collection = models.ForeignKey(Collection)
    role = models.CharField(max_length=45, choices=ROLE_TYPE)
    status = models.CharField(max_length=45, choices=STATUS_TYPE)

class Collection_Individual(models.Model):
    collection = models.ForeignKey(Collection, related_name='individuals')
    individual_id = models.CharField(max_length=60)
    added_from = models.ForeignKey(Collection, null=True)
    from_user = models.ForeignKey(User, null=True)
    date_added = models.DateTimeField()
