#encoding=UTF-8
from django import template
from django.conf import settings
from django.contrib.sites.models import Site

register = template.Library()

@register.simple_tag
def uservoice_client_key():
    return settings.USERVOICE_CLIENT_KEY

@register.simple_tag
def disqus_short_name():
    return settings.DISQUS_SHORT_NAME

@register.simple_tag
def candidate_info_contact_mail():
    return settings.INFO_CONTACT_MAIL

@register.simple_tag
def candidate_info_contact_mail_subject():
    return settings.CANDIDATE_CONTACT_SUBJECT

@register.simple_tag
def ga_account_id():
    return settings.GOOGLE_ANALYTICS_TRACKER_ID

@register.simple_tag
def ga_account_domain():
    return settings.GOOGLE_ANALYTICS_DOMAIN

@register.simple_tag
def url_domain():
    return Site.objects.get_current().domain

@register.simple_tag
def ga_script():
    domain_url = Site.objects.get_current().domain
    expected_script = u"<script type=\"text/javascript\">\n"
    expected_script += u"  var _gaq = _gaq || [];\n"
    counter = 0
    for tracker_id in settings.GOOGLE_ANALYTICS_TRACKER_ID:
        index = ""
        if counter > 0:
            index = chr(counter + 96)+"."
        expected_script += u"  _gaq.push(['"+index+"_setAccount', '"+tracker_id+"']);\n"
        expected_script += u"  _gaq.push(['"+index+"_trackPageview']);\n"
        counter+=1
    expected_script += u"  _gaq.push(['_setDomainName', '"+domain_url+"']);\n"
    expected_script += u"  _gaq.push(['_trackPageview']);\n\n  (function() {\n"
    expected_script += u"    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;\n"
    expected_script += u"    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\n"
    expected_script += u"    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);\n"
    expected_script += u"  })();\n\n</script>"
    return expected_script