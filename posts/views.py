from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views import View

from users.models import Person
from .models import Category, Homework, HomeworkDetail, Post

from .forms import PostForm

from .utils import get_timestamp, seperate_homeworks, left_started_homeworks, check_post_404, valid_checker

from django.contrib import messages
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth.mixins import LoginRequiredMixin

## Homework Views

class HomeworkList(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, *args, **kwargs):
        user = req.user

        enabled_homeworks, disabled_homeworks = seperate_homeworks(Homework.objects.all())

        content = {
            'title': 'WEB | Ödevler',
            'categories': [i for i in Category.objects.all() if i.get_hw_amount() > 0],
            'homeworks': left_started_homeworks(enabled_homeworks) + left_started_homeworks(disabled_homeworks),
            'style_file': 'posts/css/homework_list.css',
            'js_files': [
                'partials/js/_navbar.js',
                'posts/js/homework_list.js',
            ]
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'posts/homework_list.html', content))

class HomeworkListByType(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    def get(self, req, category, *args, **kwargs):
        user = req.user

        if not Category.objects.filter(name=category).exists():
            messages.error(req, f"Uygun kategori bulunamadı: {category}")
            return HttpResponseRedirect("/homeworks")

        enabled_homeworks, disabled_homeworks = seperate_homeworks(Homework.objects.filter(category__name = category))

        content = {
            'title': f'WEB | Ödevler - {category}',
            'categories': [i for i in Category.objects.all() if i.get_hw_amount() > 0],
            'homeworks': left_started_homeworks(enabled_homeworks) + left_started_homeworks(disabled_homeworks),
            'style_file': 'posts/css/homework_list.css',
            'js_files': [
                'partials/js/_navbar.js',
                'posts/js/homework_list.js',
            ]
        }

        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)

        return HttpResponse(render(req, 'posts/homework_list.html', content))

class HomeworkDetailById(LoginRequiredMixin, View):

    login_url = "login"
    redirect_field_name = "next"

    post_form = PostForm

    def get(self, req, _id, *args, **kwargs):
        user = req.user
        homework = Homework.objects.get(pk=_id)

        content = {
            'title': f'WEB | Ödevler - {homework.name}',
            'homework' : homework,
            'details': HomeworkDetail.objects.filter(homework__id = homework.id),
            'posts': sorted(Post.objects.filter(homework__id = homework.id), key=lambda person: get_timestamp(person.post_at)),
            'form': self.post_form(),
            'personpost': None,
            'style_file': 'posts/css/homework_detail.css',
            'js_files': [
                'partials/js/_navbar.js',
                'posts/js/homework_detail.js'
            ]
        }
        
        if not isinstance(user, AnonymousUser):
            content['person'] = Person.objects.get(pk=user.id)
            if content['person'] in [i.person for i in content["posts"]]:
                content['personpost'] = Post.objects.get(person = content['person'], homework=content['homework'])

        return HttpResponse(render(req, 'posts/homework_detail.html', content))

class HomeworkPostNew(View):

    post_form = PostForm

    def post(self, req, _id, *args, **kwargs):

        user = req.user
        person = Person.objects.get(pk=user.pk)

        try:
            homework = Homework.objects.get(pk=_id) 
        except Exception:
            homework = None

        if homework is None:
            messages.warning(req, "Uygun ödev bulunamamıştır")
            return HttpResponseRedirect('/homeworks')

        homework_page_url = f'/homeworks/id/{homework.pk}/detail'

        post_form = self.post_form(req.POST)
        if not post_form.is_valid():
            messages.warning(req, "Uygun veriler gönderilmedi")
            return HttpResponseRedirect(homework_page_url+"#post__area")

        errors = valid_checker.check_post_valid(post_form.cleaned_data['github_url'], person.github_url)

        if errors:
            for error in errors:
                messages.warning(req, error)
            return HttpResponseRedirect(homework_page_url+"#post__area")

        post = Post.objects.create(person=person, homework=homework, post_url=post_form.cleaned_data['github_url'])
        post.post_404 = check_post_404(post.post_url)
        post.save()
        messages.success(req, "Post başarıyla atıldı")
        return HttpResponseRedirect(homework_page_url+"#post__table")

class HomeworkPostUpdate(View):

    update_post = PostForm

    def post(self, req, homework_id, post_id, *args, **kwargs):

        person = req.user.person
        update_form = self.update_post(req.POST)
        return_url = f'/homeworks/id/{homework_id}/detail#post__area'

        try:
            post = Post.objects.get(pk=post_id)
        except Exception:
            post = None

        if post is None:
            messages.warning(req, "Aranılan post bulunamadı")
            return HttpResponseRedirect(return_url)

        if post.person != person:
            messages.warning(req, "Postu atan kişi siz olmak zorundasınız")
            return HttpResponseRedirect(return_url)

        if not update_form.is_valid():
            messages.warning(req, "Girilen veriler geçerli değildir")
            return HttpResponseRedirect(return_url)

        errors = valid_checker.check_post_valid(update_form.cleaned_data['github_url'], person.github_url)

        if errors:
            for error in errors:
                messages.warning(req, error)
            return HttpResponseRedirect(return_url)

        post.post_url = update_form.cleaned_data['github_url']
        post.post_404 = check_post_404(post.post_url)
        post.save()
        messages.success(req, 'Post başarıyla değiştirildi')
        return HttpResponseRedirect(return_url)

class HomeworkPostDelete(View):

    def get(self, req, homework_id, post_id, *args, **kwargs):

        return_url = f'/homeworks/id/{homework_id}/detail#post__area'
        try:
            post = Post.objects.get(pk=post_id)
        except Exception:
            post = None

        if post is None:
            messages.warning(req, "Aranılan post bulunamadı")
            return HttpResponseRedirect(return_url)

        if post.person != req.user.person:
            messages.warning(req, "Postu atan kişi siz olmak zorundasınız")
            return HttpResponseRedirect(return_url)

        post.delete()
        messages.success(req, "Post başarıyla silindi")
        return HttpResponseRedirect(return_url)