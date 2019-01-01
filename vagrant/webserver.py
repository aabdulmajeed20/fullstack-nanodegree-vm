from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import cgi

from database_setup import Base, Restaurant, MenuItem
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverhandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if(self.path.endswith("/restaurants")):
                restaurants = session.query(Restaurant).all()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<a href='restaurants/new'><h1>Create New restaurant</h1></a>"
                for restaurant in restaurants:
                    output += restaurant.name
                    output += "</br>"
                    output += "<a href='/restaurants/%s/edit'>Edit</a>" % restaurant.id
                    output += "</br>"
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "</br>"
                    output += "</br>"
                    output += "</br>"
                output += "</body></html>"
                self.wfile.write(output)
                return

            if(self.path.endswith("/restaurants/new")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1>Make new Restaurant</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/restaurants/new'><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if(self.path.endswith("/edit")):
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()
                if(restaurantQuery != []):
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1>%s</h1>" % restaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/edit' >" % restaurantId
                    output += "<input name='newRestaurant' type='text' placeholder='%s' >" % restaurantQuery.name
                    output += "<input type='submit' value='Rename'>"
                    output += "</form>"
                    output += "</body></html>"

                    self.wfile.write(output)
                    return

            if(self.path.endswith("/delete")):
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()
                if(restaurantQuery != []):
                    self.send_response(200)
                    self.send_header('content-type', 'text/html')
                    self.end_headers()
                    output = "<html><body>"
                    output += "<h1> Are you sure to delete %s restaurant?</h1>" % restaurantQuery.name
                    output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantId
                    output += "<input type='submit' value='delete' >"
                    output += "</form></body></html>"

                    self.wfile.write(output)
                    return
            if(self.path.endswith("/hello")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            
                output = ""
                output += "<html><body>"
                output += "<h1>Hello MAjeedd</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return

            if(self.path.endswith("/majeed")):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
            
                output = ""
                output += "<html><body>"
                output += "<h1>Majeed You are FANTASTIC!!!</h1>"
                output += '''<form method='POST' enctype='multipart/form-data' action='/hello'><h2>What would you like me to say?</h2><input name="message" type="text" ><input type="submit" value="Submit"> </form>'''
                output += "</body></html>"
                self.wfile.write(output)
                print(output)
                return
            
            

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)
    def do_POST(self):
        try:
            if(self.path.endswith("/edit")):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurant')
                restaurantId = self.path.split("/")[2]

                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()
                if(restaurantQuery != []):
                    restaurantQuery.name = messagecontent[0]
                    session.add(restaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

            if(self.path.endswith("/delete")):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                restaurantId = self.path.split("/")[2]
                restaurantQuery = session.query(Restaurant).filter_by(id = restaurantId).one()
                if(restaurantQuery != []):
                    session.delete(restaurantQuery)
                    session.commit()

                    self.send_response(301)
                    self.send_header('content-type', 'text/html')
                    self.send_header('Location', '/restaurants')
                    self.end_headers()
                    return

            if(self.path.endswith("/restaurants/new")):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('message')

                newRestaurant = Restaurant(name = messagecontent[0])
                session.add(newRestaurant)
                session.commit()

                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                return
        except:
            pass

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webserverhandler)
        print("web server running on port %s" % port)
        server.serve_forever()

    except KeyboardInterrupt:
        print("^C entered, Server stopped...")
        server.socket.close()

if __name__ == '__main__':
    main()