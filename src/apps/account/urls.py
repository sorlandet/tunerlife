from django.conf.urls import patterns, url
from django.contrib.auth.views import logout
from django.views.generic import TemplateView

from ajax_validation.views import validate
from emailconfirmation.views import confirm_email

from src.apps.account.forms import SignupForm


urlpatterns = patterns("src.apps.account.views",
    url(r"^email/$", "email", name="acct_email"),
    
    url(r"^signup/$", "signup", name="acct_signup"),
    
    url(r"^login/$", "login", name="acct_login"),
    url(r"^login/openid/$", "login", {"associate_openid": True}, name="acct_login_openid"),
    
    url(r"^password_change/$", "password_change", name="acct_passwd"),
    url(r"^password_set/$", "password_set", name="acct_passwd_set"),
    url(r"^password_delete/$", "password_delete", name="acct_passwd_delete"),
    url(r"^password_delete/done/$",
        TemplateView.as_view(template_name="account/password_delete_done.html"),
        name="acct_passwd_delete_done"),
    
    url(r"^timezone/$", "timezone_change", name="acct_timezone_change"),
    
    url(r"^other_services/$", "other_services", name="acct_other_services"),
    url(r"^other_services/remove/$", "other_services_remove", name="acct_other_services_remove"),
    
    url(r"^language/$", "language_change", name="acct_language_change"),
    url(r"^logout/$", logout, {"template_name": "account/logout.html"}, name="acct_logout"),
    
    url(r"^confirm_email/(\w+)/$", confirm_email, name="acct_confirm_email"),
    
    # password reset
    url(r"^password_reset/$", "password_reset", name="acct_passwd_reset"),
    url(r"^password_reset/done/$", "password_reset_done", name="acct_passwd_reset_done"),
    url(r"^password_reset_key/(?P<uidb36>[0-9A-Za-z]+)-(?P<key>.+)/$", "password_reset_from_key", name="acct_passwd_reset_key"),
    
    # ajax validation
    (r"^validate/$", validate, {"form_class": SignupForm}, "signup_form_validate"),
)
