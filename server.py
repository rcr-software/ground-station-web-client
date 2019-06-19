
import web
import threading
import json
import time
import datetime

from read_database import connect_database, read_rocket, get_max_launch_id

urls = (
    '/data', 'data',
    '/', 'hello',
    '/(.*)', 'static'
)
app = web.application(urls, globals())


db = connect_database()
print('launch id --->>> ', get_max_launch_id(db))


class hello():
    def GET(self):
        return open('index.html').read()

class data():
    def GET(self):
        d = web.input(last_tn_id=None, last_tv_id=None)
        d.last_tn_id = int(d.last_tn_id)
        d.last_tv_id = int(d.last_tv_id)
        launch_id =  get_max_launch_id(db)
        if  d.last_tn_id is None or d.last_tv_id is None:
            self.BadRequest(message='must have last_tn_id and last_tv_id')
            return 'ERROR need last_tn_id and last_tv_id!!'
        return json.dumps(read_rocket(db, launch_id, d.last_tn_id, d.last_tv_id), default=str)

class static:
    def GET(self, fname):
        print('opening', fname)
        try:
            f = open('./'+fname, 'rb')
            return f.read()
        except:
            return '<h1>404</h1>' # you can send an 404 error here if you wan

if __name__ == "__main__":
    app.run()
