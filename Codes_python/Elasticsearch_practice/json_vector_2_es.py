from elasticsearch import Elasticsearch
from elasticsearch import helpers
import time
import json
import glob

class ES_dense:
    def __init__(self):
        self.es = Elasticsearch(hosts=["http://localhost:9200"], timeout=30, max_retries=100, retry_on_timeout=True)
        self.dense_idx = 'dense_test'
        ## 추후 vector dimension이 변경되면 매핑 시 값 조절 가능
        self.vec_dims = 300

    def dense_vector_es(self):
        dense_q_body = {
             "mappings": {
                "properties": {
                    "doc_title_STR": {
                        "type": "text" 
                    },
                    "doc_pdf_url_STR": {
                        "type": "text"
                    },
                    "doc_id_STR": {
                        "type": "text"
                    },
                    "channel_name_STR": {
                        "type": "text"
                    },
                    "chapter_name_STR": {
                        "type": "text"
                    },
                    "channel_language_STR": {
                        "type": "text"
                    },
                    "chapter_start_page_INT": {
                        "type": "integer"
                    },
                    "chapter_end_page_INT": {
                        "type": "integer"
                    },
                    "chapter_summary_STR": {
                        "type": "text"
                    },
                    "chapter_text_STR": {
                        "type": "text"
                    },
                    "chapter_vector_LIST": {
                        "type": "dense_vector",
                        "dims": self.vec_dims
                    },
                    "extract_keyword_LIST": {
                        "type": "keyword"
                    },
                    "page_text_STR": {
                        "type": "text"
                    },
                    "page_vector_LIST": {
                        "type": "dense_vector",
                        "dims": self.vec_dims
                    }
                }
            }
        }
        ## Index 중복 여부 체크 후 Idx Scheme 생성
        if self.es.indices.exists(self.dense_idx) == True:
            print("동일한 인덱스명("+self.dense_idx+")이 존재합니다. 인덱스명을 확인해주세요.")
        else:
            self.es.indices.create(index=self.dense_idx, body=dense_q_body)

        self.json2ES_bulk() ## json data bulk to Elasticsearch
    
    def json2ES_bulk(self):
        target_path = "/Users/mskim/Desktop/json_samples/*_unit_*.json"
        file_cnt = 1
        files_list = glob.glob(target_path)
        dict_list = []
        print("JSON File reading...")
        for file_name in files_list:
            with open(file_name, "r", encoding="utf-8") as json_file:
                json_data = json.load(json_file)
                dict_list += [json_data]
                file_cnt += 1 ## 파일 개수 체크
        action = dict_list
        bulk_start = time.time()
        helpers.bulk(client=self.es, actions=action, index=self.dense_idx)
        bulk_end = time.time()-bulk_start

        print(str(file_cnt) + "개의 파일 Bulk 소요시간: "+ str(bulk_end) +" sec")


if __name__ == "__main__":
    obj = ES_dense()
    obj.dense_vector_es()