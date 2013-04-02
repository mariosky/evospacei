# Create your views here.
# Python
import urllib
import urlparse

import cgi, json
import datetime
import ast
import itertools

import redis
# Django
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect, HttpResponse
from django.conf import settings
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

# Project
from shapes import models
from shapes.models import Collection, User_Collection, Collection_Individual, FacebookSession
from lib.evospace import Population, Individual
from lib.colors import init_pop, evolve_Tournament



EVOLUTION_INTERVAL = 2
REINSERT_THRESHOLD = 20
popName='pop'

@csrf_exempt
def evospace(request):
    if  request.method == 'POST':
            population = Population(popName)
            #print 'Raw Data___: "%s"' % request.body
            #print type(request.body)
            json_data = json.loads(request.body)
            method = json_data["method"]
            params = json_data["params"]
            id     = json_data["id"]
            
            if method == "initialize":
                result = population.initialize()
                data = json.dumps({"result" : result,"error": None, "id": id})
                print data
                return HttpResponse(data, mimetype='application/javascript')
            elif method == "getSample":
                #Auto ReInsert
                if population.read_sample_queue_len() >= REINSERT_THRESHOLD:
                    population.respawn(5)
                result = population.get_sample(params[0])
                if result:
                    data = json.dumps({"result" : result,"error": None, "id": id})
                else:
                    data = json.dumps({"result" : None,"error":
                                        {"code": -32601, "message": "EvoSpace empty"}, "id": id})    
                return HttpResponse(data, mimetype='application/json')
            elif method == "read_pop_keys":
                result = population.read_pop_keys()
                if result:
                    data = json.dumps({"result" : result,"error": None, "id": id})
                else:
                    data = json.dumps({"result" : None,"error":
                        {"code": -32601, "message": "EvoSpace empty"}, "id": id})
                return HttpResponse(data, mimetype='application/json')
            elif method == "read_sample_queue":
                result = population.read_sample_queue()
                if result:
                    data = json.dumps({"result" : result,"error": None, "id": id})
                else:
                    data = json.dumps({"result" : None,"error":
                        {"code": -32601, "message": "EvoSpace empty"}, "id": id})
                return HttpResponse(data, mimetype='application/json')

            elif method == "putSample":
                #Cada EVOLUTION_INTERVAL evoluciona
                if not population.get_returned_counter() % EVOLUTION_INTERVAL:
                    evolve_Tournament()
                population.put_sample(params[0])
                return HttpResponse(json.dumps("Success"), mimetype='application/json')
            elif method == "init_pop":
                data = init_pop(populationSize=params[0])
                return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
            elif method == "respawn":
                data = population.respawn(n=params[0])
                return HttpResponse(json.dumps("Success"), mimetype='application/javascript')
            elif method == "put_individual":
                print  "params",params[0]
                population.put_individual(**params[0])
                data = json.dumps({"result" : None,"error": None, "id": id})
                return HttpResponse(data, mimetype='application/json')


    else:
        return HttpResponse("ajax & post please", mimetype='text')
            
#@ensure_csrf_cookie            
def home(request):
    if request.user.is_authenticated():
        #REFACTOR GET_FRIENDS
        face =FacebookSession.objects.get(uid=request.user.username)
        friends = face.query("me",connection_type="friends",fields='name,installed')

        if friends:
        # Mejor con FQL
            app_friends = [f for f in friends['data'] if f.has_key('installed')]
        else:
            app_friends = None
    else:
        app_friends = None

    return render_to_response('django_index.html', {'static_server': 'https://s3.amazonaws.com/evospace/prototype/',
      'api_server':'http://app.evospace.org','friends':app_friends},context_instance=RequestContext(request) )



def individual_view(request,individual_id):
    key = "pop:individual:%s" % (individual_id)
    individual =  Individual(id=key).get(as_dict=True)
    mama = None
    papa = None
    if "mama" in individual:
        mama = Individual(id=individual["mama"]).get(as_dict=True)

    if "papa" in individual:
        papa = Individual(id=individual["papa"]).get(as_dict=True)


    individual_json = json.dumps(individual)

    return render_to_response('individual.html', {'static_server': 'http://evospace.org/prototype/',
      'api_server':'http://app.evospace.org', 'individual':individual, 'individual_json':individual_json,'mama':mama,'papa':papa},context_instance=RequestContext(request) )





def facebook_get_login(request):
    state = request.session.session_key
    url = """https://www.facebook.com/dialog/oauth?client_id=%s&redirect_uri=%s&state=%s""" % \
              (settings.FACEBOOK_APP_ID ,settings.FACEBOOK_REDIRECT_URL,
               state
                )

    return HttpResponseRedirect(url)

def facebook_login(request):


    if 'error' in request.GET:
        return HttpResponseRedirect('/')


    code = request.GET['code']
    UID = request.GET['state']

    args = { "client_id" : settings.FACEBOOK_APP_ID,
             "redirect_uri" : settings.FACEBOOK_REDIRECT_URL ,
             "client_secret" : settings.FACEBOOK_APP_SECRET,
             "code" : code }

    response = urllib.urlopen( "https://graph.facebook.com/oauth/access_token?" + urllib.urlencode(args))
    response = urlparse.parse_qs(response.read())
    access_token = response["access_token"][-1]
    profile = json.load(urllib.urlopen(
        "https://graph.facebook.com/me?" +
        urllib.urlencode(dict(access_token=access_token))))
    expires = response['expires'][0]

    facebook_session = models.FacebookSession.objects.get_or_create(
        access_token=access_token)[0]

    facebook_session.expires = expires
    facebook_session.save()

    user = authenticate(token=access_token)
    if user:
        if user.is_active:
            login(request, user)
            return HttpResponseRedirect('/')
        else:
            error = 'AUTH_DISABLED'

    if 'error_reason' in request.GET:
        error = 'AUTH_DENIED'
    ### TO DO Log Error
    return HttpResponseRedirect('/')


@login_required
def logout_view(request):
    # Log a user out using Django's logout function and redirect them
    # back to the homepage.
    logout(request)
    return HttpResponseRedirect('/')

@csrf_exempt
def add_collection(request, username):
    global message
    errors = []
    if request.method == 'POST':

        #users=User.objects.all();
        #u1=User.objects.get(username=username)
        #u=users[0]

        n=request.POST['name']
        d=request.POST['description']
        v=request.POST['visibility']

        c = Collection(name=n,
            description=d,
            creation_date=datetime.datetime.now(),
            visibility=v
        )
        c.save()
        #c_id=Collection.objects.latest('id')
        #c_id=c_id.id
        #u_id=u1.id

        #if User.objects.get(id=u_id) and Collection.objects.get(id=c_id):
            #u=User.objects.get(id=u_id)
            #c=Collection.objects.get(id=c_id)
        uc= User_Collection(user=request.user,
                collection=c,
                role="O",
                status="PU"
            )
        uc.save()
        message= "You are now linked to this collection!"
        #else:
        #    message= "Sorry there is no collection or user"
            #add_user_collection(id,c_id)
        #col= Collection.objects.all()

        data=({'name':n,'description':d,'visibility':v, 'message':message})
        datar=json.dumps(data)


    return HttpResponse(datar, mimetype='application/json')

def get_user_collections(request, username):

    if User.objects.get(username=username):
        u1=User.objects.get(username=username)
        u_id=u1.id
        uc=Collection.objects.all().filter(user_collection__user_id__exact=u_id)
        jd = { 'collections': [{'id': col.id, 'name':col.name} for col in uc]}
        j=json.dumps(jd)
    return HttpResponse(j, mimetype='application/json')


def get_collection(request, username, collection= None):

    if request.user.is_authenticated():

        #REFACTOR GET_FRIENDS
        face =FacebookSession.objects.get(uid=request.user.username)
        friends = face.query("me",connection_type="friends",fields='name,installed')
        # Mejor con FQL
        app_friends = [f for f in friends['data'] if f.has_key('installed')]

        face_owner =FacebookSession.objects.get(uid=username)

        url = 'https://graph.facebook.com/%s?fields=name' % username
        owner = face_owner.query("me",fields='name')
        #owner = json.load(urllib.urlopen(url))
        print username, owner

        r = redis.Redis(host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB)
        if collection:
            inds_psql = Collection.objects.get(user_collection__user__username=username,id=collection).individuals.all()
            collection_obj = Collection.objects.get(id=collection)

        else:
            collections = Collection.objects.filter(user_collection__user__username=username,visibility='PU' )
            lists_of_inds =[ind for ind  in [ col.individuals.all() for col in collections]]
            inds_psql = list( itertools.chain.from_iterable(lists_of_inds) )

            collection_obj = None

        inds = [ {"id":r["id"],"chromosome":r["chromosome"]} for r in
                 [ ast.literal_eval(i) for i in
                   [ r.get(ind_.individual_id) for ind_ in inds_psql ] if i
                 ]
        ]

        #inds = [ (i["id"], i["chromosome"]) for i in [ r.get(ind_.individual_id) for ind_ in inds_psql ] if i ]
        j =json.dumps(inds)
        return render_to_response('collection.html', {'static_server': 'http://evospace.org/prototype/',
                                                      'api_server':'http://app.evospace.org',
                                                      'individualsjs':j,'individuals':inds,
                                                       'collection_obj':collection_obj,"friends":app_friends,
                                                       'owner':owner
                                                        },
            context_instance=RequestContext(request) )
    else:
        return HttpResponse('noup')



@csrf_exempt
def add_ind_to_col(request, username):
    global message
    if request.method == 'POST':

        if  request.user.is_authenticated():

            u1=User.objects.get(username=username)
            u=User.objects.get(id=u1.id)



            col=request.POST['collection']
            ind=request.POST['individual']

            c=Collection.objects.get(id=col)

            itc=Collection_Individual( collection=c,
                 individual_id=ind,
                 added_from=c,
                 from_user=u,
                 date_added=datetime.datetime.now())

            itc.save()
            message="Individual is now added to this collection!"
        else:
            message="No username in evoart!"


        data=({'collection':col,'individual':ind, 'message':message})
        datar=json.dumps(data)


    return HttpResponse(datar, mimetype='application/json')


def dashboard(request):
    return render_to_response('dashboard.html', {'static_server': 'http://evospace.org/prototype/',
            'api_server':'http://app.evospace.org'},context_instance=RequestContext(request) )
