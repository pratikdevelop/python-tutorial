""" from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config
from book_routes import books
from student_routes import students
from db_config import get_db
from views/ import

# @view_config(route_name='hello', request_method='GET')
# def hello_world(request):
#    return Response('Hello World!')

@view_config(route_name='hello', renderer='templates/index.html')
def hello_world(request):
   return {'name':'Pyramid!'}

@view_config(route_name='about', request_method='GET')
def about_uus(request):
   return Response('about us')

@view_config(route_name='contact', request_method='GET')
def about_uus(request):
   print(request.matchdict)
   return Response('contact us')

def notfound(request):
   return Response('Not Found', status='404 Not Found')
   

if __name__ == '__main__':
   with Configurator() as config:
      config.add_static_view(name='static', path='static')
      config.add_route('hello', '/')
      config.add_route('about', '/about')
      config.add_route('contact', '/contact/{name}')
      config.include(students, route_prefix='/student')
      config.include(books, route_prefix='/book')
      config.include(aut)
      config.add_notfound_view(notfound)
      
      config.include('pyramid_jinja2')
      config.add_jinja2_renderer(".html")
      my_session_factory = SignedCookieSessionFactory('abcQWE123!@#')
      config.set_session_factory(my_session_factory)
      config.scan()
      # config.add_view(hello_world, route_name='hello')
      # config.add_view(about_uus, route_name='about')
      config.registry.db = get_db()
      app = config.make_wsgi_app()
      app.debug_notfound = True
   server = make_server('0.0.0.0', 6543, app)
   server.serve_forever()
   server.allow_reuse_address = False"""

from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.session import SignedCookieSessionFactory
from pyramid.view import view_config
from db_config import get_db
from views.user_view import auth 
import subprocess
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f'Reloading server due to change in {event.src_path}')
            restart_server()

def restart_server():
    if hasattr(restart_server, "server_process"):
        restart_server.server_process.terminate()
    restart_server.server_process = subprocess.Popen(['pserve', 'development.ini'])

@view_config(route_name='hello', renderer='templates/index.html')
def hello_world(request):
    return {'name': 'Pyramid!'}

def notfound(request):
    return Response('Not Found', status='404 Not Found')

if __name__ == '__main__':
    # Start the initial server
    # restart_server()

    # Set up the watchdog observer
    observer = Observer()
    observer.schedule(ChangeHandler(), path='.', recursive=True)  # Monitor current directory
    observer.start()

    try:
        with Configurator() as config:
            config.add_static_view(name='static', path='static')
            config.add_route('hello', '/')
            config.include(auth)  # Include your auth routes
            config.add_notfound_view(notfound)
            config.include('pyramid_jinja2')
            config.add_jinja2_renderer(".html")
            my_session_factory = SignedCookieSessionFactory('abcQWE123!@#')
            config.set_session_factory(my_session_factory)
            config.registry.db = get_db()  # Set up the database connection
            
            config.scan()  # Scan for views
            
            app = config.make_wsgi_app()
            app.debug_notfound = True

        while True:
            time.sleep(1)  # Keep the main thread alive
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
