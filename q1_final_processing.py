#!/usr/bin/env python
'''
q1_final_processing.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 2
  Date of Last Update: March 29, 2022

  Functional Summary
      Extracting data within preprocessed data file that is within given date range.
'''

#Import necessary libraries
import sys
import csv
import re
import datetime

'''
Populates dictionary of all public health units, calculates the percent 
positivity (from ICES_positivity.csv) and test availability (from test_availability.csv ). Outputs dictionary contents to final_positivity_by_test.csv under the headers 
PHU,AVG_POS,AVG_TEST.
'''
def final_processing_q1(dates):
  # make sure required data is there
  if len(dates) != 3:
    print("Run with start and end dates: final_positivity_by_test.py <start date> <end date>", file=sys.stderr)
    sys.exit()
  # extract dates from arguments
  try:
    date_str = re.split("-", dates[1])
    start_date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]) )
    
    date_str = re.split("-", dates[2])
    end_date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]) )
  except:
    print("Run with start and end dates: final_positivity_by_test.py <start date> <end date> where dates are formatted yyyy-mm-dd", file=sys.stderr)
    sys.exit()
  # dictionary to be populated with file data
  phus = {2226: {"name":"ALG", "pos":0, "test":0, "weeks":0}, 2227:{"name":"BRN", "pos":0, "test":0, "weeks":0}, 2240:{"name":"CKH", "pos":0, "test":0, "weeks":0}, 2230:{"name":"DUR", "pos":0, "test":0, "weeks":0}, 2258:{"name":"EOH", "pos":0, "test":0, "weeks":0}, 2233:{"name":"GBH", "pos":0, "test":0, "weeks":0}, 2236:{"name":"HAL", "pos":0, "test":0, "weeks":0}, 2237:{"name":"HAM", "pos":0, "test":0, "weeks":0}, 2235:{"name":"HKP", "pos":0, "test":0, "weeks":0}, 2234:{"name":"HNH", "pos":0, "test":0, "weeks":0}, 2238:{"name":"HNH", "pos":0, "test":0, "weeks":0}, 5183:{"name":"HPH", "pos":0, "test":0, "weeks":0}, 2241:{"name":"KFL", "pos":0, "test":0, "weeks":0}, 2242:{"name":"LAM", "pos":0, "test":0, "weeks":0}, 2243:{"name":"LGL", "pos":0, "test":0, "weeks":0}, 2244:{"name":"MSL", "pos":0, "test":0, "weeks":0}, 2246:{"name":"NIA", "pos":0, "test":0, "weeks":0}, 2247:{"name":"NPS", "pos":0, "test":0, "weeks":0}, 2249:{"name":"NWR", "pos":0, "test":0, "weeks":0}, 2251:{"name":"OTT", "pos":0, "test":0, "weeks":0}, 2253:{"name":"PEL", "pos":0, "test":0, "weeks":0}, 2255:{"name":"PET", "pos":0, "test":0, "weeks":0}, 2256:{"name":"PQP", "pos":0, "test":0, "weeks":0}, 2257:{"name":"REN", "pos":0, "test":0, "weeks":0}, 2275:{"name":"SWH", "pos":0, "test":0, "weeks":0}, 2260:{"name":"SMD", "pos":0, "test":0, "weeks":0}, 2261:{"name":"SUD", "pos":0, "test":0, "weeks":0}, 2262:{"name":"THB", "pos":0, "test":0, "weeks":0}, 3895:{"name":"TOR", "pos":0, "test":0, "weeks":0}, 2263:{"name":"TSK", "pos":0, "test":0, "weeks":0}, 2265:{"name":"WAT", "pos":0, "test":0, "weeks":0}, 2266:{"name":"WDG", "pos":0, "test":0, "weeks":0}, 2268:{"name":"WEK", "pos":0, "test":0, "weeks":0}, 2270:{"name":"YRK", "pos":0, "test":0, "weeks":0}}
  # open positivity rate file
  filename = "data/q1/preprocessed_data/ICES_positivity.csv"
  try:
    positivity_fh = open(filename, encoding="utf-8-sig")
  except:
    print("Unable to open {}".format(filename), file=sys.stderr)
    sys.exit()
  
  positivity_csv = csv.reader(positivity_fh);
  #remove heading row
  next(positivity_csv)
  # list of dates for graph
  dates = []
  # get positivity rate and weeks in question
  for phu in positivity_csv:
    date_str = re.split("-", phu[1])
    date = datetime.date(int(date_str[0]), int(date_str[1]), int(date_str[2]))
    if date >= start_date and date <= end_date:
      phus[float(phu[0])]["pos"] += float(phu[2])
      phus[float(phu[0])]["weeks"] += 1
      dates.append(phu[1])
  positivity_fh.close()
  #open testing availability file
  filename = "data/q1/preprocessed_data/test_availability.csv"
  try:
    test_availability_fh = open(filename, encoding="utf-8-sig")
  except:
    print("Unable to open {}".format(filename), file=sys.stderr)
    sys.exit()
    
  test_availability_csv = csv.reader(test_availability_fh)
  next(test_availability_csv)
  #get test availability per week, weeks provided by ICES_positivity
  for phu in test_availability_csv:
    if int(phu[0]) in phus:
      if phu[1] in dates:
        phus[float(phu[0])]["test"] += float(phu[2])
  try:
    f = open("data/processed_data/final_positivity_by_test.csv", "w")
  except:
    print("Unable to open {}".format("data/processed_data/final_positivity_by_test.csv"), file=sys.stderr)
    sys.exit()
  # write to output file
  f.write("PHU,AVG_POS,AVG_TEST\n")
  for phu in phus:
    try:
      f.write(phus[phu]["name"]+"," + str(phus[phu]["pos"] /phus[phu]["weeks"])+"," + str(phus[phu]["test"] /  phus[phu]["weeks"]) + "\n")
    except:
      print("Unable to output data for  {}".format(phu), file=sys.stderr)
  f.close()