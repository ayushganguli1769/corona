from background_task import background
####Aman's code library import
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from datetime import datetime as dt
import datetime as dt
###pusher
import pusher
from django.contrib.auth.models import User
pusher_client = pusher.Pusher(
  app_id='967595',
  key='c73ea8196f369f3e7364',
  secret='3e271da7d6f8256557c1',
  cluster='ap2',
  ssl=True
)

@background(schedule=1)
def xmyContactsTraceFunctionCaller(User_Match,User_Complete,channel_name,parent_node,option):
    print("execution started")
    print(channel_name)

    # Note:-
    # 1. One may merge Filter and Trace_Contacts Function
    # 2. Date_Threshold and Time_Threshold are to be selected as per convinience
    # In[41]:


    ### Defining Variables
    #N = None # Total No. of Users
    #N1 = None # Total entries of user being matched
    #N2 = None # Total entries of all the users except the on being traced
    #User_Match = [[0,0,0] for a in range(N1)]# Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
    #User_Complete = [[0,0,0,0] for b in range(N2)] # Matrix of location data of all other users except the user in User_Match . Information in columns is that of lattitude, longitude, Timestamp and Unique ID


    # In[42]:


    ### Data Preprocessing : Filtering User_Complete Matrix

    def Filter(User_Match,User_Complete):
        
        """
        Function to filter out nearby entries from User_Complete Matrix
        
        Inputs :
        User_Match - Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
        User_Complete -  Matrix of location data of all other users except the user in User_Match . Information in columns is that of lattitude, longitude, Timestamp and Unique ID
        
        Returns :
        User_Filtered -  Matrix of only filtered entries for User_Match
        
        """
        # Array Conversion
        User_Match = np.array(User_Match)
        User_Complete = np.array(User_Complete)
        
        # Initializing List
        User_Filtered = []
        
        # Computing Bounding Box
        x_max = np.max(User_Match[:,0])
        x_min = np.min(User_Match[:,0])
        y_max = np.max(User_Match[:,1])
        y_min = np.min(User_Match[:,1])
        
        Bounding_Box = [x_max,x_min,y_max,y_min]
        
        # Filtering User_Complete
        for i in range(User_Complete.shape[0]):
            if(User_Complete[i,0] <= x_max and User_Complete[i,0] >= x_min and User_Complete[i,1] <= y_max and User_Complete[i,1] >= y_min):
                User_Filtered.append(User_Complete[i])
        
        # Forming Array and Returning User_Filtered
        User_Filtered = np.array(User_Filtered)
        return User_Filtered


    # In[50]:


    ### Distance Calculator

    def distance(origin, destination):
    
        lat1, lon1 = origin
        lat2, lon2 = destination
        radius = 6371 # km

        dlat = math.radians(lat2-lat1)
        dlon = math.radians(lon2-lon1)
        a = math.sin(dlat/2) * math.sin(dlat/2) + math.cos(math.radians(lat1))         * math.cos(math.radians(lat2)) * math.sin(dlon/2) * math.sin(dlon/2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = radius * c

        return d

    # In[58]:


    ### Tracing Contact

    def Trace_Contact(User_Match,User_Filtered,Distance_Threshold,Time_Threshold):
        
        """
        Function to return a list of UniqueID with whom entity in User_Match met with
        
        Inputs : 
        User_Match - Matrix of the user being matched. Information in columns is that of lattitude, longitude and Timestamp
        User_Filtered -  Matrix of only filtered entries for User_Match
        Distance_Threshold - Threshold of Maximum Spatial Seperation in Kms
        Time_Threshold - Threshold of Maximum Time Separation in seconds
        
        Ouputs :
        User_Contacts - List of UniqueIDs of other users with whom entity in User_Match met
        
        """
        
        # Initializing User_Contacts and other lists as arrays
        User_Contacts = []
        User_Match = np.array(User_Match)
        from datetime import datetime as dt
        
        # Defining Trace Contacts Function's Mechanism
        for i in range(np.array(User_Match).shape[0]):
            for j in range(User_Filtered.shape[0]):
                if(distance(User_Match[i,0:2],User_Filtered[j,0:2]) <= Distance_Threshold):
                    if(User_Match[i,2]>User_Filtered[j,2]):
                        if(((User_Match[i,2])-(User_Filtered[j,2])) <= Time_Threshold):
                            User_Contacts.append(User_Filtered[j])
                    elif(User_Match[i,2]<User_Filtered[j,2]):
                        if(((User_Filtered[j,2])-(User_Match[i,2])) <= Time_Threshold):
                            User_Contacts.append(User_Filtered[j])
                    else:
                        User_Contacts.append(User_Filtered[j])
                        
        # Returning User_Contacts
        User_Contacts = np.array(User_Contacts)
        return User_Contacts           


    # In[ ]:


    ### Testing

    # Defining 2-D List of dimensions (N1,(LAT,LONG,TIMESTAMP)) and (N2,(LAT,LONG,TIMESTAMP,INDEX)) for User_Match and User_Complete respectively : First filtering by backend database must be done
    # Basically User_Match is the matrix(List) which is to be assigned for the User whoose contacts are being traced
    # User_Complete is the matrix(List) which contains (LAT,LONG,TIMESTAMP,INDEX) info of all other except the user whoose contacts are being traced

    #############Main driver code over here
    User_Filtered = Filter(User_Match,User_Complete)

    # Function for getting Output

    Traced_Contacts = Trace_Contact(User_Match,User_Filtered,100,2000)
    print(Traced_Contacts.tolist())
    unique_contacts = []
    unique_contacts_with_username = []
    for object_contact in Traced_Contacts.tolist():
        if object_contact[3] not in unique_contacts:
            user_unique = User.objects.get(id= object_contact[3])
            unique_contacts.append(object_contact[3])
            unique_contacts_with_username.append([object_contact[3],user_unique.username])
    pusher_client.trigger(channel_name, 'my-event', {'data':Traced_Contacts.tolist(),'unique_contacts':unique_contacts_with_username,'parent_id':parent_node,'option':option})