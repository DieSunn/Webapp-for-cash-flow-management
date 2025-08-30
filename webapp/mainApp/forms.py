from django import forms
from .models import CashFlow, Status, Type, Category, SubCategory


# Форма для создания и редактирования записей ДДС
class CashFlowForm(forms.ModelForm):
    class Meta:
        model = CashFlow
        # Список полей, отображаемых в форме
        fields = ["created_at", "status", "type", "category", "subcategory", "amount", "comment"]

        # Настройка виджетов для каждого поля формы
        widgets = {
            "created_at": forms.DateInput(
                attrs={"type": "date", "class": "form-control", "required": True}
            ),
            "status": forms.Select(attrs={"class": "form-select", "required": True}),
            "type": forms.Select(attrs={"class": "form-select", "required": True}),
            "category": forms.Select(attrs={"class": "form-select", "required": True}),
            "subcategory": forms.Select(attrs={"class": "form-select"}),
            "amount": forms.NumberInput(
                attrs={"class": "form-control", "required": True, "step": "0.01", "min": "0.01"}
            ),
            "comment": forms.Textarea(
                attrs={"class": "form-control", "rows": 2, "maxlength": 500}
            ),
        }

    def clean(self):
        """
        Кастомная валидация формы:
        - Проверяет, что категория принадлежит выбранному типу.
        - Проверяет, что подкатегория принадлежит выбранной категории.
        """
        cleaned_data = super().clean()
        type_obj = cleaned_data.get("type")
        category_obj = cleaned_data.get("category")
        subcategory_obj = cleaned_data.get("subcategory")

        # Проверка: категория соответствует типу
        if category_obj and type_obj and category_obj.type != type_obj:
            self.add_error(
                "category",
                f"Категория «{category_obj}» не принадлежит типу «{type_obj}»."
            )

        # Проверка: подкатегория соответствует категории
        if subcategory_obj and category_obj and subcategory_obj.category != category_obj:
            self.add_error(
                "subcategory",
                f"Подкатегория «{subcategory_obj}» не принадлежит категории «{category_obj}»."
            )

        return cleaned_data


# Форма для создания и редактирования статусов
class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True, "maxlength": 100}),
        }

    def clean_name(self):
        """
        Проверяет уникальность имени статуса (без учёта регистра).
        """
        name = self.cleaned_data["name"].strip()
        if Status.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Такой статус уже существует")
        return name


# Форма для создания и редактирования типов
class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ["name"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True, "maxlength": 100}),
        }

    def clean_name(self):
        """
        Проверяет уникальность имени типа (без учёта регистра).
        """
        name = self.cleaned_data["name"].strip()
        if Type.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Такой тип уже существует")
        return name


# Форма для создания и редактирования категорий
class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ["name", "type"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True, "maxlength": 100}),
            "type": forms.Select(attrs={"class": "form-select", "required": True}),
        }

    def clean_name(self):
        """
        Проверяет уникальность имени категории для выбранного типа.
        """
        name = self.cleaned_data["name"].strip()
        if Category.objects.filter(name__iexact=name, type=self.cleaned_data.get("type")).exists():
            raise forms.ValidationError("Категория с таким именем уже есть для данного типа")
        return name


# Форма для создания и редактирования подкатегорий
class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = SubCategory
        fields = ["name", "category"]
        widgets = {
            "name": forms.TextInput(attrs={"class": "form-control", "required": True, "maxlength": 100}),
            "category": forms.Select(attrs={"class": "form-select", "required": True}),
        }

    def clean_name(self):
        """
        Проверяет уникальность имени подкатегории для выбранной категории.
        """
        name = self.cleaned_data["name"].strip()
        if SubCategory.objects.filter(name__iexact=name, category=self.cleaned_data.get("category")).exists():
            raise forms.ValidationError("Подкатегория с таким именем уже существует в этой категории")
        return name