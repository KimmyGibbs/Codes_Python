## 공공데이터포털 : 건축물대장정보 서비스
## https://www.data.go.kr/tcs/dss/selectApiDataDetailView.do?publicDataPk=15044713
import requests
from urllib.request import Request, urlopen
from urllib.parse import urlencode, quote_plus, unquote
import json
import xmltodict

key = "API_KEY" ## 공공데이터 포탈 기준
url = "http://apis.data.go.kr/1611000/BldRgstService/getBrBasisOulnInfo"
## 쿼리 파라미터는 API 문서 참고 추천
queryParams =  '?' + 'sigunguCd=' + '11680' + '&bjdongCd=' + '10300' \
                    + '&bun=' + '0012' + '&ji=' + '0000' + '&ServiceKey=' + key                

url = url + queryParams
res = requests.get(url)

#result = res.content ## .content : byte type이라 unicode로 값이 나오는 것 같은데..

result = res.text ## utf-8 인코딩 기준, 한글 출력 잘 된다
print("XML Contents\n", result) ## OpenAPI 정보 xml print finish

jsonString = json.dumps(xmltodict.parse(result), indent=4, ensure_ascii=False)
print("JSON Content\n", jsonString) ## json print from xml string