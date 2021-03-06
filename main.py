import web
import os
from weixinInterface import WeixinInterface
from merryme import merryme

urls = (
    '/weixin', 'WeixinInterface',
    '/lingjiang', 'merryme',
)

if __name__ == '__main__':
    app_root = os.path.dirname(__file__)
    templates_root = os.path.join(app_root, 'templates')
    render = web.template.render(templates_root)
    app = web.application(urls, globals())
    app.run()