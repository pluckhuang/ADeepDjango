import csv
from django.core.management import BaseCommand
from jobs.models import Job

# run command to import jobs:
# python manage.py import_jobs --path /path/to/your/file.csv


class Command(BaseCommand):
    help = '从一个CSV文件的内容中读取工作列表，导入到数据库中'

    def add_arguments(self, parser):
        parser.add_argument('--path', type=str)

    def handle(self, *args, **kwargs):
        path = kwargs['path']
        with open(path, 'rt', encoding="utf-8") as f:
            reader = csv.reader(f, dialect='excel', delimiter=';')
            for row in reader:

                job = Job.objects.create(
                    job_type=row[0],
                    job_name=row[1],
                    job_city=row[2],
                    job_responsibility=row[3],
                    job_requirement=row[4],
                )
                print(job)