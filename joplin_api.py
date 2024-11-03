import requests
import json
import configparser

config = configparser.ConfigParser()
config.read('config.ini')

class Routine():
    TOKEN_VALUE = config['USERDATA']['TOKEN_VALUE'] 
    BASE_URL = config['USERDATA']['BASE_URL']
    NOTES = 'notes'

    def __init__(self) -> None:
        self.state = {}
        self.load_state()

    def token(self,url):
        return url + "?token="+self.TOKEN_VALUE
    
    def get_all(self):
        session = requests.Session()
        session.auth = ('token',self.TOKEN_VALUE)
        resp = session.get(url= (self.token(self.BASE_URL+self.NOTES)+'&fields=id,title,updated_time'))
        resp_dict = json.loads(resp.text)
        return resp_dict
    
    def save_state(self):
        json_state = self.get_all()
        with open('state.json', 'w') as file:
            json.dump(json_state, file)
    
    def load_state(self):
        with open('state.json', 'r') as file:
            self.state = json.load(file)

    def compare_state(self):
        new_state = self.get_all()
        if new_state == self.state:
            print("Mesma coisa")
        else:
            print("Teve mudança")

    def create_example(self):
        session = requests.Session()
        session.auth = ('token',self.TOKEN_VALUE)
        data_json = { "title": "My note", "body": "Some note in **Markdown**"}
        resp = session.post(url= self.token(self.BASE_URL+self.NOTES),data=json.dumps(data_json))
        resp_dict = json.loads(resp.text)
        print(resp_dict)
        print()

    def modify_note_exemple(self):
        session = requests.Session()
        session.auth = ('token',self.TOKEN_VALUE)
        id = '4a67474dc3dc4473973b4acc657a2880'
        data_json = { "title": "My note", "body": "BUNDA TOP"}
        resp = session.put(url= self.token(self.BASE_URL+self.NOTES+'/'+id),data=json.dumps(data_json))
        resp_dict = json.loads(resp.text)
        print(resp_dict)
        print()

Routine().compare_state()