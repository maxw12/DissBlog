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
        return context

    def get_queryset(self):
        tag_filter = self.request.GET.get('tag')
        if not tag_filter:
            return Submission.objects.all().order_by(*self.ordering)
        context = Submission.objects.filter(tag=tag_filter).order_by(*self.ordering)
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
        comments = Comment.objects.filter(post_id=self.kwargs['pk'])
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        likes_total = post.likes_total()
        context = super(DetailView, self).get_context_data()
        context["likes_total"] = likes_total
        context["liked"] = liked
        context["comments"] = comments
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        post = Submission.objects.filter(id=self.kwargs['pk'])[0]
        comment_by = request.user
        content = request.POST['content']
        comment = Comment.objects.create(comment_by=comment_by, content=content, post=post)
        comment.save()
        context = self.get_context_data(*args, **kwargs)
        return self.render_to_response(context=context)


        # post = get_object_or_404(Submission, pk=pk)  # request.POST.get('submission_id')
        #
        # comments = post.comments.filter(status=True)
        # user_comment = None
        # if request.method == 'POST':
        #     comment_form = NewCommentForm(request.POST)
        #     if comment_form.is_valid():
        #         user_comment = comment_form.save(commit=False)
        #         user_comment.post = post
        #         user_comment.save()
        #         return HttpResponseRedirect('/' + post.pk)
        # else:
        #     comment_form = NewCommentForm()
        # return render(request, 'blog/submission_detail.html',
        #               {'post': post, 'comment': user_comment, 'comments': comments, 'comment_form': comment_form})
    #     comment = request.POST['comment']
    #     comments = Comment.objects.create(
    #         content=comment,
    #         commented_on=post,
    #         commented_by=request.user
    #     )
    #     return HttpResponseRedirect('submission-detail', pk=post.pk)
    #
    # return render(request, 'blog/submission_detail.html', {'comments': comments})


class AddSubmissionView(LoginRequiredMixin, generic.CreateView):
    model = Submission
    template_name = 'blog/submit.html'
    form_class = SubmissionForm
    login_url = 'login'
    redirect_field_name = 'login'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

# def upload_file(request):
#     if request.POST:
#         form = SubmissionForm(request.POST, request.FILES)
#         print(request.POST['file'])
#         if form.is_valid()
#             form.save()
#             return HttpResponseRedirect()

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
    return HttpResponseRedirect(reverse('submission-detail', args=[str(pk)]))


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
