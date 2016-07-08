from teams.views import get_member_type

def member_type(request):
    try:
        if not request.user.is_superuser:
            return {'user_type':get_member_type(request.user)}
    except:
        pass
    return {}
#------------------------------------------------------------------------------#
