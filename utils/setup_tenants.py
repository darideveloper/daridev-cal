import os
import sys
import django

# Add project root to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")
django.setup()

from companies.models import Client, Domain

def setup():
    # 1. Create Public Tenant
    if not Client.objects.filter(schema_name='public').exists():
        print("Creating public tenant...")
        public_tenant = Client(
            schema_name='public',
            name='Public Schema'
        )
        public_tenant.save()
        
        Domain.objects.create(
            domain='localhost',
            tenant=public_tenant,
            is_primary=True
        )
        Domain.objects.create(
            domain='127.0.0.1',
            tenant=public_tenant,
            is_primary=False
        )
        print("Public tenant created.")
    else:
        print("Public tenant already exists.")

    # 2. Create a Test Company
    if not Client.objects.filter(schema_name='company1').exists():
        print("Creating company1 tenant...")
        company = Client(
            schema_name='company1',
            name='First Company'
        )
        company.save()  # This will trigger schema creation and migration
        
        Domain.objects.create(
            domain='company1.localhost',
            tenant=company,
            is_primary=True
        )
        print("Company1 tenant created. Access it at http://company1.localhost:8000/admin/")
    else:
        print("Company1 tenant already exists.")

if __name__ == "__main__":
    setup()
