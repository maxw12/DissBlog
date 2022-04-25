from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import FormView

from .models import Submission, User, Comment, Course
from .forms import SubmissionForm, CreateUserForm, LoginUser, NewCommentForm


# # Create your views here.
class HomeView(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'blog/home.html'
    login_url = 'login'
    redirect_field_name = 'login'
    ordering = ['-pub_date']

    def get_context_data(self, **kwargs):
        context = super(HomeView, self).get_context_data(**kwargs)
        context['courses'] = Course.objects.all()
        if self.request.GET.get('tag'):
            context['selected_tag'] = int(self.request.GET.get('tag'))
        if self.request.GET.get('query'):
            context['current_query'] = self.request.GET.get('query')
        return context

    def get_queryset(self):
        tag_filter = self.request.GET.get('tag')
        query_filter = self.request.GET.get('query')
        result_sets = None
        if query_filter:
            result_sets = Submission.objects.filter(title__contains=query_filter)
        else:
            result_sets = Submission.objects.all()
        if not tag_filter:
            return result_sets.order_by(*self.ordering)
        context = result_sets.filter(tag=tag_filter).order_by(*self.ordering)
        return context


class MyPostView(LoginRequiredMixin, generic.ListView):
    model = Submission
    template_name = 'blog/my_post.html'
    ordering = ['-pub_date']
    login_url = 'login'
    redirect_field_name = 'login'


class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Submission
    form_class = NewCommentForm
    template_name = 'blog/submission_detail.html'
    login_url = 'login'
    redirect_field_name = 'login'

    def get_context_data(self, *args, **kwargs):
        post = Submission.objects.filter(id=self.kwargs['pk'])[0]
        comments = Comment.objects.filter(post_id=self.kwargs['pk']).order_by("-comment_by__type", "pub_date")
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        likes_total = post.likes_total()
        context = super(DetailView, self).get_context_data()
        context["likes_total"] = likes_total
        context["liked"] = liked
        context["comments"] = comments
        if self.request.GET.get('previous_page'):
            context["previous_page"] = self.request.GET.get('previous_page')
        else:
            context["previous_page"] = self.request.META.get('HTTP_REFERER')
        if not context["previous_page"]:
            context["previous_page"] = reverse_lazy('home')
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = Submission.objects.filter(id=self.kwargs['pk'])[0]
        comment_by = request.user
        content = request.POST['content']
        if not content or content == "":
            context = self.get_context_data(*args, **kwargs)
            return self.render_to_response(context=context)
        comment = Comment.objects.create(comment_by=comment_by, content=content, post=post)
        comment.save()
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_response(context=context)


class AddSubmissionView(LoginRequiredMixin, generic.CreateView):
    model = Submission
    template_name = 'blog/submit.html'
    form_class = SubmissionForm
    login_url = 'login'
    redirect_field_name = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class DeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Submission
    template_name = 'blog/delete_submission.html'
    success_url = reverse_lazy('home')
    login_url = 'login'
    redirect_field_name = 'login'


class RegisterView(generic.CreateView):
    form_class = CreateUserForm
    template_name = 'blog/register.html'
    success_url = reverse_lazy('login')


def Logout(request):
    """logout logged in user"""
    logout(request)
    return HttpResponseRedirect(reverse_lazy('login'))


def LikeView(request, pk):
    post = get_object_or_404(Submission, id=request.POST.get('submission_id'))
    liked = False
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
    return HttpResponseRedirect(reverse('submission-detail', args=[str(pk)])+"?previous_page="+request.GET.get('previous_page'))


class LoginView(FormView):
    form_class = LoginUser
    template_name = 'blog/login.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        """ process user login"""
        credentials = form.cleaned_data

        user = authenticate(username=credentials['username'],
                            password=credentials['password'])

        if user is not None:
            login(self.request, user)
            return HttpResponseRedirect(self.success_url)

        else:
            messages.add_message(self.request, messages.INFO, 'Wrong credentials\
                                please try again')
            return HttpResponseRedirect(reverse_lazy('login'))


def CategoryView(request, cat):
    return render(request, 'categories.html')


def search(request):
    if request.method == 'POST':
        query = request.GET.get('query', '')

        if len(query) > 0:
            posts = Submission.objects.filter(title__contains=query)
            topics = Course.objects.filter(title__contains=query)
        else:
            posts = []
            topics = []

        context = {
            'query': query,
            'posts': posts,
            'topics': topics,
            'title': 'Search',
        }
        return render(request, 'blog/search.html', context)

