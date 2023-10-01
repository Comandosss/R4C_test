from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'

    def ready(self):
        from django.contrib.auth.models import Group

        tech_group, created = Group.objects.get_or_create(name='Techspec')
        manager_group, created = Group.objects.get_or_create(name='Manager')
        customer_group, created = Group.objects.get_or_create(name='Customer')

        # manager_permission_view1 = Permission.objects.get(codename='view_robot')
        # manager_group.permissions.add(manager_permission_view1)
