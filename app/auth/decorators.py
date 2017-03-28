from functools import wraps
from flask import abort, flash
from flask_login import current_user

def required_roles(*roles):
   def wrapper(f):
      @wraps(f)
      def wrapped(*args, **kwargs):
         if get_current_user_role() not in roles:
            flash('Authentication error, please check your details and try again','error')
            abort(403)
         return f(*args, **kwargs)
      return wrapped
   return wrapper
 
def get_current_user_role():
    r_id = current_user.getRole_id()
    roles = ['Admin', 'Moderator', 'User']
    for i in range(1,4):
	    if r_id==i:
	        return roles[i-1]