import os

class OperateFileUtil(object):
    def __init__(self, file, method='w+'):
        self.file = file
        self.method = method
        self.fileHandle = None

    def touch_file(self):
        if not os.path.isfile(self.file):
            f = open(self.file, self.method)
            f.close()
            print("创建文件成功")
        else:
            print("文件已经存在")

    def mv_file(self):
        if os.path.isfile(self.file):
            os.remove(self.file)
            print("删除文件成功")
        else:
            print("文件不存在")