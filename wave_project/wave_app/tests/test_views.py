import datetime as dt

from django.test import TestCase
from django.test.client import RequestFactory

from wave_app import views 
from wave_app.models import Wave, WaveUser, FACILITATOR, PARTICIPANT, BOTTLE_EXCHANGE, AI_MODERATION

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
        
        self.participant = WaveUser.objects.create_user(
            username="jane", 
            email="example2@example.com",
            password="verysafepassword2",
            user_type=PARTICIPANT
        )
        self.participant.id = 2
        self.participant.wave_id = 100

        
    def test_home_redirect_redirects_to_my_waves_for_facilitators(self):
        request = self.rf.get('')
        
        request.user = self.facilitator
        request.session = {}

        self.assertTrue(request.user.is_authenticated)
        
        response = views.home_redirect(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/wave/my-waves')
        
        
    def test_home_redirect_redirects_to_the_wave_of_a_participant(self):
        request = self.rf.get('')
        
        request.user = self.participant
        request.session = {}

        self.assertTrue(request.user.is_authenticated)
        
        response = views.home_redirect(request)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/wave/100/')
        
        
    def test_create_wave_creates_wave_and_redirects(self):
        expected_wave_name = 'Test'
        expected_event_date = '2026-10-21 19:28:00.000000 +00:00'
        expected_input_type = BOTTLE_EXCHANGE
        expected_moderation_type = AI_MODERATION
        
        request = self.rf.post('wave/create_wave/', data={
            'wave_name': expected_wave_name,
            'event_date': expected_event_date,
            'input_type': expected_input_type,
            'moderation_type': expected_moderation_type,
        })
        
        """ Logged in as facilitator """
        request.user = self.facilitator
        request.session = {}

        self.assertTrue(request.user.is_authenticated)
        
        count_before = Wave.objects.all().count()
        
        response = views.create_wave(request)
        print(response)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/wave/my-waves')
        
        count_after = Wave.objects.all().count()
        self.assertEqual(count_before + 1, count_after)
        
        latest_wave = Wave.objects.all().order_by('created_at').first()
        self.assertGreater(latest_wave.id, 0)
        self.assertEqual(latest_wave.wave_name, expected_wave_name)
        self.assertEqual(latest_wave.event_date, dt.strptime(expected_event_date, "%Y-%m-%d %H:%M:%S.%f %:z"))
        self.assertEqual(latest_wave.input_type, expected_input_type)
        self.assertEqual(latest_wave.moderation_type, expected_moderation_type)