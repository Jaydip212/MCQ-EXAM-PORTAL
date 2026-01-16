import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from api.models import User, Student

# Create superuser
username = 'jay9921'
email = 'jay9921@example.com'
password = 'Jaydip@123'

# Check if user already exists
if User.objects.filter(username=username).exists():
    print(f"User '{username}' already exists!")
    user = User.objects.get(username=username)
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.role = 'admin'
    user.save()
    print(f"Updated user '{username}' password and made admin!")
else:
    user = User.objects.create_superuser(
        username=username,
        email=email,
        password=password
    )
    user.role = 'admin'
    user.save()
    print(f"Created superuser '{username}' successfully!")

print(f"\nAdmin Login Details:")
print(f"Username: {username}")
print(f"Password: {password}")
print(f"Admin Panel: http://127.0.0.1:8000/admin")
