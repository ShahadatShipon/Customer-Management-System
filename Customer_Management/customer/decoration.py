from django.http import HttpResponse
from django.shortcuts import redirect

##This function is for user authentication /checks whether user is authenticated to view this page or not
def userUnauthenticated(def_func):
    def wrapper_func(request,*args, **kwargs):
        if request.user.is_authenticated:
            return redirect('dashboard')
        else:
            return def_func(request,*args, **kwargs)
    return wrapper_func

##This function is for setting user role/which user can view  what
def allowed_user(allowed_role=[]):
    def decorator(view_func):
        def wrapper_func(request,*args, **kwargs):
            group = None
            if request.user.groups.exists():
                group= request.user.groups.all()[0].name
            if group in allowed_role:
                return view_func(request,*args, **kwargs)
            else:
                return HttpResponse('You are not authorized to this page')
        return wrapper_func
    return decorator

"""difference admin and user"""
def admin_only(view_func):
    def wrapper_func(request,*args, **kwargs):
        group=None
        if request.user.groups.exists():
            group=request.user.groups.all()[0].name

        if group=='admin':
            return view_func(request,*args, **kwargs)
        if group=='customer':
            return redirect('user')  
    return wrapper_func        
    
    