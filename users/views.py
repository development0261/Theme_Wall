from django.shortcuts import render, redirect, get_object_or_404
from .models import Profile
from feed.models import Post
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth import get_user_model,login,authenticate
from django.conf import settings
from django.http import HttpResponseRedirect
from .models import Profile,CustomeUser,SellerRequest
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
import random
from django.core.mail import send_mail
import face_recognition
User = get_user_model()


# @login_required
# def users_list(request):
#     users = Profile.objects.exclude(user=request.user)
#     sent_friend_requests = FriendRequest.objects.filter(from_user=request.user)
#     my_friends = request.user.profile.friends.all()
#     sent_to = []
#     friends = []
#     for user in my_friends:
#         friend = user.friends.all()
#         for f in friend:
#             if f in friends:
#                 friend = friend.exclude(user=f.user)
#         friends += friend
#     for i in my_friends:
#         if i in friends:
#             friends.remove(i)
#     if request.user.profile in friends:
#         friends.remove(request.user.profile)
#     random_list = random.sample(list(users), min(len(list(users)), 10))
#     for r in random_list:
#         if r in friends:
#             random_list.remove(r)
#     friends += random_list
#     for i in my_friends:
#         if i in friends:
#             friends.remove(i)
#     for se in sent_friend_requests:
#         sent_to.append(se.to_user)
#     context = {
#         'users': friends,
#         'sent': sent_to
#     }
#     return render(request, "users/users_list.html", context)

# def friend_list(request):
# 	p = request.user.profile
# 	friends = p.friends.all()
# 	context={
# 	'friends': friends
# 	}
# 	return render(request, "users/friend_list.html", context)

# @login_required
# def send_friend_request(request, id):
# 	user = get_object_or_404(User, id=id)
# 	frequest, created = FriendRequest.objects.get_or_create(
# 			from_user=request.user,
# 			to_user=user)
# 	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

# @login_required
# def cancel_friend_request(request, id):
# 	user = get_object_or_404(User, id=id)
# 	frequest = FriendRequest.objects.filter(
# 			from_user=request.user,
# 			to_user=user).first()
# 	frequest.delete()
# 	return HttpResponseRedirect('/users/{}'.format(user.profile.slug))

# @login_required
# def accept_friend_request(request, id):
# 	from_user = get_object_or_404(User, id=id)
# 	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
# 	user1 = frequest.to_user
# 	user2 = from_user
# 	user1.profile.friends.add(user2.profile)
# 	user2.profile.friends.add(user1.profile)
# 	if(FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()):
# 		request_rev = FriendRequest.objects.filter(from_user=request.user, to_user=from_user).first()
# 		request_rev.delete()
# 	frequest.delete()
# 	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

# @login_required
# def delete_friend_request(request, id):
# 	from_user = get_object_or_404(User, id=id)
# 	frequest = FriendRequest.objects.filter(from_user=from_user, to_user=request.user).first()
# 	frequest.delete()
# 	return HttpResponseRedirect('/users/{}'.format(request.user.profile.slug))

# def delete_friend(request, id):
# 	user_profile = request.user.profile
# 	friend_profile = get_object_or_404(Profile, id=id)
# 	user_profile.friends.remove(friend_profile)
# 	friend_profile.friends.remove(user_profile)
# 	return HttpResponseRedirect('/users/{}'.format(friend_profile.slug))

@login_required
def profile_view(request, slug):
    p = Profile.objects.filter(slug=slug).first()
    u = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=p.user)
    rec_friend_requests = FriendRequest.objects.filter(to_user=p.user)
    user_posts = Post.objects.filter(user_name=u)

    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=p.user)) == 1:
            button_status = 'friend_request_sent'

        # if we have recieved a friend request
        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': u,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'post_count': user_posts.count
    }

    return render(request, "users/profile.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        print(form)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Your account has been created! You can now login!')
            return redirect('login')

    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def login_process(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user:
            login(request,user)
            if user.role == "seller":
                print(user.role)
                return redirect("home")
            elif user.role == "buyer":

                return redirect('home')
        else:
            messages.error(request,"Please make Registration First")
            return redirect("register")

    return render(request,'users/login.html')


@login_required
def edit_profile(request):
    p = request.user.profile
    you = p.user
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('edit_profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    context = {
        'u': you,
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def my_profile(request):
    p = request.user.profile
    you = p.user
    sent_friend_requests = FriendRequest.objects.filter(from_user=you)
    rec_friend_requests = FriendRequest.objects.filter(to_user=you)
    user_posts = Post.objects.filter(user_name=you)
    friends = p.friends.all()

    # is this user our friend
    button_status = 'none'
    if p not in request.user.profile.friends.all():
        button_status = 'not_friend'

        # if we have sent him a friend request
        if len(FriendRequest.objects.filter(
                from_user=request.user).filter(to_user=you)) == 1:
            button_status = 'friend_request_sent'

        if len(FriendRequest.objects.filter(
                from_user=p.user).filter(to_user=request.user)) == 1:
            button_status = 'friend_request_received'

    context = {
        'u': you,
        'button_status': button_status,
        'friends_list': friends,
        'sent_friend_requests': sent_friend_requests,
        'rec_friend_requests': rec_friend_requests,
        'post_count': user_posts.count
    }

    return render(request, "users/profile.html", context)


@login_required
def search_users(request):
    query = request.GET.get('q')
    object_list = User.objects.filter(username__icontains=query)
    context = {
        'users': object_list
    }
    return render(request, "users/search_users.html", context)


def privacy_policy(request):
    return render(request, 'users/privacy_policy.html')


def terms_condition(request):
    return render(request, 'users/terms_condition.html')


def sendActivation(request):
    if request.method == "POST" and request.user.is_authenticated:
        proof = request.FILES['proof']
        message = request.POST['message']
        fullname= request.POST['fullname']
        if not 'ImageName' in request.POST or not 'proof' in request.FILES:
            messages.error(request,'Please fill all details of form')
            return redirect('home')

        request.user.fullname = fullname
        request.user.save()
        act_msg = SellerRequest(email=request.user.email, message=message, user=request.user,proof=proof)
        act_msg.save()
        user = CustomeUser.objects.get(email=request.user.email)

        user.save()
        from django.conf import settings
        import cv2
        imagePath = act_msg.proof.path
        image = cv2.imread(imagePath)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        faceCascade = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.3,
            minNeighbors=3,
            minSize=(30, 30)
        )
        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        for (x, y, w, h) in faces:
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            roi_color = image[y:y + h, x:x + w]
            cv2.imwrite(settings.MEDIA_ROOT + '/proofs/'+str(request.user.username)+'_faces.jpg', roi_color)

        ImageName =  request.POST['ImageName'].split(',')[1]
        import base64
        with open(settings.MEDIA_ROOT + '/proofs/'+str(request.user.username)+'_captureFace.jpg', "wb") as fh:
            fh.write(base64.b64decode(ImageName))

        captured_face = settings.MEDIA_ROOT + '/proofs/'+str(request.user.username)+'_captureFace.jpg'
        verify_with = imagePath
        results = []
        cap = face_recognition.load_image_file(captured_face)
        ids = face_recognition.load_image_file(verify_with)
        if face_recognition.face_encodings(cap) == []:
            results[0] = False
        else:
            cap_encoding = face_recognition.face_encodings(cap)[0]
            id_encoding = face_recognition.face_encodings(ids)[0]

            results = face_recognition.compare_faces([cap_encoding], id_encoding)
            print(results)
            if results[0] == True:
                messages.success(request,'Your Account Accepted as Seller Account')
                request.user.role = 'seller'
                request.user.save()
            else:
                messages.error(request, 'Your ID Proof Image and Capture Image Does not Match. Please try Again')

        return redirect("sellerDash")




def activateAccount(request,email):
    user = CustomeUser.objects.get(email=email)
    user.role = 'seller'
    user.save()
    return redirect('sellerDash')

