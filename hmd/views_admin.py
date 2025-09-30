from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required
def admin_ai(request):
    # Placeholder. Later: call your MagicAI/OpenAI service.
    return render(request, "admin/tools/ai.html")
