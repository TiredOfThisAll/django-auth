from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.template import loader
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout


from api.models import CustomUser


def main_page(request):
    template = loader.get_template("main.html")
    return HttpResponse(template.render(request=request))

def login_page(request):
    template = loader.get_template("login.html")
    return HttpResponse(template.render(request=request))

@login_required(login_url='/login/')
def user_profile_page(request, id):
    if request.user.id != int(id):
        return(HttpResponseBadRequest("This page is not accessible"))
    user = CustomUser.objects.filter(id=int(id)).first()
    invited_users = CustomUser.objects.filter(invited_by=user.invite_code)
    template = loader.get_template("user_profile.html")
    return HttpResponse(template.render({
        "id": user.id,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "phone_number": user.phone_number,
        "invite_code": user.invite_code,
        "invited_by": user.invited_by,
        "invited_users": invited_users},
        request
    ))

@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/login/")
