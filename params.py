#encoding:utf-8
# -*- coding: utf-8 -*- 
Tang  = 1
Chuan = 2
def agentParamsOf(agentName):
  riskRate = catchThreshold = yellOneProb = 0.0
  if agentName == 'A':
    riskRate       = 0.1  #risk rate = 0:會挑所有能喊的骰子裡面，機率最高的；risk rate = 1，代表挑裡面機率最小的那個
    catchThreshold = 0.1  #對手機率若低於這個數就抓對方，若不抓就喊
    yellOneProb    = 0.0  #0:不會喊一
  if agentName == 'B':
    riskRate       = 0.5
    catchThreshold = 0.1
    yellOneProb    = 0.0
  if agentName == 'C':
    riskRate       = 0.0
    catchThreshold = 0.1
    yellOneProb    = 0.0

  return  [ riskRate, catchThreshold, yellOneProb ]

def learningRate(choice):
  if choice == Tang:
    learningRate = 0.8
  if choice == Chuan:
    learningRate = 0.005
  return learningRate