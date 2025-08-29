from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.apps import apps
from .models import CashFlow, Status, Type, Category, SubCategory
from .forms import CashFlowForm


#----------------------- Представления для главной страницы и редактирования записей ----------------------#

class CashFlowListView(ListView):
    model = CashFlow
    template_name = 'cashflow/cashflow_list.html'
    context_object_name = 'cashflows'
    paginate_by = 15

    def get_queryset(self):
        qs = CashFlow.objects.all()

        # --- фильтрация ---
        date_from = self.request.GET.get("date_from")
        date_to = self.request.GET.get("date_to")
        status = self.request.GET.get("status")
        type_id = self.request.GET.get("type")
        category_id = self.request.GET.get("category")
        subcategory_id = self.request.GET.get("subcategory")

        if date_from:
            qs = qs.filter(created_at__date__gte=date_from)
        if date_to:
            qs = qs.filter(created_at__date__lte=date_to)
        if status:
            qs = qs.filter(status_id=status)
        if type_id:
            qs = qs.filter(type_id=type_id)
        if category_id:
            qs = qs.filter(category_id=category_id)
        if subcategory_id:
            qs = qs.filter(subcategory_id=subcategory_id)

        return qs.order_by("-created_at")

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Status.objects.all()
        ctx["types"] = Type.objects.all()
        ctx["categories"] = Category.objects.all()
        ctx["subcategories"] = SubCategory.objects.all()
        return ctx



class CashFlowCreateView(CreateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')


class CashFlowUpdateView(UpdateView):
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')


class CashFlowDeleteView(DeleteView):
    model = CashFlow
    template_name = 'cashflow/cashflow_confirm_delete.html'
    success_url = reverse_lazy('cashflow_list')


#------------------------------- Представления для управления справочниками -------------------------------#


class DictionariesUnifiedView(View):
    template_name = "cashflow/dictionaries_unified.html"

    def get(self, request):
        return render(request, self.template_name, {
            "statuses": Status.objects.all(),
            "types": Type.objects.all(),
            "categories": Category.objects.all(),
            "subcategories": SubCategory.objects.all(),
        })

    def post(self, request):
        # === СТАТУСЫ ===
        if "add_status" in request.POST:
            Status.objects.create(name=request.POST.get("name"))
        elif "edit_status" in request.POST:
            obj = get_object_or_404(Status, id=request.POST.get("id"))
            obj.name = request.POST.get("name")
            obj.save()
        elif "delete_status" in request.POST:
            get_object_or_404(Status, id=request.POST.get("id")).delete()

        # === ТИПЫ ===
        elif "add_type" in request.POST:
            Type.objects.create(name=request.POST.get("name"))
        elif "edit_type" in request.POST:
            obj = get_object_or_404(Type, id=request.POST.get("id"))
            obj.name = request.POST.get("name")
            obj.save()
        elif "delete_type" in request.POST:
            get_object_or_404(Type, id=request.POST.get("id")).delete()

        # === КАТЕГОРИИ ===
        elif "add_category" in request.POST:
            Category.objects.create(
                name=request.POST.get("name"),
                type_id=request.POST.get("type_id")
            )
        elif "edit_category" in request.POST:
            obj = get_object_or_404(Category, id=request.POST.get("id"))
            obj.name = request.POST.get("name")
            obj.type_id = request.POST.get("type_id")
            obj.save()
        elif "delete_category" in request.POST:
            get_object_or_404(Category, id=request.POST.get("id")).delete()

        # === ПОДКАТЕГОРИИ ===
        elif "add_subcategory" in request.POST:
            SubCategory.objects.create(
                name=request.POST.get("name"),
                category_id=request.POST.get("category_id")
            )
        elif "edit_subcategory" in request.POST:
            obj = get_object_or_404(SubCategory, id=request.POST.get("id"))
            obj.name = request.POST.get("name")
            obj.category_id = request.POST.get("category_id")
            obj.save()
        elif "delete_subcategory" in request.POST:
            get_object_or_404(SubCategory, id=request.POST.get("id")).delete()

        return redirect("dictionaries_unified")