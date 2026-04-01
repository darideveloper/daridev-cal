# Design: Full Unfold Integration

## Context
The project is an appointment system ("DARI DEV CAL"). The user wants a modern, branded admin interface using `django-unfold`.

## Architecture
- **Unfold Settings**: Centralized in `project/settings.py` within the `UNFOLD` dictionary.
- **Brand Color**: The hex `#87d1ff` is converted to an OKLCH scale centered around `oklch(0.81 0.11 236)` for native Unfold compatibility.
- **Navigation**: Manual navigation configuration is preferred over `show_all_applications` to allow grouping and custom icons. Links use `reverse_lazy` for dynamic URL generation.
- **Environment Callback**: A dynamic callback in `utils/callbacks.py` will read the `ENV` environment variable to show a status badge in the admin header.
- **Template Overrides**: The `project/templates/admin/base.html` will be used to inject third-party JS libraries (SimpleMDE) and custom script enhancers.

## Decision Log
- **SITE_ICON vs SITE_LOGO**: Use `SITE_ICON` to keep the `SITE_HEADER` ("DARI DEV") and `SITE_SUBHEADER` ("Calendar Management") visible in the sidebar.
- **ModelAdmin Base**: A custom `ModelAdminUnfoldBase` will be created to enforce `compressed_fields=True`, `warn_unsaved_form=True`, and `actions_row=["edit"]` across all registered models.
- **OKLCH Scaling**: Standard Unfold color scaling (50-950) is used to ensure consistent UI contrast across all interface states (hover, focus, active).
- **Navigation Icons**: Material Symbols like `calendar_today` for booking and `person` for auth will be used to improve visual hierarchy.
