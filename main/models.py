from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models

MAX_IMAGE_MB = 5


def validate_image_size(f):
    if f.size > MAX_IMAGE_MB * 1024 * 1024:
        raise ValidationError("Image is too large. Please keep it under %d MB." % MAX_IMAGE_MB)


IMAGE_RULES = [FileExtensionValidator(["jpg", "jpeg", "png", "webp"]), validate_image_size]


class SiteSettings(models.Model):
    """One single record that holds the site's logo, big photos and contact details."""

    # --- Contact ---
    phone_1 = models.CharField("Phone 1", max_length=30, default="+91 89219 89661",
                               help_text="Shown on the site, e.g. +91 89219 89661")
    phone_2 = models.CharField("Phone 2", max_length=30, blank=True, default="+91 77364 47661")
    whatsapp_number = models.CharField(
        "WhatsApp number", max_length=20, default="918921989661",
        help_text="Digits only with country code, no + or spaces. The enquiry form sends messages here.")
    email = models.EmailField(default="roopeshexperts@gmail.com")
    address = models.CharField(
        max_length=250, default="Expertz Acoustics and Interiors, Prabhakar Building, Vripadam, Malappuram District")
    top_location = models.CharField("Top bar location", max_length=120, default="Vripadam, Malappuram, Kerala")
    facebook_url = models.URLField("Facebook page", blank=True, default="https://www.facebook.com/roopeshkarad.me")
    video_url = models.URLField("'Watch our work' video link", blank=True,
                                default="https://www.facebook.com/reel/908627688266797")

    # --- Logos ---
    logo = models.ImageField("Logo (header)", upload_to="site/", validators=IMAGE_RULES, blank=True,
                             help_text="Transparent PNG, about 520 x 250 px. Shown on the light header.")
    logo_light = models.ImageField("Logo (footer, white version)", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                   help_text="Transparent PNG with light text. Shown on the dark footer.")

    # --- Big photos ---
    hero_image = models.ImageField("Home page main photo", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                   help_text="Portrait photo, about 1200 x 1400 px.")
    hero_image_2 = models.ImageField("Home page small photo", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                     help_text="About 900 x 700 px.")
    about_image_1 = models.ImageField("About section - large photo", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                      help_text="Portrait, about 1000 x 1150 px.")
    about_image_2 = models.ImageField("About section - small photo", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                      help_text="Square, about 900 x 900 px.")
    why_image = models.ImageField("'Why choose us' background", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                  help_text="Dark photo works best, about 1920 x 1080 px.")
    cta_image = models.ImageField("'Ready to transform your space' background", upload_to="site/", validators=IMAGE_RULES, blank=True,
                                  help_text="About 1920 x 1080 px.")

    class Meta:
        verbose_name = "Site settings (logo, photos, contact)"
        verbose_name_plural = "Site settings (logo, photos, contact)"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1  # always a single record
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        pass  # the settings record can't be deleted

    @classmethod
    def load(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    @property
    def whatsapp_digits(self):
        return "".join(ch for ch in self.whatsapp_number if ch.isdigit())

    @staticmethod
    def tel(value):
        return "+" + "".join(ch for ch in value if ch.isdigit()) if value else ""

    @property
    def phone_1_tel(self):
        return self.tel(self.phone_1)

    @property
    def phone_2_tel(self):
        return self.tel(self.phone_2)


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    features = models.TextField(blank=True, help_text="One bullet point per line.")
    image = models.ImageField(upload_to="services/", validators=IMAGE_RULES, help_text="4:3 photo, about 1200 x 900 px.")
    order = models.PositiveIntegerField(default=0, help_text="Smaller numbers appear first.")
    is_active = models.BooleanField("Show on website", default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title

    @property
    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class Project(models.Model):
    COMPLETED = "completed"
    ONGOING = "ongoing"
    STATUS_CHOICES = [(COMPLETED, "Previous work (completed)"), (ONGOING, "Ongoing work")]

    title = models.CharField(max_length=120)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default=COMPLETED)
    image = models.ImageField(upload_to="projects/", validators=IMAGE_RULES, help_text="4:3 photo, about 1200 x 900 px.")
    order = models.PositiveIntegerField(default=0, help_text="Smaller numbers appear first.")
    is_active = models.BooleanField("Show on website", default=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class FAQ(models.Model):
    question = models.CharField(max_length=250)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0, help_text="Smaller numbers appear first.")
    is_active = models.BooleanField("Show on website", default=True)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question
