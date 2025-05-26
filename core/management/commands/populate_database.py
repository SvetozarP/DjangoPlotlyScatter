import csv
from django.conf import settings
from django.core.management.base import BaseCommand
from core.models import PersonSalary


class Command(BaseCommand):
    help = 'Load data from wage file'

    def handle(self, *args, **kwargs):
        if PersonSalary.objects.count() > 0:
            PersonSalary.objects.all().delete()

        # open CSV
        DATA_FILE = settings.BASE_DIR / 'data' / 'wage.csv'
        assert DATA_FILE.exists()

        with open(DATA_FILE, 'r') as csvfile:
            reader = csv.DictReader(csvfile)
            # init empty list for PersonSalary objects
            db_rows = []
            for row in reader:
                db_rows.append(
                    PersonSalary(
                        age=row['age'],
                        salary=row['wage'],
                        education=row['education'],
                    )
                )
            # bulk create records
            PersonSalary.objects.bulk_create(db_rows, batch_size=1000)