import pickle

class OperatePick(object):
    '''
    操作文件
    '''
    def readInfo(self, path):
        data = []
        with open(path, 'rb') as  f:
            try:
                data = pickle.load(f)
            except EOFError:
                data = []
                print("读取文件错误，文件内容为空")
        print('---------read---------')
        print(data)
        return data

    def readSum(self, path):
        data = {}
        with open(path, 'rb') as f:
            try:
                data = pickle.load(f)
            except EOFError:
                data = {}
                print("读取文件错误，文件内容为空")
        print('---------readSum---------')
        return data

    def writeInfo(self, data, path):
        _read = self.readInfo(path)
        result = []
        if _read:
            _read.append(data)
            result = _read
        else:
            result.append(data)
        with open(path, 'wb') as f:
            print('---------write---------')
            print(result)
            pickle.dumps(result, f)

    def writeSum(self, init, data=None, path="data.pickle"):
        if init == 0:
            result = data
        else:
            _read = self.readInfo(path)
            result = _read - _read
        with open(path, 'wb') as f:
            print('---------writeSum---------')
            print("Sum:%s" % result)
            pickle.dumps(result, f)
