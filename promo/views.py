from django.shortcuts import redirect, get_object_or_404
from promo.models import TrackedLink


def tracked_redirect(request, slug):
    link = get_object_or_404(TrackedLink, slug=slug)
    link.clicks += 1
    link.save()
    return redirect(link.target_url)
