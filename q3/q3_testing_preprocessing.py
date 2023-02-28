'''
q3_testing_preprocessing.py
  Author(s): Charlotte Barnes(1154105),
             Tia Yun Fat Jeffrey Ronan Chay Loong(1181166),
             Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Preprocesses the testing data by extracting the relevant data
'''

import sys
import csv
import os
import math

# Global Constants
PREPROCESSED_FILENAME = "q3_testing_data_by_phu"
FILE_TYPE = ".csv"

def main():
  #finding testing data set file
  search_path = "data/q3/"
  testing_filename = "testing_metrics_by_phu"
  for filename in os.listdir(path=search_path):
    if (filename.find(testing_filename) != -1):
      full_filename = search_path + filename
  # opening testing file for read
  try:
    file_pointer = open(full_filename, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              full_filename, err), file=sys.stderr)
    sys.exit(0)
  file_reader = csv.reader(file_pointer)

  # initializing final preprocessed file
  search_path = "data/q3/preprocessed_data/"
  filename = search_path + PREPROCESSED_FILENAME + FILE_TYPE
  file_writer = open(filename, "w")
  print("Date,PHU_num,num_negative_7d_average",
         file = file_writer)
  
  # extracting data through file
  for row_data in file_reader:
    if row_data[0] == "DATE":
      continue

    # getting data from row
    date = row_data[0]
    phu_num = row_data[1]
    percent_positive = row_data[3]
    test_volumes = row_data[4]

    # removing comma
    test_volumes = test_volumes.replace(",", "")

    #converting to int
    try:
      percent_positive = float(percent_positive)
      test_volumes = int(test_volumes)
    except ValueError:
      print("Problem with data format - {}", row_data)
      continue

    # finding num negative tests
    percent_negative = 1 - percent_positive
    num_negative_tests = percent_negative * test_volumes
    num_negative_tests = int(math.floor(num_negative_tests + 0.5)) # rounding float

    # printing to final preprocssed file
    print("{},{},{}"
         .format(date, phu_num, num_negative_tests),
         file = file_writer)

  file_writer.close()
  file_pointer.close()

main()
