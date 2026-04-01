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

def is_tenant_request(request):
    return hasattr(request, "tenant") and getattr(request.tenant, "schema_name", "public") != "public"

def get_tenant_profile(request):
    if is_tenant_request(request):
        from scheduler.models import CompanyProfile
        from django_tenants.utils import schema_context
        with schema_context(request.tenant.schema_name):
            return CompanyProfile.objects.first()
    return None


def site_title_callback(request):
    if is_tenant_request(request):
        return request.tenant.name
    return "DARI DEV CAL"

def site_header_callback(request):
    if is_tenant_request(request):
        return request.tenant.name
    return "DARI DEV"

def site_subheader_callback(request):
    if is_tenant_request(request):
        return request.get_host()
    return "Appointment System"

def site_icon_callback(request):
    from django.templatetags.static import static
    profile = get_tenant_profile(request)
    if profile and profile.logo:
        return profile.logo.url
    return static("logo.png")

def get_brand_config(request):
    """Resolve the tenant's brand color into light, main, and dark shades."""
    profile = get_tenant_profile(request)
    brand_color = profile.brand_color if profile else "oklch(0.81 0.11 236)"

    if brand_color.startswith("oklch("):
        try:
            # Basic parsing: oklch(L C H)
            core = brand_color.replace("oklch(", "").replace(")", "")
            l, c, h = core.split()
            l_val = float(l)
            return {
                "400": f"oklch({min(l_val + 0.02, 0.99):.2f} {c} {h})",
                "500": brand_color,
                "600": f"oklch({max(l_val - 0.09, 0.1):.2f} {c} {h})",
            }
        except (ValueError, IndexError):
            pass

    return {
        "400": brand_color,
        "500": brand_color,
        "600": brand_color,
    }
