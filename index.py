import logging
import logging.config
import configparser
from flask import Flask, jsonify, request
from filemanager import FileManager, PathSchema, IdSchema
from webargs import fields
from webargs.flaskparser import use_args


app = Flask(__name__)


@app.route('/createmap', methods=['POST'])
def create_map():
    """
    create_map function, listen to POST request and 
    create map on request json data
    example cmd:
        curl -v -X POST -H "Content-Type: application/json" 
        -d "{\"id\": \"my-map\"}" http://127.0.0.1:8081/createma
    Input json data
        {"id": "my-map"}
    """
    msg, code = FileManager.CreateMap(request.get_json())
    return msg, code


@app.route('/addleaf', methods=['POST'])
@use_args(IdSchema(), location="query")
def add_leaf(args):
    """
    add_leaf fucntion, listen to POST request on agrs id and
    create a file from json data
    example cmd:
        curl -X POST -H "Content-Type: application/json" 
        -d "{\"path\": \"i\/like\/potatoes\",\"text\": \"Because I like it\"}" 
        http://localhost:0881/addleaf?id=my-map
    Input json data:
       {
            "path": "i/like/potatoes",
            "text": "Because I like it"
        } 
    """
    msg, code = FileManager.AddLeaf(args, request.get_json())
    return msg, code


@app.route('/readleaf', methods=['GET'])
@use_args(PathSchema(), location="query")
def read_leaf(args):
    """
    read_leaf function, listen on GET request,
    return the collect data from file on path parameter
    example cmd: 
        curl -X GET -H "Content-Type: application/json" 
        http://localhost:8081/readleaf?id=my-map&path=i/like/potatoes
    output json data:
       {
            "path": "i/like/potatoes",
            "text": "Because I like it"
        } 

    """
    msg, code = FileManager.GetLeaf(args)
    return jsonify(msg), code


@app.route('/readmap', methods=['GET'])
@use_args(IdSchema(), location="query")
def read_map(args):
    """
    read_map function, listen on GET request,
    return the root tree base on map id
    example cmd: 
        curl -X GET -H "Content-Type: application/json" 
        http://localhost:8081/readmap?id=my-map
    output string data:
        root/
            i/
                like/
                    potatoes
                eat/
                    tomatoes
    """
    msg, code = FileManager.GetMap(args)
    return msg, code


if __name__ == "__main__":
    """
    main index, read config file  for flsk config parameter and
    file manager main path
    """
    host = '127.0.0.1'
    port = 5000
    with open('config.ini') as fd:
        config = configparser.ConfigParser()
        config.read_file(fd)
        host = config.get('FLASK', 'host')
        port = config.getint('FLASK', 'port')
        debug = config.getboolean('FLASK', 'debug')
        FileManager.data_path = config.get('FILE_MANAGER', 'path').split('/')
        FileManager.root_dir = config.get('FILE_MANAGER', 'root_dir')

    logging.getLogger('werkzeug').setLevel(logging.ERROR)
    logging.config.fileConfig(fname='log.conf')
    FileManager.logger = logging.getLogger('file_manager')

    app.run(host=host, port=port, debug=debug)
