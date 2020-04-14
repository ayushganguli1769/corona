from django.shortcuts import render,redirect
from django.http import HttpResponse
import json
from accounts.models import extendedUser
from . models import locationDetail
import pusher
from rest_framework import viewsets
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework import permissions
from rest_framework import authentication
from django.http import HttpResponse
from . serializer import locationSerializer,extendedUserSerializer,UserSerializer
from datetime import datetime
from django.contrib.auth.models import User, auth
import pytz
from django.utils import timezone
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime, timedelta
from datetime import datetime
import pytz

####firebase
import firebase_admin
from firebase_admin import credentials, firestore,db
import os, sys
import json
import ast
script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rel_path = "covid.json"
covid = os.path.join(script_dir, rel_path)
cred = credentials.Certificate(covid)
firebase_admin.initialize_app(cred)
db = firestore.client()
"""
#####################covid2

script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
rel_path = "covid2.json"
covid2 = os.path.join(script_dir, rel_path)
cred2 = credentials.Certificate(covid2)
firebase_admin.initialize_app(cred2)
db2 = firestore.client()

###########################
"""
###pusher
pusher_client = pusher.Pusher(
  app_id='967595',
  key='c73ea8196f369f3e7364',
  secret='3e271da7d6f8256557c1',
  cluster='ap2',
  ssl=True
)

####for nearest point import
from django.db.models.functions import Radians, Power, Sin, Cos, ATan2, Sqrt, Radians
from django.db.models import F
import math
from math import cos, sqrt
R = 6371000 #radius of the Earth in m
from math import radians, cos, sin, asin, sqrt 
from .tasks import xmyContactsTraceFunctionCaller
@api_view(['POST'])
def register(request):
    global db
    serialized = UserSerializer(data = request.data)
    print(request.data['password'])
    data = {}
    my_email = request.data['email']
    my_username = request.data['username']
    my_password = request.data['password']
    if User.objects.filter(username= my_username).exists():
        my_user = User.objects.get(username= my_username)
        if my_user.extendedUser.is_admin_added == True:
            data = {'sucess':"failed",'error':"Site administrator has already uploaded your case record. Please check with admin"}
            return Response( data= data,status= status.HTTP_400_BAD_REQUEST)
        data = {'sucess':"failed",'error':"Username already exists"}
        return Response( data= data,status= status.HTTP_400_BAD_REQUEST)
    if serialized.is_valid():
        user =User.objects.create_user(email= my_email, username= my_username, password =my_password)
        a = extendedUser.objects.get(user = user)
        try:
            a.status = request.data['status']
            a.save()
        except:
            a.status = None
            a.save()
        data = {'sucess':"sucess",'error':"None"}
        channel= "channel" + str(user.id)
        print(channel)
        doc_ref = db.collection(channel).document(channel)
        doc_ref.set({
            u'latitude':None,
            u'longitude':None,
            u'last_fetched': None,
        })
        return Response(data = data ,status= status.HTTP_200_OK)
    return Response(serialized.errors, status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def updateUserDetail(request):
    my_extend_user = extendedUser.objects.get(user = request.user)
    print(my_extend_user.user.username)
    data = {}
    try:
        my_extend_user.status = int(request.data['user_status_choices'])
        print(str(my_extend_user.user_status_choices) + "changed")
        my_extend_user.save()
        data['success'] = "updated successfully"
        print(my_extend_user.status)
        return Response(data = data, status= status.HTTP_200_OK)
    except:
        data['error'] = "Data for user status missing most probably"
        return Response(data = data, status= status.HTTP_400_BAD_REQUEST)

@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def inputLocation(request):
    global pubnub
    global db
    data = {}
    user = request.user
    serializer = locationSerializer(data= request.data)
    print(request.data)
    if serializer.is_valid():
        last_date = datetime.now()
        new_location = locationDetail(user = user,latitude = request.data['latitude'], longitude = request.data['longitude'],last_fetched = last_date)
        #please manage the server time setting later 
        new_location.save()
        data['success'] = "new location saved"
        channel = "channel"+ str(request.user.id)
        print(channel)
        #####db2
        doc_ref = db.collection(channel).document(channel)
        doc_ref.set({
            u'latitude':new_location.latitude,
            u'longitude':new_location.longitude,
            u'last_fetched': str(last_date),
        })
        ###############end db2
        """
        doc_ref = db.collection(u'main_data').document(channel)
        doc_ref.set({
            u'latitude':new_location.latitude,
            u'longitude':new_location.longitude,
            u'last_fetched': str(last_date),
        })
        """
        pusher_client.trigger(channel, 'my-event', {'latitude': new_location.latitude,'longitude':new_location.longitude,'last_fetch':str(last_date)})
        return Response(data = data ,status= status.HTTP_200_OK)
    return Response(serializer.errors, status= status.HTTP_400_BAD_REQUEST)

def test(request):
    data = []
    all_user = extendedUser.objects.filter(~Q(status = 5))
    my_user = extendedUser.objects.get(user = request.user)
    for extend_user in all_user:
        try:
            location_detail = locationDetail.objects.filter(user = extend_user.user).order_by('-id')[0]
            extend_user_latitude = location_detail.latitude
            extend_user_longitude = location_detail.longitude
            extend_user_last_fetch = location_detail.last_fetched
        except:
            extend_user_latitude = None
            extend_user_longitude = None
            extend_user_last_fetch = None
        user_coordinates = {'channel_id':extend_user.user.id,'status':extend_user.status,'username':extend_user.user.username,'latitude':extend_user_latitude,'longitude':extend_user_longitude,'last_fetch':extend_user_last_fetch}
        print(extend_user.user.username + " id = " +str(extend_user.user.id))
        data.append(user_coordinates)
    try:
        user_location_detail = locationDetail.objects.filter(user = request.user).order_by('-id')[0]
        user_latitude = user_location_detail.latitude
        user_longitude = user_location_detail.longitude
        user_last_fetch = user_location_detail.last_fetched
    except:
        user_latitude = None
        user_longitude = None
        user_last_fetch = None 
    user_coordinates = {'channel_id':request.user.id,'status':my_user.status,'username':request.user.username,'latitude':user_latitude,'longitude':user_longitude,'last_fetch':user_last_fetch}
    all_data = {'global_plotted_coordinates':data,'user_plotted_data':user_coordinates}
    return render(request,'table.html',{'all_data':all_data})
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def table(request):
    def distance(lat1, lon1, lat2, lon2):
        # The math module contains a function named 
        # radians which converts from degrees to radians. 
        lon1 = radians(lon1) 
        lon2 = radians(lon2) 
        lat1 = radians(lat1) 
        lat2 = radians(lat2) 
        
        # Haversine formula  
        dlon = lon2 - lon1  
        dlat = lat2 - lat1 
        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
    
        c = 2 * asin(sqrt(a))  
        
        # Radius of earth in kilometers. Use 3956 for miles 
        r = 6371
        
        # calculate the result 
        return(c * r) 
    global R
    data = []
    all_user = extendedUser.objects.filter(~Q(status = 5))
    my_user = extendedUser.objects.get(user = request.user)
    try:
        user_location_detail = locationDetail.objects.filter(user = request.user).last()
        user_latitude = user_location_detail.latitude
        user_longitude = user_location_detail.longitude
        user_last_fetch = user_location_detail.last_fetched
    except:
        user_latitude = None
        user_longitude = None
        user_last_fetch = None
    if  (user_latitude != None and user_longitude != None) or True:#remove or True here 
        for extend_user in all_user:
            extend_user_latitude = None
            extend_user_longitude = None
            extend_user_last_fetch = None
            try:
                if extend_user.user != request.user:
                    location_detail = locationDetail.objects.filter(user = extend_user.user).last()
                    extend_user_latitude = location_detail.latitude
                    extend_user_longitude = location_detail.longitude
                    extend_user_last_fetch = location_detail.last_fetched
            except:
                extend_user_latitude = None
                extend_user_longitude = None
                extend_user_last_fetch = None

            user_coordinates = {'channel_id':extend_user.user.id,'status':extend_user.status,'username':extend_user.user.username,'latitude':extend_user_latitude,'longitude':extend_user_longitude,'last_fetch':str(extend_user_last_fetch)}
            print(extend_user.user.username + " id = " +str(extend_user.user.id))
            if (extend_user_latitude != None and extend_user_longitude != None) and (distance(user_latitude,user_longitude,extend_user_latitude,extend_user_longitude)< 100 or True):#remove or True here
                #remove or True above
                data.append(user_coordinates)
        current_lat = user_latitude
        current_long = user_longitude
        if current_lat != None and current_long != None:
            data = sorted(data, key= lambda d: distance(d["latitude"], d["longitude"], current_lat, current_long),reverse = False)
        user_coordinates = {'channel_id':request.user.id,'status':my_user.status,'username':request.user.username,'latitude':user_latitude,'longitude':user_longitude,'last_fetch':str(user_last_fetch)}
        all_data = {'global_plotted_coordinates':data,'user_plotted_data':user_coordinates}
        print(all_data)
        return Response(all_data)
    else:
        data = {}
        data['error'] = "No latitude and longitude of user found"
        return Response(data= data,status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def admin_add_user_detail(request):# admin only view.Add cutom decorator
    if request.user.is_staff:
        latitude = request.data['latitude']
        longitude = request.data['longitude']
        last_fetch = datetime.now()
        username = request.data['username']
        status = request.data['status']
        my_email = request.data['email']
        global db
        #serialized = UserSerializer(data = request.data)
        data = {}
        my_username = "autoCreated" + request.data['username']
        my_password = "auto1234"
        user =User.objects.create_user(email= my_email, username= my_username, password =my_password)
        anonymous_extendUser = extendedUser.objects.get(user = user)
        anonymous_extendUser.status = status
        anonymous_extendUser.save()
        anonymous_location = locationDetail(user = user, latitude = latitude, longitude = longitude,last_fetched = last_fetch)
        anonymous_location.save()
        data['sucess'] = "anonymous user created"
        channel= "channel" + str(user.id)
        print(channel)
        doc_ref = db.collection(u'main_data').document(channel)
        doc_ref.set({
            u'latitude':latitude,
            u'longitude':longitude,
            u'last_fetched': str(last_fetch),
        })
        return Response(data = data)
    else:
        data = {}
        data['error'] = "not a staff user"
        from rest_framework import status
        return Response(data= data, status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def pathtracing(request,user_id):
    if request.user.is_staff:
        track_user = User.objects.get(id = user_id)
        all_past_location = locationDetail.objects.filter(user= track_user).order_by('-id')
        data = []
        for location in all_past_location:
            past_loc = {'user':location.user.username,'latitude':location.latitude,'longitude':location.longitude,'last_fetched':str(location.last_fetched),'id':location.id}
            data.append(past_loc)
        return Response(data)
    else:
        data = {}
        data['error'] = "not a staff user"
        return Response(data= data, status= status.HTTP_400_BAD_REQUEST)
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def search_user(request):
    if request.user.is_staff:
        data = []
        uname = request.data['username']
        all_users = all_user = User.objects.filter(username__contains= uname)[:10]
        for user in all_user:
            instance_user = {'username':user.username,'id':user.id}
            data.append(instance_user)
        return Response(data)
    else:
        data = {}
        data['error'] = "not a staff user"
        return Response(data= data, status= status.HTTP_400_BAD_REQUEST)

def template_search_user(request,username):
    if request.user.is_staff:
        data = []
        uname = username
        queryset = (Q(username__icontains= uname))
        all_users = all_user = User.objects.filter(queryset).distinct()
        for user in all_user:
            type = None
            if user.extendedUser.status == 1:
                type = "COVID POSITIVE"
            elif user.extendedUser.status == 2:
                type = "Show Symptoms"
            elif user.extendedUser.status == 3:
                type = "Travel History Abroad"
            elif user.extendedUser.status == 4:
                type = "Close Contact"
            elif user.extendedUser.status == 5:
                type = "Normal User"
            else:
                type = "Unknown" 
            instance_user = {'username':user.username,'id':user.id,'status':type}
            data.append(instance_user)
        return HttpResponse(json.dumps(data))
    else:
        data = {}
        data['error'] = "not a staff user"
        return HttpResponse("error")
@login_required
def template_pathtracing(request,user_id):
    if request.user.is_staff:
        try:
            track_user = User.objects.get(id = user_id)
        except:
            raise Http404("User does not exist")
        all_past_location = locationDetail.objects.filter(user= track_user).order_by('-last_fetched')
        data = []
        for location in all_past_location:
            past_loc = {'user':location.user.username,'latitude':location.latitude,'longitude':location.longitude,'last_fetched':str(location.last_fetched),'id':location.id}
            data.append(past_loc)
        try:
            first_data = data[0]
        except:
            first_data = None
        try:
            first_location = data[0]
        except:
            first_location = None
        return render(request,'pathTracing.html',{'all_data':data,'first_data':first_data,'username':track_user.username,'first_location':first_location})
    else:
        data = {}
        data['error'] = "not a staff user"
        raise Http404("Not a Staff User")

@login_required
def template_admin_add_user_detail(request):# admin only view.Add cutom decorator
    if request.user.is_staff:
        if 'add' in request.POST:
            latitude = request.POST['latitude']
            longitude = request.POST['longitude']
            last_fetch = datetime.now()
            username = request.POST['username']
            status = request.POST['status']
            my_email = request.POST['email']
            global db
            #serialized = UserSerializer(data = request.data)
            data = {}
            my_username = "autoCreated" + request.POST['username']
            my_password = "auto1234"
            user =User.objects.create_user(email= my_email, username= my_username, password =my_password)
            anonymous_extendUser = extendedUser.objects.get(user = user)
            anonymous_extendUser.status = status
            anonymous_extendUser.save()
            anonymous_location = locationDetail(user = user, latitude = latitude, longitude = longitude,last_fetched = last_fetch)
            anonymous_location.save()
            data['sucess'] = "anonymous user created"
            channel= "channel" + str(user.id)
            print(channel)
            doc_ref = db.collection(u'main_data').document(channel)
            doc_ref.set({
                u'latitude':latitude,
                u'longitude':longitude,
                u'last_fetched': str(last_fetch),
            })
            return render(request,'admin_add_user.html',{'msg':"New User Added"})
        return render(request,'admin_add_user.html')
    else:
        data = {}
        data['error'] = "not a staff user"
        from rest_framework import status
        return render(request,'admin_add_user.html',{'msg':"Not a staff user"})
@login_required
def search_page(request):
    return render(request,'search.html')
def home(request):
    return render(request,'home.html')
@csrf_exempt
def api_admin_add_user_detail(request,latitude,longitude,status,username,my_email):# admin only view.Add cutom decorator
    if request.user.is_staff:
        latitude = float(latitude)
        longitude = float(longitude)
        global db
        #serialized = UserSerializer(data = request.data)
        data = {}
        my_username = "autoCreated" + username
        my_password = "auto1234"
        user =User.objects.create_user(email= my_email, username= my_username, password =my_password)
        anonymous_extendUser = extendedUser.objects.get(user = user)
        anonymous_extendUser.status = status
        anonymous_extendUser.save()
        last_fetch = datetime.now()
        anonymous_location = locationDetail(user = user, latitude = latitude, longitude = longitude,last_fetched = last_fetch)
        anonymous_location.save()
        data['sucess'] = "anonymous user created"
        channel= "channel" + str(user.id)
        print(channel)
        doc_ref = db.collection(u'main_data').document(channel)
        doc_ref.set({
            u'latitude':latitude,
            u'longitude':longitude,
            u'last_fetched': str(last_fetch),
        })
        return HttpResponse("added")
    else:
        data = {}
        data['error'] = "not a staff user"
        from rest_framework import status
        return HttpResponse("not_staff")
@api_view(['POST','GET'])
@permission_classes([IsAuthenticated])
def user_individual_track(request):
    try:
        my_user = User.objects.get(id = request.data['channel'])
    except:
        data = {}
        data['error'] = "user not found"
        return Response(data= data, status= status.HTTP_400_BAD_REQUEST)
    location_detail = locationDetail.objects.filter(user = my_user).last()
    user_latitude = location_detail.latitude
    user_longitude = location_detail.longitude
    data = {
        'latitude' : user_latitude,
        'longitude' : user_longitude
    }
    return Response(data = data ,status= status.HTTP_200_OK)
def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username, password = password)
        if user != None :
            if user.is_staff:
                auth.login(request,user)
                return redirect('/tracker/add/')
            else:
                return render(request,'login.html',{'error_message':"Not a staff user"})

        else:
            return render(request, 'login.html', {'error_message': "Invalid Credentials"})
    return render(request,'login.html')
def add(request):
    return render(request,'admin_add_user.html')
    #code for single user path tracing. I'll find the chain later
def distance(lat1, lon1, lat2, lon2):
    # The math module contains a function named 
    # radians which converts from degrees to radians. 
    lon1 = radians(lon1) 
    lon2 = radians(lon2) 
    lat1 = radians(lat1) 
    lat2 = radians(lat2) 
    
    # Haversine formula  
    dlon = lon2 - lon1  
    dlat = lat2 - lat1 
    a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2

    c = 2 * asin(sqrt(a))  
    
    # Radius of earth in kilometers. Use 3956 for miles 
    r = 6371
    
    # calculate the result 
    return(c * r) 
"""
Not using this code
@api_view(['POST','GET'])
def contactTracingHelper(request,user_id):
    try:
        my_user = User.objects.get(id= user_id)
    except:
        dict = {}
        dict['error'] = "User not found"
        return Response(data= dict, status= status.HTTP_400_BAD_REQUEST)
    x,y = contactTracing(my_user)
    x_data = []
    for contact_user in x:
        x_data.append(contact_user.username)
    dict = {'contact':x_data,'contacts_time_trace':y}
    return Response(data=dict, status= status.HTTP_200_OK)
def contactTracing(my_user):#direct contact tracing algo
    if my_user == None:
        return ([],[])
    contacts = []
    contacts_time_trace = []
    all_user_locations = locationDetail.objects.filter(user =my_user)
    for instance_loc in all_user_locations:
        lower_limit = instance_loc.last_fetched - timedelta(hours=5)
        upper_limit = instance_loc.last_fetched + timedelta(hours=5)
        loc_near_instance_loc = locationDetail.objects.filter(~Q(user=my_user),Q(last_fetched__gte= lower_limit),Q(last_fetched__lte= upper_limit))
        for x_user in loc_near_instance_loc:
            if  x_user.user != my_user and distance(instance_loc.latitude,instance_loc.longitude,x_user.latitude,x_user.longitude) < 2 :
                if x_user.user not in contacts:
                    contacts.append(x_user.user)
                time_trace = {'user':x_user.user.username,'time_first_contact_index_user':str(instance_loc.last_fetched),'time_first_contact_contacted_user':str(x_user.last_fetched),'index_user_latitude':instance_loc.latitude,'index_user_longitude':instance_loc.longitude,'contact_user_latitude':x_user.latitude,'contact_user_longitude':x_user.longitude}
                contacts_time_trace.append(time_trace)
    return (contacts,contacts_time_trace)
"""
def addPath(request,user_id):
    import datetime
    my_user = User.objects.get(id= user_id)
    if 'addCoordinates' in request.POST:
        print("submit clicked")
        total = int(request.POST['totalCount'])
        if total == 0:
            return render(request,'addPathDetail.html',{'user_id':user_id,'message':"No location entry were provided",'my_user':my_user})
        for i in range(1,total+1,1):
            name_lat = "latitude"+ str(i)
            print(name_lat)
            name_long= "longitude"+ str(i)
            name_year = "year" + str(i)
            name_month = "month" + str(i)
            name_day = "day" + str(i)
            name_hour = "hour"+ str(i)
            name_minute = "minute" + str(i)
            print(request.POST['latitude1'])
            latitude = float(request.POST[name_lat])
            longitude = float(request.POST[name_long])
            year = int(request.POST[name_year])
            month = int(request.POST[name_month])
            day = int(request.POST[name_day])
            hour = int(request.POST[name_hour])
            minute = int(request.POST[name_minute])
            timezone =  pytz.timezone("Asia/Kolkata")
            combined_time = datetime.datetime(year,month,day,hour,minute, tzinfo = timezone)
            new_location_object = locationDetail(user = my_user,latitude=latitude,longitude=longitude,last_fetched= combined_time)
            new_location_object.save()
        return render(request,'addPathDetail.html',{'user_id':user_id,'message':"Successfully Saved",'my_user':my_user})
    return render(request,'addPathDetail.html',{'user_id':user_id,'my_user':my_user})
def contactTracingHelper(request,user_id,parent_node,option):
    from datetime import datetime
    user = User.objects.get(id= user_id)
    user_locations = locationDetail.objects.filter(user= user)
    User_Match = []
    timezone =  pytz.timezone("UTC")
    channel_name = "admin" + str(request.user.id)
    start_date = datetime(2020, 1, 1, 0, 0, 0, 0,tzinfo = timezone)
    #start_date= datetime(2020,1,1,0,0,0 tzinfo = timezone)
    for location in user_locations:
        user_location_time = location.last_fetched
        time_diff = (user_location_time - start_date).total_seconds()
        attribute = [location.latitude,location.longitude,time_diff]
        User_Match.append(attribute)
    #print(User_Match)
    not_user_locations = locationDetail.objects.filter(~Q(user= user))
    User_Complete = []
    for location in not_user_locations: 
        user_location_time = location.last_fetched
        time_diff = (user_location_time - start_date).total_seconds()
        attribute = [location.latitude,location.longitude,time_diff,location.user.id]
        User_Complete.append(attribute)
    #print(User_Complete)
    #print(User_Complete)
    xmyContactsTraceFunctionCaller(User_Match,User_Complete,channel_name,user_id,option)
    return HttpResponse("ok")
def contact(request,user_id):
    if request.user.is_staff:
        user = User.objects.get(id = user_id)
        return render(request,'contact.html',{'my_user':user})
    else:
        raise Http404("Unathorized")
    
