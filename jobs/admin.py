import csv, codecs

from django.contrib import admin
from django.http import HttpResponse

from django import forms

from datetime import datetime

from jobs.models import Job, JobTypes
from datetime import datetime, timedelta
from .tasks import send_dingtalk_message


exportable_fields = (
    'job_type', 'job_name', 'job_responsibility', 'job_requirement', 'created_date')

# define export action
def export_model_as_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response.write(codecs.BOM_UTF8)
    field_list = exportable_fields
    response['Content-Disposition'] = 'attachment; filename=%s-list-%s.csv' % (
        'recruitment-jobs',
        datetime.now().strftime('%Y-%m-%d-%H-%M-%S'),
    )

    # 写入表头
    writer = csv.writer(response)
    writer.writerow([queryset.model._meta.get_field(f).verbose_name.title() for f in field_list],)

    for obj in queryset:
        ## 单行 的记录（各个字段的值）， 根据字段对象，从当前实例 (obj) 中获取字段值
        csv_line_values = []
        for field in field_list:
            field_object = queryset.model._meta.get_field(field)
            field_value = field_object.value_from_object(obj)
            if field == 'job_type':
                field_value = JobTypes[field_value][1]
            csv_line_values.append(field_value)
        writer.writerow(csv_line_values)
    # 钉钉异步通知又内容被到导出
    send_dingtalk_message.delay("有文件被导出，导出时间： %s， 导出者： %s" % (datetime.now(), request.user))

    return response


export_model_as_csv.short_description = u'导出为CSV文件'

# export_model_as_csv.allowed_permissions = ('export',)


class JobAdmin(admin.ModelAdmin):

    actions = (export_model_as_csv,)

    exclude = ('creator','created_date','modified_date')
    list_display = ('job_name', 'job_type', 'job_city', 'creator', 'created_date', 'modified_date', 'get_refreshment')

    # 右侧筛选条件
    list_filter = ('job_city',)

    # 查询字段
    search_fields = ('job_name', 'job_city', 'creator')

    ### 列表页排序字段
    ordering = (
        '-created_date',
        'job_city',
        'creator',
    )

    def get_refreshment(self, obj):
        if str(datetime.now() - timedelta(days = 1)) < str(obj.created_date):
            return "T"
        return "F"

    get_refreshment.short_description = '新颖度< 1day'
    get_refreshment.allow_tags = True

    def save_model(self, request, obj, form, change):
        if obj.creator is None:
            obj.creator = request.user
        super().save_model(request, obj, form, change)




# Register your models here.
admin.site.register(Job, JobAdmin)
