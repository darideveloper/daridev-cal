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
