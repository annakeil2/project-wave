from django.test import Client, TestCase
from django.test.client import RequestFactory

from wave_app import views 
from wave_app.models import WaveUser, FACILITATOR

class ViewsTestCase(TestCase):
    def setUp(self):
        self.rf = RequestFactory()
        self.facilitator = WaveUser.objects.create_user(
            username="bobgoulash", 
            email="example@example.com",
            password="verysafepassword1",
            user_type=FACILITATOR
        )
        self.facilitator.id = 1
        
    def test_home_redirect_redirects_to_my_waves_for_facilitators(self):
        request = self.rf.get('')
        
        request.user = self.facilitator
        request.session = {}

        self.assertTrue(request.user.is_authenticated)
        
        response = views.home_redirect(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/wave/my-waves')