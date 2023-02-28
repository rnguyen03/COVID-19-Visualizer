'''
q3_final_processing.py
  Author(s): Charlotte Barnes(1154105),
             Tia Yun Fat Jeffrey Ronan Chay Loong(1181166),
             Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Contains function processQ3Data that produces a csv file containing the date, phu number
      for the selected phu, and the respective number of vaccinated people and the number of
      negative tests. It takes data from the preprocessed vaccine and tests files.
'''
import sys
import csv
import os
from datetime import datetime

# Global constants
VACCINE_FILENAME = "q3_vaccine_data_by_PHU"
TESTING_FILENAME = "q3_testing_data_by_phu"
PROCESSED_FILENAME = "q3_data_file"
SEARCH_PATH = "data/q3/preprocessed_data/"
FILE_TYPE = ".csv"
DATE_FORMAT = "%Y-%m-%d"

def processQ3Data(params):
  # finding and creating full vaccine file path
  for filename in os.listdir(path=SEARCH_PATH):
    if (filename.find(VACCINE_FILENAME) != -1):
      vaccine_full_filename = SEARCH_PATH + filename
      
  # opening vaccine file to read
  try:
    vaccine_filePtr = open(vaccine_full_filename, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              vaccine_full_filename, err), file=sys.stderr)
    sys.exit(0)
  vaccine_fileReader = csv.reader(vaccine_filePtr)

  # finding and creating full test file path
  for filename in os.listdir(path=SEARCH_PATH):
    if (filename.find(TESTING_FILENAME) != -1):
      test_full_filename = SEARCH_PATH + filename
      
  # opening test file to read
  try:
    testing_filePtr = open(test_full_filename, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              test_full_filename, err), file=sys.stderr)
    sys.exit(0)
  testing_fileReader = csv.reader(testing_filePtr)

  # initialising final processed file
  processed_full_filename = "data/processed_data/" + PROCESSED_FILENAME + FILE_TYPE
  processed_fileWriter = open (processed_full_filename, "w")
  print("Date,PHU_num,one_or_more_doses_cumulative,num_negative_7d_average",
        file = processed_fileWriter)

  # extracting data from params
  start_date = datetime.strptime(params[0]["startDate"], DATE_FORMAT)
  end_date = datetime.strptime(params[0]["endDate"], DATE_FORMAT)
  phu_selected = int(params[1]["phuSelected"][0])

  # Finding relevant rows from vaccine file
  for vac_row_data in vaccine_fileReader:
    if vac_row_data[0] == "Date":
      continue

    # Sorting by phu number
    phu_num = int(vac_row_data[1])
    if phu_num == phu_selected:
      date_str = vac_row_data[0]
      date = datetime.strptime(date_str, DATE_FORMAT)

      # Sorting by date
      if date >= start_date and date <= end_date:
        one_dose = vac_row_data[2]
        
        # opening test file
        try:
          testing_filePtr = open(test_full_filename, encoding="utf-8-sig")
        except IOError as err:
          print("Unable to open file '{}' : {}".format(
                    test_full_filename, err), file=sys.stderr)
          sys.exit(0)
        testing_fileReader = csv.reader(testing_filePtr)

        # Finding relevant rows from test file
        for test_row_data in testing_fileReader:
          if test_row_data[0] == "Date":
            continue

          # Sorting by phu number
          phu_num2 = int(test_row_data[1])
          if phu_num2 == phu_selected:
            date2_str = test_row_data[0]
            date2 = datetime.strptime(date2_str, DATE_FORMAT)

            # Sorting by date
            if date2 == date:
              num_negative = test_row_data[2]
              print("{},{},{},{}"
                   .format(date_str, phu_num, one_dose, num_negative),
                   file = processed_fileWriter)
              break
        testing_filePtr.close()

  processed_fileWriter.close()
  vaccine_filePtr.close()
  