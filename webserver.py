import cgi
import sys

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine

Base = declarative_base()

class Restaurant(Base):
    __tablename__ = 'restaurant'
    name = Column(String(80), nullable = False)
    id = Column(Integer, primary_key = True)

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.create_all(engine)
Base.metadata.bind = engine
DBSession = sessionmaker(bind = engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant.name)
                for restaurant in restaurants:
                    output += "<h2>%s</h2>"  % restaurant
                    output += "<a href= '/restaurants'> Edit</a><br>"
                    output += "<a href= '/restaurants'> Delete</a>"
                output += "<br><br><a href= '/restaurants/new'> Make a New Restaurant Here</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
                return


            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                output += "<html><body>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants'><h2>Make a New Restaurant</h2><input name='restaurant' type='text'> <input type='Submit' value='Submit'> </form> "
                output += "</body> </html>"
                self.wfile.write(output)
                print output
                return

        except IOError:
            self.send_error(404, 'File NOt Found %s' % self.path)

    def do_POST(self):
        try:
            self.send_response(301)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                newRestaurant = fields.get('restaurant')
                createNewRestaurant = Restaurant(name=str(newRestaurant[0]))
                session.add(createNewRestaurant)
                session.commit
                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant.name)
                for restaurant in restaurants:
                    output += "<h2>%s</h2>"  % restaurant
                    output += "<a href= '/restaurants'> Edit</a><br>"
                    output += "<a href= '/restaurants'> Delete</a>"
                output += "<br><br><a href= '/restaurants/new'> Make a New Restaurant Here</a>"
                output += "</body></html>"
                self.wfile.write(output)
                print output
        except :
            pass



def main():
    try:
        port = 8080
        server = HTTPServer(('',port), webServerHandler)
        print "Web server running on port %s" % port
        server.serve_forever()

    except KeyboardInterrupt:
        print "^C entered, stopping webserver..."
        server.sockey.close()


if __name__ == '__main__':
    main()