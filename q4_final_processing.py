#!/usr/bin/env python
'''
q4_final_processing.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Retrieve data from preprocessed file pertaining to diseases specified by argv.
      Output to data/processed_data/covid_vs_disease_years_lost
'''
import csv
#argv is a string of cause of death IDs in the format <idj idj + 1..idn> where
#n is less then or equal to 51
def processQ4(argv):
  # USER MUST SPECIFY CAUSE OF DEATH IDS  
  if len(argv) < 2:
    print("please specify disease IDs")
  # OPEN FILE
  data = "data/q4/preprocessed_data/q4_preprocessed.csv"

  try:
    data_fh = open(data)
  except:
    print("Unable to open {}".format(data))
  #create csv reader
  data_csv = csv.reader(data_fh)
  #discard header
  next(data_csv)
  try:
    f = open("data/processed_data/covid_vs_disease_years_lost.csv", "w")
  except:
    print("Unable to open {}".format("data/processed_data/covid_vs_disease_years_lost.csv"))
  #create next header
  f.write("ID,CAUSE,RANK,NUMBER_OF_DEATHS\n")
  #go through all rows in file
  for cause in data_csv:
    #if user specified cause of death by id, output to processed data
    if cause[0] in argv:
      f.write(cause[0] + "," + cause[1] +","+cause[2] + "," + cause[3] + "\n")
