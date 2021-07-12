import json
from datetime import datetime
from MyPerfectRequest import MyPerfectRequest

inn_list = ['0000', '7736050003']

class Nalog():
    def __init__(self, inn_list):
        self.inn_list = inn_list
        self.inn = ''
        self.req = MyPerfectRequest.Get(use_proxy=True, desktop_headers=True)

    def start(self):
        start_url = 'https://bo.nalog.ru/nbo/organizations/search?query='
        result = []
        for inn in self.inn_list:
            self.inn = inn
            url = start_url + inn
            req = self.req.request(url).json()
            print(req)
            if not req:
                result.append({inn: 'is not exists'})
            r = self.bo_parse(req)
            result.append(r)

        with open(f'{datetime.today().strftime("%Y-%m-%d %H:%M:%S")}.json', 'w') as j:
            j.write(json.dumps(result))

    def bo_parse(self, data):
        organization_id = data['content'][0]['id']
        link = f'https://bo.nalog.ru/nbo/bfo/{organization_id}/details'
        try:
            req = self.req.request(link).json()
            r = self.audit(req)
        except:
            r = {self.inn: 'is not exists'}
        return r

    def audit(self, data):
        audit = data[0]
        date = datetime.today().strftime("%Y-%m-%d %H:%M:%S")
        bo = self.bo_gen(audit)
        r = {
            'parse_date': date,
            'inn': self.inn,
            'bo': bo
        }
        return r

    def bo_gen(self, audit):
        bo = {}
        for key, val in audit.items():
            bo = {**bo, **{key: val}}
        return bo


if __name__ == '__main__':
    n = Nalog(inn_list)
    n.start()
