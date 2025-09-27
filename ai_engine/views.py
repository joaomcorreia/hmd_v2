from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import AIContent

@staff_member_required
def preview(request):
    items = AIContent.objects.order_by("-updated_at")[:200]
    return render(request, "ai_engine/preview.html", {"items": items})

@staff_member_required
def publish(request, pk):
    item = get_object_or_404(AIContent, pk=pk)
    item.is_published = True
    item.save()
    return redirect("ai_preview")

def health(request):
    from django.http import HttpResponse
    return HttpResponse("ai ok")
