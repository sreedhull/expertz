from django.shortcuts import render

from .models import FAQ, Project, Service, SiteSettings


def home(request):
    services = list(Service.objects.filter(is_active=True))
    services_json = [
        {"t": s.title, "img": s.image.url, "d": s.description, "f": s.feature_list}
        for s in services
    ]
    projects_json = [
        {"t": p.title, "s": p.status, "img": p.image.url}
        for p in Project.objects.filter(is_active=True)
    ]
    return render(request, "main/index.html", {
        "cfg": SiteSettings.load(),
        "services_json": services_json,
        "projects_json": projects_json,
        "faqs": FAQ.objects.filter(is_active=True),
        "service_count": len(services),
    })
