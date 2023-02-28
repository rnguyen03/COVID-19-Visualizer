#!/usr/bin/env python
'''
q4_preprocessing.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 2
  Date of Last Update: March 27, 2022

  Functional Summary
      Extracting data from statscan data files relating causes of death and 
      number of deaths by age group.
'''

#Import necessary libraries
import sys
import csv
import re

def preprocessQ4():
  #dict relating causes of death with years lost due to cause of death
  deaths = {}
  
  #open each file, determine median age, calculate years lot for each cause and add to data structure
  filepath = "data/q4/"
  file_prefix = "causes_of_death_"
  #relate median age with each age defined file
  filesuffix = {0:["1_14", 7], 1:["15_24", 19], 2:["25_34", 29], 3:["35_44",39], 4:["45_54",49], 5:["55_64", 59]}
  #open all files (causes fo death by age group) and append data to dict of all causes of death
  for suffix in filesuffix:
    #open file
    filename = filepath + file_prefix + filesuffix[suffix][0] + ".csv"
    try:
      death_file = open(filename, encoding="utf-8-sig")
    except:
      print("Unable to open {}".format(filename))
      sys.exit()
    #create csv reader
    death_file_csv = csv.reader(death_file)
    #move through unneeded data at the beginning of the file    
    data = next(death_file_csv)
    while data[0] != 'Total, all causes of death  [A00-Y89]':
      data = next(death_file_csv)
      
    id = 0 #cause of death id
    #extract data
    for death in death_file_csv:
      #check for end of usable data
      if death[0] == 'Symbol legend:': #denotes end of usable data
        break
      #get cause of death string
      cause = re.search("[a-zA-Z() ]+", death[0])
      if cause != None:
        cause = cause.group()
      else:
        continue
      #get rank
      rank = death[2]
      #number of deaths on next line
      death = next(death_file_csv)
      number_of_deaths = death[2]
      if id not in deaths:
        deaths[id] = {}
      deaths[id]["cause"] = cause.rstrip()
      deaths[id]["rank"] = rank
      number_of_deaths = number_of_deaths.replace(",", "")
      try:
        years_lost = (65 - int(filesuffix[suffix][1])) * int(number_of_deaths)
      except:
        print("Error: syntaxt error in {}".format(filename), file=sys.stderr)
        sys.exit()
      #if years lost has already been added to dict, add years lost
      # else, add to dict as is
      if "years_lost" in deaths[id]:
        deaths[id]["years_lost"] += years_lost
      else:
        deaths[id]["years_lost"] = years_lost
      # increment unique id
      id = id +1
  # output data 
  print("ID,CAUSE,RANK,NUMBER_OF_DEATHS")
  for death in deaths:
    print(str(death) + "," + deaths[death]["cause"] + "," + deaths[death]["rank"] + "," + str(deaths[death]["years_lost"]))

def main(argv):
  preprocessQ4()
  
main(sys.argv)

