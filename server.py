#-*- coding:utf-8 -*-
from http.server import BaseHTTPRequestHandler,HTTPServer
import sys,os

class ServerException(Exception):
        pass
class RequestHandler(BaseHTTPRequestHandler):
    Error_Page = """\
        <html>
        <body>
        <h1>Error accessing {path}</h1>
        <p>{msg}</p>
        </body>
        </html>
        """
    def do_GET(self):
        try:
            full_path = os.getcwd() + self.path
            if not os.path.exists(full_path):
                raise ServerException("'{0}' not found".format(self.path))
            elif os.path.isfile(full_path):
                self.handle_file(full_path)
            else:
                raise ServerException("Unknown object '{0}'".format(self.path))
        except Exception as msg:
            self.handle_error(msg)
    def handle_error(self, msg):
        content = self.Error_Page.format(path=self.path, msg=msg)
        self.send_content(content, 404)
    def send_content(self, content, status=200):
        self.send_response(status)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)
    def handle_file(self,full_path):
        try:
            with open(full_path,'rb') as reader:
                content = reader.read()
                print(content)
            self.send_content(content)
        except IOError as msg:
            msg = "'{0}' cannot be read:{1}".format(self.path,msg)
            self.handle_error(msg)


    #HTTPRequestHandler class
# class testHTTPServer_RequestHandler(BaseHTTPRequestHandler):
#
#     Page = '''\
# <html>
# <body>
# <table>
# <tr>  <td>Header</td>         <td>Value</td>          </tr>
# <tr>  <td>Date and time</td>  <td>{date_time}</td>    </tr>
# <tr>  <td>Client host</td>    <td>{client_host}</td>  </tr>
# <tr>  <td>Client port</td>    <td>{client_port}</td> </tr>
# <tr>  <td>Command</td>        <td>{command}</td>      </tr>
# <tr>  <td>Path</td>           <td>{path}</td>         </tr>
# </table>
# </body>
# </html>
# '''
#     #GET
#     def do_GET(self):
#         page = self.create_page()
#         self.send_content(page)
#         #Send response status code
#         # self.send_response(200)
#     def create_page(self):
#         values = {
#             'date_time':self.date_time_string(),
#             'client_host':self.client_address[0],
#             'client_port':self.client_address[1],
#             'command':self.command,
#             'path':self.path
#         }
#         page = self.Page.format(**values)
#         return page
#     def send_content(self,page):
#         self.send_response(200)
#         self.send_header("Content-type","text/html")
#         self.send_header("Content-Length",str(len(page)))
#         self.end_headers()
#         self.wfile.write(bytes(page,"utf8"))
#         # #Send headers
#         # self.send_header('Content-type','text/html')
#         # self.end_headers()
#         #
#         # #Send message back to client
#         # message = "Hello human!"
#         # #Write content as utf8 data
#         # self.wfile.write(bytes(message,"utf8"))

def run():
    print('starting server...')
    #Server settings
    server_address = ('127.0.0.1',8888)
    httpd = HTTPServer(server_address,RequestHandler)
    print('runing server...')
    httpd.serve_forever()

    
run()