# AI_final

from math import factorial
from collections import Counter

my_dice_status = [0,2,0,0,0,1,0] # I have two 1, one 5
hostile_player_num = 2
dice_amount_per_player = 5
min_amounts = [hostile_player_num + 1] * 7
flag_one = False

def combination(n,r):
  return factorial(n)/factorial(r)/factorial(n-r)

  
def calculate_prob(n,r,prob):
  return combination(n,r) * pow(prob, r) * pow(1 - prob, n - r)


# min_amounts: the list of the minimum yelling amount for each dice number
# my_dice_status: the list of the amount of my dice for each dice number e.g. [0,3,0,0,0,2,0] if I have three 1 and two 5.
# flag_one: True if someone already yelled one (True every since someone yelled one) 
def construct_prob_dict(my_dice_status, hostile_player_num, dice_amount_per_player, flag_one, min_amounts):
  hostile_dice_amount = hostile_player_num * dice_amount_per_player
  prob_dict = Counter()
  for dice_num in xrange(1,7):
    min_amount = min_amounts[dice_num]
    if flag_one or (dice_num == 1):
      prob = 1/6.0
      my_dice = my_dice_status[dice_num]
    else:
      prob = 1/3.0
      my_dice = my_dice_status[dice_num] + my_dice_status[1]
    for amount in xrange(hostile_dice_amount, min_amount - my_dice - 1, -1):
      if amount < 1 :
        prob_dict[(amount + my_dice, dice_num)] = 1
        continue
      prob_dict[(amount + my_dice, dice_num)] = calculate_prob(hostile_dice_amount, amount, prob) + prob_dict[(amount + my_dice + 1, dice_num)]  
  return prob_dict



def combine_counter(counter_a, counter_b, w_a):
  a = Counter()
  b = Counter()
  w_b = 1 - w_a
  for element in counter_a:
    a[element] = w_a * counter_a[element]
  for element in counter_b:
    b[element] = w_b * counter_b[element]
  return a+b


prob_dict = construct_prob_dict(my_dice_status, hostile_player_num, dice_amount_per_player, flag_one, min_amounts)
credibility = 0.3
yell = (8,5)
flag_one = False
flag_switch_one = False

# yell: (dice_amount, dice_num)
# credibility: the weighting of the probability status of the new yell 
# flag_switch_one: True if this is the first round someone yells one (True only once in a game) 
def update_prob_dict(prob_dict, credibility, yell, my_dice_status, hostile_player_num, dice_amount_per_player, flag_one, flag_switch_one):
  min_amounts = [yell[0]] * 7
  for dice_num in xrange(1,yell[1]):
    min_amounts[dice_num] = yell[0] + 1
  
  if flag_switch_one:
    prob_dict = construct_prob_dict(my_dice_status, hostile_player_num, dice_amount_per_player, True, min_amounts)

  if flag_one or (dice_num == 1):
    needed = yell[0] - my_dice_status[yell[1]]
  else:
    needed = yell[0] - my_dice_status[yell[1]] - my_dice_status[1]

  if needed < 1: # the yell amount is too small to provide information
    return prob_dict
    
  hostile_dice_amount = hostile_player_num * dice_amount_per_player - needed # still un-decided dice amount
  new_dict = Counter()

  for dice_num in xrange(1,7):
    min_amount = min_amounts[dice_num]
    if flag_one or (dice_num == 1):
      prob = 1/6.0
      my_dice = my_dice_status[dice_num]
    else:
      prob = 1/3.0
      my_dice = my_dice_status[dice_num] + my_dice_status[1]
    if dice_num == yell[1]:
      my_dice = my_dice + needed
    for amount in xrange(hostile_dice_amount, min_amount - my_dice - 1, -1):
      if amount < 1:
        new_dict[(amount + my_dice, dice_num)] = 1
        continue
      new_dict[(amount + my_dice, dice_num)]  = calculate_prob(hostile_dice_amount, amount, prob) + new_dict[(amount + my_dice + 1, dice_num)]
  prob_dict = combine_counter(new_dict, prob_dict, credibility)
  return prob_dict

  
