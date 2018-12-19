# -*- coding: utf-8 -*-
import web
class merryme:
    def GET(self):
        web.header('Content-Type', 'text/html;charset=UTF-8')
        render = web.template.render("templates", base ="index")
        return render.index("霄霄")