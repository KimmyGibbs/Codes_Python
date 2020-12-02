import json

class Logfile2Json():

    def __init__(self):
        ## sample file : https://www.ibm.com/support/knowledgecenter/en/SSLTBW_2.1.0/com.ibm.zos.v2r1.hald001/exmlogfile.htm
        self.FIELD_NAMES = [
            'date', 'time', 'cs-method', 'cs-uri-stem', 'cs-uri-query', 
            's-port', 'cs--username', 'c-ip', 'cs-version', 'cs(User-Agent)', 
            'cs(Cookie)', 'cs(Referer)', 'cs-host', 'sc-status', 'sc-substatus', 
            'sc-win32-status', 'sc-bytes', 'cs-bytes', 'time-taken']

    def log2json_init(self):
        f_dict = {}        

        ## file read
        f_path = 'C:/ElasticStack/SampleData/log/u_ex171118-sample.log'

        f = open(f_path, "r")

        ### read all lines of file (lines = {~, ~, ~})
        lines = f.readlines()

        ### read each line of file
        for line in lines:
            ### split line by word
            dict_val = line.split()
            ### search each index of FIELD_NAMES as enumerate
            for i, f_names_val in enumerate(self.FIELD_NAMES):
                f_dict[f_names_val] = dict_val[i]
                with open('test.json', 'w', encoding="utf-8") as make_file:
                        json.dump(f_dict, make_file, ensure_ascii=False, indent="\t")
        f.close()

    ## multiline text convert to json
    def log2json_multilines(self):       
        ## file read
        f_path = 'u_ex171118-sample.log'
        ## dict1 is wrapping json component like as label
        dict1 = {}
        ### dict2 is saved text component as json format
        dict2 = {}
        ## text (or .log) file open
        with open(f_path) as f:
            ### init indexing num
            i = 0
            ### init labeling num
            l = 1
            for line in f:
                ### description is array about each line in text file
                description = list( line.strip().split(None, len(self.FIELD_NAMES)) )
                ### test print ==> ['date_val', 'time_val', ... , 'time_taken_val']
                ### print(description)
                ### auto labeling as numbering form
                sno = 'logSequence_' + str(l)
                ### 
                while i<len(self.FIELD_NAMES):
                    ### creating dictionary for each FIELD_NAMES
                    dict2[self.FIELD_NAMES[i]] = description[i]
                    i = i + 1
                ### make dict2 finish
                ### matching each label(dict1) with dict2
                dict1[sno] = dict2
                l = l + 1
                '''
                "logSquence_1": {
                    dict2's component list as json format
                    ...
                }
                '''
        ### creating json file
        make_json = open("new_test.json", "w")
        json.dump(dict1, make_json, indent = '\t')
        make_json.close()

    def log2ndjson_multilines(self):
        f_path = 'D:/CodeTest/personal_working/SampleData/u_ex171118-sample.log'
        line_of_file_list = []
        json_value_array = []
        pair_idx = 0
        json_pair_dict = {}
        pair_list = []

        with open(f_path) as f:
            lines = f.readlines() ## 파일 한줄씩 읽기 OK
            for line in lines:
                line_of_file_list.append(line) ## 파일의 한줄씩을 list의 component로 만듦 OK
                #print(line)
            
            for col in line_of_file_list:   ## line_of_file_list는 log 파일의 한줄이 하나의 값인 리스트
                json_value_array.append(list(col.strip().split(None, len(self.FIELD_NAMES))))    ## line_of_file_list[i]의 문자열을 나누기 as value of JSON type document
                #print(json_value_array)
                
                for json_value_col in json_value_array: ## JSON의 value 항목들을 가지고 있는 array에서 하나의 column (여기서는 json_value_col)씩 읽기
                    while pair_idx < len(self.FIELD_NAMES): ## FIELD_NAMES의 길이(19)만큼 indexing
                        json_pair_dict[self.FIELD_NAMES[pair_idx]] = json_value_col[pair_idx] ## json_pair_dict을 활용해 key:value 쌍(pair) 만들기
                        pair_idx = pair_idx + 1
                    pair_list.append(json_pair_dict) ## pair는 다시 while문 들어가면 값이 덮어씌워지므로 data loss 방지하기 위해서 리스트에 다시 집어넣기
                    pair_idx = 0
                
                '''
                List Status
                    # json_value_array[0] => ['2017-11-18', '08:48:20', 'GET', '/de', 'adpar=12345&gclid=1234567890', '443', '-', \
                    #                          '149.172.138.41', 'HTTP/2.0', \
                    # 'Mozilla/5.0+(Windows+NT+10.0;+Win64;+x64)+AppleWebKit/537.36+(KHTML,+like+Gecko)+Chrome/62.0.3202.89+Safari/537.36+OPR/49.0.2725.39', \
                    #                           '-', 'https://www.google.de/', 'www.site-logfile-explorer.com', '301', '0', '0', '624', '543', '46']
                    # json_value_array[0][0] => 2017-11-18
                '''
        #print(pair_list)
        ''' ## json.dump를 사용한 JSON 파일 생성
        with open("today.json", "w", encoding="UTF-8") as make_json:
            json.dump(pair_list, make_json, ensure_ascii=False, indent=None)
        '''
        ''' ## json.dumps를 사용한 JSON 파일 생성
        with open('today.json', 'w') as make_json:
            make_json.write(json.dumps(pair_list, ensure_ascii=False, indent='\r'))
        '''
        init_json = json.dumps(pair_list, indent='\t') ## key:value pair 리스트를 json 포맷으로 변경
        ndjson = [json.dumps(record) for record in json.loads(init_json)] ## json 포맷을 ndjson 포맷으로 변경
        #print('\n'.join(ndjson))
        with open('today.json', 'w') as make_ndjson:
            make_ndjson.write('\n'.join(ndjson)) ## ndjson 파일 생성
            
        ''' ### 결과 예시
        {key1:value1, key2:value2,...}
        {key1:value1, key2:value2,...}
        ...
        ### 만약, each dictionary에 ',' 옵션을 주고 싶다면 ',\n'.join() 사용 ==> 이후 첫 줄에 ',' 제거
        '''
