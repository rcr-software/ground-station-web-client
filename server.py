
import web
import threading
import json
import time

urls = (
    '/data', 'data',
    '/', 'hello',
    '/(.*)', 'static'
)
app = web.application(urls, globals())

database = dict()


def background_read_data_maker():
    data = []
    fifo = None
    def get_data_from_time_range(start, end):
        nonlocal data
        return_lines = []
        for t, line in data:
            if t > start and t < end:
                return_lines.append(line)
        return return_lines
    
    def background_read_data():
        nonlocal fifo, data
        while True:
            if fifo is None:
                fifo = open('datastream', 'r')
            line = fifo.readline()
            if line != "":
                line = line.strip()
                data.append((time.time()*1000, line))
                print('got data: ', line)

    return get_data_from_time_range, background_read_data



        

get_data_from_time_range, background_read_data = background_read_data_maker()

thread = threading.Thread(target=background_read_data, args=())
thread.daemon = True
thread.start()

class hello():
    def GET(self):
        return open('index.html').read()

class data():
    def GET(self):
        d = web.input(start=None, end=None)
        d.start = float(d.start)
        d.end = float(d.end)
        if not d.start or not d.end:
            return 'need start and end!!'
        return json.dumps(get_data_from_time_range(d.start, d.end))

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
