from jinja2 import Template


def temp():
    template = Template("hello {{ name }}")
    template.render(name = 'world')

if __name__ == '__main__':
    temp(the="报告")