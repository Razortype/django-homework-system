from django.test import SimpleTestCase
from django.urls import reverse, resolve
from posts import views

class TestUrls(SimpleTestCase):

    def test_url_homework_list_is_resolved(self):
        url = reverse('hw_list')
        self.assertEquals(resolve(url).func.view_class, views.HomeworkList)

    def test_url_homework_list_by_type_is_resolved(self):
        url = reverse('hw_list_by_category', kwargs={'category':'type'})
        self.assertEquals(resolve(url).func.view_class, views.HomeworkListByType)

    def test_url_homework_detail_is_resolved(self):
        url = reverse('hw_detail_by_id', kwargs={'_id':1})
        self.assertEquals(resolve(url).func.view_class, views.HomeworkDetailById)

    def test_url_homework_post_new_is_resolved(self):
        url = reverse('post_new', kwargs={'_id':1})
        self.assertEquals(resolve(url).func.view_class, views.HomeworkPostNew)
    
    def test_url_homework_post_update_is_resolved(self):
        url = reverse('post_update', kwargs={'homework_id':1, 'post_id':1})
        self.assertEquals(resolve(url).func.view_class, views.HomeworkPostUpdate)
    
    def test_url_homework_post_delete_is_resolved(self):
        url = reverse('post_delete', kwargs={'homework_id':1, 'post_id':1})
        self.assertEquals(resolve(url).func.view_class, views.HomeworkPostDelete)