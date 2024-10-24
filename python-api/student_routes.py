import pyramid
from pyramid.config import Configurator
from pyramid.response import Response
from pyramid.view import view_config
studentslist = []

@view_config( route_name='add', renderer='templates/marklist.html')
def add(request):
   student={'id':request.params['id'], 
      'name':request.params['name'],
      'percent':int(request.params['percent'])}
   studentslist.append(student)
   return {'students':studentslist}

@view_config(route_name='list')
def list(request):
   return Response('Student list')
   
def students(config):
   config.add_route('list', '/list')
   config.add_route('add', '/add')
   config.scan()


  