import sys
import csv
import os
import math
from datetime import datetime, timedelta

PREPROCESSED_FILE = "q2_vaccine_data_by_PHU"
FILE_TYPE = ".csv"
DATE_FORMAT = "%Y-%m-%d"
START_DATE = datetime.strptime("2021-08-13", DATE_FORMAT)
  


def main():
  print("----------INITIALIZING _temp AND _summarized FILES----------")
  
  # open phu id + name file
  search_path = "data/q2/"
  
  try:
    phu_file_pointer = open("data/q2/PHU_IDs.csv", encoding="utf-8-sig")
  except IOError as err:
    print("Unable to open file '{}' : {}".format(
              "data/q2/PHU_IDs.csv", err), file=sys.stderr)
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

    search_path = "data/q2/temp_preprocessing/"
    phu_filename = search_path + phu_name[0] + "_temp" + FILE_TYPE
    phu_file_temp = open(phu_filename, "w")
    print("Date,age group,Total population, one dose cumulative", file = phu_file_temp)
    phu_file_temp.close()
    
    phu_filename = search_path + phu_name[0] + "_summarized" + FILE_TYPE
    phu_file_temp = open(phu_filename, "w")
    print("Date,one dose cumulative", file = phu_file_temp)
    phu_file_temp.close()
  phu_file_pointer.close()

  print("----------COMPLETED INITIALIZATION OF _temp AND _summarized FILES----------")

  print("----------EXTRACTING OF DATA FROM DATA SET INTO _temp FILES----------")
  
  # finding and creating full data set file path
  search_path = "data/q2/"
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
      continue

    # extracting data from row
    date = last_date_str = row_data[0]
    phu_num_list.append(int(row_data[1]))
    phu_name = row_data[2].upper().split() #using only first word of phu name to identify
    if phu_name[0] == "CITY": # differentiate between city of ottawa and city of hamilton
      phu_name[0] = phu_name[2]
    phu_name = phu_name[0].split(",") #removing comma (,)
    age_group = row_data[3]
    if age_group[0].isdigit() == False: #do not include specific categories like adult_8+
      continue
    try:
      one_dose_cumulative = int(row_data[4])
    except:
      continue

    try:
      total_population = int(row_data[8])
    except:
      continue

    search_path = "data/q2/temp_preprocessing/"
    phu_filename = search_path + phu_name[0] + "_temp" + FILE_TYPE
    phu_fileWriter = open(phu_filename, "a")
    print("%s,%s,%s,%s"
          %(date, age_group, str(total_population), str(one_dose_cumulative)), 
          file = phu_fileWriter)
    phu_fileWriter.close()
  file_pointer.close()

  print("----------COMPLETED EXTRACTING OF DATA INTO _temp FILES----------")

  print("----------SUMMARIZING OF DATA INTO _summarized FILES----------")

  # summarizing data into _summarized files
  last_date = datetime.strptime(last_date_str, DATE_FORMAT)
  time_period = (last_date - START_DATE).days
  # process phu by phu
  for phu_name in phu_list:
    search_path = "data/q2/temp_preprocessing/"
    phu_filename = search_path + phu_name + "_temp" + FILE_TYPE
    phu_fileReader = open(phu_filename, "r")
    phu_csv_reader = csv.reader(phu_fileReader)
    
    current_date = START_DATE
    # processes each day for phu phu_name
    for day in range(time_period + 1):
      one_dose_cumulative = 0
      total_population = 0
      one_dose_percent = 0

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
            one_dose = int(row_data[3])
          except ValueError as err:
            print("{} : One_dose problem at {}".format(err, row_data))
            sys.exit(0)
          one_dose_cumulative += one_dose
          try:
            total_pop = int(row_data[2])
          except ValueError as err:
            print("{} : One_dose problem at {}".format(err, row_data))
            sys.exit(0)
          total_population += total_pop
          one_dose_percent = round((one_dose_cumulative / total_population) * 100, 2)
        elif date > current_date:
          break

      # writing to _summarized file
      phu_filename = search_path + phu_name + "_summarized" + FILE_TYPE
      current_date_str = datetime.strftime(current_date, DATE_FORMAT)
      phu_fileWriter = open(phu_filename, "a")
      print("%s,%s"
            %(current_date_str, str(one_dose_percent)), 
            file = phu_fileWriter)
      phu_fileWriter.close()
      phu_fileReader.seek(0)
      
      current_date += timedelta(days=1)

    print("---COMPLETED PHU %s---" %(phu_name))
    phu_fileReader.close()

  print("----------COMPLETED SUMMARIZING OF DATA INTO _summarized FILES----------")

  print("----------PREPROCESSING DATA INTO FINAL FILE----------")

  # initalizing final preprocessed file
  search_path = "data/q2/preprocessed_data/"
  filename = search_path + PREPROCESSED_FILE + FILE_TYPE
  file_writer = open(filename, "w")
  print("Date, PHU_num, One_dose_percentage",
         file = file_writer)
  file_writer.close()

  # reading data from _summarized files
  phu_file_list = []
  for phu_name in phu_list:
    search_path = "data/q2/temp_preprocessing/"
    phu_filename = search_path + phu_name + "_summarized" + FILE_TYPE
    phu_fileReader = open(phu_filename, "r")
    phu_file_list.append(phu_fileReader.readlines())
    phu_fileReader.close()

  # aggregrating data from _summarized files into final file
  file_writer = open(filename, "a")
  line_number = 1
  current_date = START_DATE
  for day in range(time_period + 1):
    current_date_str = datetime.strftime(current_date, DATE_FORMAT)
    index = 0
    
    for phu in phu_list:
      line_data = phu_file_list[index][line_number].split(",")
      one_dose_percent = line_data[1].rstrip("\n")
      print("{},{},{}"
            .format(current_date_str, phu_num_list[index], one_dose_percent),
             file = file_writer)
      index += 1

    line_number += 1
    current_date += timedelta(days=1)
    
  file_writer.close()
  
  print("----------COMPLETED PREPROCESSING DATA INTO FINAL FILE----------")
main()