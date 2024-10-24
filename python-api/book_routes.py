from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config

@view_config( route_name='new')
def add(request):
   return Response('add book')
@view_config(route_name='show')
def list(request):
   return Response('Book list')
def books(config):
   config.add_route('show', '/list')
   config.add_route('new', '/add')
   config.scan()