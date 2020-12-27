import os
from pyecharts import Bar, Line, Scatter, EffectScatter, Grid, Page, Scatter3D, Overlap
from PerConfig import AppPerCon
from AppOperatePick import OperatePick

PATH = lambda p: os.path.abspath(os.path.join(os.path.dirname(os.path.realpath('__file__')), p))
pick= OperatePick()

class Report(object):
    def __init__(self, dev, reportName, flag):
        self.reportName = reportName
        self.dev = dev
        self.pack = AppPerCon.package_name
        self.flag = flag

    def createComparReport(self):
        pass

    def createReport(self, dev):
        lisMem = pick.readInfo(AppPerCon.info_path + self.dev + '_' +self.pack + '_' + self.flag + '_mem.pickle')
        lisCpu = pick.readInfo(AppPerCon.info_path + self.dev + '_' + self.pack + '_' + self.flag + '_cpu.pickle')
        lisFps = pick.readInfo(AppPerCon.info_path + self.dev + '_' +self.pack + '_' + self.flag + '_fps.pickle')
        lisDevinfo = pick.readInfo(AppPerCon.info_path + 'info.pickle')

        pix = lisDevinfo[0][dev]['header']['pix']
        net = lisDevinfo[0][dev]['header']['net']
        name = lisDevinfo[0][dev]['header']['phone_name']
        rom = lisDevinfo[0][dev]['header']['rom']

        devinfo = '设备信息-分辨率' + pix + '\\' + '网络：' + net + '\\' + '设备名' + name + '\\' +'内存容量' + str(rom)+'MB'

        v1 = [i for i in lisCpu if type(i) == str]
        v2 = [i for i in lisCpu if type(i) != str]
        v3 = [i for i in lisMem if type(i) == str]
        v4 = [i for i in lisMem if type(i) != str]
        v5 = [i for i in lisFps if type(i) == str]
        v6 = [i for i in lisFps if type(i) != str]

        page = Page(self.reportName.encode('utf-8').decode('utf-8'))

        attr = v1
        bar = Bar()
        bar.add('ROKI_bar', attr, v2)
        line = Line(self.reportName + '-' + 'CPU占用', devinfo, width=1200, height=400)
        # is_stack:
        # is_label_show:是否正常显示标签，默认不显示。标签即各点的数据项信息
        # is_smooth:
        # is_more_utils:是否提供更多的使用工具按钮。默认只提供 数据试图 和 下载 按钮
        # is_datazoom_show:是否使用区域缩放组件，默认为False
        # yaxis_formatter:y轴标签格式器，如'天'，则y轴的标签为数据加'天'
        # mark_point:list,标记点，默认有'min','max','average'可选。支持自定义标记点
        # mark_line:list,标记线，默认有'min','max','average'可选
        line.add('ROKI_line', attr, v2, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                 is_datazoom_show=False, yaxis_formatter='%', mark_point=['max', 'min'], mark_line=['average'])

        overlap = Overlap(self.reportName + '-' + 'CPU占用', width=1200, height=400)
        overlap.add(line)
        overlap.add(bar)
        page.add(overlap)

        attr1 = v3
        line1 = Line(self.reportName + '-' + 'MEM消耗', width=1200, height=400)
        line1.add('ROKI_line', attr1, v4, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                  is_datazoom_show=False, yaxis_formatter='MB', mark_point=['max', 'min'], mark_line=['average'])
        bar1 = Bar()
        bar1.add('ROKI_bar', attr1, v4)
        overlap1 = Overlap(width=1200, height=400)
        overlap1.add(line1)
        overlap1.add(bar1)
        page.add(overlap1)

        attr2 = v5
        line2 = Line(self.reportName + '-' + 'FPS帧率', width=1200, height=400)
        line2.add('ROKI_line', attr2, v6, is_stack=True, is_label_show=True, is_smooth=False, is_more_utils=True,
                  is_datazoom_show=False, yaxis_formatter='fps', mark_point=['max', 'min'], mark_line=['average'])
        bar2 = Bar()
        bar2.add('ROKI_bar', attr2, v6)
        overlap2 = Overlap(width=1200, height=400)
        overlap2.add(line2)
        overlap2.add(bar2)
        page.add(overlap2)

        page.render(AppPerCon.report_path + self.dev + '_' + self.pack + '_' + self.flag + '_' + 'report.html')

if __name__ == '__main__':
    rep = Report('xxxxxxx', 'xxxxxx', 'Medium')
    rep.createReport('xxxxxxxxx')




































