from django.apps import apps
from django.contrib.admin.sites import site
from django.contrib.admin.views.decorators import staff_member_required
from django.http import JsonResponse, Http404
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_http_methods


def _get_admin(model):
    return site._registry.get(model)


def _extra_context(model, instance):
    extra = {}
    if model._meta.model_name == "slide":
        slides = list(model.objects.order_by("order", "id"))
        entries = []
        current_index = 0
        for idx, slide in enumerate(slides, 1):
            if slide.pk == instance.pk:
                current_index = idx
            entries.append({"id": slide.pk, "title": slide.title or f"Slide {idx}", "index": idx, "active": slide.pk == instance.pk})
        extra = {
            "slides": entries,
            "current_index": current_index,
            "total": len(slides),
            "primary_fields": ["title", "subtitle", "cta1_label", "cta1_url", "cta2_label", "cta2_url", "order", "is_active", "image"],
        }
    elif model._meta.model_name == "homeaboutpanel":
        extra = {
            "primary_fields": ["title_emphasis", "title_rest", "lead_text", "body_text", "cta_label", "cta_url"],
        }
    elif model._meta.model_name == "homevalueblock":
        extra = {
            "primary_fields": ["image", "image_alt", "title_emphasis", "title_rest", "body", "link_1_label", "link_1_url", "link_2_label", "link_2_url", "link_3_label", "link_3_url"],
        }
    elif model._meta.model_name == "abouthero":
        extra = {
            "primary_fields": ["title", "background_image"],
        }
    elif model._meta.model_name == "aboutcarouselitem":
        extra = {
            "primary_fields": ["alt_text", "order", "image"],
        }
    elif model._meta.model_name == "aboutcompanyblock":
        extra = {
            "primary_fields": ["years_number", "years_label", "heading", "body", "cta_label", "cta_url"],
        }
    elif model._meta.model_name == "aboutbenefit":
        extra = {
            "primary_fields": ["order", "title", "subtitle", "description", "image", "image_alt"],
        }
    elif model._meta.model_name == "aboutprocessstep":
        extra = {
            "primary_fields": ["order", "step_title", "heading", "description", "image"],
        }
    elif model._meta.model_name == "homecarouselitem":
        extra = {
            "primary_fields": ["alt_text", "order", "image"],
        }
    return extra

@staff_member_required
@csrf_protect
@require_http_methods(["GET", "POST"])
def preview_edit(request, app_label, model_name, pk):
    model = apps.get_model(app_label, model_name)
    if model is None:
        raise Http404

    model_admin = _get_admin(model)
    if model_admin is None:
        raise Http404

    obj = get_object_or_404(model, pk=pk)
    if not model_admin.has_change_permission(request, obj):
        raise Http404

    form_class = model_admin.get_form(request, obj, change=True)
    form = form_class(request.POST or None, request.FILES or None, instance=obj)

    def render_fragment(form_obj):
        instance = form_obj.instance
        context = {
            "form": form_obj,
            "obj": instance,
            "opts": model._meta,
            "endpoint": request.path,
            "extra": _extra_context(model, instance),
        }
        return render_to_string("admin/preview_form_fragment.html", context, request=request)

    if request.method == "POST":
        if form.is_valid():
            form_validated_obj = form.save(commit=False)
            model_admin.save_model(request, form_validated_obj, form, change=True)
            if hasattr(form, "save_m2m"):
                form.save_m2m()
            model_admin.log_change(
                request,
                form_validated_obj,
                model_admin.construct_change_message(request, form, None),
            )
            html = render_fragment(form_class(instance=form_validated_obj))
            return JsonResponse({"success": True, "html": html})
        html = render_fragment(form)
        return JsonResponse({"success": False, "html": html}, status=400)

    html = render_fragment(form)
    return JsonResponse({"html": html})




