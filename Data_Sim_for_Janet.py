import numpy as np

from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

#Data simulation algorithm
import statistics as stat

### Functions used in the Algorithm###


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
    
    #make sure conditions are satisfied
    if n % 2 != 0:
        return "n is not even"
    
    if n < 4:
        return "n is not greater then 4"
    
    
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
pair-wise with a probability of p.  Also keeps track of the number of switches 

    Returns
    -------
    Dictionary of colors switched based off the above rule, number of switches

    """
    
    #Select the pairs based of the probability selected
    number_switches = 0
    for pair in pair_list:
        #Determine whether flip is going to happen
        choice = np.random.choice(['Flip' , 'Dont Flip'] , p= [prob , 1-prob])
        #Condition on the exchange
        if choice == 'Flip':
            #Keep track of the total number of switches
            number_switches += 1
            x[pair[0]]['Flip'] = 'YES'
            x[pair[1]]['Flip'] = 'YES'

            #Switch the Color
            if x[pair[0]]['Color'] == 'BLUE':
                x[pair[0]]['Color'] = 'RED'
                x[pair[1]]['Color'] = 'BLUE'
                
                
            else:
                x[pair[0]]['Color'] = 'BLUE'
                x[pair[1]]['Color'] = 'RED'
        
        else:
             x[pair[0]]['Flip'] = 'NO'
             x[pair[1]]['Flip'] = 'NO'
        
    return x , number_switches

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


###END###

###Actual Algorithm###
def Data_Simulation_Algorithm(n , M , T , prob,beta):
    """
    

    Parameters
    ----------
    n : int
        Number of players
    
    M:int
      Initial balance of each BLUE players
    
    T:int
      Number of Periods algorithm runs for

    prob:float
        Probability a pair switches color during the switch routine
    
    beta:float
        Probability of the algorithm continuing after period T

    Returns
    -------
    distribution of balances at each period (min balance , max balance , mean, s.d)
    balance_data - List Tracking the balances for each player in each period
    color_data - List Tracking the color of each player in each period
    Tprime - The period in which algorithm ends 
    switch_data_individual- nested List Tracking whether the player switched or not 
    switch_data_cumulative- how many switches occured


    """
    #Check the conditions of n
    if n % 2 != 0:
        return "n is not even"
    
    if n < 4:
        return "n is not greater then 4"
    
    
    #First translate the period T into a list that can be looped over
    T_list = []
    for i in range(1 , T+1):
        T_list.append(i)
    
    #Intialize empty lists
    min_balance = []
    max_balance = []
    mean = []
    sd = []
    balance_data = []
    color_data = []
    switch_data_individual = []
    switch_data_cumulative = []
    #Given the first period, we need to intialize the players values
    
    for i in T_list:
        if i == 1:
            
            player_dict = intialization(n , M)
            
            

    #Now create the pairs via the matching routine
        pair_list = matchroutine(player_dict)

    #Using the list just created, activate the switch routine
        player_dict , number_switches = switchroutine(player_dict , pair_list , prob)

    #Activate the trade routine
        player_dict = trade_routine(player_dict , pair_list)
    
    #Activate the stop routine
        if i >= T:
            T_list = stoproutine(T_list , beta)
            
    
    #Produce the required statistics
    #Create list for balance
        balance_list = []
        color_list = []
        switch_list = []

        
        for i in range(1 , n+1):
            balance_list.append(player_dict[i]['Balance'])
            color_list.append(player_dict[i]['Color']) 
            switch_list.append(player_dict[i]['Flip'])
            
        
        min_balance.append(min(balance_list))
        max_balance.append(max(balance_list))
        mean.append(stat.mean(balance_list))
        sd.append(stat.stdev(balance_list))
        balance_data.append(balance_list)
        color_data.append(color_list)
        Tprime = len(balance_data)
        switch_data_individual.append(switch_list)
        switch_data_cumulative.append(number_switches)


    return min_balance , max_balance , mean , sd , balance_data , color_data , Tprime , switch_data_individual , switch_data_cumulative

###END###

###Testing outputs###
np.random.seed(0)
min_balance , max_balance , mean , sd , balance_data , color_data , Tprime , switch_data_individual , switch_data_cumulative = Data_Simulation_Algorithm(10 ,5 , 1000 , 0.9,0.75)

#Histogram plot
# Creating histogram
fig, ax = plt.subplots(figsize =(10, 7))
ax.hist(balance_data[999], bins = np.arange(25) - 0.5 ,alpha=0.7, rwidth=0.85)
ax.xaxis.set_major_locator(ticker.MultipleLocator(1))
 
# Show plot
plt.show()