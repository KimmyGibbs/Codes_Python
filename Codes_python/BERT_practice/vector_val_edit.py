from elasticsearch import Elasticsearch ## git에다가 정리해볼까..
from elasticsearch import helpers
import math
## BERT에서 원하는 벡터값을 받아왔다고 가정
## 해당 리스트는 BERT Tutorial 수행 후, layer 개수(12개) 만큼 반복하여 벡터값을 저장한 리스트이다
## len(LIST) is 12 that be considered dims in ES
bert_init_res = [' 0.7795,  0.0712, -3.1866, -0.1754, -1.6867', 
                ' 1.1940,  0.5174, -2.1626, -0.0878, -0.4390', 
                ' 1.4634,  0.1623, -1.0486, -0.5986,  0.4816', 
                ' 2.0376,  0.6043, -1.5335, -0.6858,  0.8482', 
                ' 2.3391,  0.4184, -1.1123, -0.5445,  1.0927', 
                ' 2.0862,  0.1855, -1.2649, -0.0174,  0.6790', 
                ' 1.6657, -0.6275, -0.7260,  0.2000,  1.2586', 
                ' 1.1927, -0.0797, -1.1341,  0.6215,  0.9804', 
                ' 0.7028,  0.2555, -0.7486,  0.3023,  0.6843', 
                '-0.3867, -1.2279, -0.4509,  0.6132,  1.9610', 
                ' 0.2515,  0.0329, -1.0688,  1.5329,  2.6500', 
                ' 1.3352,  0.0856, -0.7011,  2.3049,  2.8961']
## bert_init_res -> convert to edit_list = [0.1, 0.2, -0.3, ..., ...]
print(bert_init_res)
print("\n")
rm_space_list = []
for idx in range(len(bert_init_res)-1):
    temp_list = ' '.join(bert_init_res[idx].split())
    print(temp_list)
    rm_space_list.append(temp_list)

edit_list = []
idx = 0
for idx in range(len(bert_init_res)-1):
    tmp = rm_space_list[idx] ## ex> tmp = '0.1, -0.2, -0.3, 0.4, 0.5'
    val_tmp=tmp.split(', ') ## ex> val_tmp = ['0.1', '-0.2', '0.3', '-0.4', '0.5']
    for col in range(len(val_tmp)):
        tmp_float=float(val_tmp[col])
        edit_list.append(tmp_float)
    idx += 1
#print(edit_list)

'''
## Elasticsearch 접속 (IP:PORT)
es = Elasticsearch(['http://ID:PWD@localhost:9200'])

index_name = 'ez_dense_vec_test'
body_context = {
    'query' : {
        'match' : {
            'filed_name' : 'text value'
        }
    }, 'size' : 5, 'explain' : True
}


results = es.search(index = index_name, body=body_context)
'''
