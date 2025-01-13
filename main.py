import tornado.web
import tornado.ioloop
from handler.LogWebSocketHandler import LogWebSocketHandler
from handler.ProjectsHandler import ProjectHandler
from handler.SpecificProjectHandler import SpecificProjectHandler
from handler.StatusWebSocketHandler import StatusWebSocketHandler
from handler.baseHandler import BaseHandler
from util.log_util import Log



class App(tornado.web.Application):
    def __init__(self):
        settings = {
            'debug': True
        }
        super(App, self).__init__(
            handlers=[
        (r"/", BaseHandler), 
        (r"/ws", StatusWebSocketHandler), 
        (r"/ws/logs", LogWebSocketHandler),
        (r"/projects", ProjectHandler),
        (r"/project", SpecificProjectHandler),
        ],
            **settings
        )

if __name__ == "__main__":
    app = App()
    app.listen(8888)
    Log.i("Tornado server started on http://localhost:8888")
    tornado.ioloop.IOLoop.current().start()
