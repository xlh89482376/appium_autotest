import hashlib
from itertools import islice

f = open("/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/emulator-5554/crash/crash_com.zhidao.testapplication_1.txt", "rb")

# f1 = f.read().decode('utf-8')
#
# print(f1)
#
# print(f1)
# print(f1)

# f1.encode(encoding='utf-8')

# print(f1)

# print(f.read())

# def getCrashHash(f):
#     # hash = []
#     # hash = hashlib.md5()
#     # Crash log首行pid不同，去掉首行进行比对
#     # for line in islice(f, 10, None):
#     lines = f.readlines()
#     for line in lines:
#         print(line.decode('utf-8'))
#         # hash.append(line)
#         # b = line.encode(encoding='utf-8')
#         # hash.update(line)
#     # print(hash)
#
# getCrashHash(f)
#
# # print(f.read().decode('utf-8'))
# # print(f.read().decode('utf-8'))
# f.seek(0)
# print(f.read().decode('utf-8'))
#
# f.close()

# def samefile():
#     with open('/Users/xuanlonghua/Documents/ZD/Projects/appium_autotest/monkey/logs/emulator-5554/crash/crash_com.zhidao.testapplication_1.txt')\

# def samefile(f1, f2):
#     if ((for line in islice(f1, 1, None) == (for line in islice(f2, 1, None))):

# print(type(f.read().decode('utf-8')))

def convertReportFile(f):
    lines = f.readlines()
    str = ''
    for line in lines:
        line_new =line.decode('utf-8')+ r'<br>'
        str += line_new
    return str

convertReportFile(f)