from django.core.management.base import BaseCommand
from ai_engine.models import AIProfile, ServiceTag, LocationTag, AIContent, AILog
from ai_engine.utils import generate_piece

class Command(BaseCommand):
    help = "Generate AI SEO pieces per plan limits"

    def add_arguments(self, parser):
        parser.add_argument("--profile-id", type=int, help="AIProfile id")
        parser.add_argument("--language", default="nl")

    def handle(self, *args, **opts):
        pid = opts.get("profile_id")
        lang = opts.get("language", "nl")
        profiles = AIProfile.objects.filter(id=pid) if pid else AIProfile.objects.all()
        total = 0

        for profile in profiles:
            services = ServiceTag.objects.all()[:profile.max_services]
            locs = list(LocationTag.objects.all()[:profile.max_locations]) or [None]
            kinds = ["meta_title", "meta_desc", "jsonld", "faq"]

            for s in services:
                for loc in locs:
                    for k in kinds:
                        content = generate_piece(k, s, loc, lang)
                        AIContent.objects.update_or_create(
                            profile=profile, service=s, location=loc, language=lang, kind=k,
                            defaults={"content": content, "is_published": profile.auto_publish},
                        )
                        total += 1

            AILog.objects.create(profile=profile, event="generation",
                                 detail=f"generated={total}, lang={lang}")

        self.stdout.write(self.style.SUCCESS(f"Done. Generated {total} items."))
