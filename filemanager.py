import configparser
import logging
import logging.config
import os
import posixpath
import ntpath
from marshmallow import Schema, fields, ValidationError, validate


class IdSchema(Schema):
    """
    class IdSchema, define the Id schematic 
    """
    id = fields.Str(required=True, validate=validate.Length(min=1))


class FileSchema(Schema):
    """
    class FileSchema, define the path and text schematic
    """
    path = fields.Str(required=True, validate=validate.Length(min=1))
    text = fields.Str(required=True)


class PathSchema(Schema):
    """
    class PathSchema, define the id and path schematic
    """
    id = fields.Str(required=True, validate=validate.Length(min=1))
    path = fields.Str(required=True, validate=validate.Length(min=1))


class FileManager(object):
    """
    class FileManager, create file and/or directory, read file data
    """
    data_path = ['.', 'data']
    root_dir = 'root'
    logger = logging.getLogger(__name__)

    def __init__(self):
        pass

    def __repr__(self) -> str:
        return super().__repr__("File Management")

    @classmethod
    def CreateMap(cls, pkg):
        """
        CreateMap function, check input argument and 
        create tree diretory base on args. input
        Input:
            pkg: json Id
        Output:
            None
        """
        input = {}

        # create root directory
        try:
            # check id schema
            input = IdSchema().load(pkg)
            # check id special caracter
            _id = input.get("id")
            if(posixpath.sep in _id or ntpath.sep in _id):
                raise ValueError("Input path error")

            path = os.path.join(
                *(cls.data_path + [_id] + [cls.root_dir]))

            os.makedirs(path, exist_ok=True)
            return "", 200
        except ValueError as ex:
            # log error
            cls.logger.exception("{}".format(ex))
            return str(ex), 400
        except ValidationError as ex:
            cls.logger.exception("{}".format(ex.messages))
            return ex.messages, 422
        except Exception as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 500

    @classmethod
    def AddLeaf(cls, id, pkg):
        """
        AddLeaf function, check input argument and 
        create tree diretory and data file base on args. input
        Input:
            id: id of map
            pkg: json path string and text data
        Output:
            None
        """
        input_pkg = {}
        input_id = {}

        try:
            input_id = IdSchema().load(id)
            # check id
            _id = input_id.get('id')
            if(posixpath.sep in _id or ntpath.sep in _id):
                raise ValueError("Input Id error, Id with os separator")

            # check data schema
            input_pkg = FileSchema().load(pkg)

            # check data path
            root_path = os.path.join(
                *(cls.data_path + [_id] + [cls.root_dir]))
            _path = input_pkg.get('path')
            path, file = cls.get_path(root_path, _path)

            # create directory
            os.makedirs(path, exist_ok=True)

            # check if file exist
            full_path = os.path.join(path, file)
            if os.path.isfile(full_path):
                pass
            else:
                with open(full_path, 'w') as fd:
                    fd.write(input_pkg.get('text'))
            return "", 200
        except ValueError as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 400
        except ValidationError as ex:
            cls.logger.exception("{}".format(ex.messages))
            return ex.messages, 422
        except Exception as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 500

    @classmethod
    def GetLeaf(cls, id):
        """
        GetLeaf function, check input argument and 
        get data file base on args. input
        Input:
            id: id of map
        Output:
            Json path string and text data
        """
        input = {}
        data = ''
        output = {}

        try:
            # check schema
            input = PathSchema().load(id)

            _id = input.get('id')
            if(posixpath.sep in _id or ntpath.sep in _id):
                raise ValueError("Input Id error, Id with os separator")

            # get root path
            root_path = os.path.join(
                *(cls.data_path + [_id] + [cls.root_dir]))
            # check data path
            _path = input.get('path')

            path, file = cls.get_path(root_path, _path)
            # check if file exist
            full_path = os.path.join(path, file)
            if not os.path.isfile(full_path):
                raise ValueError("Input path error, no file at this path")
            else:
                with open(full_path, 'r') as fd:
                    data = fd.read()
            output['path'] = _path
            output['text'] = data
            return output, 200
        except ValueError as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 400
        except ValidationError as ex:
            cls.logger.exception("{}".format(ex.messages))
            return ex.messages, 422
        except Exception as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 500

    @classmethod
    def GetMap(cls, id):
        """
        GetMap function, return tree map of an id.
        Input:
            id: id of map
        Output:
            Tree map string
        """
        treemap = ""
        input_id = {}

        try:
            # check id schema
            input_id = IdSchema().load(id)

            _id = input_id.get('id')
            if(posixpath.sep in _id or ntpath.sep in _id):
                raise ValueError("Input Id error, Id with os separator")

            # check data path
            root_path = os.path.join(
                *(cls.data_path + [_id] + [cls.root_dir]))

            for root, dirs, files in os.walk(root_path):
                level = root.replace(root_path, '').count(os.sep)
                indent = ' ' * 4 * (level)
                treemap += '{}{}/\n'.format(indent, os.path.basename(root))
                subindent = ' ' * 4 * (level + 1)
                for f in files:
                    treemap += '{}{}\n'.format(subindent, f)
            return str(treemap), 200
        except ValueError as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 400
        except ValidationError as ex:
            cls.logger.exception("{}".format(ex.messages))
            return ex.messages, 422
        except Exception as ex:
            cls.logger.exception("{}".format(ex))
            return str(ex), 500

    @staticmethod
    def get_path(root_path, path):
        """
        get_root_path function,
        Input:
            root_path: root path
            path: sub path
        Output:
            path: full path to file
            file: file name
        """
        _lpath = []
        _path = ''
        _file = ''
        try:
            if posixpath.sep in path:
                _lpath = path.split(posixpath.sep)
                _path = os.path.join(root_path, *(_lpath[:-1]))
                _file = _lpath[-1]
            elif ntpath.sep in path:
                _lpath = path.split(ntpath.sep)
                _path = os.path.join(root_path, *(_lpath[:-1]))
                _file = _lpath[-1]
            else:
                # input is file name
                _path = root_path
                _file = path
            return _path, _file
        except Exception as ex:
            raise ex
