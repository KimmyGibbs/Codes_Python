import glob
import csv
import os
import re


target_path = "/*_result.txt"

list_of_files = glob.glob(target_path)

time_list = []
f_name_list = []

for f_list in list_of_files:
	f_name_list.append(re.sub('.txt', '', os.path.basename(f_list)))
	file = open(f_list, "r", encoding="utf-8")
	strings = file.readlines()
	time_list.append(strings[3])

	#print(strings)
	#print('\n')
#print(time_list)
#print(f_name_list)
'''
for row in time_list:
	# print(row)
	print(row.split(":"))
'''



header_info = time_list[0].split(":")
header_csv = header_info[0]

with open('./_2020_0731_laps_2.csv', 'w', newline='') as file:
	writer = csv.writer(file)
	writer.writerow([header_csv])
	for row in time_list:
		writer.writerow([re.sub('sec\n', '', row.split(":")[2])+ '\n'])
file.close()