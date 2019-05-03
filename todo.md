## 功能迭代
May 2019

UI定型

April 2019 

### Portrait传输

```
    def postPortrait(self):
        #init portrait dict

        portraits = {"plist":[]}
        #load portrait
        print("[Load Portrait]")
        for portrait in os.listdir(r"./portrait"):              
            pname = portrait[:-4]
            print('./portrait/'+portrait)
            with open('./portrait/'+portrait, 'rb') as f:
                 img=base64.b64encode(f.read())
            pdata = img.decode('utf-8') 
            '''
            pdata = cv2.imread('./portrait/'+portrait)
            '''
            print("pdata type="+str(type(pdata)))

            #ndarray to list
            #pdata = pdata.tolist()
            print("pdata type="+str(type(pdata)))
            #add to dict
            tmpPDict={"name":pname,"data":pdata}
            portraits["plist"].append(tmpPDict)
            #print("portraits dict:"+str(portraits))
        print("[Load Portrait]-PASS") 
        print('[Post Portraits JSON]') 
        pJson = json.dumps(portraits)
        #print(pJson)
        post_portrait = ServHttp('POST','http://127.0.0.1:5000/api/portrait',portraits)
        try:
            post_portrait.process()
        except:
            print("[Portraits Json]-传输失败")
        else:
            print("[Portraits Json]-传输成功")   


```

### 邮件通知
