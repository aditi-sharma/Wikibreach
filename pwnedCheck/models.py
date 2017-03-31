from django.db import models
from oauth2client.contrib.django_util.models import CredentialsField
from django.contrib.auth.models import User

# Create your models here.
class PrivacyRightsRecord(models.Model):
    TYPE_OF_BREACHES = (
        ('CARD', 'Payment Card Fraud'),
        ('HACK', 'Hacking or Matware attack'),
        ('INSD', 'Insider Breach Attack'),
        ('PHYS', 'Physical Loss'),
        ('PORT', 'Portable Device Breach'),
        ('STAT', 'Stationary Computer Loss'),
        ('DISC', 'Uninteded Disclosure'),
        ('Unknown', 'Uncertain Type of Breach')
    )
    ORGANIZATION_TYPES = (
        ('BSF', 'BUsinesses-Financial and Insurance Services'),
        ('BSO', 'Businesses-Other'),
        ('BSR', 'Businesses-Retail/Merchant-Including Online Retail'),
        ('EDU', 'Educational Instituitions'),
        ('GOV', 'Government & Military'),
        ('MED', 'Healthcare, Medical Providers & Medical Insurance Services'),
        ('NGO', 'Nonprofits')
    )
    date_made_public = models.CharField(blank=False, null=False, max_length=25)
    company_name = models.TextField(null=False, blank=False)
    location = models.CharField(max_length=30, null=False)
    breach_type = models.CharField(max_length=8, choices=TYPE_OF_BREACHES)
    org_type = models.CharField(max_length=3, choices=ORGANIZATION_TYPES)
    numberOf_records_breaches = models.TextField()
    total_records = models.CharField(max_length=10)
    description = models.TextField()
    info_source = models.CharField(max_length=30)

class meta:
    ordering = ['date_made_public']

class CredentialsModel(models.Model):
    user_id = models.OneToOneField(User)
    credential = CredentialsField()