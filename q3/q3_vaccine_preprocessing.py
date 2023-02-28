'''
q3_vaccine_preprocessing.py
  Author(s): Charlotte Barnes(1154105),
             Tia Yun Fat Jeffrey Ronan Chay Loong(1181166),
             Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Preprocesses the vaccine data by extracting the relevant data
'''
import sys
import csv
import os
from datetime import datetime, timedelta

# Global constants
PREPROCESSED_FILENAME = "q3_vaccine_data_by_PHU"
FILE_TYPE = ".csv"
DATE_FORMAT = "%Y-%m-%d"
START_DATE = datetime.strptime("2021-07-26", DATE_FORMAT)

def main():
  print("----------INITIALIZING _temp AND _summarized FILES----------")
  # open phu id + name file
  search_path = "data/q3/"
  try:
    phu_file_pointer = open("data/q3/PHU_IDs.csv", encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              "data/q3/PHU_IDs.csv", err), file=sys.stderr)
    sys.exit(0)
  phuID_reader = csv.reader(phu_file_pointer)

  # initialising phu _temp and _summarized files files
  # [_temp: stores date and corresponding total per age groups]
  # [_summarized: stores summarized one dose per day]
  phu_list = []
  for row_data in phuID_reader:
    if row_data[0] == "Reporting_PHU_ID":
      continue
    phu_name = row_data[1].upper().split()
    if phu_name[0] == "CITY":
      phu_name[0] = phu_name[2]
    phu_name = phu_name[0].split(",")
    phu_list.append(phu_name[0])
    search_path = "data/"

    search_path = "data/q3/temp_preprocessing/"
    phu_filename = search_path + phu_name[0] + "_temp" + FILE_TYPE
    phu_file_temp = open(phu_filename, "w")
    print("Date,age group,one dose cumulative", file = phu_file_temp)
    phu_file_temp.close()
    
    phu_filename = search_path + phu_name[0] + "_summarized" + FILE_TYPE
    phu_file_temp = open(phu_filename, "w")
    print("Date,one dose cumulative", file = phu_file_temp)
    phu_file_temp.close()
  phu_file_pointer.close()

  print("----------COMPLETED INITIALIZATION OF _temp AND _summarized FILES----------")

  print("----------EXTRACTING OF DATA FROM DATA SET INTO _temp FILES----------")
  # finding and creating full data set file path
  search_path = "data/q3/"
  vaccine_filename = "vaccines_by_age_phu_"
  for filename in os.listdir(path=search_path):
    if (filename.find(vaccine_filename) != -1):
      full_filename = search_path + filename
  # opening vaccine file
  try:
    file_pointer = open(full_filename, encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              full_filename, err), file=sys.stderr)
    sys.exit(0)
  file_reader = csv.reader(file_pointer)

  # extracting data from data set into _temp files
  last_date_str = ""
  phu_num_list = []
  for row_data in file_reader:
    if row_data[0] == "Date":
      # date = row_data[0]
      continue

    # extracting data from row
    date = last_date_str = row_data[0]
    phu_num_list.append(int(row_data[1]))
    phu_name = row_data[2].upper().split() #using only first word of phu name to identify
    if phu_name[0] == "CITY":              #differentiate between city of ottawa and city of hamilton
      phu_name[0] = phu_name[2]
    phu_name = phu_name[0].split(",")      #removing comma (,)
    age_group = row_data[3]
    if age_group[0].isdigit() == False:    #do not include specific categories like adult_8+ or ontario_12+
      continue
    try:
      one_dose_cumulative = int(row_data[4])
    except:
      continue

    # Writing to files
    search_path = "data/q3/temp_preprocessing/"
    phu_filename = search_path + phu_name[0] + "_temp" + FILE_TYPE
    phu_fileWriter = open(phu_filename, "a")
    print("%s,%s,%s"
          %(date, age_group, str(one_dose_cumulative)), 
          file = phu_fileWriter)
    phu_fileWriter.close()
  file_pointer.close()

  print("----------COMPLETED EXTRACTING OF DATA INTO _temp FILES----------")
  
  print("----------SUMMARIZING OF DATA INTO _summarized FILES----------")
  last_date = datetime.strptime(last_date_str, DATE_FORMAT)
  time_period = (last_date - START_DATE).days
  # process phu data by phu
  for phu_name in phu_list:
    search_path = "data/q3/temp_preprocessing/"
    phu_filename = search_path + phu_name + "_temp" + FILE_TYPE
    phu_fileReader = open(phu_filename, "r")
    phu_csv_reader = csv.reader(phu_fileReader)
    
    current_date = START_DATE
    # processes each day for phu phu_name
    for day in range(time_period + 1):
      one_dose_cumulative = 0

      # finds data from file and sums one_dose for that day
      for row_data in phu_csv_reader:
        if row_data[0] == "Date":
          continue

        # extracting date from a row and converting from str to date
        date_str = row_data[0]
        try:
          date = datetime.strptime(date_str, DATE_FORMAT)
        except ValueError as err:
          print("{}: Date format problem at {}".format(err, row_data))
          sys.exit(0)

        # performing summarization for day current_date
        if date == current_date:
          try:
            one_dose = int(row_data[2])
          except ValueError as err:
            print("{} : One_dose problem at {}".format(err, row_data))
            sys.exit(0)
          one_dose_cumulative += one_dose
        elif date > current_date:
          break

      # writing to _summarized file
      phu_filename = search_path + phu_name + "_summarized" + FILE_TYPE
      current_date_str = datetime.strftime(current_date, DATE_FORMAT)
      phu_fileWriter = open(phu_filename, "a")
      print("%s,%s"
            %(current_date_str, str(one_dose_cumulative)), 
            file = phu_fileWriter)
      phu_fileWriter.close()
      phu_fileReader.seek(0)
      
      current_date += timedelta(days=1)

    print("---COMPLETED PHU %s---" %(phu_name))
    phu_fileReader.close()

  print("----------COMPLETED SUMMARIZING OF DATA INTO _summarized FILES----------")

  print("----------AGGREGATING DATA INTO TEMP FINAL FILE----------")
  # initalizing temp final preprocessed file
  search_path = "data/q3/temp_preprocessing/"
  filename = search_path + PREPROCESSED_FILENAME + "_temp" + FILE_TYPE
  file_writer = open(filename, "w")
  print("Date,PHU_num,one_or_more_doses_cumulative",
         file = file_writer)
  file_writer.close()

  # reading data from _summarized files
  phu_file_list = []
  for phu_name in phu_list:
    search_path = "data/q3/temp_preprocessing/"
    phu_filename = search_path + phu_name + "_summarized" + FILE_TYPE
    phu_fileReader = open(phu_filename, "r")
    phu_file_list.append(phu_fileReader.readlines())
    phu_fileReader.close()

  # aggregrating data from _summarized files into temp final file
  file_writer = open(filename, "a")
  line_number = 1
  current_date = START_DATE
  for day in range(time_period + 1):
    current_date_str = datetime.strftime(current_date, DATE_FORMAT)
    index = 0
    for phu in phu_list:
      line_data = phu_file_list[index][line_number].split(",")
      one_dose = line_data[1].rstrip("\n")

      print("{},{},{}"
            .format(current_date_str, phu_num_list[index], one_dose),
             file = file_writer)
      index += 1
    
    line_number += 1
    current_date += timedelta(days=1)
    
  file_writer.close()
  
  print("----------COMPLETED AGGREGATING DATA INTO TEMP FINAL FILE----------")

  print("----------CALCULATING ONTARIO DATA AND AGGREGATING DATA INTO FINAL FILE----------")
  # initalizing final preprocessed file
  search_path = "data/q3/preprocessed_data/"
  filename = search_path + PREPROCESSED_FILENAME + FILE_TYPE
  file_writer = open(filename, "w")

  # opening temp preprocessed file
  search_path = "data/q3/temp_preprocessing/"
  preprocessed_filename = search_path + PREPROCESSED_FILENAME + "_temp" + FILE_TYPE
  preprocessed_fileReader = open(preprocessed_filename, "r")
  preprocessed_csv_reader = csv.reader(preprocessed_fileReader)

  # totalling data to find for all ontario
  NUM_PHUS = 35
  ontario_one_dose = 0
  index = 0
  for row_data in preprocessed_csv_reader:
    # storing ontario data for each date
    if index == NUM_PHUS:
      date_str = row_data[0]
      date = datetime.strptime(date_str, DATE_FORMAT)
      date -= timedelta(days=1)
      date_str = datetime.strftime(date, DATE_FORMAT)
      print("{},{},{}"
         .format(date_str, 35, ontario_one_dose),
         file = file_writer)
      index = 0
      
    print("{},{},{}"
         .format(row_data[0], row_data[1], row_data[2]),
         file = file_writer)
    if row_data[0] == "Date":
      continue
      
    ontario_one_dose += int(row_data[2])
    index += 1
    
  print("----------COMPLETED FINAL PREPROCESSING----------")
main()
