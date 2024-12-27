import importlib
import re
import ast

DM_INFO = re.compile(r'^(?P<module>.+)\.(?P<class>.+)$')

class ToobukError(Exception) :
    def __init__(self, msg):
        super().__init__(msg)

from enum import Enum
class JsonConf(Enum) :
    BS_TYPE = 'html.parser'
    BS_ENCODING = 'UTF-8'

    def get(self, json, key) :
        return json.get(key) or self.value

def getdinfo(text) :
    info = DM_INFO.search(text)

    if info is None :
        raise ToobukError('not exist module' + text)

    module = info.group("module")
    cls = info.group("class")

    return module, cls

def getPlugin(text) :
    module, cls = getdinfo(text)

    mod = importlib.import_module(module)
    return getattr(mod, cls)

def runPlugin(text, *args) :
    f = getPlugin(text)
    return f(*args)

def regConverter(regx, replace) :
    reg = re.compile(regx)

    def converter (text, r) :
        # print("regx--->" + regx)
        # print("replace--->" + replace)
        # print('text--->' + text)
        return reg.sub(replace, text)

    return converter

def jsonToObj(jsonStr) :
    return ast.literal_eval(jsonStr)

def isSpace(text, r) :
    return text.isspace()
