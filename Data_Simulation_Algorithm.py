#Final Data simulation code
import Data_Simulation_Code as DSC
import statistics as stat


def Data_Simulation_Algorithm(n , M , T , prob , beta):
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
    distribution of balances at each period (min balance , max balance , mean, s.d , balance_data_red , balance_data_blue)

    """
    #First check the conditions on n
     #make sure conditions are satisfied
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
    #Given the first period, we need to intialize the players values
    
    for i in T_list:
        if i == 1:
            player_dict = DSC.intialization(n , M)
    
    #If the period is anytime after the first, activate the Color Partition step
        else:
            player_dict = DSC.colorpartition(player_dict , n)

    #Now create the pairs via the matching routine
        pair_list = DSC.matchroutine(player_dict)

    #Using the list just created, activate the switch routine
        player_dict = DSC.switchroutine(player_dict , pair_list , prob)

    #Activate the trade routine
        player_dict = DSC.trade_routine(player_dict , pair_list)
    
    #Activate the stop routine
        if i >= T:
            T_list = DSC.stoproutine(T_list , beta)
            
    
    #Produce the required statistics
    #Create list for balance
        balance_list = []
        for i in range(1 , n+1):
            balance_list.append(player_dict[i]['Balance']) 
        
        min_balance.append(min(balance_list))
        max_balance.append(max(balance_list))
        mean.append(stat.mean(balance_list))
        sd.append(stat.stdev(balance_list))
        balance_data.append(balance_list)

    return min_balance , max_balance , mean , sd , balance_data
        




