#!/usr/bin/env python
'''
q4_plot.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 2
  Date of Last Update: March 29, 2022

  Functional Summary
      Create bar graph from covid_vs_disease_years_lost.csv
'''
import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt

def createQ4Plot():
  # open file with processed data
  csv_filename = "data/processed_data/covid_vs_disease_years_lost.csv"
  try:
    csv_df = pd.read_csv(csv_filename)
  except IOError as err:
    print("Unable to open source file", csv_filename,
            ": {}".format(err), file=sys.stderr)
    sys.exit(-1)
  # create figure
  fig = plt.figure()
  #draw barplot
  sns.barplot(x="NUMBER_OF_DEATHS", y="CAUSE", data=csv_df,
            label="Total", color="b")
  # rotate y axis tick marks
  plt.yticks(rotation = 45, ha = 'right')
  # add x axis label
  plt.xlabel("Total number of working years lost")
  # add y axis label
  plt.ylabel("Cause of death")
  # add title
  plt.title("Number of Working Years Lost Due to Top Causes of Death in Canada")
  # save as pdf
  fig.savefig("q4.pdf", bbox_inches='tight')
