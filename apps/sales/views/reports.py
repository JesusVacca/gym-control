from datetime import datetime, time

from django.utils.dateparse import parse_date

from django.db.models import Sum, Count, DateField
from django.db.models.functions import Cast
from django.http import HttpResponse
from django.views import View
from django.views.generic import ListView

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Spacer, SimpleDocTemplate, Table, TableStyle

from apps.sales.models import Income
from apps.management.models import AppSettings



class ReportsListView(ListView):
    template_name = 'reports/list.html'
    model = Income
    context_object_name = 'daily_incomes'

    def get_paginate_by(self, queryset):
        app_settings = AppSettings.load()
        return app_settings.elements_per_section if app_settings else 10

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['start_date'] = self.request.GET.get('start_date')
        context['end_date'] = self.request.GET.get('end_date')
        context['selected_type'] = self.request.GET.get('selected_type')
        context['selected_payment_method'] = self.request.GET.get('selected_payment_method')
        context['type_list'] = Income.IncomeCategory.choices
        context['payment_methods'] = Income.IncomeMethod.choices
        return context

    def get_queryset(self):
        return self.get_filtered_queryset()

    def get_base_queryset(self):
        queryset = Income.objects.all()
        start_date = self.request.GET.get('start_date')
        end_date = self.request.GET.get('end_date')
        selected_type = self.request.GET.get('selected_type')
        selected_payment_method = self.request.GET.get('selected_payment_method')

        if start_date and end_date:
            start = datetime.combine(parse_date(start_date), time.min)
            end = datetime.combine(parse_date(end_date), time.max)
            queryset = queryset.filter(created_at__range=[start, end])
        if selected_type:
            queryset = queryset.filter(category=selected_type)
        if selected_payment_method:
            queryset = queryset.filter(payment_method=selected_payment_method)

        return queryset

    def get_filtered_queryset(self):
        queryset = self.get_base_queryset()

        return queryset.annotate(
            day=Cast('created_at', output_field=DateField()),
        ).values('day').annotate(
            total=Sum('amount'),
            count=Count('id')
        ).order_by('-day')


class ReportsGeneratePDFView(ReportsListView, View):

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_filtered_queryset())
        base_qs = self.get_base_queryset()

        category_summary = (
            base_qs
            .values('category')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        payment_method_summary = (
            base_qs
            .values('payment_method')
            .annotate(total=Sum('amount'))
            .order_by('-total')
        )

        category_dict = dict(Income.IncomeCategory.choices)
        payment_method_dict = dict(Income.IncomeMethod.choices)

        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'inline; filename="reporte.pdf"'

        doc = SimpleDocTemplate(response)
        styles = getSampleStyleSheet()
        elements = []

        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')

        elements.extend([
            Paragraph("Reporte de Ingresos", styles['Title']),
            Spacer(1, 10),
            Paragraph(f"Desde: {start_date or '-'}", styles['Normal']),
            Paragraph(f"Hasta: {end_date or '-'}", styles['Normal']),
            Spacer(1, 10),
        ])

        table_data = [['Fecha', 'Ventas', 'Total']] + [
            [str(item['day']), item['count'], f"${int(item['total'] or 0):,}"]
            for item in queryset
        ]

        table = Table(table_data, colWidths=[6 * cm, 4 * cm, 3 * cm])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))

        category_data = [['Categoría', 'Total']] + [
            [
                category_dict.get(item['category'], item['category']),
                f"${int(item['total'] or 0):,}"
            ]
            for item in category_summary
        ]
        category_table = Table(category_data, colWidths=[8 * cm, 5 * cm])
        category_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))

        payment_data = [['Método de pago', 'Total']] + [
            [
                str(payment_method_dict.get(item['payment_method'], item['payment_method'])).upper(),
                f"${int(item['total'] or 0):,}"
            ]
            for item in payment_method_summary
        ]
        payment_table = Table(payment_data, colWidths=[8 * cm, 5 * cm])
        payment_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.black),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
            ('ALIGN', (1, 1), (-1, -1), 'RIGHT'),
        ]))

        elements.extend([
            table,
            category_table,
            payment_table
        ])

        doc.build(elements)
        return response