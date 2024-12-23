from django.contrib import admin
from .models import Client, Phone
from django.urls import path
from django_excel_response import ExcelResponse
from django.utils.translation import gettext_lazy as _

# Configura el encabezado, título y descripción del admin
admin.site.site_header = "ClientTrol"  # Título en la parte superior
admin.site.site_title = "Panel de Control de Clientes"  # Título de la pestaña del navegador
admin.site.index_title = "Bienvenido al Panel de Administración"  # Título de la página de inicio

class RelatedModelInline(admin.TabularInline):  # O admin.StackedInline
    model = Phone
    extra = 1

class ActiveFilter(admin.SimpleListFilter):
    title = 'Referido por'
    parameter_name = 'refer'

    def lookups(self, request, model_admin):
        subquery = Client.objects.values_list('refer', 'refer').distinct().order_by('refer')
        subquery = list(subquery)
        subquery.append(("sin_referido", 'Sin referido'))
        for x in subquery:
            if(x==None):
                x = ("sin_referido", 'Sin referido')
                break
        return subquery
    
    def queryset(self, request, queryset):
        if self.value() == 'sin_referido':
            return queryset.filter(refer__isnull=True)
        elif self.value() == None:
            return queryset
        else:
            return queryset.filter(refer=self.value())
        
@admin.register(Client)
class AuthorAdmin(admin.ModelAdmin):
    # form = ClientForm
    list_display = ['name', 'phone', 'email', 'address', 'refer', 'phones_numbers', 'created_at', 'updated_at']
    change_list_template = 'admin/exportar_cambio_lista.html'
    search_fields = ('name', 'phone', 'phones__number')  # Busca por estos campos
    #campo de refer con filtro
    inlines = [RelatedModelInline]
    list_filter = [ActiveFilter]
    actions = ['exportar_csv', 'delete_selected']  # Registra la acción

    def phones_numbers(self, obj):
        return ", ".join([phone.number for phone in obj.phones.all()])

    phones_numbers.short_description = 'Números de teléfono'

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('exportar-todo/', self.admin_site.admin_view(self.exportar_todo), name='exportar_todo'),
        ]
        return custom_urls + urls

    def exportar_csv(self, request, queryset):
        # Crea el archivo CSV
        data = [
            ['Nombre', 'Teléfono', 'Correo', 'Dirección', 'Referido por', 'Resgistrado'],
        ]
        
        # Escribe los datos
        for obj in queryset:
            data.append([obj.name, obj.phone, obj.email, obj.address, obj.refer, obj.created_at])

        return ExcelResponse(data, 'clients', font='name SimSum')


    def exportar_todo(self, request):
        data = [
            ['Nombre', 'Teléfono', 'Correo', 'Dirección', 'Referido por', 'Resgistrado'],
        ]
        for obj in Client.objects.all():
            data.append([obj.name, obj.phone, obj.email, obj.address, obj.refer, obj.created_at])

        return ExcelResponse(data, 'clients', font='name SimSum')
    
    exportar_csv.short_description = "Exportar Clientes seleccionados"

    def get_actions(self, request): 
        actions = super().get_actions(request)
        
        if 'delete_selected' in actions: 
            transcrip = list(actions['delete_selected'])
            transcrip[2] = 'Eliminar %(verbose_name_plural)s seleccionados'
            actions['delete_selected'] = tuple(transcrip)

        return actions

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }