from allauth.account.adapter import DefaultAccountAdapter
from django.contrib.auth import get_user_model

User = get_user_model()


class CustomAccountAdapter(DefaultAccountAdapter):
    """
    Custom adapter for allauth to handle phone-based authentication
    """
    
    def save_user(self, request, user, form, commit=True):
        """
        Save a new user instance using information provided in the signup form.
        """
        from allauth.account.utils import user_field
        
        data = form.cleaned_data
        phone_number = data.get('phone_number')
        full_name = data.get('full_name')
        email = data.get('email')
        role = data.get('role')
        
        user_field(user, 'phone_number', phone_number)
        user_field(user, 'full_name', full_name)
        
        if email:
            user_field(user, 'email', email)
        
        if role:
            user_field(user, 'role', role)
        
        if 'password1' in data:
            user.set_password(data['password1'])
        
        if commit:
            user.save()
        
        return user