#!/usr/bin/env python
# coding: utf-8

# # Probable Spatial Direction Determination of Epidemic Spread

# In[1]:


### Importing Libraries

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt


# In[36]:


### Defining Variables and Constants

n = 18 # No. of Divisions of a region
l = 360/n # Arc Angle
W = np.zeros((n,1)) # Weighting Matrix
person_index = np.array([0,1,2]) # Matrix of Class of Person; With 0-Not Affected,1-Foreign_Travel/Symptoms and 2-COVID-19_positive

N = 2 # No of people
Tau = 2 # Threshold of Meetings

Person = [0 for d in range(N)] # 1-D vector representing person_index of a person 
Meeting = [[[0 for a in range(N)],[0 for b in range(N)]] for c in range(n)] # 3-D Matrix of dimesion N*N*n; with it's (i,j,l)th entry showing time for which person i and person j met in nth arc  
Carry_Matrix = [[[0 for a in range(N)],[0 for b in range(N)]] for c in range(n)] # 3-D Matrix of dimension N*N*n with (i,j,l)th entry being considered 1 to meet of ith person with jth person is considered

probability = np.array([[0,0],[0.7,0.65],[0.9,0.85]]) # Probabilities 


# In[44]:


### Defining Spatial_Probable Function

# While Initializing this function Carry_Matrix must be set to zero matrix of dimensions being N*N*n ie. No. of total people*No. of total people*No. of total arcs

def Spatial_Probable(Person,Meeting,Carry_Matrix,n,N,probability,Tau):
    
       # "Function to Output W - Weighting Matrix with taking following inputs:-
       # "Person - 1-D vector representing person_index of a person"
       # "Meeting - 3-D Matrix of dimesion N*N*n containing data about meetings; If (i,j)th entry of Meeting matrix is 1 for nth channel then ith person met with jth person in the nth arc" 
       # "Carry_Matrix - 3-D Matrix of dimesion N*N*n with (i,j,n) entry being considered 1 to meet of ith person with jth person is considered"
       # "n - Number of arcs"
       # "N - Total Number of people"
       # "probability - Matrix containing various probabilities of spread"
       # "Tau - Threshold of Meeting"
    
    ## Converting Lists into arrays
    Person = np.array(Person)
    Meeting = np.reshape(np.array(Meeting),(N,N,n))
    Carry_Matrix = np.reshape(np.array(Carry_Matrix),(N,N,n))
    
    ## Producing a Dummy Weighting Matrix
    W_dummy = np.zeros((N,N,n))
    
    ## Implementing the function
    
    for channel_number in range(n):
        for entity_1 in range(N):
            for entity_2 in range(N):
                if(Meeting[entity_1,entity_2,channel_number] != 0):
                    if(Carry_Matrix[entity_1,entity_2,channel_number] == 0):
                        if(Person[entity_1] > Person[entity_2]):
                            entity_class = Person[entity_1]
                            if(Meeting[entity_1,entity_2,channel_number]>Tau):
                                prob_class = 0
                            else:
                                prob_class = 1
                            W_dummy[entity_1,entity_2,channel_number] = probability[entity_class,prob_class]
                        elif(Person[entity_2] > Person[entity_1]):
                            entity_class = Person[entity_2]
                            if(Meeting[entity_1,entity_2,channel_number]>Tau):
                                prob_class = 0
                            else:
                                prob_class = 1
                            W_dummy[entity_1,entity_2,channel_number] = probability[entity_class,prob_class]
                        else:
                            W_dummy[entity_1,entity_2,channel_number] = 0
                    Carry_Matrix[entity_1,entity_2,channel_number] = 1
                    Carry_Matrix[entity_2,entity_1,channel_number] = 1
                    
    ## Computation of W from W_dummy
    W = np.sum(np.sum(W_dummy,axis=0),axis=0)
    
    ## Returning W
    return W       

