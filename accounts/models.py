
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager

class Permission(models.Model):
    name = models.CharField(max_length=100) 
    route = models.CharField(max_length=100) 
    method = models.CharField(max_length=100) 
    
    def __str__(self):
        return f"{self.name}->{self.method}"

    class Meta:
        db_table = 'permissions'
        unique_together = ('route','method') #route rw method same xa vane twice save nahuna suppose route:/api/blog method : get aaba feri aarko ni tahi req xa vane aarko choti tyo combination save nahuna lai
    
class Role(models.Model):
    name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        db_table = 'roles' #databaseko table ko name role banako nroamlly auth_kkk hunxa yesko name change garya matrai ho
        
class RolePermission(models.Model):
    role = models.ForeignKey(Role,on_delete=models.CASCADE,related_name='roles_of_rp')
    permission = models.ForeignKey(Permission,on_delete=models.CASCADE,related_name='permissions_of_rp')
    
    class Meta:
        db_table = 'role_permissions'    
    
    def __str__(self):
        return f"{self.role}->{self.permission}"

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Users must have an email address")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other')
    )
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=50, blank=False)
    last_name = models.CharField(max_length=50, blank=False)
    email_verified = models.BooleanField(default=False)
    otp = models.CharField(max_length=10)
    is_staff = models.BooleanField(default=False)   
    is_active = models.BooleanField(default=True)   
    is_customer = models.BooleanField(default=False) 
    groups = None
    user_permissions = None
    role = models.ManyToManyField(
        RolePermission,
    )
    related_name="rolesofuser",
    help_text="Roles of user",
    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['first_name', 'last_name'] 

    objects = CustomUserManager()

    def __str__(self):
        return self.email

#staff 
class Staff(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.PROTECT, related_name='staff')
    is_assigned = models.BooleanField(default=False)
    date_time = models.DateTimeField(auto_now_add=True)
    roles = models.ManyToManyField(RolePermission, related_name="roles")

    def __str__(self):
        return self.user.email[:10]


