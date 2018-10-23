# coding:utf8
'''
导入excel处理
'''

import xadmin
from django.template import loader
from django.http import HttpResponseRedirect

from xadmin.sites import site
from xadmin.views import BaseAdminPlugin, ListAdminView


class ImportExcel(BaseAdminPlugin):
    import_excel = False

    def init_request(self, *args, **kwargs):
        return bool(self.import_excel)

    def block_top_toolbar(self, context, nodes):
        nodes.append(loader.render_to_string('xadmin/excel/top_toolbar.importexcel.html', context_instance=context))

xadmin.site.register_plugin(ImportExcel, ListAdminView)