from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, TemplateView
from django.apps import apps
from .models import CashFlow, Status, Type, Category, SubCategory
from .forms import CashFlowForm
from django.contrib import messages


#----------------------- Представления для главной страницы и редактирования записей ----------------------#

class CashFlowListView(ListView):
    """
    Список записей денежных потоков с фильтрацией и пагинацией.
    """
    model = CashFlow
    template_name = 'cashflow/cashflow_list.html'
    context_object_name = 'cashflows'
    paginate_by = 15

    def get_queryset(self):
        """
        Возвращает QuerySet с применёнными фильтрами по дате, статусу, типу, категории и подкатегории.
        """
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
        """
        Добавляет справочники в контекст для фильтрации.
        """
        ctx = super().get_context_data(**kwargs)
        ctx["statuses"] = Status.objects.all()
        ctx["types"] = Type.objects.all()
        ctx["categories"] = Category.objects.all()
        ctx["subcategories"] = SubCategory.objects.all()
        return ctx


class CashFlowCreateView(CreateView):
    """
    Класс для создания новой записи движения денежных средств.
    """
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')


class CashFlowUpdateView(UpdateView):
    """
    Класс для редактирования существующей записи движения денежных средств.
    """
    model = CashFlow
    form_class = CashFlowForm
    template_name = 'cashflow/cashflow_form.html'
    success_url = reverse_lazy('cashflow_list')


class CashFlowDeleteView(DeleteView):
    """
    Класс для удаления записи движения денежных средств.
    """
    model = CashFlow
    template_name = 'cashflow/cashflow_confirm_delete.html'
    success_url = reverse_lazy('cashflow_list')


def cashflow_create(request):
    """
    Функция для создания записи движения денежных средств через форму.
    Обрабатывает POST-запрос, сохраняет запись, выводит сообщения.
    """
    if request.method == "POST":
        form = CashFlowForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно создана ✅")
            return redirect("record_list")  # на список записей
        else:
            messages.error(request, "Исправьте ошибки в форме ⛔")
    else:
        form = CashFlowForm()

    context = {
        "form": form,
        "type": Type.objects.all(),           
        "category": Category.objects.all(),  
        "subcategories": SubCategory.objects.all(),
    }
    return render(request, "cashflow_form.html", context)


def cashflow_edit(request, pk):
    """
    Функция для редактирования записи движения денежных средств.
    Загружает запись по pk, обрабатывает POST-запрос, сохраняет изменения.
    """
    record = get_object_or_404(CashFlow, pk=pk)

    if request.method == "POST":
        form = CashFlowForm(request.POST, instance=record)
        if form.is_valid():
            form.save()
            messages.success(request, "Запись успешно обновлена ✅")
            return redirect("record_list")
        else:
            messages.error(request, "Исправьте ошибки в форме ⛔")
    else:
        form = CashFlowForm(instance=record)

    context = {
        "form": form,
        "type": Type.objects.all(),
        "category": Category.objects.all(),
        "subcategories": SubCategory.objects.all(),
    }
    return render(request, "cashflow_form.html", context)

#------------------------------- Представления для управления справочниками -------------------------------#


class DictionariesUnifiedView(View):
    """
    Класс для управления всеми справочниками (статусы, типы, категории, подкатегории) на одной странице.
    """
    template_name = "cashflow/dictionaries_unified.html"

    def get(self, request):
        """
        Отображает страницу со всеми справочниками.
        """
        return render(request, self.template_name, {
            "statuses": Status.objects.all(),
            "types": Type.objects.all(),
            "categories": Category.objects.all(),
            "subcategories": SubCategory.objects.all(),
        })

    def post(self, request):
        # --- Статусы ---
        for key in request.POST:
            if key.startswith("edit_status_"):
                status_id = key.split("_")[-1]
                obj = get_object_or_404(Status, id=status_id)
                obj.name = request.POST.get("name")
                obj.save()
                return redirect("dictionaries_unified")
            if key.startswith("delete_status_"):
                status_id = key.split("_")[-1]
                get_object_or_404(Status, id=status_id).delete()
                return redirect("dictionaries_unified")
        # --- Типы ---
            if key.startswith("edit_type_"):
                type_id = key.split("_")[-1]
                obj = get_object_or_404(Type, id=type_id)
                obj.name = request.POST.get("name")
                obj.save()
                return redirect("dictionaries_unified")
            if key.startswith("delete_type_"):
                type_id = key.split("_")[-1]
                get_object_or_404(Type, id=status_id).delete()
                return redirect("dictionaries_unified")
        # --- Категории ---
            if key.startswith("edit_category_"):
                cat_id = key.split("_")[-1]
                obj = get_object_or_404(Category, id=cat_id)
                obj.name = request.POST.get("name")
                obj.type_id = request.POST.get("type_id")
                obj.save()
                return redirect("dictionaries_unified")
            if key.startswith("delete_category_"):
                cat_id = key.split("_")[-1]
                get_object_or_404(Category, id=cat_id).delete()
                return redirect("dictionaries_unified")
        # --- Подкатегории ---
            if key.startswith("edit_subcategory_"):
                subcat_id = key.split("_")[-1]
                obj = get_object_or_404(SubCategory, id=subcat_id)
                obj.name = request.POST.get("name")
                obj.category_id = request.POST.get("category_id")
                obj.save()
                return redirect("dictionaries_unified")
            if key.startswith("delete_subcategory_"):
                subcat_id = key.split("_")[-1]
                get_object_or_404(SubCategory, id=subcat_id).delete()
                return redirect("dictionaries_unified")
        # --- Добавление ---
        if "add_status" in request.POST:
            Status.objects.create(name=request.POST.get("name"))
        elif "add_type" in request.POST:
            Type.objects.create(name=request.POST.get("name"))
        elif "add_category" in request.POST:
            Category.objects.create(
                name=request.POST.get("name"),
                type_id=request.POST.get("type_id")
            )
        elif "add_subcategory" in request.POST:
            SubCategory.objects.create(
                name=request.POST.get("name"),
                category_id=request.POST.get("category_id")
            )
        return redirect("dictionaries_unified")