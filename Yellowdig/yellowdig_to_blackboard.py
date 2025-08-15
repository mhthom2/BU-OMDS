# -*- coding: utf-8 -*-
"""
Created on Tue May  6 17:18:27 2025

@author: Matt Thomas

Description : 
     This script processes Yellowdig participation grades from a CSV export 
     and formats them for direct import into Blackboard's grade center.

Usage:
     python yellowdig_to_blackboard.py <input_csv> <possible_course_points> <percent_yellowdig>

Arguments:
     <input_csv>                The CSV file exported from Yellowdig, which should be in the same directory.
     <possible_course_points>   Total number of points possible for course. (found in syllabus)
     <percent_yellowdig>        Percentage of grade assigned to Yellowdig (also in syllabus), expressed as an integer.
     
Exampl:
     For instance, there might be 1000 points possible in the course and Yellowdig is 2% of the grade: 

     python3 yellowdig_to_blackboard.py yellowdig_export.csv 1000 2 
     
     or within Jupyter QtConsole: %run yellowdig_to_blackboard.py Yellowdig-points.csv 1000 2

Output:
     A CSV file ready to be imported into Blackboard.
"""

import sys
import pandas as pd

# Name of Yellowdig file 
filename = sys.argv[1]
# Cast number of number of course points to integer 
course_points = int(sys.argv[2])
# Percentage Yellowdig
yellowdig_percent = int(sys.argv[3]) / 100
# Possible points awarded to Yellowdig 
points = course_points * yellowdig_percent

# Load data
df = pd.read_csv(filename)
# Remove unneeded columns 
df = df.drop(['user/username', 'Total Points Earned'], axis=1)
# Add columns for Yellowdig score 
df['Yellowdig'] = round(df['Participation Grade'] * points, 4)

# Clean-up column names to match Blackboard requirements 
df = df.rename(columns={'user/firstname' : 'First Name',
                        'user/lastname' : 'Last Name'}).drop('Participation Grade', axis=1)

# Split emails into usernames and BU domain
splits = df['user/primary-email'].str.split('@')
# Set column with usernames 
df['Username'] = [pair[0] for pair in splits]

# Set-up dataframe in Blackboard format with Yellowdig as the name of the assignment
final_df = df[['Username', 'Last Name', 'First Name', 'Yellowdig']]

# File export grades to 
BLACKBOARD_FILE_NAME = 'ReadyToImport_Yellowdig.csv'
# Write scores to file 
final_df.to_csv(BLACKBOARD_FILE_NAME, index=False)


