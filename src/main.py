from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse
import json
import logging
from setup_log import setup_log
setup_log(logging.INFO)
from device_manager import DeviceManager, ModuleManager

class Router:
    def __init__(self):
        self.routes = {}

    def add_route(self, path, method, handler):
        path = self._remove_query_params(path)
        if path not in self.routes:
            self.routes[path] = {}
        self.routes[path][method.upper()] = handler

    def get_handler(self, path, method):
        path = self._remove_query_params(path)
        method = method.upper()
        handler = self.routes.get(path, {}).get(method)
        if not handler:
            return None
        return handler

    def _remove_query_params(self, path):
        return urllib.parse.urlparse(path).path

class RequestHandler(BaseHTTPRequestHandler):
    router = None  # 初始化类变量

    def log_message(self, format, *args):
        logging.info((self.address_string(), format % args))

    def log_error(self, format, *args):
        logging.error(self.address_string(), format % args)

    def parse_http_params(self):
        parsed_url = urllib.parse.urlparse(self.path)
        query = parsed_url.query
        params = urllib.parse.parse_qs(query, keep_blank_values=True)

        if self.command == 'POST':
            content_length = int(self.headers['Content-Length'])  # 获取请求体的长度
            post_data = self.rfile.read(content_length)  # 读取请求体
            post_params = urllib.parse.parse_qs(post_data.decode('utf-8'), keep_blank_values=True)
            params.update(post_params)

        for key, value in params.items():
            if len(value) == 1:
                params[key] = value[0]
        return params

    def do_GET(self):
        handler = self.router.get_handler(self.path, 'GET')
        if handler:
            params = self.parse_http_params()
            self.send_response(200)
            self.end_headers()
            try:
                response_content = handler(params)
                response = {
                    "code": 0,
                    "description": "",
                    "data": response_content
                }
            except Exception as e:
                logging.error("exception: {}".format(e))
                device = params.get("device")
                logging.error('{} {}'.format(device, type(device)))
                if device and type(device) == str:
                    device = json.loads(device)
                DeviceManager().destroy_device(device)
                response = {
                    "code": -1,
                    "description": e.__str__(),
                    "data": None
                }
            logging.info("Response: {}".format(response))
            self.wfile.write(json.dumps(response).encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        handler = self.router.get_handler(self.path, 'POST')
        if handler:
            params = self.parse_http_params()
            self.send_response(200)
            self.end_headers()
            response_content = handler(params)
            self.wfile.write(response_content.encode('utf-8'))
        else:
            self.send_error(404, "Not Found")


def process(params):
    device = params.get("device")
    if device and type(device) == str:
        device = json.loads(device)
    method = params.get("method")
    arguments = params.get("arguments")
    if arguments and type(arguments) == str:
        arguments = json.loads(arguments)
    if type(arguments) == dict:
        data = getattr(DeviceManager().get_device(device), method)(**arguments)
    else:
        data = getattr(DeviceManager().get_device(device), method)(*arguments)
    return json.dumps(data)


def run(server_class=HTTPServer, handler_class=RequestHandler):
    router = Router()
    router.add_route('/', 'GET', process)
    router.add_route('/', 'POST', process)

    handler_class.router = router  # 将router赋值给RequestHandler类的router变量

    server_address = ('', 61721)
    httpd = server_class(server_address, handler_class)
    logging.info("Server running on port {}".format(server_address[1]))
    httpd.serve_forever()


if __name__ == '__main__':
    ModuleManager()
    DeviceManager()
    run()
