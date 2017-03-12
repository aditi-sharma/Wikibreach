csv_filepath = "/Users/Aditi/CapstoneProject/WikiBreach/pwnedCheck/Privacy_Rights_Clearinghouse-Data-Breaches-Export.csv"
django_home = "/Users/Aditi/CapstoneProject/WikiBreach/"

import sys, os
sys.path.append(django_home)
os.environ['DJANGO_SETTINGS_MODULE'] = 'WikiBreach.settings'

import django
django.setup()

import csv
from pwnedCheck.models import PrivacyRightsRecord

with open(csv_filepath, newline='', encoding='latin-1') as file:
    dataReader = csv.reader(file,  delimiter=',')
    for row in dataReader:
        if row[0] != "Date Made Public":
            dataRecord = PrivacyRightsRecord()
            dataRecord.date_made_public = row[0]
            dataRecord.company_name = row[1]
            dataRecord.location = row[2]
            dataRecord.breach_type = row[3]
            dataRecord.org_type = row[4]
            dataRecord.numberOf_records_breaches = row[5]
            dataRecord.total_records = row[6]
            dataRecord.description = row[7]
            dataRecord.info_source = row[8]
            dataRecord.save()