from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Company
from .form import UpdateCompanyForm
from users.models import User
from django.contrib.auth.models import AnonymousUser

#update company
def update_company(request):
    if request.user.is_authenticated:
        user = request.user
    else:
        # Create a default user for AnonymousUser
        user, created = User.objects.get_or_create(username='anonymous_user')

    # Get or create the Company instance associated with the user
    try:
        # Get or create the Company instance associated with the user
        company, created = Company.objects.get_or_create(user=user)
    except User.DoesNotExist:
        # Handle the case where the user cannot be found
        messages.warning(request, 'User not found.')
        return redirect('login')  # Redirect to login or handle as appropriate
    if request.method == 'POST' :
        form = UpdateCompanyForm(request.POST, instance=company)
        if form.is_valid():
            var = form.save(commit=False)
            user = User.objects.get(id=request.user.id)
            user.has_company = True
            var.save()
            user.save()
            messages.info(request, "Your company info has been updated!")
            return redirect('dashboard')
        else:
            messages.warning(request, 'Something went wrong')

    else:
        form = UpdateCompanyForm(instance=company)
        context = {'form':form}
        return render(request, 'company/update_company.html', context)
    
#view company details   
def company_details(request, pk):
    company = Company.objects.get(pk=pk)
    context = {'company':company}
    return render(request, 'company/company_details.html', context)
