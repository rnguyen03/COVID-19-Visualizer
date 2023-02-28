'''
q2_plot.py
  Author(s): Charlotte Barnes(1154105),
             Tia Yun Fat Jeffrey Ronan Chay Loong(1181166),
             Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Contains the function createQ2Plot(). This function creates the line plot for Question 2 
      using the data from data/processed_data/q2_data_file.csv
'''
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as ticktools

#generates the a graph in PDF from based off of the data/processed_data/q2_data_file.csv file
def createQ2Plot():
  # opening processed file for data
  csv_filename = "data/processed_data/q2_data_file.csv"
  try:
      csv_df = pd.read_csv(csv_filename)
  except IOError as err:
    print("Unable to open source file", csv_filename,": {}".format(err), file=sys.stderr)
    sys.exit(-1)

  # creating figure
  fig = plt.figure()
  
  # plotting graph
  ax = sns.lineplot(x = "Date", y = "One_dose_percentage", hue="PHU_num", data=csv_df)

	# set the number of axis labels to 5
  ax.xaxis.set_major_locator(ticktools.MaxNLocator(8))

  # rotate the ticks on the x-axis to 45 degrees
  plt.xticks(rotation = 45, ha = 'right')

  # setting title of graph
  plt.title("One_dose_percentage")

  # saving graph to q2.pdf
  fig.savefig("q2.pdf", bbox_inches="tight")

def main():
  createQ2Plot()
main()