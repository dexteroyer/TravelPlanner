from functools import wraps
from flask import abort, flash
from flask_login import current_user
from model import Role

def required_roles(*roles):
   def wrapper(f):
      @wraps(f)
      def wrapped(*args, **kwargs):
         if get_role() not in roles:
            flash('Authentication error, please check your details and try again','error')
            abort(403)
         return f(*args, **kwargs)
      return wrapped
   return wrapper
 
def get_role():
    return current_user.getRole_name()
