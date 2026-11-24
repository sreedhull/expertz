"""Loads the starting content: your photos, services, projects and FAQs.

Run once after migrating:   python manage.py seed_content
Safe to re-run: it only fills things that are still empty. Use --reset to wipe and reload services/projects/FAQs.
"""
from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.management.base import BaseCommand

from main.models import FAQ, Project, Service, SiteSettings

SEED = Path(settings.BASE_DIR) / "seed_images"


def attach(obj, field, filename):
    path = SEED / filename
    with open(path, "rb") as fh:
        getattr(obj, field).save(filename, File(fh), save=False)


SERVICES = [
    ("Home Interior Works", "photo-08.jpg",
     "We design and execute modern and stylish home interiors including living rooms, bedrooms, kitchens and customized wall designs that enhance comfort and beauty.",
     ["Living rooms, bedrooms and kitchens", "Customized wall designs", "Comfortable, modern and stylish finishes", "Support from design to execution"]),
    ("Soundproofing Solutions", "photo-23.jpg",
     "Professional soundproofing systems designed to block unwanted noise and create peaceful environments for studios, theatres and private spaces.",
     ["Blocks unwanted noise", "For studios, theatres and private spaces", "Calm, distraction-free rooms", "Planned around your space"]),
    ("Acoustic Panel Supply & Installation", "photo-05.jpg",
     "We provide high-quality acoustic panels that reduce echo, control sound reflections and improve acoustic performance for studios, offices and homes.",
     ["Reduces echo", "Controls sound reflections", "Studios, offices and homes", "Quality panels, professional fitting"]),
    ("Recording Studio Setup", "photo-11.jpg",
     "Complete audio recording studio acoustic treatment and installation including wall panels, ceiling treatment and sound isolation systems.",
     ["Wall panel treatment", "Ceiling treatment", "Sound isolation systems", "Complete installation"]),
    ("Auditorium Acoustic Works", "photo-07.jpg",
     "Advanced auditorium acoustic design and installation to ensure clear sound distribution and reduced echo.",
     ["Clear sound distribution", "Reduced echo", "Advanced acoustic design", "Professional installation"]),
    ("Home Theatre Acoustic Setup", "photo-09.jpg",
     "Create the perfect home theatre experience with proper acoustic treatment and soundproofing.",
     ["Proper acoustic treatment", "Soundproofing for private viewing", "Clearer dialogue and effects", "Tailored to your room"]),
]

# (title, status, photo)
PROJECTS = [
    ("Living room interior", "completed", "photo-06.jpg"),
    ("Recording studio", "completed", "photo-11.jpg"),
    ("Acoustic wall panels", "completed", "photo-05.jpg"),
    ("Modular kitchen", "completed", "photo-02.jpg"),
    ("Luxury living room", "completed", "photo-08.jpg"),
    ("Navy modular kitchen", "completed", "photo-12.jpg"),
    ("Master bedroom", "completed", "photo-21.jpg"),
    ("Gypsum ceiling work", "ongoing", "photo-23.jpg"),
    ("Home theatre", "ongoing", "photo-09.jpg"),
    ("Auditorium treatment", "ongoing", "photo-07.jpg"),
    ("Kitchen with bar counter", "ongoing", "photo-01.jpg"),
    ("Green modular kitchen", "ongoing", "photo-03.jpg"),
    ("Green L-shaped kitchen", "ongoing", "photo-04.jpg"),
    ("Bedroom with feature wall", "ongoing", "photo-10.jpg"),
    ("Navy and white kitchen", "ongoing", "photo-13.jpg"),
    ("Bedroom with dresser", "ongoing", "photo-14.jpg"),
    ("Entrance passage", "ongoing", "photo-15.jpg"),
    ("Pantry and wardrobe", "ongoing", "photo-16.jpg"),
    ("Study bedroom", "ongoing", "photo-17.jpg"),
    ("Foyer with mirror", "ongoing", "photo-18.jpg"),
    ("Dining area", "ongoing", "photo-19.jpg"),
    ("Bedroom with slat wall", "ongoing", "photo-20.jpg"),
    ("Guest bedroom", "ongoing", "photo-22.jpg"),
]

FAQS = [
    ("What is the difference between soundproofing and acoustic treatment?",
     "Soundproofing blocks sound from travelling into or out of a room. Acoustic treatment (such as acoustic panels) controls echo and reflections inside the room so speech and music sound clear. Studios, theatres and home theatres usually need both."),
    ("Will acoustic panels stop noise coming from outside?",
     "Panels on their own mainly improve how a room sounds on the inside. To keep outside noise out, a soundproofing system is needed. We look at your space and tell you which one, or which combination, will actually solve your problem."),
    ("Which kinds of spaces do you work on?",
     "Homes, recording studios, auditoriums, home theatres, offices and other commercial spaces. Whether it is one room or a full interior, we plan the work around your needs."),
    ("Can you handle interior design as well as acoustics?",
     "Yes. Acoustic work and interior work are done by one team, so your space sounds good and looks good, with complete project support from design to installation."),
    ("How do I get a quote?",
     "Call or WhatsApp us, or send an enquiry through the form below with a few details about your space. The cost depends on the size of the space, the materials and the scope of work, so we start with a consultation to understand what you need."),
    ("What happens after I contact you?",
     "We begin with a consultation about your space, sound requirements and design needs. Then we prepare a customized layout, carry out the installation with quality materials, and finish with testing for the best acoustic performance and appearance."),
]


class Command(BaseCommand):
    help = "Load the starting photos and content for the website."

    def add_arguments(self, parser):
        parser.add_argument("--reset", action="store_true", help="Delete and reload services, projects and FAQs.")

    def handle(self, *args, **opts):
        cfg = SiteSettings.load()
        slots = {
            "logo": "logo.png",
            "logo_light": "logo-light.png",
            "hero_image": "photo-05.jpg",
            "hero_image_2": "photo-11.jpg",
            "about_image_1": "photo-08.jpg",
            "about_image_2": "photo-11.jpg",
            "why_image": "photo-09.jpg",
            "cta_image": "photo-07.jpg",
        }
        for field, fname in slots.items():
            if not getattr(cfg, field):
                attach(cfg, field, fname)
        cfg.save()

        if opts["reset"]:
            Service.objects.all().delete()
            Project.objects.all().delete()
            FAQ.objects.all().delete()

        if not Service.objects.exists():
            for i, (title, photo, desc, feats) in enumerate(SERVICES, 1):
                s = Service(title=title, description=desc, features="\n".join(feats), order=i)
                attach(s, "image", photo)
                s.save()
        if not Project.objects.exists():
            for i, (title, status, photo) in enumerate(PROJECTS, 1):
                p = Project(title=title, status=status, order=i)
                attach(p, "image", photo)
                p.save()
        if not FAQ.objects.exists():
            for i, (q, a) in enumerate(FAQS, 1):
                FAQ.objects.create(question=q, answer=a, order=i)

        self.stdout.write(self.style.SUCCESS("Starting content loaded."))
