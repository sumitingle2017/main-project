# Mala Shree Om Bhel & Namkeen - Django
1. Database: PostgreSQL / Supabase
2. `pip install -r requirements.txt`
3. Configure `.env`:
   - `host`: Supabase host (e.g., `aws-0-ap-south-1.pooler.supabase.com`)
   - `port`: `5432`
   - `database`: `postgres`
   - `user`: Supabase user (e.g., `postgres.pgchbxqiuqvubzwuryts`)
   - `password`: Your Supabase database password
4. Run migrations: `python manage.py migrate`
5. Create admin/staff: `python manage.py createsuperuser`
6. Start development server: `python manage.py runserver 0.0.0.0:8000`
Pages: / (customer menu), /counter/, /kitchen/, /manage/, /login/
