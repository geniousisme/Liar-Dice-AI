# AI_final

from math import factorial
from math import floor
from collections import Counter
from random import random, randrange

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


class ProbAgent():
  def __init__(self, my_dice_status, hostile_player_num, dice_amount_per_person, flag_one, yell_threshold,risk_rate,catch_threshold):
    self.my_dice_status = my_dice_status
    self.hostile_player_num = hostile_player_num
    self.dice_amount_per_person = dice_amount_per_person
    self.flag_one = flag_one
    self.min_amounts = [hostile_player_num + 1] * 7
    self.prob_dict = Counter()
    self.construct_prob_dict()
    self.yell_threshold = yell_threshold
    self.risk_rate = risk_rate
    self.catch_threshold = catch_threshold
    self.credibility_list = {1:0.1,2:0.1,3:0.1}

  def combination(self,n,r):
    return factorial(n)/factorial(r)/factorial(n-r)

  
  def calculate_prob(self,n,r,prob):
    return self.combination(n,r) * pow(prob, r) * pow(1 - prob, n - r)

  def set_flag_one(self,flag_one):
    self.flag_one = flag_one

  def get_prob_dict(self):
    return self.prob_dict

  def show_prob_table(self):
    for letter, count in self.prob_dict.most_common(len(self.prob_dict)):
      print letter,":",count

  
  def construct_prob_dict(self):
    hostile_dice_amount = self.hostile_player_num * self.dice_amount_per_person
    min_amounts = [hostile_player_num + 1] * 7
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
    for element in counter_a:
      a[element] = w_a * counter_a[element]
    for element in counter_b:
      b[element] = w_b * counter_b[element]
    return a+b

  def choose_yell(self,yell = False):
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
  
  def make_decision(self, yell = False):
    catch_threshold = self.catch_threshold
    yell_one_threshold = 0.9

    if yell == False:

      """
      First Player
      """
      return self.choose_yell(yell)
    else:
      yell_rate = self.prob_dict[yell]
      
      print yell_rate

      if yell_rate < catch_threshold:
        return "CATCH!"
      elif yell_rate < yell_one_threshold:
         
        return (yell[0]+1,1)

      else:
        
        return self.choose_yell(yell)
  
  
  # pyk
  #3. Given catch_prob(can increase when game goes on), if don't catch then with follow_prob follow or randon yell a number, wuth yell_one_prob yell one
  def make_decision_method_3(self, yell = False, follow_prob = 0.4, yell_one_prob = 0):
    one = random()
    if yell == False: #First Player
      if one < yell_one_prob:
        dice_num = 1
      else:
        dice_num = randrange(2,7)
      return (self.hostile_player_num + 1, dice_num)
    catch_prob = pow(0.5, max(0, 0.5 * (self.hostile_player_num + 1) * self.dice_amount_per_person - yell[0]))
    catch = random()
    follow = random()
    if catch < catch_prob:
      return "CATCH!"
    elif follow < follow_prob:
      return (yell[0]+1, yell[1])
    else:
      if one < yell_one_prob:
        dice_num = 1
      else:
        dice_num = randrange(2,7)
      
      if dice_num > yell[1]:
        return (yell[0], dice_num)
      else:
        return (yell[0]+1, dice_num)
  
  
  def update_status(self, agent_nember, yell, flag_switch_one):
    credibility = self.credibility_list[agent_nember]
    self.update_prob_dict(credibility, yell, flag_switch_one)


  def update_prob_dict(self, credibility, yell, flag_switch_one):
    min_amounts = [yell[0]] * 7
    for dice_num in xrange(1,yell[1]):
      min_amounts[dice_num] = yell[0] + 1
    
    if flag_switch_one:
      self.set_flag_one(True)
      self.prob_dict = self.construct_prob_dict()

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




A_dice_status = [0,2,1,1,0,1,0]
B_dice_status = [0,1,1,2,1,0,0]
C_dice_status = [0,0,0,1,0,2,2]

result = [(A_dice_status[1]+B_dice_status[1]+C_dice_status[1],1),(A_dice_status[2]+B_dice_status[2]+C_dice_status[2],2),(A_dice_status[3]+B_dice_status[3]+C_dice_status[3],3),(A_dice_status[4]+B_dice_status[4]+C_dice_status[4],4),(A_dice_status[5]+B_dice_status[5]+C_dice_status[5],5),(A_dice_status[6]+B_dice_status[6]+C_dice_status[6],6)]

hostile_player_num = 2
dice_amount_per_person = 5
flag_one = False
risk_rate = 0
yell_threshold = 0.5
catch_threshold = 0.2

A_Agent = ProbAgent(A_dice_status,hostile_player_num,dice_amount_per_person,flag_one,0.8,0.0,0.2)
B_Agent = ProbAgent(B_dice_status,hostile_player_num,dice_amount_per_person,flag_one,0.5,0.3,0.1)
C_Agent = ProbAgent(C_dice_status,hostile_player_num,dice_amount_per_person,flag_one,0.5,0.0,0.1)


#A_Agent.show_prob_table()
decision = A_Agent.make_decision_method_3()
print "A:",decision
B_Agent.update_status(1,decision,False)
C_Agent.update_status(1,decision,False)

while (not decision == "CATCH!" and decision[0] < (hostile_player_num + 1) * dice_amount_per_person):
  decision = B_Agent.make_decision_method_3(decision)
  print "B:",decision
  if decision == "CATCH!":
    break
  A_Agent.update_status(2,decision,False)
  C_Agent.update_status(2,decision,False)

  decision = C_Agent.make_decision_method_3(decision)
  print "C:",decision
  if decision == "CATCH!":
    break
  A_Agent.update_status(3,decision,False)
  B_Agent.update_status(3,decision,False)

  decision = A_Agent.make_decision_method_3(decision)
  print "A:",decision
  if decision == "CATCH!":
    break
  B_Agent.update_status(1,decision,False)
  C_Agent.update_status(1,decision,False)

  
  
  
  
"""
#A_Agent.show_prob_table()
decision = A_Agent.make_decision()
print decision
B_Agent.update_status(1,decision,False)
C_Agent.update_status(1,decision,False)

decision = B_Agent.make_decision(decision)
print decision
A_Agent.update_status(2,decision,False)
C_Agent.update_status(2,decision,False)

decision = C_Agent.make_decision(decision)
print decision
A_Agent.update_status(3,decision,False)
B_Agent.update_status(3,decision,False)

decision = A_Agent.make_decision(decision)
print decision
B_Agent.update_status(1,decision,False)
C_Agent.update_status(1,decision,False)

decision = B_Agent.make_decision(decision)
print decision
"""