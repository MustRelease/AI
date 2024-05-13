import requests, json

class Controller:
    def init_db(self, userId):
        r = requests.post("http://sw.uos.ac.kr:8000/make/collection", data=json.dumps({'userId' : userId}))
        return r.status_code

    def init_save(self, initData):
        for d in initData.data:
            dic = {
				"userId" : initData.userId,
				"timestamp" : 0,
				"observation" : d.content,
				"importance" : 1.0
			}
            r = requests.post("http://sw.uos.ac.kr:8000/memory/add", data=json.dumps(dic))
            if r.status_code != 200:
                return r.status_code
        return r.status_code

    def save(self, userId, playTime, content, importance):
        times = playTime.split(sep=":")
        time = 3600 * int(times[0]) + 60 * int(times[1]) + int(times[2])
        dic = {
				"userId" : userId,
				"timestamp" : time,
				"observation" : content,
				"importance" : importance
			}
        r = requests.post("http://sw.uos.ac.kr:8000/memory/add", data=json.dumps(dic))
        return r.status_code

    def load_memory(self, query, userId):
        url = "http://sw.uos.ac.kr:8000/memory/get/"
        url += (query + "/")
        url += userId
        r = requests.get(url)
        return r.json()
