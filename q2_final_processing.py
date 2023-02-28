'''
q2_final_processing.py
  Author(s): Charlotte Barnes(1154105),
             Tia Yun Fat Jeffrey Ronan Chay Loong(1181166),
             Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Contains function processQ2Data that filters the data/q2/preprocessed_data/q2_vaccine_data_by_PHU.csv
      file using the parameters passed through and generates a new file
'''
import sys
import csv
import os

# Global Constants
DATE_FORMAT = "%Y-%m-%d"
VACCINE_FILENAME = "q2_vaccine_data_by_PHU"
PROCESSED_FILENAME = "q2_data_file"
SEARCH_PATH = "data/q2/preprocessed_data/"
FILE_TYPE = ".csv"
DATE_FORMAT = "%Y-%m-%d"

#Filters the data/q2/preprocessed_data/q2_vaccine_data_by_PHU.csv file using the parameters passed through
#and generates a new file
def processQ2Data(params):
  # finding and creating full vaccine file path
  for filename in os.listdir(path=SEARCH_PATH):
    if (filename.find(VACCINE_FILENAME) != -1):
      vaccine_full_filename = SEARCH_PATH + filename
  # opening vaccine file
  try:
    vaccine_filePtr = open(vaccine_full_filename, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              vaccine_full_filename, err), file=sys.stderr)
    sys.exit(0)
  vaccine_fileReader = csv.reader(vaccine_filePtr)

  #initialising final processed file
  processed_full_filename = "data/processed_data/" + PROCESSED_FILENAME + FILE_TYPE
  processed_fileWriter = open (processed_full_filename, "w")
  print("Date,PHU_num,One_dose_percentage",
        file = processed_fileWriter)

  # Extracting phu number from params
  phu_selected = int(params["phuSelected"][0])
  if len(params["phuSelected"]) == 2:
    phu_selected2 = int(params["phuSelected"][1])
  else:
    phu_selected2 = 0

  # extracting data from preprocessed file
  for vac_row_data in vaccine_fileReader:
    if vac_row_data[0] == "Date":
      continue
      
    phu_num = int(vac_row_data[1])
    if (phu_num == phu_selected) or (phu_num == phu_selected2):
      date_str = vac_row_data[0]
      one_dose_percent = vac_row_data[2]
      print("{},{},{}"
           .format(date_str, phu_num, one_dose_percent),
           file = processed_fileWriter)

  processed_fileWriter.close()
  vaccine_filePtr.close()

def main():
  # arbitrary parameter for testing purposes
  parameters_q2 = [
    {
      "type": "phuNum",
      "multiple": True, # see if multiple phus can be chosen at once
      "phuSelected": [2226, 2227] # stores phu num of selected phus
    }
  ]
  processQ2Data(parameters_q2[0])

main()