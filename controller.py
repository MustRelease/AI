import requests, json
import urllib.parse

base_url = "http://ec2-3-25-229-168.ap-southeast-2.compute.amazonaws.com:8000/"

class Controller:
    def init_db(self, userId):
        r = requests.post(base_url + "make/collection", data=json.dumps({'userId' : userId}))
        return r.status_code

    def init_save(self, initData):
        save_data = []
        for d in initData.data:
            dic = {
				"userId" : initData.userId,
				"timestamp" : 0,
				"observation" : d.content,
				"importance" : 1.0,
                "isEventScene" : False,
                "reasonIds" : "null"
			}
            save_data.append(dic)
        r = requests.post(base_url + "memory/add", data=json.dumps(save_data))
        if r.status_code != 200:
            return r.status_code
        return r.status_code

    def save(self, userId, playTime, content, importance, reason_list=None):
        save_data = []
        dic = {
				"userId" : userId,
				"timestamp" : 0,
				"observation" : content,
				"importance" : importance,
                "isEventScene" : True,
                "reasonIds" : "null" if reason_list==None else reason_list
			}
        save_data.append(dic)
        r = requests.post(base_url + "memory/add", data=json.dumps(save_data))
        return r.status_code

    def save_all(self, memories, isEvent):
        save_data = []
        for data in memories:
            dic = {
		    		"userId" : data.userId,
		    		"timestamp" : 0,
		    		"observation" : data.content,
		    		"importance" : data.importance,
                    "isEventScene" : isEvent,
                    "reasonIds" : "null"
		    	}
            save_data.append(dic)
        r = requests.post(base_url + "memory/add", data=json.dumps(save_data))
        return r.status_code

    def load_memory(self, query, userId):
        encode_query = urllib.parse.quote(query)
        url = base_url + "memory/get/"
        url += (encode_query + "/")
        url += (userId + "/10")
        r = requests.get(url)
        return r.json()

    def load_memory_id(self, id, userId):
        url = base_url + "memory/get/id/"
        url = url + userId + "/"
        url += str(id)
        r = requests.delete(url)
        return r.status_code

    def load_buffer(self, userId):
        url = base_url + "memory/get/buffer/"
        url += userId
        r = requests.get(url)
        return r.json()

    def relocate_buffer(self, userId):
        url = base_url + "memory/relocate/"
        url += userId
        r = requests.patch(url)
        return r.status_code

    def delete_buffer(self, userId):
        url = base_url + "memory/delete/buffer/all/"
        url += userId
        r = requests.delete(url)
        return r.status_code
