# AI_final

from math import factorial
from math import floor
import random
from collections import Counter
"""
my_dice_status = [0,2,0,0,0,1,0]
hostile_player_num = 2
dice_amount_per_person = 3
min_amounts = [hostile_player_num + 1] * 7
flag_one = False
"""



# min_amounts: the list of the minimum yelling amount for each dice number
# my_dice_status: the list of the amount of my dice for each dice number e.g. [0,3,0,0,0,2,0] if I have three 1 and two 5.
# flag_one: True if someone already yelled one (True every since someone yelled one) 

# risk
class ProbAgent():
  def __init__(self, my_dice_status, hostile_player_num, dice_amount_per_person, risk_rate, catch_threshold, yell_one_prob,credibility_list):
    self.my_dice_status = my_dice_status
    self.hostile_player_num = hostile_player_num
    self.dice_amount_per_person = dice_amount_per_person
    self.flag_one = False
    self.min_amounts = [hostile_player_num + 1] * 7
    self.prob_dict = Counter()
    self.construct_prob_dict()
    self.yell_threshold = 0.0
    self.risk_rate = risk_rate
    self.catch_threshold = catch_threshold
    self.credibility_list = credibility_list
    self.yell_one_prob = yell_one_prob

  def combination(self,n,r):
    return factorial(n)/factorial(r)/factorial(n-r)

  
  def calculate_prob(self,n,r,prob):
    return self.combination(n,r) * pow(prob, r) * pow(1 - prob, n - r)

  def set_flag_one(self,flag_one):
    self.flag_one = flag_one

  def get_prob_dict(self):
    return self.prob_dict

  def show_prob_table(self,number = False):
    total = 0.0
    for letter, count in self.prob_dict.most_common(len(self.prob_dict)):
      if number == letter[1]:
        print letter,":",count
      total += count
    print total


  
  def construct_prob_dict(self):
    hostile_dice_amount = self.hostile_player_num * self.dice_amount_per_person
    min_amounts = [self.hostile_player_num + 1] * 7
    for dice_num in xrange(1,7):
      min_amount = min_amounts[dice_num]
      if self.flag_one or (dice_num == 1):
        prob = 1/6.0
        my_dice = self.my_dice_status[dice_num]
      else:
        prob = 1/3.0
        my_dice = self.my_dice_status[dice_num] + self.my_dice_status[1]
      for amount in xrange(hostile_dice_amount, min_amount - my_dice - 1, -1):
        if amount < 1 :
          self.prob_dict[(amount + my_dice, dice_num)] = 1
          continue
        self.prob_dict[(amount + my_dice, dice_num)] = self.calculate_prob(hostile_dice_amount, amount, prob) + self.prob_dict[(amount + my_dice + 1, dice_num)]  
    


  def combine_counter(self,counter_a, counter_b, w_a):
    a = Counter()
    b = Counter()
    w_b = 1 - w_a
    if counter_a:
      for element in counter_a:
        a[element] = w_a * counter_a[element]
    if counter_b:
      for element in counter_b:
        b[element] = w_b * counter_b[element]
    return a+b

  def choose_yell(self,yell = False):
    #print "yell:",yell
    yell_threshold = self.yell_threshold
    risk_rate = self.risk_rate
    qualify_dict = Counter()
    new_dict = Counter()

    """
    filter out valid yell
    """
    if yell != False:
      yell_amount,yell_point = yell
      for letter, count in self.prob_dict.most_common(len(self.prob_dict)):
        amount,point = letter
        if amount > yell_amount:
          qualify_dict[letter] = count
        
        if amount == yell_amount:
          if point > yell_point:
            qualify_dict[letter] = count
    else:
      qualify_dict = self.prob_dict

    """
    select probability greater than yell_threshold
    """
    for letter, count in qualify_dict.most_common(len(qualify_dict)):
      #print " Take:",yell," Qualified:",letter, count
      if count > yell_threshold:
        new_dict[letter] = count
    
    """
    select decision greater depend on risk rate
    """
    num_above_threshold = len(new_dict)
    if num_above_threshold == 0:
      return "CATCH"
    select_number = float(floor((num_above_threshold-1) * risk_rate) )
    yell_card = ()
    index = 0.0
    for letter, count in new_dict.most_common(num_above_threshold):
      
      if index == select_number:
        yell_card = letter
      index += 1.0

    return yell_card
    

  # yell: (dice_num, dice_amount)
  # credibility: the weighting of the probability status of the new yell 
  # flag_switch_one: True if this is the first round someone yells one (True only once in a game) 
  
  def make_decision(self,yell = False):

    catch_threshold = self.catch_threshold
    
    one_ratio = float(self.my_dice_status[1]) / float(self.dice_amount_per_person)
    yell_one_prob = self.yell_one_prob
    random.seed()
    random_num = random.random()
   

    if yell == False:

      """
      First Player
      """
      return (self.choose_yell(yell),False)
    else:
      yell_rate = self.prob_dict[yell]
      

      if yell_rate < catch_threshold:
        # print 'CATCH A'
        return ((0,0),True)

      elif yell_one_prob > random_num:
        return ((yell[0]+1,1),False)

      else:
        if self.choose_yell(yell) == "CATCH":
          # print 'CATCH B'
          return ((0,0),True)
        else:
          return (self.choose_yell(yell), False)


  def update_status(self,agent_nember,yell,flag_switch_one):
    credibility = self.credibility_list[agent_nember]
    self.update_prob_dict(credibility,yell,flag_switch_one)


  def update_prob_dict(self,credibility, yell,flag_switch_one):
    

    min_amounts = [yell[0]] * 7
    for dice_num in xrange(1,yell[1]):
      min_amounts[dice_num] = yell[0] + 1
    
    if flag_switch_one:
      self.set_flag_one(True)
      self.construct_prob_dict()

    if self.flag_one or (yell[1] == 1):
      needed = yell[0] - self.my_dice_status[yell[1]]
    else:
      needed = yell[0] - self.my_dice_status[yell[1]] - self.my_dice_status[1]

    if needed < 1: # the yell amount is too small to provide information
      return self.prob_dict
      
    hostile_dice_amount = self.hostile_player_num * self.dice_amount_per_person - needed # still un-decided dice amount
    new_dict = Counter()

    for dice_num in xrange(1,7):
      min_amount = min_amounts[dice_num]
      if self.flag_one or (dice_num == 1):
        prob = 1/6.0
        my_dice = self.my_dice_status[dice_num]
      else:
        prob = 1/3.0
        my_dice = self.my_dice_status[dice_num] + self.my_dice_status[1]
      if dice_num == yell[1]:
        my_dice = my_dice + needed
      for amount in xrange(hostile_dice_amount, min_amount - my_dice - 1, -1):
        if amount < 1:
          new_dict[(amount + my_dice, dice_num)] = 1
          continue
        new_dict[(amount + my_dice, dice_num)]  = self.calculate_prob(hostile_dice_amount, amount, prob) + new_dict[(amount + my_dice + 1, dice_num)]
    self.prob_dict = self.combine_counter(new_dict, self.prob_dict, credibility)


