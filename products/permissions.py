from rest_framework.permissions import BasePermission as DRFBasePermission
# from products.urls import *

ANONYMOUS_USER_WHITELIST = [  
                        'productview',
                        'productviewdetail',
                        'productreviewview',
                        ]

ANONYMOUS_LIST2 = [
    'registerview' ,
    'verifyotp',
    'token_obtain_pair',
    ]

class CustomBasePermission(DRFBasePermission):
    def has_permission(self,request,view):
            user = request.user #user,anonymous
            method = request.method.lower() #get,post
            print(user)  
            url_name = request.resolver_match.url_name #productdetailview urlname linxa not path
            print(url_name,method)  

            # if url_name in ANONYMOUS_LIST2 and method == 'post' and user.is_anonymous or user.is_superuser:
            #     return True
            
            if url_name in ANONYMOUS_USER_WHITELIST and method == 'get':
                return True
               
            elif request.user.is_anonymous: 
                 return False
          
            elif request.user.is_authenticated:
                permission__name= url_name,
                permission__method=method,
                print(user.role.filter(
            ).exists())
                return user.role.filter(
                    permission__name= url_name,
                    permission__method=method,
                        ).exists()