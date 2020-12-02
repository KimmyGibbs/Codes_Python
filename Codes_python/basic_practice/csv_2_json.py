#-*- coding:euc-kr -*-
import csv, json
### multiline csv convert to json

DESCRIPTION_VALS = ["STN_IDX", "STN_LINE", "STN_NM", "STN_ROAD_ADDR", "STN_ADDR", "STN_ZIP_CODE", "STN_PHONE"]

csv_path = '서울교통공사 지하철 역별 주소 정보.csv'
json_path = 'SeoulMetro_StnInfo.json'

test_description_dict = {}
test_data_dict = {}
test_data_list = []
test_whole_dict = {}

with open(csv_path, newline='') as csvFile:
    csvReader = csv.reader(csvFile, delimiter=',')
    for csvRow in csvReader:
        if csvReader.line_num == 1:
            for i in range(len(DESCRIPTION_VALS)):
                test_description_dict[DESCRIPTION_VALS[i]] = csvRow[i]
            test_whole_dict["DESCRIPTION"] = test_description_dict
        else:
            for i in range(len(DESCRIPTION_VALS)):
                test_data_dict[DESCRIPTION_VALS[i].lower()] = csvRow[i]
            test_data_list.append(test_data_dict)
        test_whole_dict["DATA"] = test_data_list
#print(test_description_dict)
#print(test_data_dict)
#print(test_data_list)
#print(test_whole_dict)

#print(json.dumps(test_whole_dict, ensure_ascii=False, indent=4))

with open(json_path, "w") as jsonFile:
    jsonFile.write(json.dumps(test_whole_dict,ensure_ascii=False, indent=4))
