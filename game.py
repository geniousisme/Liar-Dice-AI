A_dice_status = [0,2,1,1,0,1,0]
B_dice_status = [0,1,1,2,1,0,0]
C_dice_status = [0,2,0,1,0,2,0]

hostile_player_num = 2
dice_amount_per_person = 5
flag_one = False
risk_rate = 0
yell_threshold = 0.5
catch_threshold = 0.2

A_Agent = ProbAgent(A_dice_status,hostile_player_num,dice_amount_per_person,flag_one,0.8,0.5,0.2)
B_Agent = ProbAgent(B_dice_status,hostile_player_num,dice_amount_per_person,flag_one,0.5,0.3,0.1)
C_Agent = ProbAgent(C_dice_status,hostile_player_num,dice_amount_per_person,flag_one,0.5,0.5,0.1)


#A_Agent.show_prob_table()
decision = A_Agent.make_decision()
print decision

B_Agent.update_status(1,decision[0],False)
C_Agent.update_status(1,decision[0],False)

decision = B_Agent.make_decision(decision[0])
print decision
A_Agent.update_status(2,decision[0],False)
C_Agent.update_status(2,decision[0],False)

decision = C_Agent.make_decision(decision[0])
print decision
A_Agent.update_status(3,decision[0],False)
B_Agent.update_status(3,decision[0],False)