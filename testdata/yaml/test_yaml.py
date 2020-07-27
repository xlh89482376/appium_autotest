from common.utils.ParamCheckUtil import ParamCheckUtil
from common.utils.FilePathUtil import FilePathUtil

class testyaml():

    def __init__(self):
        self.filepath = FilePathUtil().get_yaml_path()
        self.yamlcheck = ParamCheckUtil().load_yaml_data(self.filepath)



if __name__ == '__main__':
    t = testyaml()
    aqy_yaml_path = t.filepath + "aqy_login.yml"
    print(t.yamlcheck)



