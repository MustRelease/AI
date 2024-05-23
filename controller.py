import requests, json
import urllib.parse

class Controller:
    def init_db(self, userId):
        r = requests.post("http://sw.uos.ac.kr:8000/make/collection", data=json.dumps({'userId' : userId}))
        return r.status_code

    def init_save(self, initData):
        save_data = []
        for d in initData.data:
            dic = {
				"userId" : initData.userId,
				"timestamp" : 0,
				"observation" : d.content,
				"importance" : 1.0,
                "isEventScene" : False
			}
            save_data.append(dic)
        r = requests.post("http://sw.uos.ac.kr:8000/memory/add", data=json.dumps(save_data))
        if r.status_code != 200:
            return r.status_code
        return r.status_code

    def save(self, userId, playTime, content, importance):
        save_data = []
        times = playTime.split(sep=":")
        time = 3600 * int(times[0]) + 60 * int(times[1]) + int(times[2])
        dic = {
				"userId" : userId,
				"timestamp" : time,
				"observation" : content,
				"importance" : importance,
                "isEventScene" : True
			}
        save_data.append(dic)
        r = requests.post("http://sw.uos.ac.kr:8000/memory/add", data=json.dumps(save_data))
        return r.status_code

    def save_all(self, memories, isEvent):
        save_data = []
        for data in memories:
            times = data.playTime.split(sep=":")
            time = 3600 * int(times[0]) + 60 * int(times[1]) + int(times[2])
            dic = {
		    		"userId" : data.userId,
		    		"timestamp" : time,
		    		"observation" : data.content,
		    		"importance" : data.importance,
                    "isEventScene" : isEvent
		    	}
            save_data.append(dic)
        r = requests.post("http://sw.uos.ac.kr:8000/memory/add", data=json.dumps(save_data))
        return r.status_code

    def load_memory(self, query, userId):
        encode_query = urllib.parse.quote(query)
        url = "http://sw.uos.ac.kr:8000/memory/get/"
        url += (encode_query + "/")
        url += (userId + "/10")
        r = requests.get(url)
        return r.json()

    def load_buffer(self, userId):
        url = "http://sw.uos.ac.kr:8000/memory/get/buffer/"
        url += userId
        r = requests.get(url)
        return r.json()

    def relocate_buffer(self, userId):
        url = "http://sw.uos.ac.kr:8000/memory/relocate/"
        url += userId
        r = requests.patch(url)
        return r.status_code
