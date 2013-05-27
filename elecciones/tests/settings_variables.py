from django.test import TestCase
from django.template import Template, Context
from django.conf import settings
from django.contrib.sites.models import Site

class SettingsVariablesInTemplate(TestCase):
    def setUp(self):
        pass

    def test_it_provides_uservoice_template_tag(self):
        settings.USERVOICE_CLIENT_KEY = "USERVOICE KEY"
        template = Template('{% load settingsvars_tags %}{% uservoice_client_key %}')
        self.assertEqual(template.render(Context({})), "USERVOICE KEY")

    def test_it_provides_google_analytics_template_tag(self):
        settings.GOOGLE_ANALYTICS_TRACKER_ID = "GOOGLE ANALYTICS ACCOUNT ID"
        settings.GOOGLE_ANALYTICS_DOMAIN = "testdomain.com"
        template = Template('{% load settingsvars_tags %}{% ga_account_id %} - {% ga_account_domain %}')
        self.assertEqual(template.render(Context({})), "GOOGLE ANALYTICS ACCOUNT ID - testdomain.com")



    def test_it_provides_several_google_analytics_temlate_tags(self):
        settings.GOOGLE_ANALYTICS_TRACKER_ID = ['UA-10694322-1','UA-77777' ]
        domain_url = Site.objects.get_current().domain
        expected_script = u"<script type=\"text/javascript\">\n"
        expected_script += u"  var _gaq = _gaq || [];\n"
        expected_script += u"  _gaq.push(['_setAccount', 'UA-10694322-1']);\n"
        expected_script += u"  _gaq.push(['_trackPageview']);\n"
        expected_script += u"  _gaq.push(['a._setAccount', 'UA-77777']);\n"
        expected_script += u"  _gaq.push(['a._trackPageview']);\n"
        expected_script += u"  _gaq.push(['_setDomainName', '"+domain_url+"']);\n"
        expected_script += u"  _gaq.push(['_trackPageview']);\n\n  (function() {\n"
        expected_script += u"    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;\n"
        expected_script += u"    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';\n"
        expected_script += u"    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);\n"
        expected_script += u"  })();\n\n</script>"
        template = Template('{% load settingsvars_tags %}{% ga_script %}')
        self.assertEqual(template.render(Context({})), expected_script)

    def test_it_provides_disqus_short_name_template_tag(self):
        settings.DISQUS_SHORT_NAME = "DISQUS_SHORT_NAME"
        template = Template('{% load settingsvars_tags %}{% disqus_short_name %}')
        self.assertEqual(template.render(Context({})), "DISQUS_SHORT_NAME")

    def test_it_provides_mail_subject_template_tag(self):
        settings.CANDIDATE_CONTACT_SUBJECT = "Mail Subject"
        template = Template('{% load settingsvars_tags %}{% candidate_info_contact_mail_subject %}')
        self.assertEqual(template.render(Context({})), "Mail Subject")

    def test_it_provides_mail_address_template_tag(self):
        settings.INFO_CONTACT_MAIL = "candidatos@mail.com"
        template = Template('{% load settingsvars_tags %}{% candidate_info_contact_mail %}')
        self.assertEqual(template.render(Context({})), "candidatos@mail.com")




