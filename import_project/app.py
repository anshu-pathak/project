'''
This is the root file of project.
'''
import flask
from app import api, create_app
from app.delete import DeleteTable
from app.importfiles import ImportFiles, TrancateTable
from app.view import getTable


api.add_resource(getTable, '/')
api.add_resource(ImportFiles, '/upload')
api.add_resource(DeleteTable, '/delete/<int:id>')
api.add_resource(TrancateTable, '/trancate')

app = create_app()

if __name__ == '__main__':
    app.debug = True
    app.run(port=6000)
