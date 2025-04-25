from django.contrib.auth.models import Group, User


# Create groups if they don't exist
Group.objects.get_or_create(name="Employee")
Group.objects.get_or_create(name="Admin")

# Assign an existing user to a group
username = "your_user"  # Replace with an actual username in your DB

try:
    user = User.objects.get(username=username)
    employee_group = Group.objects.get(name='Employee')
    user.groups.add(employee_group)
    print(f"✅ Added user '{username}' to Employee group.")
except User.DoesNotExist:
    print(f"❌ User '{username}' does not exist.")
