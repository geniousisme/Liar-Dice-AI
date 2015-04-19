# Liar-Dice-AI
AI project which simulate the credibility of each player in liar dice game

#指令說明：

*python liarDice.py:
只跑一次，單純看結果＆print log

*python liarDice.py -q -t 500:
-q: quiet, 把print都關掉，只顯示最後統計數據
-t: 表示要traing or 統計了，500表示跑500次

*python liarDice.py -q -t 500 -l 2:
-l: 表示要使用學習演算法，2表示我們後來新開發的演算法，只能選 1 or 2

*python liarDice.py -q -t 500 -l 2 -agentB 0.7 -agentC 0.1:
-agentB & -agentC: 
透過command line直接改agentB & agentC的riskRate，0.7表示愛亂喊(喊發生機率很小的牌面組合)，0.1表示不愛亂喊(喊發生機率很大的牌面組合)
