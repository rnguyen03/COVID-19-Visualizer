#!/usr/bin/env python
'''
main_menu.py
  Authors: Charlotte Barnes, Tia Yun Fat Jeffrey Ronan Chay Loong, Ryan Nguyen

  Functional Summary
      Drives main menu of data analyzation tool
'''
import csv
import sys
import os
import time
import re
from datetime import datetime
from q3_final_processing import processQ3Data
from q1_final_processing import final_processing_q1
from q1_plot import createQ1Plot
from q3_plot import createQ3Plot
from q4_final_processing import processQ4
from q2_final_processing import processQ2Data
from q4_plot import createQ4Plot
from q2_plot import createQ2Plot

# Global Constants
DEFAULT_STARTDATE = "2021-11-27"
DEFAULT_ENDDATE = "2022-03-05"
phu_list = ["2226  Algoma Public Health Unit",
            "2227  Brant County Health Unit",
            "2230  Durham Region Health Department",
            "2233  Grey Bruce Health Unit",
            "2234  Haldimand-Norfolk Health Unit",
            "2235  Haliburton, Kawartha, Pine Ridge District Health Unit",
            "2236  Halton Region Health Department",
            "2237  City of Hamilton Public Health Services",
            "2238  Hastings and Prince Edward Counties Health Unit",
            "2240  Chatham-Kent Health Unit",
            "2241  Kingston, Frontenac and Lennox & Addington Public Health",
            "2242  Lambton Public Health",
            "2243  Leeds, Grenville and Lanark District Health Unit",
            "2244  Middlesex-London Health Unit",
            "2246  Niagara Region Public Health Department",
            "2247  North Bay Parry Sound District Health Unit",
            "2249  Northwestern Health Unit",
            "2251  City of Ottawa Public Health",
            "2253  Peel Public Health",
            "2255  Peterborough Public Health",
            "2256  Porcupine Health Unit",
            "2257  Renfrew County and District Health Unit",
            "2258  Eastern Ontario Health Unit",
            "2260  Simcoe Muskoka District Health Unit",
            "2261  Sudbury & District Health Unit",
            "2262  Thunder Bay District Health Unit",
            "2263  Timiskaming Health Unit",
            "2265  Waterloo, Public Health",
            "2266  Wellington-Dufferin-Guelph Public Health",
            "2268  Windsor-Essex County Health Unit",
            "2270  York Region Public Health Services",
            "3895  Toronto Public Health",
            "4913  Southwestern Public Health",
            "5183  Huron Perth District Health Unit",
            " 35   Ontario"]


'''
Displays the main menu
'''
def printMenu():
  print("************************************************ MAIN MENU ************************************************")
  print("Question 1:")
  print("     Was the COVID-19 positivity rate for adults 18+ higher in areas with more available tests per person?")
  print("Question 2:")
  print("     Where did the vaccine mandate have a positive effect on vaccine administration rate?")
  print("Question 3:")
  print("     Are fewer negative tests being done as the number of vaccinated people increases in Ontario?")
  print("Question 4:")
  print("     How many years of labor have been lost to COVID-19 compared to other diseases in 2020?")
  print("Choose a question (Enter \"5\" to exit program):", end = " ")
  return
  

'''
Checks if userInput is an integer in the range lowerBound and upperBound inclusive
Returns whether userInput is valid (True) or invalid (False)
'''
def validateIntInput(userInput, lowerBound, upperBound):
  valid = True
  # checks if input is integer
  try:
    choice = int(userInput)
  except ValueError:
    valid = False
    os.system("clear")
    print("ERROR ENCOUNTERED: \"{}\" is not a valid input".format(userInput))
    print("Please input an integer between {} and {} inclusive".format(lowerBound, upperBound))
    #time.sleep(2)

  # checks if input is in range
  if valid and (choice < lowerBound or choice > upperBound):
    valid = False
    os.system("clear")
    print("ERROR ENCOUNTERED: \"{}\" is not a valid input".format(userInput))
    print("Please input an integer between {} and {} inclusive".format(lowerBound, upperBound))
    #time.sleep(2)

  os.system("clear")
  return valid


'''
Displays menu for parameter settings and performs any edits necessary
'''
def parameterSettings(question, parameterList):
  os.system("clear")
  screen_header = "************************************ PARAMETER SETTINGS FOR QUESTION {} ************************************\n".format(question)

  # parameter screen for q1
  if question == 1:
    # Loops until the user input is valid
    while True:
      print(screen_header)
      print("---------- Parameter: Date Range ----------")
      # Print start and end dates
      startDate_date = datetime.strptime(parameterList[0]["startDate"], "%Y-%m-%d")
      endDate_date = datetime.strptime(parameterList[0]["endDate"], "%Y-%m-%d")
      date_format = "%d %B %Y"
      startDate_full_str = datetime.strftime(startDate_date, date_format)
      endDate_full_str = datetime.strftime(endDate_date, date_format)
      print("Start Date: {}".format(startDate_full_str))
      print("End Date  : {}".format(endDate_full_str))
      print()

      # Print user choices
      print("1. Change date range")
      print("2. Return to Question {}".format(question))
      print("Choose an option to perform:", end = " ")
      choice = input()
      valid = validateIntInput(choice, 1, 2)
      if not valid:
        continue

      edited = False # check if paramters have been changed

      # change parameter date range
      if choice == "1":
        while True:
          saved = editDateRange(parameterList[0])
          if saved == True:
            os.system("clear")
            print("New date range has been saved!")
            print("Returning to Parameter Settings...".format(question))
            #time.sleep(1)
            os.system("clear")
            edited = True
            break

      # return to question 1 screen
      if choice == "2":
        os.system("clear")
        if edited:
          print("Changes to parameters have been saved!")
        print("Returning to Question {}...".format(question))
        #time.sleep(1)
        break
        
  # paramter screen for q2
  if question == 2:
    # Loops until the user input is valid
    while True:
      print(screen_header)
      print("---------- Parameter: Selected PHU ----------")
      # Print selected phu(s)
      phu_selected = parameterList[0]["phuSelected"]
      for phu in phu_list:
        phu_num = int(phu[0:4])
        if phu_num in phu_selected:
          print(phu)
      print()

      # Print user choices
      print("1. Change PHU(s) selected")
      print("2. Return to Question {}".format(question))
      print("Choose an option to perform:", end = " ")
      choice = input()
      valid = validateIntInput(choice, 1, 2)
      if not valid:
        continue

      edited = False # check if paramters have been changed

      # change parameter PHU IDs
      if choice == "1":
        while True:
          saved = editSelectedPhu(parameterList[0])
          if saved == True:
            break

      # return to question 2 screen
      if choice == "2":
        os.system("clear")
        if edited:
          print("Changes to parameters have been saved!")
        print("Returning to Question {}...".format(question))
        #time.sleep(1)
        break
      
  #parameter screen for q3
  if question == 3:
    # Loops until the user input is valid
    while True:
      print(screen_header)
      print("---------- Parameter: Date Range ----------")
      # Print start and end dates
      startDate_date = datetime.strptime(parameterList[0]["startDate"], "%Y-%m-%d")
      endDate_date = datetime.strptime(parameterList[0]["endDate"], "%Y-%m-%d")
      date_format = "%d %B %Y"
      startDate_full_str = datetime.strftime(startDate_date, date_format)
      endDate_full_str = datetime.strftime(endDate_date, date_format)
      print("Start Date: {}".format(startDate_full_str))
      print("End Date  : {}".format(endDate_full_str))
      print()
      
      print("---------- Parameter: Selected PHU ----------")
      # Print selected phu
      phu_selected = parameterList[1]["phuSelected"]
      for phu in phu_list:
        phu_num = int(phu[0:4])
        if phu_num in phu_selected:
          print(phu)
      print()

      # Print user choices
      print("1. Change Date Range")
      print("2. Change PHU Selected")
      print("3. Return to Question {}".format(question))
      print("Choose an option to perform:", end = " ")
      choice = input()
      valid = validateIntInput(choice, 1, 3)
      if not valid:
        continue
      edited = False

      # Return to Q3 screen
      if choice == "3":
        os.system("clear")
        if edited:
          print("Changes to parameters have been saved!")
        print("Returning to Question {}...".format(question))
        #time.sleep(1)
        break

      # Edit date range
      if choice == "1":
        while True:
          saved = editDateRange(parameterList[0])
          if saved == True:
            os.system("clear")
            print("New date range has been saved!")
            print("Returning to Parameter Settings...".format(question))
            #time.sleep(1)
            os.system("clear")
            edited = True
            break

      # Edit selected phu
      if choice == "2":
        while True:
          saved = editSelectedPhu(parameterList[1])
          if saved == True:
            break

  # parameter screen for q4
  if question == 4:
    edited = False # check if paramters have been changed
    #open preprocessed data
    filename = "data/q4/preprocessed_data/q4_preprocessed.csv"
    try:
      causes_of_death_fh = open(filename, encoding="utf-8-sig")
    except:
      print("Internal error. Unable to retrieve cause of death information. Please try again")
      
    causes_of_death_csv = csv.reader(causes_of_death_fh)
    next(causes_of_death_csv)
    
    #initiliaze dict to hold data in csv
    causes_of_death_dict = {}
    for deaths in causes_of_death_csv:
      causes_of_death_dict[deaths[0]] = deaths[1]
      
    #counter only allows edited to be updated if first loop or edited is False
    # this ensures the "saving changes" message appears whenever changes have been           
    # made at least once
    loop = 0
    #loop until user chooses to return to q4
    while True:
      print(screen_header)
      print("---------- Parameter: Causes of death ----------")
      # print current selections
      print("Current causes of death: ")
      for selection in parameterList[0]["diseaseSelected"]:
        print(str(selection) + "\t"+ causes_of_death_dict[str(selection)])
        
      #user options
      print("\n1. Change causes of death selected")
      print("2. Return to Question {}".format(question))
      print("Choose an option to perform:", end = " ")
      choice = input()
      # validate user input
      valid = validateIntInput(choice, 1, 2)
      if not valid:
        continue
        
      #user chooses to edit parameters
      # bring user to parameter settings
      if choice == "1":
        current_edited = editDiseaseSelections(causes_of_death_dict, parameterList)
        if loop == 1 or edited == False:
          edited = current_edited
          
      #user chooses not to edit paramters, return to question menu
      elif choice == "2":
        os.system("clear")
        if edited:
          print("Changes to parameters have been saved!")
        print("Returning to Question {}...".format(question))
        #time.sleep(1)
        break
        
      loop += loop

'''
Displays menu to edit the selected phu. Either one or two phu is chosen, based on whether the 
function was needed for question 2 or 3
Returns whether the new parameters have been saved (True) or not (False)
'''
def editSelectedPhu(selectedPhuOriginal):
  os.system("clear")
  screen_header = "************************ EDITING SELECTED PHU ************************\n"

  phu_selected = []  # A list to store the selected phu number(s)

  # Loop until user input is valid
  while True:
    print(screen_header)
    # Print phus that can be selected
    for phu in phu_list:
      if selectedPhuOriginal["multiple"] and phu != " 35   Ontario":
        print(phu)
    print()

    # Prompt user to enter phu
    print("Enter a PHU number to select new PHU: ", end = "")
    choice = input()
    # Check if choice is a valid integer
    valid = validateIntInput(choice, 35, 5183)
    # Check if choice is a valid phu number
    if valid:
      valid = False
      for phu in phu_list:
        phu_num = phu[0:4]
        if choice == phu_num:
          valid = True
      # Display error if phu is not valid
      if not valid:
        os.system("clear")
        print("ERROR - PHU number is not valid")
        print("Please enter a PHU number that is in the given list")
        #time.sleep(2.5)
        os.system("clear")
      else:
        # update phu_selected list
        phu_selected.append(int(choice))
        break

  # For Q3: check if only 1 phu needed and return to parameter setting screen if true
  if not selectedPhuOriginal["multiple"]:
    selectedPhuOriginal["phuSelected"] = [int(choice)]
    os.system("clear")
    print("New PHU selected has been saved!")
    print("Returning to Parameter Settings...")
    #time.sleep(1.7)
    os.system("clear")
    return True

  # For Q2: Continue to select 2nd phu (if desired)
  while True:
    # Print phu list
    print(screen_header)
    for phu in phu_list:
      if phu != " 35   Ontario":
        print(phu)
    print()
    
    print("Enter second PHU number to select (Enter '-1' to exit): ", end = "")
    choice = input()

    # Return to parameter settings if -1 is input
    if choice == '-1':
      selectedPhuOriginal["phuSelected"] = phu_selected
      os.system("clear")
      print("New PHU selected has been saved!")
      print("Returning to Parameter Settings...")
      #time.sleep(1.7)
      os.system("clear")
      return True
    else:
      # Validate user input
      valid = validateIntInput(choice, 35, 5183)
      if valid:
        # Check if phu number is in list
        valid = False
        for phu in phu_list:
          phu_num = phu[0:4]
          if choice == phu_num and choice != "35":
            valid = True
        # Display error if phu is not in list
        if not valid:
          os.system("clear")
          print("ERROR - PHU number is not valid")
          print("Please enter a PHU number that is in the given list")
          #time.sleep(2.5)
          os.system("clear")
        else:
          # Return to parameter settings if phu number is valid
          phu_selected.append(int(choice))
          selectedPhuOriginal["phuSelected"] = phu_selected
          os.system("clear")
          print("New PHU selected has been saved!")
          print("Returning to Parameter Settings...")
          #time.sleep(1.7)
          os.system("clear")
          return True
      else:
        # Display error if phu is not a valid integer
        os.system("clear")
        print("ERROR ENCOUNTERED: input is invalid")
        print("Please enter a valid integer")
        #time.sleep(2)
        os.system("clear")    
'''
Edit the disease selections for Q4, alters parameterList
--paramter list must always include the int "44" to represent COVID-19
'''
def editDiseaseSelections(causes_of_death_dict, parameterList):
  # print options
  print("Unique ID:\tCause of Death")
  for deaths in causes_of_death_dict:
    print(str(deaths) + "\t" + causes_of_death_dict[str(deaths)])
    
  # get user input for disease selections
  print("Please enter up to 10 unique id(s) of the causes of death you wish to compare with COVID-19")
  # loop until valid IDs enterred
  while True:
    choices = input()
    # extract user entered disease ids
    match = re.findall("[0-9]+", choices)
    if not match:
      print("Please enter disease IDs seperated by spaces.")
      continue
    # validate number of user inputs (<=10)
    valid = validateIntInput(len(match), 1, 10)
    if not valid:
      return False
    # remove invalid ids
    for selection in match:
      if int(selection) > 51 or int(selection) < 0:
        print("Disease {} out of range, disease cannot be selected".format(selection))
        match.remove(selection)
    # none of selections are valid
    if len(match) < 1:
      return False
      
    # valid selctions exist
    while True:
      # output new disease selections
      print("New selections:")
      for selection in match:
          print(str(selection) + "\t" + causes_of_death_dict[str(selection)])
      # ask user to save
      print("Would you like to save these choices? ('y' for Yes and 'n' for No)")
      save = input()
      # validate user input
      if (save != 'y') and (save != 'n'):
        os.system("clear")
        print("ERROR ENCOUNTERED: \"{}\" is not a valid input".format(save))
        print("Please enter either 'y' or 'n'")
        #time.sleep(2)
        os.system("clear")
        continue
        
      # user chooses to save selection, update parameterList: return true
      if save =="y":
        parameterList[0]["diseaseSelected"].clear()
        parameterList[0]["diseaseSelected"].append(44)
        for diseaseChoice in match:
          valid = validateIntInput(diseaseChoice, 0, 51)
          if valid:
            parameterList[0]["diseaseSelected"].append(int(diseaseChoice))
          else:
            print("Cannot add disease choice {}".format(int(diseaseChoice)))
        os.system("clear")
        print("Saved!")
        #time.sleep(2)
        os.system("clear")
        return True
      # user chooses not to save, do not update paramter list, return false 
      elif save == 'n':
        os.system("clear")
        print("Changes will not be saved.")
        #time.sleep(2)
        os.system("clear")
        return False

'''
Displays menu to edit the date range
'''
def editDateRange(dateRangeOriginal):
  os.system("clear")
  screen_header = "************************ EDITING DATE RANGE ************************\n"
  
  current_startDate_str = dateRangeOriginal["startDate"]
  current_startDate = datetime.strptime(current_startDate_str, "%Y-%m-%d")
  # edits year of start year
  while True:
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): ", end = "")
    input_year = input()
    valid = validateIntInput(input_year, 1, 2)

    if valid:
      if input_year == "1":
        input_year = 2021
      else:
        input_year = 2022
      current_startDate = current_startDate.replace(year = int(input_year))
      break

  # edits month of start year
  while True:
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_startDate.year))
    print("   New Month (Enter number of month): ", end = "")
    input_month = input()
    valid = validateIntInput(input_month, 1, 12)

    if valid:
      current_startDate = current_startDate.replace(month = int(input_month))
      break

  # edits date of start year
  while True:
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_startDate.year))
    print("   New Month (Enter number of month): {}"
          .format(current_startDate.month))
    # find number of days in selected month
    leap = 0
    year = current_startDate.year
    month = current_startDate.month
    if year % 400 == 0:
       leap = 1
    elif year % 100 == 0:
       leap = 0
    elif year % 4 == 0:
       leap = 1
    if month == 2:
       upperBound = 28 + leap
    else:
      months_31_days = [1,3,5,7,8,10,12]
      if month in months_31_days:
        upperBound = 31
      else:
        upperBound = 30
    print("   New Date (Enter an ineteger between 1 and {}): "
          .format(upperBound)
          , end = "")
    input_day = input()
    
    valid = validateIntInput(input_day, 1, upperBound)

    if valid:
      current_startDate = current_startDate.replace(day = int(input_day))
      break

  current_endDate_str = dateRangeOriginal["endDate"]
  current_endDate = datetime.strptime(current_endDate_str, "%Y-%m-%d")
  #edits year of end year
  while True:
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_startDate.year))
    print("   New Month (Enter number of month): {}"
          .format(current_startDate.month))
    print("   New Date (Enter an ineteger between 1 and {}): {}"
          .format(upperBound, current_startDate.day))
    
    print()
    
    print("End Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): ", end = "")
    input_year = input()
    valid = validateIntInput(input_year, 1, 2)

    if valid:
      if input_year == "1":
        input_year = 2021
      else:
        input_year = 2022
      current_endDate = current_endDate.replace(year = int(input_year))
      break

  #edits month of end year
  while True:
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_startDate.year),)
    print("   New Month (Enter number of month): {}"
          .format(current_startDate.month))
    print("   New Date (Enter an ineteger between 1 and {}): {}"
          .format(upperBound, current_startDate.day))
    
    print()
    
    print("End Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_endDate.year))
    print("   New Month (Enter number of month): ", end = "")
    input_month = input()
    valid = validateIntInput(input_month, 1, 12)

    if valid:
      current_endDate = current_endDate.replace(month = int(input_month))
      break

  # edits date of end year
  while True:
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_startDate.year),)
    print("   New Month (Enter number of month): {}"
          .format(current_startDate.month))
    print("   New Date (Enter an ineteger between 1 and {}): {}"
          .format(upperBound, current_startDate.day))
    
    print()
    
    print("End Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_endDate.year))
    print("   New Month (Enter number of month): {}"
          .format(current_endDate.month))
    # find number of days in selected month
    leap = 0
    year = current_endDate.year
    month = current_endDate.month
    if year % 400 == 0:
       leap = 1
    elif year % 100 == 0:
       leap = 0
    elif year % 4 == 0:
       leap = 1
    if month == 2:
       upperBound2 = 28 + leap
    else:
      months_31_days = [1,3,5,7,8,10,12]
      if month in months_31_days:
        upperBound2 = 31
      else:
        upperBound2 = 30
    print("   New Date (Enter an ineteger between 1 and {}): "
          .format(upperBound2)
          , end = "")
    input_day = input()
    
    valid = validateIntInput(input_day, 1, upperBound2)

    if valid:
      current_endDate = current_endDate.replace(day = int(input_day))
      break

  # check if start and end dates are valid [ie end is not before start]
  if current_endDate < current_startDate:
      os.system("clear")
      print("ERROR ENCOUNTERED: Ending date is greater than starting date")
      print("Please input a valid date range")
      #time.sleep(2.5)
      return False
  
  # displays final start date and end dates to user to see if inputs are acceptable
  while True:
    valid = True
    print(screen_header)
    print("Start Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_startDate.year),)
    print("   New Month (Enter number of month): {}"
          .format(current_startDate.month))
    print("   New Date (Enter an ineteger between 1 and {}): {}"
          .format(upperBound, current_startDate.day))
    
    print()
    
    print("End Date:")
    print("   New Year (Enter \"1\" for 2021 or \"2\" for 2022): {}"
          .format(current_endDate.year))
    print("   New Month (Enter number of month): {}"
          .format(current_endDate.month))
    print("   New Date (Enter an ineteger between 1 and {}): {}"
          .format(upperBound2, current_endDate.day))

    print()

    # ask user if dates are ok
    current_startDate_str = datetime.strftime(current_startDate, "%d %B %Y")
    print("New Start Date: {}".format(current_startDate_str))
    current_endDate_str = datetime.strftime(current_endDate, "%d %B %Y")
    print("New End Date: {}".format(current_endDate_str))
    print("Is this the new date range you wanted? ('y' for Yes and 'n' for No): "
          , end = "")
    decision = input().lower()

    # validate user input
    if (decision != 'y') and (decision != 'n'):
      os.system("clear")
      print("ERROR ENCOUNTERED: \"{}\" is not a valid input".format(decision))
      print("Please enter either 'y' or 'n'")
      #time.sleep(2)
      os.system("clear")
      valid = False

    if valid:
      break

  # checks if dates should be saved or not
  if decision == 'n':
    saved = False
  else:
    saved = True
    current_startDate_str = datetime.strftime(current_startDate, "%Y-%m-%d")
    current_endDate_str = datetime.strftime(current_endDate, "%Y-%m-%d")
    dateRangeOriginal.update({"startDate": current_startDate_str})
    dateRangeOriginal.update({"endDate": current_endDate_str})
  
  return saved


'''
Performs all main menu processing
'''
def menuProcessing(parameters_q1, parameters_q2, parameters_q3, parameters_q4):
  printMenu()
  
  # Validating user input
  choice = input()
  while True:
    valid = validateIntInput(choice, 1, 5)
    if valid:
      break
    else:
      printMenu()
      choice = input()
      
  # Exiting program - Only way to exit program other than keyboard interrupt
  if choice == "5":
    os.system("clear")
    print("************************ EXITING PROGRAM ************************")
    print("Thank you for listening to our demo!")
    print("Do you have any questions?")
    sys.exit(0)

  # q1 menu
  if choice == "1":
    while True:
      # Print q1 info
      os.system("clear")
      print("********************************************* QUESTION 1 *********************************************")
      print("Was the COVID-19 positivity rate for adults 18+ higher in areas with more available tests per person?")
      print()
      print("     Will the positivity rate go up as testing capacity increases for COVID-19? We wish to see the effect")
      print("of test availability on positivity rates for a specified period of time. Although having a greater number")
      print("of tests allows health units to reach a greater number of individuals and potentially more individuals with")
      print("COVID-19, it may be the case that there is an inverse relationship between positivity rates and testing")
      print("availability.")
      print()
      print("1. Process data and create a graph")
      print("2. Parameter Settings")
      print("3. Return to main menu")
      print("Choose an option to perform:", end = " ")
      action = input()
      # Validate input
      valid = validateIntInput(action, 1, 3)
      if not valid:
        continue

      # Process and create graph
      if action == "1":
        q1_dates = []
        q1_dates.append("")
        q1_dates.append(parameters_q1[0]['startDate'])
        q1_dates.append(parameters_q1[0]['endDate'])
        final_processing_q1(q1_dates)
        print("Processed File!")
        createQ1Plot()
        print("Created Plot!")
        print("Graph has been saved in \"q1.pdf\"")
        #time.sleep(2)
        os.system("clear")
        
      # go back to main menu
      elif action == "3":
        os.system("clear")
        break
        
      # Edit parameters
      elif action == "2":
        parameterSettings(1, parameters_q1)
        
  # q2 menu
  if choice == "2":
    while True:
      # Print q2 info
      os.system("clear")
      print("********************************************* QUESTION 2 *********************************************")
      print("Where did the vaccine mandate have a positive effect on vaccine administration rate?")
      print()
      print("     Did the vaccine mandate increase the vaccination rate per day while it was in effect?")
      print("Does the effectivness depend on the location or is it universal?")
      print("After a long time, a lot of contraversy sprouted from the vaccine mandate.")
      print("Did the vaccine mandate help or was it just a headache?")
      print("An increased administration rate should mean that the mandate was effective")
      print()
      print("1. Process data and create a graph")
      print("2. Parameter Settings")
      print("3. Return to main menu")
      print("Choose an option to perform:", end = " ")
      action = input()
      valid = validateIntInput(action, 1, 3)
      if not valid:
        continue

      # go back to main menu
      if action == "3":
        os.system("clear")
        break
        
      # Edit parameters
      elif action == "2":
        parameterSettings(2, parameters_q2)

      # process and create graph
      elif action == "1":
        processQ2Data(parameters_q2[0])
        print("Processed File!")
        createQ2Plot()
        print("Created Plot!")
        print("Graph has been saved in \"q2.pdf\"")
        #time.sleep(2)
        os.system("clear")

  #q3 menu
  if choice == "3":
    while True:
      # Print q3 info
      os.system("clear")
      print("********************************************* QUESTION 3 *********************************************")
      print("Are fewer negative tests being done as the number of vaccinated people increases in Ontario?")
      print()
      print("     COVID-19 has often been compared with other illnesses such as influenza or the common cold.") 
      print("Early symptoms are similar between these diseases, after all.")
      print("However, with the number of administered vaccine doses increasing, are such mistakes decreasing?")
      print("We thought to see whether there was a correlation between the number of vaccinated people and the total")
      print("number of negative COVID tests done in Ontario.")
      print()
      print("1. Process data and create a graph")
      print("2. Parameter Settings")
      print("3. Return to main menu")
      print("Choose an option to perform:", end = " ")
      choice = input()
      #validate user input
      valid = validateIntInput(choice, 1, 3)
      if not valid:
        continue

      # go back to main menu
      if choice == "3":
        os.system("clear")
        break
        
      # Edit parameters
      elif choice == "2":
        parameterSettings(3, parameters_q3)

      # Process and create graph
      elif choice == "1":
        processQ3Data(parameters_q3)
        print("Processed File!")
        # Find name of selected phu
        phu_num = parameters_q3[1]["phuSelected"][0]
        phu_name = ""
        for phu in phu_list:
          phu_num_check = int(phu[0:4])
          if phu_num == phu_num_check:
            phu_name = phu[5:len(phu)]
        
        createQ3Plot(phu_name)
        print("Created Plot!")
        print("Graph has been saved in \"q3.pdf\"")
        #time.sleep(2)
        os.system("clear")

        
  #q4 menu
  if choice == "4":
    while True:
      # Print q4 info
      os.system("clear")
      print("********************************************* QUESTION 4 *********************************************")
      print("How many working years were lost due to COVID-19 deaths in Canada compared to other leading causes")
      print("of death?")
      print()
      print("     Given the major financial burden that the pandemic has placed upon the shoulders of Canadians, we ")
      print("wishto quantify the effects of this terrible virus. This tool allows for the direct comparision of working years lost due to COVID-19 and 51 other leading causes of death accross all age groups in Canada.")
      print()
      print("1. Process data and create a graph")
      print("2. Parameter Settings")
      print("3. Return to main menu")
      print("Choose an option to perform:", end = " ")
      choice = input()

      valid = validateIntInput(choice, 1, 3)
      if not valid:
        continue
      if choice == "2":
        parameterSettings(4, parameters_q4)
      elif choice == "3":
        os.system("clear")
        break 
      elif choice == "1":
        causes_of_death = []
        for cause in parameters_q4[0]['diseaseSelected']:
          causes_of_death.append(str(cause))
        processQ4(causes_of_death)
        print("Processed File!")
        createQ4Plot()
        print("Created Plot!")
        print("Graph has been saved in \"q4.pdf\"")
        #time.sleep(3)
        os.system("clear")
      
def main():
  os.system("clear")
  print("************************ 2250 GROUP PROJECT DEMO ************************")
  print()
  print("               Welcome to our demo for the Group Project!")
  print()
  print("  Date:")
  print("       28 March 2022")
  print()
  print("  Team Name:")
  print("       Group")
  print("  Team Members:")
  print("       Charlotte Barnes")
  print("       Ronan Chay Loong")
  print("       Ryan Nguyen ")
  print()
  #time.sleep(25)
  os.system("clear")

  #initalization of paramters
  parameters_q1 = [
    {
      "type": "dateRange",
      "startDate": DEFAULT_STARTDATE,
      "endDate": DEFAULT_ENDDATE
    }
  ]
  parameters_q2 = [
    {
      "type": "phuNum",
      "multiple": True, # see if multiple phu can be chosen at once
      "range": [1, 2],  # gives range of number of phus that can be selected in the form of [minimum, maximum]
      "phuSelected": [2226, 2227] # stores phu num of selected phus
    }
  ]
  parameters_q3 = [
    {
      "type": "dateRange",
      "startDate": DEFAULT_STARTDATE,
      "endDate": DEFAULT_ENDDATE
    },
    {
      "type": "phuNum",
      "multiple": False,
      "range": [1, 1],
      "ontario": False,  # flag to know if user wants data for all of ontario ie all phus
      "phuSelected": [2226]
    }
  ]
  parameters_q4 = [
    {
      "type": "disease",
      "multiple": True,
      "range": [0, 51],
      "diseaseSelected": [0, 1, 2, 44]  # stores id of diseases selected
    }
  ]
  while True:
    menuProcessing(parameters_q1, parameters_q2, parameters_q3, parameters_q4)

main()