import datetime
from io import StringIO
from faker import Faker
import itertools

from config import settings
from config.celery import celery
from django.apps import apps
import csv
import boto3


class GeneratorSwitch:
    def __init__(self):
        self.fake = Faker()
        self.column = None

    def fake_name(self):
        return self.fake.name()

    def fake_job(self):
        return self.fake.job()

    def fake_email(self):
        return self.fake.email()

    def fake_domain(self):
        return self.fake.domain_name()

    def fake_phone(self):
        return self.fake.phone_number()

    def fake_company(self):
        return self.fake.company()

    def fake_text(self):
        return ' '.join(self.fake.sentences(self.fake.random_int(self.column.start, self.column.end)))

    def fake_int(self):
        return str(self.fake.random_int(self.column.start, self.column.end))

    def fake_address(self):
        return self.fake.address()

    def fake_date(self):
        return self.fake.date()

    def dispatch(self, column):
        method_name = 'fake_' + str(column.kind)
        self.column = column
        return getattr(self, method_name)()


@celery.task
def generate_csv(task_id):
    task_model = apps.get_model(app_label='task', model_name='Task')
    task = task_model.objects.select_related('schema').get(id=task_id)
    file_name = str(datetime.datetime.now().strftime('%s')) + '.csv'
    try:
        with StringIO() as file:
            # create virtual file
            writer = csv.writer(file, delimiter=task.schema.separator)
            columns = task.schema.column_set.all()
            names = list()
            [names.append(column.name) for column in columns]
            names.insert(0, '#')
            writer.writerow(names)
            generator = GeneratorSwitch()
            counter = 1
            for _ in itertools.repeat(None, task.rows):
                item = list()
                [item.append(generator.dispatch(column)) for column in columns]
                item.insert(0, counter)
                writer.writerow(item)
                counter += 1

            # upload to aws
            file.seek(0)
            s3 = boto3.resource('s3')
            s3_object = s3.Object(settings.AWS_BUCKET, file_name)
            s3_object.put(Body="")
            client = boto3.client('s3')
            client.put_object(Body=file.read(), Bucket=settings.AWS_BUCKET, Key=file_name, ACL='public-read')
            bucket_location = client.get_bucket_location(Bucket=settings.AWS_BUCKET)
            object_url = "https://s3-{0}.amazonaws.com/{1}/{2}".format(
                bucket_location['LocationConstraint'],
                settings.AWS_BUCKET,
                file_name
            )

            task.status = 10
            task.file = object_url
            task.save()
    except Exception as e:
        task.status = 1
        task.error = e
        task.save()
        exit()
