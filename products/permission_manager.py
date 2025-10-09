
from accounts.models import Role,Permission,RolePermission,CustomUser
from products.api_routes import PermissionManager

def update_permission():
    """Update permission in the system."""
    Permission.objects.all().delete() #permissions blog->get,
    pm = PermissionManager()
    permisisons_map = pm.get_permission_map() #sabai dict permission haru aayo
    for role, permission in permisisons_map.items(): #key-value
        role_obj, _ = Role.objects.get_or_create(name=role) 
        permission_routes = flatten_list(permission) 
        for each_permission in permission_routes:           
            )
            permission_obj, _ = Permission.objects.get_or_create(
                route=each_permission[0], method=each_permission[1],
                name=each_permission[0]
            rolep, _ = RolePermission.objects.get_or_create(
                role=role_obj, permission=permission_obj
            )
           
            if role == 'user':
                normal_users = CustomUser.objects.filter(is_superuser=False,is_staff=False) 
                for user in normal_users:
                    user.role.add(rolep)
            else:
                user = CustomUser.objects.filter(is_superuser=True,is_staff=True)
                for user in user:
                    user.role.add(rolep)
                                    
def flatten_list(nested_list):
    """Convert nested list to single list."""
    final_list = []
    for each in nested_list: 
        #[[('blogcreateview', 'get'), ('profile', 'get'), ('blogdetailview', 'get')], ('blogdetailview', 'post')] 
        if not isinstance(each, list): #it is a list or not tyo check garxa
            final_list.append(each)
            continue
        final_list.extend(flatten_list(each)) #calling tyo function again with that list []
    return final_list