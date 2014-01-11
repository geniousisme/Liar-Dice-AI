class UpdateStatusClass():

  def __init__(self, result, history_lists, credibility_list, learning_rate):
    self.result = result
    self.history_lists = history_lists
    self.credibility_list = credibility_list
    self.learning_rate = learning_rate

  def calcErrorDistance(self, yell_value, flag_one):
    distance = 0
    dice_amount,dice_point = yell_value
    
    if flag_one == False and dice_point != 1:
      one_amount = self.result[0][0]

      for result_element in self.result:
        result_dice_amount,result_dice_point = result_element
        if result_dice_point == dice_point:
          distance = abs(result_dice_amount + one_amount - dice_amount)
      
    else:    
      for result_element in self.result:
        result_dice_amount,result_dice_point = result_element
        if result_dice_point == dice_point:
          distance = abs(result_dice_amount-dice_amount)
     
    return distance


  def calcDistanceFromHistory(self,history_list):
    total_distance = 0
    total_number = 0
    for history in history_list: 
      yell_value,flag_one = history
      
      distance = self.calcErrorDistance(yell_value,flag_one)
      total_distance += distance
      total_number += 1
    average_distance = float(total_distance)/float(total_number)
    return average_distance

  def calcDistanceFromHistoryList(self):
    
    total_distances = []
    
    for key,history_list in self.history_lists.items():
      total_distance = self.calcDistanceFromHistory(history_list)
      total_distances.append(total_distance)
    

    
    
    sum_distance = sum(total_distances)
    average_distance = sum_distance/len(total_distances)
    max_distance = max(total_distances)

    
    for index in range(len(total_distances)):
      total_distances[index] = float(total_distances[index] - average_distance) / float(sum_distance)


    for index in range(len(self.credibility_list)):
      new_value = self.credibility_list[index] - (total_distances[index]* self.learning_rate)
      if new_value > 0 and new_value < 1:
        self.credibility_list[index] = new_value
    
    #print total_distances
    return self.credibility_list
    #print max_distance

  
result = [(2,1),(3,2),(1,3),(1,4),(1,5),(1,6)]
A_history = {1:[((1,2),False),((3,2),True)],2:[((2,2),False),((3,4),True)],3:[((3,1),True)]}

#old credibility_list
credibility_list = [0.34,0.2,0.5]
print credibility_list
#construct a class
learning = UpdateStatusClass(result,A_history,credibility_list,0.8)
#calculate new credibility_list
new_credibility_list = learning.calcDistanceFromHistoryList()
print new_credibility_list
