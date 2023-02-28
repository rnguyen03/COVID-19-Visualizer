#!/usr/bin/env python
'''
q1_ICES_preprocessing.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 13, 2022

  Functional Summary
      Extracting data from the ICES csv files.
'''

#Import necessary libraries

import sys
import csv
import os
import re
import datetime

def get_date(date_string):
  months = {
    "Jan": 1,
    "Feb": 2,
    "Mar": 3,
    "Apr": 4,
    "May": 5,
    "Jun": 6,
    "Jul": 7,
    "Aug": 8,
    "Sep": 9,
    "Oct": 10,
    "Nov": 11,
    "Dec": 12
    }
  match = re.findall("[\d]+", date_string) 
  #get day and year
  try:
    day = int(match[0])
    year = int(match[1])
  except:
    print("error")
    sys.exit(0)
  #get month
  month_string = re.search("[A-Za-z]+", date_string)
  try:
    month = months[month_string[0]]
  except:
    print("error")
    sys.exit(0)
  #create date object
  date_object = datetime.date(year, month, day)
  return date_object

def main(argv):
  #PHU name abbreviations
  PHU_names = {"ALG": 2226, "BRN":2227, "CKH":2240, "DUR":2230, "EOH":2258, "GBH":2233, "HAL":2236, "HAM":2237, "HKP":2235, "HNH":2234, "HPE":2238, "HPH":5183, "KFL":2241, "LAM":2242, "LGL":2243,  "MSL":2244, "NIA":2246, "NPS":2247, "NWR":2249, "OTT":2251, "PEL":2253, "PET":2255, "PQP":2256, "REN":2257, "SWH":2275,"SMD":2260, "SUD":2261, "THB":2262, "TOR":3895, "TSK":2263, "WAT":2265, "WDG":2266, "WEK":2268, "YRK":2270}
  # filename + path
  search_path = "data/q1/ICES_case_by_age/"
  generic_filename = "_ICES-COVID19-Testing-Data_PHUxAge-Groups-percent-positivity"
  #loop through each file, open file and extract
  #end of week date and positivity rate for
  #those over 18
  for PHU_abbreviation in PHU_names:
    positivity_filename = PHU_abbreviation + generic_filename
    # finding and creating full data set file path
    for filename in os.listdir(path=search_path):
      if (filename.find(positivity_filename) != -1):
        current_filename = search_path + filename
    #open file
    try:
      open_file = open(current_filename, encoding="utf-8-sig")
    except IOError as err:
      print("Unable to open names file '{}' : {}".format(
              current_filename, err), file=sys.stderr)
      sys.exit(1)  
    #create csv reader
    positivity_rate_reader = csv.reader(open_file)
    #for each row in file extract data if age range is 18+
    for row in positivity_rate_reader:
      if row[0] == '18+':
        date = get_date(row[2])
        print(str(PHU_names[PHU_abbreviation]) + "," +str(date) + "," + row[3][0:len(row[3]) - 1])

main(sys.argv)