# Django Unfold Integration Guide

This document describes how `django-unfold` is integrated into this project to provide a modern, responsive, and customizable Django Admin interface.

## 0. Prerequisites

Before proceeding, ensure the core infrastructure (Environment Variables, Static Files, and Templates) has been set up following the [Project Setup Guide](project-setup.md).

## 1. Dependencies

Add the following package to your `requirements.txt`:

```text
django-unfold==0.77.1
```

## 2. Configuration in `settings.py`

### 2.1 Installed Apps

Ensure `unfold` and its optional components are placed **before** `django.contrib.admin`:

```python
INSTALLED_APPS = [
    "unfold",
    "unfold.contrib.filters",
    "unfold.contrib.forms",
    "unfold.contrib.inlines",
    # ... other apps
    "django.contrib.admin",
    "django.contrib.auth",
    # ...
]
```

### 2.2 Static Files & Templates

Ensure root static and templates directories are configured in `settings.py` to allow overriding admin assets, as described in the [Project Setup Guide](project-setup.md#6-core-settings--app-integration).

## 3. UNFOLD Settings Dictionary

Key logic:
- **SITE_ICON**: When used, the **SITE_HEADER** and **SITE_SUBHEADER** remain visible in the sidebar.
- **SITE_FAVICONS**: When used, it replaces the **SITE_ICON**, but the **SITE_HEADER** and **SITE_SUBHEADER** remain visible.
- **SITE_LOGO**: When used, it replaces the **SITE_FAVICONS**, **SITE_HEADER**, and **SITE_SUBHEADER** in the sidebar.
- **COLORS**: Defined using OKLCH for modern browser support and consistent shading.
- **SIDEBAR**: `show_all_applications: False` is used to allow manual, collapsible grouping via `navigation`.

```python
from django.templatetags.static import static
from django.urls import reverse_lazy
from django.utils.translation import gettext_lazy as _

UNFOLD = {
    "SITE_TITLE": "leochan.sh Dashboard",
    "SITE_HEADER": "leochan.sh Admin", # Fallback when logo is missing
    "SITE_SUBHEADER": "leochan.sh Dashboard", # Visible below logo
    "SITE_URL": "/",
    "SITE_ICON": lambda request: static("favicon.png"),
    "SITE_LOGO": lambda request: static("logo.webp"),
    "SITE_SYMBOL": "directions_car",
    "SITE_FAVICONS": [
        {
            "rel": "icon",
            "sizes": "32x32",
            "type": "image/png",
            "href": lambda request: static("favicon.png"),
        },
    ],
    "SHOW_HISTORY": True,
    "SHOW_VIEW_ON_SITE": True,
    "ENVIRONMENT": "utils.callbacks.environment_callback",
    "THEME": "light",
    "COLORS": {
        "primary": {
            "50": "oklch(0.97 0.02 296)",
            "100": "oklch(0.92 0.04 296)",
            "200": "oklch(0.85 0.08 296)",
            "300": "oklch(0.75 0.15 296)",
            "400": "oklch(0.70 0.22 296)",
            "500": "oklch(0.68 0.28 296)",  # C92FFF
            "600": "oklch(0.60 0.25 296)",
            "700": "oklch(0.50 0.20 296)",
            "800": "oklch(0.40 0.16 296)",
            "900": "oklch(0.30 0.12 296)",
            "950": "oklch(0.20 0.08 296)",
        },
    },
    "SIDEBAR": {
        "show_search": True,
        "show_all_applications": False,
        "navigation": [
            {
                "title": _("Autenticación"),
                "separator": True,
                "collapsible": False, # Keep open by default
                "items": [
                    {
                        "title": _("Usuarios"),
                        "icon": "person",
                        "link": reverse_lazy("admin:auth_user_changelist"),
                    },
                ],
            },
            {
                "title": _("Tienda"),
                "separator": True,
                "collapsible": True,
                "items": [
                    {
                        "title": _("Ventas"),
                        "icon": "payments",
                        "link": reverse_lazy("admin:store_sale_changelist"),
                    },
                ],
            },
            {
                "title": _("Sección de Traslados"),
                "separator": True,
                "items": [], # Used as a section divider
            },
            {
                "title": _("App Name"),
                "collapsible": True,
                "items": [
                    {
                        "title": _("Models"),
                        "icon": "directions_car",
                        "link": reverse_lazy("admin:app_model_changelist"),
                    },
                ],
            },
        ],
    },
}
```

## 4. Custom Callbacks (`utils/callbacks.py`)

Provides environment-specific badges in the admin header.

```python
import os

def environment_callback(request):
    env = os.getenv("ENV", "dev")
    env_mapping = {
        "prod": ["Production", "danger"],
        "staging": ["Staging", "warning"],
        "dev": ["Development", "info"],
        "local": ["Local", "success"],
    }
    return env_mapping.get(env, ["Unknown", "info"])
```

## 5. Static Assets (Unfold Enhancements)

These scripts enhance the Unfold interface with custom styling and functionality.

### static/js/add_tailwind_styles.js
Adds Tailwind classes to Unfold elements on load.
```javascript
document.addEventListener("DOMContentLoaded", () => {
  const classes = [
    {
      selector: ".btn",
      classes: "bg-primary-600 block border border-transparent cursor-pointer font-medium px-3 py-2 rounded-default text-white w-full lg:w-auto flex items-center justify-center hover:bg-primary-700 hover:text-white transition-colors duration-300",
    },
    {
      selector: ".img-preview",
      classes: "w-auto h-16 rounded-xl object-cover",
    },
  ]
  for (const elem_data of classes) {
    const { selector, classes } = elem_data
    const elems = document.querySelectorAll(selector)
    elems.forEach((elem) => {
      elem.classList.add(...classes.split(" "))
    })
  }
})
```

### static/js/load_markdown.js
Integrates SimpleMDE for text areas within Unfold.
```javascript
document.addEventListener("DOMContentLoaded", () => {
  const noMarkdownIds = ["google_maps_src", "description"]
  let textAreasSelector = 'div > textarea'
  const notSelector = noMarkdownIds.map(id => `:not(#id_${id})`).join("")
  textAreasSelector = `div > textarea${notSelector}`
  const textAreas = document.querySelectorAll(textAreasSelector)

  setTimeout(() => {
    textAreas.forEach(textArea => {
      new SimpleMDE({
        element: textArea,
        toolbar: [
          "bold", "italic", "heading", "|",
          "quote", "code", "link", "image", "|",
          "unordered-list", "ordered-list", "|",
          "undo", "redo", "|",
          "preview",
        ],
        spellChecker: false,
      })
    })
  }, 100)
})
```

### static/js/range_date_filter_es.js
Localizes placeholder text for Unfold's range date filters.
```javascript
document.addEventListener("DOMContentLoaded", function () {
  const texts = [
    { names: ["created_at_from", "updated_at_from"], text: "Desde" },
    { names: ["created_at_to", "updated_at_to"], text: "Hasta" },
  ]

  texts.forEach((text) => {
    text.names.forEach((name) => {
      const elem = document.querySelector(`[name="${name}"]`)
      if (!elem) return
      elem.placeholder = text.text
    })
  })
})
```

## 6. Admin Interface Overrides

Override the base admin template to inject SimpleMDE and other custom assets.

### project/templates/admin/base.html
```html
{% extends "unfold/layouts/base.html" %} {% load static %} {% block extrahead %}
{{ block.super }}
<!-- Load markdown libraries -->
<link rel="stylesheet" href="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.css" />
<script src="https://cdn.jsdelivr.net/simplemde/latest/simplemde.min.js"></script>

<!-- Load Unfold custom scripts -->
<script src="{% static 'js/add_tailwind_styles.js' %}"></script>
<script src="{% static 'js/load_markdown.js' %}"></script>
<script src="{% static 'js/range_date_filter_es.js' %}"></script>
{% endblock %}
```

## 7. Admin Implementation

### 7.1 Customizing Auth Models (`project/admin.py`)

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.admin import GroupAdmin as BaseGroupAdmin
from django.contrib.auth.models import User, Group
from unfold.forms import AdminPasswordChangeForm, UserChangeForm, UserCreationForm
from unfold.admin import ModelAdmin

admin.site.unregister(User)
admin.site.unregister(Group)

@admin.register(User)
class UserAdmin(BaseUserAdmin, ModelAdmin):
    # Forms loaded from `unfold.forms`
    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

@admin.register(Group)
class GroupAdmin(BaseGroupAdmin, ModelAdmin):
    pass
```

### 7.2 Base Admin Class (`ModelAdminUnfoldBase`)

Provides common UI enhancements like row actions and compressed fields.

```python
from unfold.admin import ModelAdmin
from unfold.decorators import action
from django.shortcuts import redirect
from django.urls import reverse

class ModelAdminUnfoldBase(ModelAdmin):
    compressed_fields = True
    warn_unsaved_form = True
    list_filter_sheet = False
    change_form_show_cancel_button = True
    
    actions_row = ["edit"]

    @action(description="Edit", permissions=["change"])
    def edit(self, request, object_id):
        return redirect(reverse(f"admin:{self.model._meta.app_label}_{self.model._meta.model_name}_change", args=[object_id]))
```
