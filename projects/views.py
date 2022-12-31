from multiprocessing import context
from winreg import DeleteValue
from django.shortcuts import render, redirect
from django.contrib import messages
from accounts.models import *
from donations.models import *
from daanbaksho import settings
from django.contrib.auth.models import Group
from django.contrib.auth.models import User
from .models import *
from django.views.generic import ListView, DetailView, UpdateView, CreateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.db.models import Sum

# Create your views here.

# Post
class ProjectListView(ListView):
    model = project
    context_object_name = 'd_projects'


class ProjectDetailView(DetailView):
    model = project



class ProjectCreateView(LoginRequiredMixin, CreateView):
    model = project
    fields = ['title', 'short_desc', 'content','image']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)




class ProjectUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = project
    fields = ['title', 'short_desc', 'content','image']

    def form_valid(self, form):
        form.instance.post_user = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False


class ProjectDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = project
    success_url = '/projects/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.post_user:
            return True
        return False



def ProjectDonation(request, pk):
    d_project = project.objects.get(id=pk)

    print("Reached", d_project)

    context = {
        'project': d_project,
    }

    if request.method == 'POST':
        d_amount = request.POST.get('d_amount')
        d_method = request.POST.get('d_method')
        d_phone = request.POST.get('d_phone')
        d_txid = request.POST.get('d_txid')

        d_donor = request.user

        donation = projectDonation.objects.create(
            donor=d_donor, project=d_project, amount=d_amount, p_method=d_method, phone=d_phone, txid=d_txid)


        subject = "Project Donation Requsted - Daanbaksho"
        message = "Hello " + d_donor.first_name + "!! \n" + \
            "We have received your request for project donation. We will get back to you soon.\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [d_donor.email]
        send_mail(subject, message, from_email,
                  to_list, fail_silently=True)

        messages.success(
            request, "Your Donation Was Succesfully Submitted for Verification")

        return redirect('donorFoodDonationHistory')

    return render(request, 'projects/project_donation.html', context)




# Project Coordinator
def viewProjectDonations(request):
    projects = project.objects.all()
    total = project.objects.annotate(total_amount=Sum('projectDonation_set__amount'))
    context = {
        'projects': projects,
        'total': total
    }

    print(projects)
    print(total)
    # total= []
    # i = 0

    # for project in projects:
    #     total[i] = project.projectDonation.aggregate(Sum('amount'))

    return render(request, 'projects/view_project_donations.html', context)