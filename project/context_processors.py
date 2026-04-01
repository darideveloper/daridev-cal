from utils.callbacks import get_brand_config

def branding(request):
    """Provide derived brand color config to templates."""
    return {
        "brand_colors": get_brand_config(request)
    }
