# Tạo một tệp management/commands/reset_db.py trong dự án Django của bạn.
from django.core.management.base import BaseCommand
from django.db import connection

class Command(BaseCommand):
    help = 'Resets the PostgreSQL database.'

    def handle(self, *args, **options):
        with connection.cursor() as cursor:
            cursor.execute('DROP DATABASE IF EXISTS SaleSystemPortal;')
            cursor.execute('CREATE DATABASE SaleSystemPortal;')
