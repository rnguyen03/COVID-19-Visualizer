#!/usr/bin/env python
'''
q1_test_metrics_preprocessing.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 13, 2022

  Functional Summary
      Extracting data from the testing metrics csv files.
'''

#Import necessary libraries
import sys
import csv

def main(argv):
  #open file
  test_filename = "data/q1/testing_metrics_by_phu.csv"
  try:
    test_fh = open(test_filename, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open names file '{}' : {}".format(
              test_filename, err), file=sys.stderr)
    sys.exit(0)
  
  test_reader = csv.reader(test_fh)
  #extract phu number, date and tests per region for all 
  # phu's except the ontario wide code "35"
  for row in test_reader:
    if row[1]!='35':
      phu_number = row[1]
      date = row[0]
      avg_tests_per_person = row[5]
      print(phu_number + "," + date + "," + avg_tests_per_person)

main(sys.argv)