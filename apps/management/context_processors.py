from apps.management.models import AppSettings

def management_processor(request):
    return {
        'app_settings': AppSettings.load(),
    }