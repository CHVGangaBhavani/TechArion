from django.shortcuts import render , redirect
from .models import *
from django.contrib import messages
from django.contrib.auth.models import User , auth
from django.db.models import Q
from django.core.paginator import Paginator , EmptyPage  
# Create your views here.


# Register view
def Register(request):
	if request.method=='POST':
		username = request.POST['username']
		email = request.POST['email']
		password1 = request.POST['password1']
		password2 =request.POST['password2']
		if password1==password2:
			if User.objects.filter(username = username).exists():
				messages.info(request , "Username already taken")
				return redirect('register')
			elif User.objects.filter(email = email).exists():
				messages.info(request,"email already exist")
				return redirect('register')
			else:
				user = User.objects.create_user(username = username , email=email , password=password1 )
				usermodel = UserModel( username =username , email=email)
				usermodel.save()
				user.save()
				return redirect('register')
	return render(request , 'index.html')

#login view.....
def Login(request):
	if request.method=='POST':
		username = request.POST['username']
		password = request.POST['password1']
		user = auth.authenticate(username=username, password=password)
		if user is not None:
			auth.login(request , user)
			if username ==	"product":
				return redirect('dashboard')
			else:
				return redirect('add to cart')
		else:
			messages.success(request, ('invalid credentials '))
			return redirect('login')
	return render(request,'index.html')

# Logout view... 
def logout(request):
	auth.logout(request)
	return redirect('login')

# VIEW FOR CHANGE THE PASSWORD FOR THE EXISTING USER BY USING TOKEN AUTHENTICATION ... 
def ChangePassword(request , token):
    context = {}
 
    try:
        profile_obj = UserModel.objects.filter(forget_password_token = token).first()
        user_name = profile_obj.username
        print(f"forgotten username ==={user_name}")
        #context = {'user_name' : profile_obj.username}
        
        if request.method == 'POST':
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('reconfirm_password')
            
            
            if user_name is  None:
                messages.success(request, 'No user id found.')
                return redirect(f'/change-password/{token}/')
                
            
            if  new_password != confirm_password:
                messages.success(request, 'both should  be equal.')
                return redirect(f'/change-password/{token}/')
                         
            
            user_obj = User.objects.get(username = user_name)
            user_obj.set_password(new_password)
            user_obj.save()
            return redirect('/login/')
                            
    except Exception as e:
        print(e)
    return render(request , 'change-password.html' , context)

    

# VIEW FOR GENERATE AND RESET PASSWORD ....
import uuid
def ForgetPassword(request):
    try:
        if request.method == 'POST':
            username = request.POST.get('username')
            
            if not User.objects.filter(username=username).first():
                messages.success(request, 'Not user found with this username.')
                return redirect('/forget-password/')
            
            user_obj = User.objects.get(username = username)
            token = str(uuid.uuid4())
            profile_obj= UserModel.objects.get(username = user_obj)
            profile_obj.forget_password_token = token
            profile_obj.save()
            
            send_forget_password_mail(user_obj.email , token)
            messages.success(request, 'An email is sent.')
            return redirect('/forget-password/')
                
    
    
    except Exception as e:
        print(e)
    return render(request , 'forget-password.html')


# VIEW AND LIBRARIES FOR SENDING REST PASSWORD ....
from email.message import EmailMessage
import ssl
import smtplib


def send_forget_password_mail(email , token):
	lemail = ""
	lemail = email
	token = token
	email_sender = 'ganga@gmail.com'
	email_password = 'miuxfsxjfbxrwlak'


	email_reciver = lemail


	subject = "Reset Password product admin"
	body = f'Hi , click on the link to reset your password http://127.0.0.1:8000/change-password/{token}/'
	
	em = EmailMessage()
	em['From'] = email_sender
	em['To'] = email_reciver
	em['subject'] = subject
	em.set_content(body)


	context = ssl.create_default_context()

	with smtplib.SMTP_SSL('smtp.gmail.com' , 465 , context = context) as smtp:
	    smtp.login(email_sender , email_password)
	    smtp.sendmail(email_sender , email_reciver , em.as_string())





# add data form collecting view
def add_data(request):
	
	if request.method =='POST':
		Device_Name = request.POST['Device_Name']
		Device_Serial = request.POST['Device_Serial']
		Issued_To = request.POST['Issued_To']
		Remarks = request.POST['Remarks']
		other = request.POST['other']
		data = Itdb(Product_Name = product_name , Product_id = product_Serial)
		data.save()
		return redirect("add_data")
	else:
		return render(request ,'add_data.html')


#admin dashboard .... 
def admin_dashboard(request):
	if 'q' in request.GET:
		q= request.GET['q']
		multiple_q = Q(Q(productname=q) | Q(productprice =q) )
		data =Itdb.objects.filter(multiple_q)
		context = {
			'data': data,
		}
		return render(request , 'admin_dashboard.html' , context)
	else:

		dobj = Itdb.objects.all()
		p = Paginator(dobj , 8 )
		page_num = request.GET.get('page' ,1)
		page = p.page(page_num)
		try:
			page = p.page(page_num)
		except EmptyPage:
			page = p.page(1)
	
		context = {
			'data': page,
		}
		return render(request , 'admin_dashboard.html' , context)


def Edit_data(request , id):
	if request.method =='POST':
		PhoneNumber = request.POST['phonenumeber']
		Email = request.POST['Email']
		IssCustomer = request.POST['IsCustomer']
		IsAdmin=request.POST['IsAdmin']
		data.save()
		return redirect("dashboard")
	else:
		return redirect("dashboard")

def product_updates(request):
	if request.user.username =="Admin":

		if 'q' in request.GET:
			q= request.GET['q']
			multiple_q = Q(Q(productname =q) | Q(productprice =q) )
			data =Complaints.objects.filter(multiple_q)

			context = {
				'data': data,
			}
			return render(request , 'product_updates.html' , context)
			
		else:
			dobj = Complaints.objects.all().order_by('-date')
			p = Paginator(dobj , 8 )
			page_num = request.GET.get('page' ,1)
			page = p.page(page_num)
			try:
				page = p.page(page_num)
			except EmptyPage:
				page = p.page(1)
		
			context = {
				'data': page,
			}
			return render(request , 'productupdates.html' , context)
	else:
		return redirect('login')

def update_status(request ,id):
	if request.method =='POST':
		solved = Complaints.objects.get(id = id)
		ack = request.POST['ack']
		reject = request.POST['reject']
		dobj = Complaints(id =id  , ack = ack , reject = reject ,Name = solved.Name , Id_Numbeer = solved.Id_Numbeer , Class = solved.Class ,Device_Name= solved.Device_Name , Description = solved.Description , videoproof = solved.videoproof , )
		dobj.save()

	return redirect('poduct_updates')

def completed(request ,id):
	if request.user.is_authenticated:
		solved = Complaints.objects.get(id = id)
		Rating = request.POST.get('Rating')
		suggestions = request.POST.get('suggestions')
		
		dobj = SolvedComplaints(Name = solved.Name , Id_Numbeer = solved.Id_Numbeer , Class = solved.Class ,Device_Name= solved.Device_Name , Description = solved.Description , videoproof = solved.videoproof , Rating = Rating , suggestions =suggestions)
		dobj.save()
		delojb = Complaints.objects.get(id = id).delete()
		return redirect('mycomplaints')
	else:
		return redirect('login')

def mycomplaints(request):
	if request.user.is_authenticated:
		username  = request.user.username
		dobj = Complaints.objects.filter(Name = username).order_by('-date')
		p = Paginator(dobj , 8 )
		page_num = request.GET.get('page' ,1)
		page = p.page(page_num)
		try:
			page = p.page(page_num)
		except EmptyPage:
			page = p.page(1)
		
		context = {
			'data': page,
		}
		return render(request , 'mycomplaints.html' , context)
	else:
		return redirect('login')
		

def addtocart(request):
	if request.user.username =="Admin":

		if 'q' in request.GET:
			q= request.GET['q']
			multiple_q = Q(Q(product name =q) | Q(product price=q) )
			data =completedlist.objects.filter(multiple_q)

			context = {
				'data': data,
			}
			return render(request , 'completed.html' , context)
			
		else:
			dobj = completedlist.objects.all().order_by('-date')
			p = Paginator(dobj , 8 )
			page_num = request.GET.get('page' ,1)
			page = p.page(page_num)
			try:
				page = p.page(page_num)
			except EmptyPage:
				page = p.page(1)
		
			context = {
				'data': page,
			}
			return render(request , 'completed.html' , context)
	else:
		return redirect('login')

