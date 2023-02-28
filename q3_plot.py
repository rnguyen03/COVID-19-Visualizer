'''
q3_plot.py
  Author(s): Charlotte Barnes(1154105),
             Tia Yun Fat Jeffrey Ronan Chay Loong(1181166),
             Ryan Nguyen(1187680)

  Project: Milestone 3
  Date of Last Update: March 29, 2022

  Functional Summary
      Contains the function createQ3Plot(). This function creates the line plots for Question 3 
      using the data from data/processed_data/q3_data_file.csv
'''
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as ticktools
from matplotlib.lines import Line2D

def createQ3Plot(phu):
  # Opening and reading from processed data file
  csv_filename = "data/processed_data/q3_data_file.csv"
  try:
    csv_df = pd.read_csv(csv_filename)
  except IOError as err:
      print("Unable to open source file", csv_filename,
              ": {}".format(err), file=sys.stderr)
      sys.exit(-1)
    
  # create figure
  fig, ax1 = plt.subplots()
  
  # draw plot
  ax1 = sns.lineplot(y = "one_or_more_doses_cumulative", x = "Date", color = 'blue', data=csv_df)
  ax2 = ax1.twinx()
  sns.lineplot(y = "num_negative_7d_average", x = "Date", color = 'orange', data = csv_df, ax = ax2)
  
  # adjust x axis
  ax1.xaxis.set_major_locator(ticktools.MaxNLocator(12))
  # style labels
  plt.setp(ax1.get_xticklabels(), rotation=45)

  # set labels for axes and title
  ax1.set_xlabel("Date")
  ax1.set_ylabel("Number of People with One or More Vaccine Doses")
  ax2.set_ylabel("Number of Negative Tests (7 day average)")
  plt.title("Number of Vaccinated People vs Number of Negative Tests by Date".format(phu))

  # create legend
  plt.legend(handles=[Line2D([], [], color='blue', label='Number of Vaccinated People'), Line2D([], [], color='orange', label='Number of Negative Tests')], loc=(1.15,0.8), title = phu)

  # saving figure to q3.pdf file
  fig.savefig("q3.pdf", bbox_inches="tight")

def main(argv):
  createQ3Plot(2255) #arbitrary input for testing
  
main(sys.argv)