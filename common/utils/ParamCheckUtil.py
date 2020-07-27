import yaml,os
from common.utils.FilePathUtil import FilePathUtil
from xml.dom.minidom import parse

class ParamCheckUtil():
    def __init__(self):
        self.xml_path = FilePathUtil().get_xml_path()
        self.yml_path = FilePathUtil().get_yml_path()

    def load_yml_data(self, file_name):
        """
        读取yaml文件
        """
        file_path = self.yml_path + file_name
        with open(file_path,"r") as f:
            return yaml.load(f,Loader=yaml.FullLoader)

    def write_yaml_data(self, file_name, data):
        """
        写入yaml文件
        """
        file_path = self.yml_path + file_name
        with open(file_path, "w", encoding='utf-8') as f:
            yaml.dump(data, f, allow_unicode=True)

    def load_xml_data(self, file_name):
        dict = {}
        path = self.xml_path + file_name
        doc = parse(path)
        for node in doc.getElementsByTagName("node"):
            id = node.getAttribute("resource-id")
            text = node.getAttribute("text")
            bounds = node.getAttribute("bounds")
            bound = bounds.strip('[').strip(']').replace('[','').replace(']',',')
            x1 = int(bound.split(',')[0])
            y1 = int(bound.split(',')[1])
            x2 = int(bound.split(',')[2])
            y2 = int(bound.split(',')[3])
            x = int((x2 - x1)/2 + x1)
            y = int((y2 - y1)/2 + y1)
            xy = str([x, y])
            dict[xy] = {"id":id,"text":text}

        return dict


if __name__ == '__main__':
    name = 'com.mogo.launcher.xml'
    p = ParamCheckUtil()
    print(p.load_xml_data(name))


