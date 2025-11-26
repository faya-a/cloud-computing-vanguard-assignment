# Django

Django is a web framework for the backend.


Typical project structure looks like:

```
project/
    settings.py
    urls.py
    app/
        models.py
        views.py
        urls.py
        templates/

```

## Demo Code: Django Basics (Models, Views, URLs, Templates, Admin)

### 1. Model Definition


```py

# app/models.py
from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.name

```

### 2. Function-Based View


```py
# app/views.py
from django.shortcuts import render
from .models import Product

def product_list(request):
    items = Product.objects.filter(is_active=True)
    return render(request, "product_list.html", {"items": items})

```

### 3. URL Mapping

```py
# app/urls.py
from django.urls import path
from .views import product_list

urlpatterns = [
    path("products/", product_list, name="product_list"),
]

```

> [!IMPORTANT]
> Connect to project

```py
# project/urls.py
from django.urls import path, include

urlpatterns = [
    path("", include("app.urls")),
]

```

### 4. Template rendering

```html
<!-- app/templates/product_list.html -->
<h2>Products</h2>
<ul>
{% for item in items %}
    <li>{{ item.name }} – {{ item.price }}</li>
{% endfor %}
</ul>
```

### 5. Class-based View

```py
# app/views.py
from django.views.generic import ListView
from .models import Product

class ProductListView(ListView):
    model = Product
    template_name = "product_list.html"

```


### 6. Form Handling


```py
# app/forms.py
from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "price", "is_active"]

```


```py
# app/views.py
from django.shortcuts import render, redirect
from .forms import ProductForm

def add_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect("product_list")
    return render(request, "add_product.html", {"form": form})

```

### 7. Admin Registration


```py
# app/admin.py
from django.contrib import admin
from .models import Product

admin.site.register(Product)

```
