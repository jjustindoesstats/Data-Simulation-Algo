# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""
#Data simulation algorithm
import numpy as np 


#Color Partition
#Define a function that initializes list
def intialization(n, M):
    """
    

    Parameters
    ----------
    n : int
        Number of players (>= 4)
    M : int
        Number of balance points per players (>=2)

    Returns
    -------
    Dictionary with key being BLUE or RED value being the balance
    Blue should have balance = M and Red should have balance = 0

    """
    
    #Fill dictionary with RED or BLUE
    
    x = {}

    #initialize red
    for i in np.arange(1 , n/2 + 1):
        x[i] = {}
        x[i]['Color'] = 'RED'
        x[i]['Balance'] = 0
    
    #Initialize blue
    for i in np.arange(n/2 + 1 , n+1):
       x[i] = {}
       x[i]['Color'] = 'BLUE'
       x[i]['Balance'] = M
    

    #Merge both into nested dictionary
    return x

        
        
#Create color partition dictionary
def colorpartition(x , n):
    """
    

    Parameters
    ----------
    n : int
        Represents number of players (must be even and must be >=4 and eqaul to len(x))
    x : dict
        represents dictionary of players
    Returns
    -------
    Changes entries that are 'BLUE' to 'RED'  and vice versa

    """
    for i in np.arange(1,n+1):
        if x[i]['Color'] == 'RED':
            x[i]['Color'] = 'BLUE'
        
        else:
            x[i]['Color'] = 'RED'
    
    return x
        
#Coding the matching routine algorithm
def matchroutine(x):
    """
    

    Parameters
    ----------
    x : dict
        dictionary storing the color and balance of each player

    Returns
    -------
    list of pairs corresponding to the matching routine setup
    Each pair should have one blue and one red and only be included once
    

    """
    #Create empty lists to fill (one for blue, another for red)
    blue = []
    red = []
    
    #Loop through the dictionary and start filling the blue list
    for key in range(1, len(x)+1):
        if x[key]['Color'] == 'BLUE':
            blue.append(key)
            
        else:
            red.append(key)
    
    #Create empty list that we will fill with the pairs
    pair_list = []
    
    for i in range(len(red)):
        #randomly select an element from blue
        
        z = np.random.choice(blue)
        
        
        #insert both the element from red and the element chossen from blue
        pair_list.append([red[i] , z])
        
        #Delete item from blue
        blue.remove(z)
        
        
            
    return pair_list
        

#Create the switch routine algoritm
def switchroutine(x , pair_list , prob):
    """
    

    Parameters
    ----------
    x : dict
        dictionary storing the color and balance of each player
    pair_list : list
        RED/BLUE pairs outputted from the matching routine
    p: Float
       Probability of a pair exchanging colors
    

Description: Takes dictionary and pairlist and exchanges the color identity
pair-wise with a probability of p 

    Returns
    -------
    Dictionary of colors switched based off the above rule

    """
    
    #Select the pairs based of the probability selected
    for pair in pair_list:
        #Determine whether flip is going to happen
        choice = np.random.choice(['Flip' , 'Dont Flip'] , p= [prob , 1-prob])
        #Condition on the exchange
        if choice == 'Flip':
            if x[pair[0]]['Color'] == 'BLUE':
                x[pair[0]]['Color'] = 'RED'
                x[pair[1]]['Color'] = 'BLUE'
                
            else:
                x[pair[0]]['Color'] = 'BLUE'
                x[pair[1]]['Color'] = 'RED'
        
    return x

#Code in trade routine algorithm

def trade_routine(x , pair_list):
    """
    

    Parameters
    ----------
    x : dict
        Dictionary of players and their associated balances and colors
    pair_list : list
        Represents the pairs from the matching routine
        
Description:Exchanges balances pairwise by 1 (BLUE gives to RED) if
BLUES balance>1 otherwise no exchange

    Returns
    -------
    x

    """
    #Loop through the pairs_list
    for i in pair_list:
        if x[i[0]]["Color"] == 'BLUE':
            if x[i[0]]["Balance"] >= 1 :
                x[i[0]]["Balance"] = x[i[0]]["Balance"] - 1
                x[i[1]]["Balance"] = x[i[1]]["Balance"] + 1
        else:
            if x[i[1]]["Balance"] >= 1 :
                x[i[0]]["Balance"] = x[i[0]]["Balance"] + 1
                x[i[1]]["Balance"] = x[i[1]]["Balance"] - 1
    return x

                
                
#Code in the Stop Routine
def stoproutine(T , beta):
    """
    

    Parameters
    ----------
    T : list
        List of periods in which the simulation algorithm loops through

Description:Implements the stopping routine, appends an extra period
depending on the beta probability
    
    
    Returns
    -------
    T

    """
    choice = np.random.choice(['STOP' , 'GO'] , p = [1-beta , beta])
    #If the algorithm keeps going, add another element to the list (period + 1)
    if choice == 'GO':
        T.append(T[-1] + 1)
    
    return T
    
y = intialization(10,10)

y
