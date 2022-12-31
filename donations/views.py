from operator import inv
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView
from .models import *
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.decorators import login_required
from . decorators import *
from django.utils.decorators import method_decorator
from django.contrib import messages
from django.core.mail import send_mail
from daanbaksho import settings
from . forms import *
from accounts.models import *
from projects.models import *


# Create your views here.
decorators = [login_required, donor_only]


@login_required
@donor_only
def donate(request):
    return render(request, 'donations/donate.html')


@method_decorator(decorators, name='dispatch')
class donateMoney(SuccessMessageMixin, CreateView):
    model = money_donation
    fields = ['amount', 'p_method', 'phone', 'txid']
    success_url = reverse_lazy("home")
    success_message = "Your Donation Was Succesfully Submitted for Verification"

    def form_valid(self, form):
        form.instance.donor = self.request.user
        return super().form_valid(form)


# some is in abandoned


# Projects


# def projects(request):
#     return render(request, 'projects.html')


# food donation
def donateFood(request):
    if request.method == 'POST':
        dquantity = request.POST.get('fquantity')
        desc = request.POST.get('desc')
        donorID = request.POST.get('d_user')

        donor = User.objects.get(id=donorID)

        donation = food_donation.objects.create(
            quantity=dquantity, description=desc)

        donation.d_user.add(donor)

        subject = "Food Donation Requsted - Daanbaksho"
        message = "Hello " + donor.first_name + "!! \n" + \
            "We have received your request for food donation. We will get back to you soon.\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [donor.email]
        send_mail(subject, message, from_email,
                  to_list, fail_silently=True)

        messages.success(
            request, "Your Donation Was Succesfully Submitted for Verification")

        return redirect('donorFoodDonationHistory')

    return render(request, 'donations/food_donation_form.html')


# cloth donation
def donateCloth(request):
    if request.method == 'POST':
        dquantity = request.POST.get('fquantity')
        desc = request.POST.get('desc')
        donorID = request.POST.get('d_user')

        donor = User.objects.get(id=donorID)

        donation = cloth_donation.objects.create(
            total_items=dquantity, items_description=desc)

        donation.d_user.add(donor)

        subject = "Cloth Donation Requsted - Daanbaksho"
        message = "Hello " + donor.first_name + "!! \n" + \
            "We have received your request for cloth donation. We will get back to you soon.\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [donor.email]
        send_mail(subject, message, from_email,
                  to_list, fail_silently=True)

        messages.success(
            request, "Your Donation Was Succesfully Submitted for Verification")

        return redirect('donorClothDonationHistory')

    return render(request, 'donations/cloth_donation_form.html')


# donor donation history ------------------------------------------------
# donor money donation history
def donorMoneyDonationHistory(request):
    donorUser = request.user

    moneyDonationList = money_donation.objects.filter(donor=donorUser)

    context = {
        'moneyDonations': moneyDonationList,
    }

    return render(request, 'donations/donor_money_donation_history.html', context)


# Donor food donation history
def donorFoodDonationHistory(request):
    donorUser = request.user

    foodDonationList = food_donation.objects.filter(d_user=donorUser)

    context = {
        'foodDonations': foodDonationList,
    }

    return render(request, 'donations/donor_food_donation_history.html', context)


# donor cloth donation history

def donorClothDonationHistory(request):
    donorUser = request.user

    clothDonationList = cloth_donation.objects.filter(d_user=donorUser)

    context = {
        'clothDonations': clothDonationList,
    }

    return render(request, 'donations/donor_cloth_donation_history.html', context)

# end of donor history --------------------------------------------------------

# volunteer assignment


def volunteerFoodDonationAssignment(request):
    foodDonationList = food_donation.objects.all()

    context = {
        'foodDonations': foodDonationList,

    }

    if request.method == 'POST':

        mydonation = food_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        donorUser = mydonation.d_user.all()
        donor = User.objects.get(username=donorUser[0])

        volunteerUser = request.user

        if request.POST.get("status") == 'Accept':

            mydonation.status = 'About to Be Picked'
            mydonation.save()
            mydonation.d_user.add(volunteerUser)

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Food Donation Will Be Picked ASAP - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, We are happy to inform you that your food donation was succesfully assigned to a volunteer. The volunteer will be contacting you very soon.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nVolunteer Name: " + \
                volunteerUser.first_name+"\nVolunteer Phone: " + \
                volunteerUser.profile.phone+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Food Donation Assigned to Pick Up - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have assigned to pick up a food donation. Please contact with the donor and collect the donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nDonor Name: "+donor.first_name + \
                "\nDonor Phone: "+donor.profile.phone+"\nDonor Address: " + \
                donor.profile.address+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Food Donation Has Been Assigned to You")

            return redirect('volunteer_food_donation_assignment')

    return render(request, 'donations/volunteer_food_donation_acceptence.html', context)


# Volunteer Cloth Donation Assignment

def volunteerClothDonationAssignment(request):
    clothDonationList = cloth_donation.objects.all()

    context = {
        'clothDonations': clothDonationList,
    }

    if request.method == 'POST':

        mydonation = cloth_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        donorUser = mydonation.d_user.all()
        donor = User.objects.get(username=donorUser[0])

        volunteerUser = request.user

        if request.POST.get("status") == 'Accept':

            mydonation.status = 'About to Be Picked'
            mydonation.save()
            mydonation.d_user.add(volunteerUser)

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Cloth Donation Will Be Picked ASAP - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, We are happy to inform you that your cloth donation was succesfully assigned to a volunteer. The volunteer will be contacting you very soon.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nVolunteer Name: " + \
                volunteerUser.first_name + "\nVolunteer Phone: " + \
                volunteerUser.profile.phone + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Cloth Donation Assigned to Pick Up - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have assigned to pick up a cloth donation. Please contact with the donor and collect the donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nDonor Name: " + donor.first_name + \
                "\nDonor Phone: " + donor.profile.phone + "\nDonor Address: " + \
                donor.profile.address + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(
                request, "Cloth Donation Has Been Assigned to You")

            return redirect('volunteer_cloth_donation_assignment')

    return render(request, 'donations/volunteer_cloth_donation_acceptence.html', context)


# Volunteer Donation Pick Up history-----------------------------------------------
# volunteerFoodDonationPickUpHistory
def volunteerFoodDonationPickUpHistory(request):
    volunteer = request.user

    foodDonationList = food_donation.objects.filter(d_user=volunteer)

    context = {
        'foodDonations': foodDonationList,
    }

    return render(request, 'donations/volunteer_food_donation_history.html', context)


# volunteerClothDonationPickUpHistory
def volunteerClothDonationPickUpHistory(request):
    volunteer = request.user

    clothDonationList = cloth_donation.objects.filter(d_user=volunteer)

    context = {
        'clothDonations': clothDonationList,
    }

    return render(request, 'donations/volunteer_cloth_donation_history.html', context)

# --------------------------------------------------------------------------------------------


# Volunteer Food Donation Pick Up Confirmation

def volunteerFoodDonationPickUpConfirmation(request):
    volunteerUser = request.user
    foodDonationList = food_donation.objects.filter(d_user=volunteerUser)

    context = {
        'foodDonations': foodDonationList,

    }

    if request.method == 'POST':
        # volunteerUser = request.user

        mydonation = food_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        donorUser = mydonation.d_user.all()
        donor = User.objects.get(username=donorUser[1])

        if request.POST.get("status") == 'Picked':

            mydonation.status = 'Picked'
            mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Food Donation Has Been Picked Up - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our volunteer has picked up your food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nVolunteer Name: " + \
                volunteerUser.first_name+"\nVolunteer Phone: " + \
                volunteerUser.profile.phone+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Food Donation Picked Up - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have picked up a food donation. Please deliver the donation to our warehouse.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nDonor Name: "+donor.first_name + \
                "\nDonor Phone: "+donor.profile.phone+"\nDonor Address: " + \
                donor.profile.address+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Food Donation Has Been Picked Up")

            return redirect('volunteer_food_donation_assignment')

    return render(request, 'donations/volunteer_food_donation_pickup.html', context)


# Volunteer Cloth Donation Pick Up Confirmation

def volunteerClothDonationPickUpConfirmation(request):
    volunteerUser = request.user
    clothDonationList = cloth_donation.objects.filter(d_user=volunteerUser)

    context = {
        'clothDonations': clothDonationList,
    }

    if request.method == 'POST':

        mydonation = cloth_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        donorUser = mydonation.d_user.all()
        donor = User.objects.get(username=donorUser[1])

        # volunteerUser = request.user

        if request.POST.get("status") == 'Picked':

            mydonation.status = 'Picked'
            mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Cloth Donation Has Been Picked Up - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our volunteer has picked up your donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nVolunteer Name: " + \
                volunteerUser.first_name + "\nVolunteer Phone: " + \
                volunteerUser.profile.phone + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Cloth Donation Assigned to Pick Up - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have picked up a food donation. Please deliver the donation to our warehouse.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nDonor Name: " + donor.first_name + \
                "\nDonor Phone: " + donor.profile.phone + "\nDonor Address: " + \
                donor.profile.address + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(
                request, "Cloth Donation Has Been Picked Up")

            return redirect('volunteer_cloth_donation_assignment')

    return render(request, 'donations/volunteer_cloth_donation_pickup.html', context)


# ----------------------------------------------------------------------------------

# Volunteer Donation Delivered

# Volunteer Food Donation Delivery Confirmation

def volunteerFoodDonationDeliveryConfirmation(request):
    volunteerUser = request.user
    foodDonationList = food_donation.objects.filter(d_user=volunteerUser)

    context = {
        'foodDonations': foodDonationList,

    }

    if request.method == 'POST':
        # volunteerUser = request.user

        mydonation = food_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        donorUser = mydonation.d_user.all()
        donor = User.objects.get(username=donorUser[1])

        if request.POST.get("status") == 'Delivered':

            mydonation.status = 'Delivered'
            mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Food Donation Has Been Picked Up - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our volunteer has delivered your food donation to our distribution team.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nVolunteer Name: " + \
                volunteerUser.first_name+"\nVolunteer Phone: " + \
                volunteerUser.profile.phone+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Food Donation Picked Up - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have delivered a food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nDonor Name: "+donor.first_name + \
                "\nDonor Phone: "+donor.profile.phone+"\nDonor Address: " + \
                donor.profile.address+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Food Donation Has Been Delivered")

            return redirect('volunteer_food_donation_assignment')

    return render(request, 'donations/volunteer_food_donation_delivery.html', context)


# Volunteer Cloth Donation Delivery Confirmation

def volunteerClothDonationDeliveryConfirmation(request):
    volunteerUser = request.user
    clothDonationList = cloth_donation.objects.filter(d_user=volunteerUser)

    context = {
        'clothDonations': clothDonationList,
    }

    if request.method == 'POST':

        mydonation = cloth_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        donorUser = mydonation.d_user.all()
        donor = User.objects.get(username=donorUser[1])

        # volunteerUser = request.user

        if request.POST.get("status") == 'Delivered':

            mydonation.status = 'Delivered'
            mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Cloth Donation Delivered to Distribution Team - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our volunteer has delivered your cloth donation to our distribution team.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nVolunteer Name: " + \
                volunteerUser.first_name + "\nVolunteer Phone: " + \
                volunteerUser.profile.phone + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Cloth Donation Delivered to Distribution Team - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have delivered a food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nDonor Name: " + donor.first_name + \
                "\nDonor Phone: " + donor.profile.phone + "\nDonor Address: " + \
                donor.profile.address + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(
                request, "Cloth Donation Has Been Delivered")

            return redirect('volunteer_cloth_donation_assignment')

    return render(request, 'donations/volunteer_cloth_donation_delivery.html', context)


# Donation Coordinator-----------------------------------
# ----------------------------------------------------------------------------------

# Donation Coordinator Donation Delivered

# Donation Coordinator Food Donation Delivery Confirmation

def donCoFoodDonationReceivedConfirmation(request):
    # volunteerUser = request.user
    foodDonationList = food_donation.objects.all()

    context = {
        'foodDonations': foodDonationList,

    }

    if request.method == 'POST':
        # volunteerUser = request.user

        mydonation = food_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        users = mydonation.d_user.all()
        volunteerUser = User.objects.get(username=users[0])
        donor = User.objects.get(username=users[1])

        if request.POST.get("status") == 'Decline':

            mydonation.status = 'Declined'
            mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Food Donation Has Been Declined - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our distribution team has Declined your donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nVolunteer Name: " + \
                volunteerUser.first_name+"\nVolunteer Phone: " + \
                volunteerUser.profile.phone+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Food Donation Received - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have delivered a food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nDonor Name: "+donor.first_name + \
                "\nDonor Phone: "+donor.profile.phone+"\nDonor Address: " + \
                donor.profile.address+"\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Food Donation Has Been Declined")

            return redirect('volunteer_food_donation_assignment')

    return render(request, 'donations/donco_food_donation_received.html', context)


# Volunteer Cloth Donation Delivery Confirmation

def donCoClothDonationReceivedConfirmation(request):
    # volunteerUser = request.user
    clothDonationList = cloth_donation.objects.all()

    context = {
        'clothDonations': clothDonationList,
    }

    if request.method == 'POST':

        mydonation = cloth_donation.objects.get(
            id=request.POST.get("donation_id"))

        # donorUserID = mydonation.d_user.id
        users = mydonation.d_user.all()
        volunteerUser = User.objects.get(username=users[0])
        donor = User.objects.get(username=users[1])

        # volunteerUser = request.user

        if request.POST.get("status") == 'Decline':

            mydonation.status = 'Declined'
            mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
            subject = "Cloth Donation Declined - Daanbaksho"
            message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our volunteer has declined your cloth donation to our distribution team.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nVolunteer Name: " + \
                volunteerUser.first_name + "\nVolunteer Phone: " + \
                volunteerUser.profile.phone + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donor.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
            subject = "Cloth Donation Declined to Distribution Team - Daanbaksho"
            message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have declined a food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nDonor Name: " + donor.first_name + \
                "\nDonor Phone: " + donor.profile.phone + "\nDonor Address: " + \
                donor.profile.address + "\n\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [volunteerUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(
                request, "Cloth Donation Has Been declined")

            return redirect('donco_cloth_donation_received')

    return render(request, 'donations/donco_cloth_donation_received.html', context)


# Money Donation Verification
def moneyDonationVerification(request):
    donationList = money_donation.objects.all()

    context = {
        'donations': donationList
    }

    if request.method == 'POST':

        mydonation = money_donation.objects.get(
            id=request.POST.get("donation_id"))

        donorUser = mydonation.donor

        if request.POST.get("status") == 'Verify':

            mydonation.status = 'Received'
            mydonation.save()

            # print('Reaches 1')

            subject = "Money Donation Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are happy to inform you that your money donation was succesfully verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Money Donation Verified")

            return render('money_donation_verification')

        elif request.POST.get("status") == 'Decline':

            mydonation.status = 'Declined'
            mydonation.save()
            # print('Reaches 2')

            subject = "Money Donation Could Not Be Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are sorry to inform you that your money donation could not be verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.warning(request, "Money Donation Declined")

            return render('money_donation_verification')

    return render(request, 'donations/money_donation_verification.html', context)


# Project Donation Verification
def projectDonationVerification(request):
    donationList = projectDonation.objects.all()

    context = {
        'donations': donationList
    }

    if request.method == 'POST':

        mydonation = projectDonation.objects.get(
            id=request.POST.get("donation_id"))

        donorUser = mydonation.donor

        if request.POST.get("status") == 'Verify':

            mydonation.status = 'Received'
            mydonation.save()

            # print('Reaches 1')

            subject = "Money Donation Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are happy to inform you that your money donation was succesfully verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Money Donation Verified")

            return render('money_donation_verification')

        elif request.POST.get("status") == 'Decline':

            mydonation.status = 'Declined'
            mydonation.save()
            # print('Reaches 2')

            subject = "Money Donation Could Not Be Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are sorry to inform you that your money donation could not be verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.warning(request, "Project Donation Declined")

            return render('project_donation_verification')

    return render(request, 'donations/project_donation_verification.html', context)


# Food Donation Verification
def foodDonationVerification(request):
    donationList = food_donation.objects.all()

    context = {
        'donations': donationList
    }

    if request.method == 'POST':

        mydonation = food_donation.objects.get(
            id=request.POST.get("donation_id"))

        donorUser = mydonation.donor

        if request.POST.get("status") == 'Verify':

            mydonation.status = 'Accepted'
            mydonation.save()

            # print('Reaches 1')

            subject = "Food Donation Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are happy to inform you that your food donation was succesfully verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Money Donation Verified")

            return render('money_donation_verification')

        elif request.POST.get("status") == 'Decline':

            mydonation.status = 'Declined'
            mydonation.save()
            # print('Reaches 2')

            subject = "Money Donation Could Not Be Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are sorry to inform you that your food donation could not be verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.warning(request, "Money Donation Declined")

            return render('food_donation_verification')

    return render(request, 'donations/food_donation_verification.html', context)

    # Cloth Donation Verification


def clothDonationVerification(request):
    donationList = cloth_donation.objects.all()

    context = {
        'donations': donationList
    }

    if request.method == 'POST':

        mydonation = cloth_donation.objects.get(
            id=request.POST.get("donation_id"))

        donorUser = mydonation.donor

        if request.POST.get("status") == 'Verify':

            mydonation.status = 'Accepted'
            mydonation.save()

            # print('Reaches 1')

            subject = "Money Donation Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are happy to inform you that your cloth donation was succesfully verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.success(request, "Cloth Donation Verified")

            return render('money_donation_verification')

        elif request.POST.get("status") == 'Decline':

            mydonation.status = 'Declined'
            mydonation.save()
            # print('Reaches 2')

            subject = "Money Donation Could Not Be Verified - Daanbaksho"
            message = "Hello " + donorUser.first_name + "!! \n" + \
                "We are sorry to inform you that your cloth donation could not be verified.\n" + "Details: " + "\nAmount: " + \
                str(mydonation.amount) + "\nMethod: " + mydonation.p_method + \
                "\nTransaction ID: " + mydonation.txid + "\n\n\nDaanbaksho Team"
            from_email = settings.EMAIL_HOST_USER
            to_list = [donorUser.email]
            send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            messages.warning(request, "Money Donation Declined")

            return render('cloth_donation_verification')

    return render(request, 'donations/cloth_donation_verification.html', context)


# Cloth Donation Coordinator Thing
def clothInventoryFunc(request, pk):
    mydonation = cloth_donation.objects.get(id=pk)
    inventory = clothInventory.objects.get(id=1)
    # clothDonationList = cloth_donation.objects.all()

    # donorUserID = mydonation.d_user.id
    users = mydonation.d_user.all()
    volunteerUser = User.objects.get(username=users[0])
    donor = User.objects.get(username=users[1])

    if request.method == 'POST':
        i_shirt = inventory.shirt + int(request.POST.get('i_shirt'))
        i_pant = inventory.pant + int(request.POST.get('i_pant'))
        i_t_shirt = inventory.t_shirt + int(request.POST.get('i_t_shirt'))
        i_vest = inventory.vest + int(request.POST.get('i_vest'))
        i_lungi = inventory.lungi + int(request.POST.get('i_lungi'))
        i_salwar = inventory.salwar + int(request.POST.get('i_salwar'))
        i_pajama = inventory.pajama + int(request.POST.get('i_pajama'))
        i_saree = inventory.saree + int(request.POST.get('i_saree'))
        i_panjabi = inventory.panjabi + int(request.POST.get('i_panjabi'))
        i_blanket = inventory.blanket + int(request.POST.get('i_blanket'))

        inventory.shirt = i_shirt
        inventory.pant = i_pant
        inventory.t_shirt = i_t_shirt
        inventory.vest = i_vest
        inventory.lungi = i_lungi
        inventory.salwar = i_salwar
        inventory.pajama = i_pajama
        inventory.saree = i_saree
        inventory.panjabi = i_panjabi
        inventory.blanket = i_blanket

        inventory.save()

        mydonation.status = 'Received'
        mydonation.save()

        # volunteer = User.objects.get(username=donorUser[0])
        # Email to Donor
        subject = "Cloth Donation Delivered to Distribution Team - Daanbaksho"
        message = "Hello " + donor.first_name + "!! \n" + \
            "Respectable donor, our volunteer has delivered your cloth donation to our distribution team.\n\n\n\nDetails:\n"+"Food Donation For: " + \
            str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nVolunteer Name: " + \
            volunteerUser.first_name + "\nVolunteer Phone: " + \
            volunteerUser.profile.phone + "\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [donor.email]
        send_mail(subject, message, from_email,
                  to_list, fail_silently=True)

        # Email to volunteer
        subject = "Cloth Donation Delivered to Distribution Team - Daanbaksho"
        message = "Hello " + volunteerUser.first_name + "!! \n" + \
            "Respectable Volunteer, You have delivered a food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
            str(mydonation.total_items) + "\nDescription: " + mydonation.items_description + "\nDonor Name: " + donor.first_name + \
            "\nDonor Phone: " + donor.profile.phone + "\nDonor Address: " + \
            donor.profile.address + "\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [volunteerUser.email]
        send_mail(subject, message, from_email,
                  to_list, fail_silently=True)

        messages.success(request, "Donation received and inventory updated")

        return redirect('donco_cloth_donation_received')

    return render(request, 'donations/cloth_inventory_verification.html')


def foodInventoryFunc(request, pk):
    mydonation = food_donation.objects.get(id=pk)
    inventory = foodInventory.objects.get(id=1)
    # clothDonationList = cloth_donation.objects.all()

    # donorUserID = mydonation.d_user.id
    users = mydonation.d_user.all()
    volunteerUser = User.objects.get(username=users[0])
    donor = User.objects.get(username=users[1])

    if request.method == 'POST':
        people = inventory.for_people + int(request.POST.get('people'))

        inventory.for_people = people
        inventory.save()

        mydonation.status = 'Received'
        mydonation.save()

            # volunteer = User.objects.get(username=donorUser[0])
            # Email to Donor
        subject = "Food Donation Has Been Received - Daanbaksho"
        message = "Hello " + donor.first_name + "!! \n" + \
                "Respectable donor, our distribution team has received your donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nVolunteer Name: " + \
                volunteerUser.first_name+"\nVolunteer Phone: " + \
                volunteerUser.profile.phone+"\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [donor.email]
        send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

            # Email to volunteer
        subject = "Food Donation Received - Daanbaksho"
        message = "Hello " + volunteerUser.first_name + "!! \n" + \
                "Respectable Volunteer, You have delivered a food donation.\n\n\n\nDetails:\n"+"Food Donation For: " + \
                str(mydonation.quantity)+"\nDescription: "+mydonation.description+"\nDonor Name: "+donor.first_name + \
                "\nDonor Phone: "+donor.profile.phone+"\nDonor Address: " + \
                donor.profile.address+"\n\n\n\nDaanbaksho Team"
        from_email = settings.EMAIL_HOST_USER
        to_list = [volunteerUser.email]
        send_mail(subject, message, from_email,
                      to_list, fail_silently=True)

        messages.success(request, "Food Donation Has Been Delivered")

        return redirect('donco_food_donation_received')

    return render(request, 'donations/food_inventory_verification.html')