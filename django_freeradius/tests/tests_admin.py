import os
from unittest import skipIf

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from ..models import (
    Nas, RadiusAccounting, RadiusCheck, RadiusGroup, RadiusGroupCheck, RadiusGroupReply, RadiusGroupUsers,
    RadiusPostAuth, RadiusReply, RadiusUserGroup,
)


@skipIf(os.environ.get('SAMPLE_APP', False), 'Running tests on SAMPLE_APP')
class TestAdmin(TestCase):
    def test_users_not_login(self):
        resp = self.client.get('/admin/auth/')
        self.assertEqual(resp.status_code, 302)

    def test_users(self):
        self.client.login(username='gino', password='ciao')
        resp = self.client.get('/admin/login/?next=/admin/')
        self.assertEqual(resp.status_code, 200)

    def test_nas_change(self):
        User.objects.create_superuser(username='gino', password='cc', email='giggi_vv@gmail.it')
        obj = Nas.objects.create(name='fiore', short_name='ff', type='cisco',
                                 secret='d', ports='22', community='vmv',
                                 description='ciao', server='jsjs')
        self.client.login(username='gino', password='cc')
        resp = self.client.get(reverse('admin:django_freeradius_nas_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiuscheck_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiuscheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusreply_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                         op=':=', value='passbob')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupreply_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroupReply.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroupreply_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupcheck_change(self):
        User.objects.create_superuser(username='fiorella', password='ciao', email='giggi_fiore@gmail.it')
        obj = RadiusGroupCheck.objects.create(groupname='students', attribute='Cleartext-Password',
                                              op=':=', value='PPP')
        self.client.login(username='fiorella', password='ciao')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroupcheck_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroup_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusGroup.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                         groupname='students', priority='1', notes='hh')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiususergroup_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        obj = RadiusUserGroup.objects.create(username='bob', groupname='students', priority='1')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiususergroup_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusgroupusers_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        reply = RadiusReply.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        check = RadiusCheck.objects.create(username='bob', attribute='Cleartext-Password',
                                           op=':=', value='passbob')
        obj = RadiusGroupUsers.objects.create(id='870df8e8-3107-4487-8316-81e089b8c2cf',
                                              username='bob', groupname='students')
        obj.radius_reply.add(reply)
        obj.radius_check.add(check)
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusgroupusers_change', args=[obj.pk]))
        self.assertContains(resp, 'ok')

    def test_radiusaccounting_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        ola = RadiusAccounting.objects.create(
            unique_id='2', username='bob', nas_ip_address='127.0.0.1', start_time='2017-06-10 10:50:00',
            stop_time='2017-06-10 11:50:00', session_time='5', authentication='RADIUS',
            connection_info_start='f', connection_info_stop='hgh',
            input_octets='1', output_octets='4', update_time='2017-03-10 11:50:00'
        )
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiusaccounting_change', args=[ola.pk]))
        self.assertContains(resp, 'ok')

    def test_postauth_change(self):
        User.objects.create_superuser(username='gino', password='cic', email='giggi_vv@gmail.it')
        olu = RadiusPostAuth.objects.create(username='gino', password='ciao',
                                            reply='ghdhd', date='2017-09-02')
        self.client.login(username='gino', password='cic')
        resp = self.client.get(reverse('admin:django_freeradius_radiuspostauth_change', args=[olu.pk]))
        self.assertContains(resp, 'ok')
