import hashlib  #hash
import requests
import json
import time
import uuid

class YouDaoFanyi():
    def __init__(self, appKey, appSecret):
        self.YOUDAO_URL = 'https://openapi.youdao.com/api/'
        self.APP_KEY = '7a8e1e60f26f8514'  # 应用id
        self.APP_SECRET = 'rSZorXXlhX6tglvqvZsOXl2jQVn81MOI'  # 应用密钥
        self.langFrom = 'en'   # 翻译前文字语言,auto为自动检查
        self.langTo = 'zh-CHS'     # 翻译后文字语言,auto为自动检查
        #self.vocabId = "用户词表ID"

    def encrypt(self,signStr):     #加密
        hash_algorithm = hashlib.sha256()    #sha256加密
        hash_algorithm.update(signStr.encode('utf-8'))
        return hash_algorithm.hexdigest()
    
    def truncate(self,q):
        if q is None:
            return None
        size = len(q)
        return q if size <= 20 else q[0:10] + str(size) + q[size - 10:size]

    def do_request(self,data):
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        return requests.post(self.YOUDAO_URL, data=data, headers=headers)


    def translate(self,q):
        data = {}
        data['from'] = self.langFrom
        data['to'] = self.langTo
        data['signType'] = 'v3'
        curtime = str(int(time.time()))
        data['curtime'] = curtime
        salt = str(uuid.uuid1())
        signStr = self.APP_KEY + self.truncate(q) + salt + curtime + self.APP_SECRET
        sign = self.encrypt(signStr)
        data['appKey'] = self.APP_KEY
        data['q'] = q
        data['salt'] = salt
        data['sign'] = sign
        response = self.do_request(data)
        
        result = json.loads(response.content.decode('utf-8'))['translation'][0]
        #print(result)
        return result 
