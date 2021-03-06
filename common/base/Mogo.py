

class Mogo(object):
    """
    mogo相关 都放这里 保证单一功能的可复用性
    """

    def __init__(self, sn):
        self.sn = sn
        self.product = ''

    def set_product(self):
        print(self.sn)
        if self.starts_with(self.sn, "XTCBA"):
            self.product = 'C80'
        elif self.starts_with(self.sn, "ZD821", "ZD822", "D801A", "D802A"):
            self.product = 'D82'
        elif self.starts_with(self.sn, "ZD801", "ZD802", "D801C", "D802C"):
            self.product = 'D80'
        elif self.starts_with(self.sn, "ZD811", "ZD812", "D801B", "D802B"):
            self.product = 'D81'
        elif self.starts_with(self.sn, "ZD841", "ZD842", "D841C", "D842C"):
            self.product = 'D84'
        elif self.starts_with(self.sn, "E841A", "E842A", "D801L", "D802L"):
            self.product = '9832(1+16)'
        elif self.starts_with(self.sn, "E841D", "E842D"):
            self.product = '9832(2+16)'
        elif self.starts_with(self.sn, "E841C", "E842C", "D801K", "D802K"):
            self.product = '9832(2+32)'
        elif self.starts_with(self.sn, "E851J", "E852J", "E841J", "E842J"):
            self.product = 'E85'
        elif self.starts_with(self.sn, "F803B", "F803E"):
            self.product = 'F80'
            print('F80')
        elif self.starts_with(self.sn, "H600C"):
            self.product = 'H600CD'
        else:
            print("sn匹配错误")
            self.product = '未知'
            return self.product
        return self.product

    @staticmethod
    def starts_with(sn, *args):
        flag = False
        for item in args:
            if sn.startswith(item):
                flag = True
                break
        return flag

if __name__ == '__main__':
    mogo = Mogo('H600CD000000000')

    mogo.set_product()