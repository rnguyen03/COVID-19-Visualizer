#!/usr/bin/env python
'''
q1_plot.py
  Author(s): Charlotte Barnes(1154105), Tia Yun Fat Jeffrey Ronan Chay Loong(1181166), Ryan Nguyen(1187680)

  Project: Milestone 2
  Date of Last Update: March 29, 2022

  Functional Summary
      Create scatterplot from data/processed_data/final_positivity_by_test.csv
'''

import sys
import pandas as pd
import seaborn as sns
from matplotlib import pyplot as plt
from matplotlib import ticker as ticktools

def createQ1Plot():
  csv_filename = "data/processed_data/final_positivity_by_test.csv"
  # open processed data
  try:
        csv_df = pd.read_csv(csv_filename)

  except IOError as err:
      print("Unable to open source file", csv_filename,
              ": {}".format(err), file=sys.stderr)
      sys.exit(-1)
  # create figure
  fig = plt.figure()
  # draw plot
  ax = sns.scatterplot(y = "AVG_POS", x = "AVG_TEST", hue = "PHU", data=csv_df)
  # adjust x axis
  ax.xaxis.set_major_locator(ticktools.MaxNLocator(12))
  # style labels
  plt.xticks(rotation = 45, ha = 'right')
  # add y label
  plt.ylabel("Percent positivity (%)")
  # add x label
  plt.xlabel("Average number of tests available per 1000 people")
  # add title
  plt.title("Percent Positivity by Number of Tests Available by Ontario Public Health Unit")
  # add legend to right of graph
  plt.legend(loc='center left', bbox_to_anchor=(1.25, 0.5), ncol=1)
  # save as pdf
  fig.savefig("q1.pdf", bbox_inches="tight")
