# -*- coding:utf-8 -*-

from django.contrib import admin
from .models import InRecord, OutRecord, Warehouse

from .services import set_salary


class OutRecordAdmin(admin.ModelAdmin):
    fields = ['number', 'product', 'create_date']
    list_display = ['product', 'number', 'create_date', 'updated_datetime']
    search_fields = ['product', 'number']
    list_filter = ['product', 'create_date', 'updated_datetime']

    def save_models(self):
        obj = self.new_obj
        if obj.number == 0:
            # 抛出异常
            pass

        if obj.status_number == 0:
            # 新建 出库记录
            ware = Warehouse.objects.get(product=obj.product)
            if ware is not None or ware.number < obj.number:
                # 抛出异常 库存不足
                # return '库存不足'
                pass
            obj.status_number = obj.number
            obj.save()
            ware.number -= obj.number
            ware.save(update_fields=['number'])
        else:
            # 更新出库记录
            ware = Warehouse.objects.get(product=obj.product)
            if ware.number < obj.number:
                # 抛出异常 库存不足
                # return '库存不足'
                pass
            ware.number += obj.status_number
            ware.number -= obj.number
            obj.status_number = obj.number
            ware.save(update_fields=['number'])
            obj.save(update_fields=['status_number', 'number'])


class InRecordAdmin(admin.ModelAdmin):
    fields = ['number', 'employee', 'product', 'create_date', 'updated_datetime']
    list_display = ['employee', 'product', 'number', 'create_date', 'updated_datetime']
    search_fields = ['employee', 'product', 'number']
    list_filter = ['employee', 'product', 'create_date', 'updated_datetime']
    readonly_fields = ['create_date', 'updated_datetime']

    def save_models(self):
        obj = self.new_obj

        if obj.number == 0:
            # 抛出异常
            pass

        if obj.status_number == 0:
            # 创建 入库 记录的操作
            # 更新记录
            obj.status_number = obj.number
            obj.save()
            # 更新库存
            ware = Warehouse.objects.filter(product=obj.product).first()
            if ware:
                ware.number += obj.number
            else:
                ware = Warehouse.objects.create(product=obj.product, number=obj.number)
            ware.save()

            # 更新工资记录
            set_salary(obj)

        else:
            # 更新 入库记录
            # 更新库存状态
            ware = Warehouse.objects.get(product=obj.product)
            ware.number -= obj.status_number
            ware.number += obj.number
            ware.save(update_fields=['number'])
            # 更新记录状态
            obj.status_number = obj.number
            obj.save(update_fields=['status_number', 'number'])
            # 更新工资记录
            set_salary(obj)


class WarehouseAdmin(admin.ModelAdmin):
    list_display = ['product', 'number', 'updated_time']
    search_fields = ['product', 'number']
    list_filter = ['product', 'number', 'updated_time']
    readonly_fields = list_display


admin.site.register(OutRecord, OutRecordAdmin)
admin.site.register(InRecord, InRecordAdmin)
admin.site.register(Warehouse, WarehouseAdmin)
