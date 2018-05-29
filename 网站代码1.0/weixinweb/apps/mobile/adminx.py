# coding:utf8

import xadmin
from xadmin import views
from openpyxl import load_workbook

from models import MobileInfo, OperationLog
import logging
import uuid

logger = logging.getLogger('django')

class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


class GlobalSetting(object):
    site_title = '后台管理系统'
    site_footer = '后台管理'
    menu_style = 'accordion'


class MobileInfoAdmin(object):
    list_display = ['id', 'mobile_type', 'type', 'number', 'color', 'sn', 'current_user', 'last_user', 'mobile_state', 'update_time']
    search_fields = ['current_user', 'last_user', 'type', 'number', 'color',  'sn', 'mobile_type', 'mobile_state', 'update_time']
    list_filter = ['type', 'number', 'color']
    import_excel = True

    def post(self, request, *args, **kwargs):
        try:
            filename = request.FILES['excel']
            wb = load_workbook(filename)
            # sheets = wb.get_sheet_names()
            # # print sheets
            # for i in sheets:
            #     if i == u'出入库登记':
            #         print i
            #     else:
            #         pass
            ws = wb.get_sheet_by_name(u'出入库登记')
            # 获得每一行数据
            rows = ws.rows
            # 将每一行数据放到列表中，并且排除表头
            i = 0
            for row in rows:
                if i:
                    line = [col.value for col in row]
                    if line[2] and line[3] and line[4] and line[5] and line[6]:
                        MobileInfo.objects.get_or_create(type=line[2], mobile_type=line[3], number=line[4], color=line[5], sn=line[6])
                        logger.info('{},{},{},{},{}'.format(line[2], line[3], line[4], line[5], line[6]))
                    elif not line[6]:
                        MobileInfo.objects.get_or_create(type=line[2], mobile_type=line[3], number=line[4], color=line[5], sn=uuid.uuid4())
                        logger.info('{},{},{},{},{}'.format(line[2], line[3], line[4], line[5], line[6]))
                    else:
                        pass
                else:
                    i = 1
            MobileInfo.save()
        except:
            pass
        return super(MobileInfoAdmin, self).post(request, args, kwargs)


class OperationLogAdmin(object):
    list_display = ['user', 'operation', 'entity', 'operation_date']
    search_fields = ['user', 'operation', 'entity', 'operation_date']
    list_filter = ['user', 'operation', 'entity', 'operation_date']


xadmin.site.register(MobileInfo, MobileInfoAdmin)
xadmin.site.register(OperationLog, OperationLogAdmin)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(views.CommAdminView, GlobalSetting)