import os

from rest_framework.serializers import Serializer
import users
import requests
from django.contrib.auth import authenticate, login, logout

# from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

# from django.views.generic.base import TemplateView
# from .forms import SignUpForm
from .forms import UserCustomCreationForm, AuthenticationCustomForm
from .models import User, Sand, Alarm, create_auth_token
from posts.models import Folder, Post
from questions.models import QuestionPost, Answer, QuestionFolder
from django.views import View
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import check_password

# 이메일 인증 관련 import
import logging
from django.http import HttpResponse
from django.db.models import Sum, query

# SMTP 관련 인증
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_text
from .tokens import account_activation_token, password_reset_token
from django.contrib import messages

# from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.http.response import JsonResponse

# api
from rest_framework import generics, permissions
from .serializers import (
    ResetPasswordEmailSerializer,
    UserSerializer,
    RegisterSerializer,
    AlarmSerailzer,
    AlarmUpdateSerializer,
    ChangePasswordSerializer,
    ChangedescSerializer,
    ChangeimageSerializer,
    ChangeNicknameSerializer,
    # InputEmailSerializer,
    Unlogin_ChangePasswordSerializer,
    # SetNewPasswordSerializer,
)
from rest_framework.response import Response
from django.contrib.auth import login
from rest_framework import permissions
from rest_framework.decorators import api_view
from rest_framework.authtoken.models import Token

# new
from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import status, mixins
from rest_framework import generics  # generics class-based view 사용할 계획
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.decorators import permission_classes, authentication_classes
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
from rest_framework.exceptions import NotFound
from rest_framework.views import APIView
from allauth.account.models import EmailConfirmation, EmailConfirmationHMAC
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
)
from django.core.mail import EmailMultiAlternatives

# import for new code
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.encoding import (
    smart_str,
    force_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .utils import Util
import random

# ------------------------------

# Create your views here.
# ________________________________________________ 회원가입, 로그인, 로그아웃 ________________________________________________
# 회원가입
# 아래 도메인은 이메일 인증 관련 도메인 바뀌면 my_site domain도 변경해주어야함.
my_site = Site.objects.get(pk=1)
my_site.domain = "localhost:3000"
my_site.name = "digging_main"
my_site.save()


class Registration(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        current_site = get_current_site(request)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "이미 존재함"}, status=status.HTTP_409_CONFLICT)

        serializer.is_valid(raise_exception=True)
        user = serializer.save(request)
        user.is_active = False

        user.save()
        to_email = user.email
        message = render_to_string(
            "users/user_activate_email.html",
            {
                "user": user,
                "domain": current_site.domain,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "token": account_activation_token.make_token(user),
            },
        )
        # sending mail to future user
        mail_subject = "Activate your blog account."
        to_email = serializer.cleaned_data.get("email")
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()

        # request 필요 -> 오류 발생
        return Response(
            {
                # get_serializer_context: serializer에 포함되어야 할 어떠한 정보의 context를 딕셔너리 형태로 리턴
                # 디폴트 정보 context는 request, view, format
                "user": UserSerializer(user, context=self.get_serializer_context()).data
            },
            status=status.HTTP_200_OK,
        )


# @csrf_exempt
# def signup(request):
#     if request.method == "POST":
#         user_form = UserCustomCreationForm(request.POST)
#         if user_form.is_valid():
#             user = user_form.save(commit=False)
#             user.is_active = False
#             user.save()
#             current_site = get_current_site(request)
#             message = render_to_string(
#                 "users/user_activate_email.html",
#                 {
#                     "user": user,
#                     "domain": current_site.domain,
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "token": account_activation_token.make_token(user),
#                 },
#             )
#             # sending mail to future user
#             mail_subject = "Activate your blog account."
#             to_email = user_form.cleaned_data.get("email")
#             email = EmailMessage(mail_subject, message, to=[to_email])
#             email.send()

#             # user가 생기자마자 바로 해결, 미해결 폴더 만들기
#             # return HttpResponse('Please confirm your email address to complete the registration') -> 이메일 인증 성공 확인 가능 메세지

#             return redirect("users:login")
#     else:
#         user_form = UserCustomCreationForm()

#     ctx = {"signup_form": user_form}
#     return render(request, "users/signup.html", context=ctx)


# 이메일 인증 후 계정 활성화
def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend="django.contrib.auth.backends.ModelBackend")
        return redirect("posts:main")
    else:
        return HttpResponse("Activation link is invalid!")


# 유저정보 api


class LoadUserView(APIView):
    def get(self, request, format=None):
        try:
            user = request.user
            user = UserSerializer(user)

            return Response({"user": user.data}, status=status.HTTP_200_OK)
        except:
            return Response(
                {"error": "Something went wrong when trying to load user"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


"""@csrf_exempt
def log_in(request):
    context = {}
    if request.method == "POST":
        form = AuthenticationCustomForm(request, request.POST)
        if form.is_valid():
            # login(request, form.get_uer())
            login(
                request,
                form.get_user(),
                backend="django.contrib.auth.backends.ModelBackend",
            )  # 추가
            user = form.get_user()
            return redirect("posts:main")

    else:
        form = AuthenticationCustomForm()
    ctx = {"form": form}
    return render(request, template_name="users/login.html", context=ctx)
"""

# 로그아웃
class LogoutView(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            refresh_token = request.data["refresh_token"]
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_400_BAD_REQUEST)


# 비밀번호를 모르겠을때, email을 작성하는 부분
# one tow
# class Password_reset(generics.GenericAPIView):
#     # email 받으면
#     serializer_class = InputEmailSerializer

#     def post(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         current_site = get_current_site(request)
#         # email 이 존재하는 이메일인지 확인
#         if not serializer.is_valid(raise_exception=True):
#             return Response({"message": "이미 존재함"}, status=status.HTTP_409_CONFLICT)
#         else:
#             # 있으면 메일 보내기
#             user = User.objects.get(
#                 email=self.request.data.get("email"),
#                 username=self.request.data.get("username"),
#             )
#             current_site = get_current_site(request)
#             message = render_to_string(
#                 "users/password_reset_email.html",
#                 {
#                     "user": user,
#                     "domain": current_site.domain,
#                     "domain": my_site.domain,
#                     "uid": urlsafe_base64_encode(force_bytes(user.pk)),
#                     "token": password_reset_token.make_token(user),
#                 },
#             )
#             # sending mail to future user
#             mail_subject = "Change your Password."
#             msg = EmailMultiAlternatives(
#                 mail_subject, message, to=[self.request.data.get("email")]
#             )
#             msg.send()
#             return Response(
#                 {
#                     "user": UserSerializer(
#                         user, context=self.get_serializer_context()
#                     ).data
#                 },
#                 status=status.HTTP_200_OK,
#             )
#             "users:password_reset_form", user.id


# # 이메일 인증


# def password_reset_email(request, uidb64, token):
#     try:
#         uid = force_text(urlsafe_base64_decode(uidb64))
#         user = User.objects.get(pk=uid)
#     except (TypeError, ValueError, OverflowError, User.DoesNotExist):
#         user = None
#     # 잘 넘어오면
#     if user is not None and password_reset_token.check_token(user, token):
#         ctx = {
#             "user": user,
#         }
#         return redirect("users:password_reset_API", user.id)
#     else:
#         ctx = {"user": user}
#         return render(request, template_name="password_email_fail.html", context=ctx)


class Password_resetAPI(generics.GenericAPIView):
    # queryset = User.objects.all()
    serializer_class = Unlogin_ChangePasswordSerializer

    def put(self, request):
        username = User.objects.get(username=self.request.data.get("username"))
        if username.username == self.request.data.get("username"):
            print("aa")
            if int(username.temp) == int(self.request.data.get("temp")):
                print("dd")
                if (
                    len(self.request.data.get("new_password")) >= 8
                    or len(self.request.data.get("password_confirm")) >= 8
                ):
                    print("cc")
                    username.set_password(self.request.data.get("password_confirm"))
                    username.save()
        else:
            Response(
                {"success": False, "message": "비밀번호 변경 실패"}, status=status.HTTP_200_OK
            )
        return Response(
            {"success": True, "message": "비밀번호 변경 성공"}, status=status.HTTP_200_OK
        )


# _______________________________________________social login____________________________________________
# github login
def github_login(request):
    client_id = os.environ.get("GITHUB_ID")
    redirect_uri = "https://diggging.com/users/login/github/callback"
    return redirect(
        f"https://github.com/login/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope=read:user"
    )


def github_callback(request):
    try:
        client_id = os.environ.get("GITHUB_ID")
        client_secret = os.environ.get("GITHUB_SECRET")
        code = request.GET.get("code", None)
        if code is not None:
            token_request = requests.post(
                f"https://github.com/login/oauth/access_token?client_id={client_id}&client_secret={client_secret}&code={code}",
                headers={"Accept": "application/json"},
            )
            token_json = token_request.json()
            error = token_json.get("error", None)
            if error is not None:
                raise Exception("Can't get access token")
            else:
                access_token = token_json.get("access_token")
                profile_request = requests.get(
                    "https://api.github.com/user",
                    headers={
                        "Authorization": f"token {access_token}",
                        "Accept": "application/json",
                    },
                )
                profile_json = profile_request.json()
                user_name = profile_json.get("login", None)
                if user_name is not None:
                    # email = profile_json.get("email")
                    try:
                        user = User.objects.get(username=user_name)
                        if user.login_method != User.LOGIN_GITHUB:
                            raise Exception(f"Please log in with: {user.login_method}")
                    except User.DoesNotExist:
                        user = User.objects.create(
                            username=user_name,
                            user_nickname=user_name,
                            login_method=User.LOGIN_GITHUB,
                        )
                        user.set_unusable_password()
                        user.save()
                    login(
                        request,
                        user,
                        backend="django.contrib.auth.backends.ModelBackend",
                    )
                    ctx = {"user": user}
                    return redirect("posts:main")
                else:
                    raise Exception("Can't get your profile")
        else:
            raise Exception("Can't get code")
    except Exception as e:
        messages.error(request, e)
        return redirect(reverse("users:login"))


# ________________________________________________ mypage ________________________________________________
# my page
def my_page(request, pk):
    # 왼쪽 상단 - host의 상태를 위한 변수들
    host = get_object_or_404(User, pk=pk)
    host_following = host.user_following.all()
    host_follower = host.user_followed.all()

    # 폴더 보여주기위한 변수
    language_folders = Folder.objects.filter(folder_user=host, folder_kind="language")
    framework_folders = Folder.objects.filter(folder_user=host, folder_kind="framework")
    solve_folders = Folder.objects.filter(folder_user=host, folder_kind="solved")

    # 질문 모음
    my_questions = QuestionPost.objects.filter(user=host)
    questions_language_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="language"
    )
    questions_framework_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="framework"
    )

    # 최근에 남긴 질문
    my_recent_questions = QuestionPost.objects.filter(user=host).order_by("-created")
    # 지수가 필요해서 넣었음
    my_recent_logs = Post.objects.filter(user=host).order_by("-created")

    # 모래
    my_sand = Sand.objects.filter(user=host).order_by("-id")
    my_sand_sum = my_sand.aggregate(Sum("amount"))
    sands = serializers.serialize("json", my_sand)
    if my_sand_sum["amount__sum"] == None:
        my_sand_sum = 0
    else:
        if int(my_sand_sum["amount__sum"]) < 2000:
            host.user_level = 0
        elif int(my_sand_sum["amount__sum"]) < 7000:
            host.user_level = 1
        elif int(my_sand_sum["amount__sum"]) < 18000:
            host.user_level = 2
        else:
            host.user_level = 3

    ctx = {
        # 왼쪽 상단을 위한 변수
        "host": host,
        "host_follower": host_follower,
        "host_following": host_following,
        "language_folders": language_folders,
        "framework_folders": framework_folders,
        "solve_folders": solve_folders,
        "questions_language_folder": questions_language_folder,
        "questions_framework_folder": questions_framework_folder,
        #'my_questions': my_questions,
        "my_recent_questions": my_recent_questions,
        "my_recent_logs": my_recent_logs,
        "my_all_sands": my_sand,  # sand 모든 object list
        "my_sand_sum": my_sand_sum,  # 현재까지 sand 총합
        "sands": sands,
    }
    return render(request, template_name="users/my_page.html", context=ctx)


def my_posts(request, host_id):
    # 왼쪽 상단 - host의 상태를 위한 변수들
    host = get_object_or_404(User, pk=host_id)
    host_following = host.user_following.all()
    host_follower = host.user_followed.all()

    # 폴더 보여주기위한 변수
    language_folders = Folder.objects.filter(folder_user=host, folder_kind="language")
    framework_folders = Folder.objects.filter(folder_user=host, folder_kind="framework")
    solve_folders = Folder.objects.filter(folder_user=host, folder_kind="solved")

    # 질문 모음
    my_questions = QuestionPost.objects.filter(user=host)
    questions_language_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="language"
    )
    questions_framework_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="framework"
    )

    # 최근에 남긴 질문
    my_recent_questions = QuestionPost.objects.filter(user=host).order_by("-created")
    # 지수가 필요해서 넣었음
    my_recent_logs = Post.objects.filter(user=host).order_by("-created")

    # 모래
    my_sand = Sand.objects.filter(user=host).order_by("-id")
    my_sand_sum = my_sand.aggregate(Sum("amount"))
    sands = serializers.serialize("json", my_sand)
    if my_sand_sum["amount__sum"] == None:
        my_sand_sum = 0
    else:
        if int(my_sand_sum["amount__sum"]) < 2000:
            host.user_level = 0
        elif int(my_sand_sum["amount__sum"]) < 7000:
            host.user_level = 1
        elif int(my_sand_sum["amount__sum"]) < 18000:
            host.user_level = 2
        else:
            host.user_level = 3

    ctx = {
        # 왼쪽 상단을 위한 변수
        "host": host,
        "host_follower": host_follower,
        "host_following": host_following,
        #'my_questions': my_questions,
        "my_recent_questions": my_recent_questions,
        "my_recent_logs": my_recent_logs,
        "my_all_sands": my_sand,  # sand 모든 object list
        "my_sand_sum": my_sand_sum,  # 현재까지 sand 총합
        "sands": sands,
    }
    return render(request, template_name="users/my_posts.html", context=ctx)


def my_questions(request, host_id):
    # 왼쪽 상단 - host의 상태를 위한 변수들
    host = get_object_or_404(User, pk=host_id)
    host_following = host.user_following.all()
    host_follower = host.user_followed.all()

    # 폴더 보여주기위한 변수

    # 질문 모음
    my_questions = QuestionPost.objects.filter(user=host)
    questions_language_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="language"
    )
    questions_framework_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="framework"
    )

    # 최근에 남긴 질문
    my_recent_questions = QuestionPost.objects.filter(user=host).order_by("-created")
    # 지수가 필요해서 넣었음
    my_recent_logs = Post.objects.filter(user=host).order_by("-created")

    # 모래
    my_sand = Sand.objects.filter(user=host).order_by("-id")
    my_sand_sum = my_sand.aggregate(Sum("amount"))
    sands = serializers.serialize("json", my_sand)
    if my_sand_sum["amount__sum"] == None:
        my_sand_sum = 0
    else:
        if int(my_sand_sum["amount__sum"]) < 2000:
            host.user_level = 0
        elif int(my_sand_sum["amount__sum"]) < 7000:
            host.user_level = 1
        elif int(my_sand_sum["amount__sum"]) < 18000:
            host.user_level = 2
        else:
            host.user_level = 3

    ctx = {
        # 왼쪽 상단을 위한 변수
        "host": host,
        "host_follower": host_follower,
        "host_following": host_following,
        #'my_questions': my_questions,
        "my_recent_questions": my_recent_questions,
        "my_recent_logs": my_recent_logs,
        "my_all_sands": my_sand,  # sand 모든 object list
        "my_sand_sum": my_sand_sum,  # 현재까지 sand 총합
        "sands": sands,
    }
    return render(request, template_name="users/my_questions.html", context=ctx)


def my_answers(request, host_id):
    # 왼쪽 상단 - host의 상태를 위한 변수들
    host = get_object_or_404(User, pk=host_id)
    host_following = host.user_following.all()
    host_follower = host.user_followed.all()

    # 질문 모음
    my_questions = QuestionPost.objects.filter(user=host)
    questions_language_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="language"
    )
    questions_framework_folder = QuestionFolder.objects.filter(
        folder_user=host, folder_kind="framework"
    )

    # 최근에 남긴 질문
    my_recent_questions = QuestionPost.objects.filter(user=host).order_by("-created")
    # 지수가 필요해서 넣었음
    my_recent_logs = Post.objects.filter(user=host).order_by("-created")

    # 모래
    my_sand = Sand.objects.filter(user=host).order_by("-id")
    my_sand_sum = my_sand.aggregate(Sum("amount"))
    if my_sand_sum["amount__sum"] == None:
        my_sand_sum = 0
    else:
        if int(my_sand_sum["amount__sum"]) < 2000:
            host.user_level = 0
        elif int(my_sand_sum["amount__sum"]) < 7000:
            host.user_level = 1
        elif int(my_sand_sum["amount__sum"]) < 18000:
            host.user_level = 2
        else:
            host.user_level = 3

    ctx = {
        # 왼쪽 상단을 위한 변수
        "host": host,
        "host_follower": host_follower,
        "host_following": host_following,
        #'my_questions': my_questions,
        "my_recent_questions": my_recent_questions,
        "my_recent_logs": my_recent_logs,
        "my_all_sands": my_sand,  # sand 모든 object list
        "my_sand_sum": my_sand_sum,  # 현재까지 sand 총합
    }
    return render(request, template_name="users/my_answers.html", context=ctx)


# -----삽질 기록모음, mypage
@csrf_exempt
def lang_folder(request, pk):
    host = get_object_or_404(User, pk=pk)
    folder = Folder.objects.filter(folder_user=host, folder_kind="language")
    data = folder.values()

    return JsonResponse(list(data), safe=False)


@csrf_exempt
def solved_folder(request, pk):
    host = get_object_or_404(User, pk=pk)
    folder = Folder.objects.filter(folder_user=host, folder_kind="solved")
    data = folder.values()

    return JsonResponse(list(data), safe=False)


@csrf_exempt
def framework_folder(request, pk):
    host = get_object_or_404(User, pk=pk)
    folder = Folder.objects.filter(folder_user=host, folder_kind="framework")
    data = folder.values()

    return JsonResponse(list(data), safe=False)


##folder post
@csrf_exempt
def lang_folder_posts(request, pk):
    folder = Folder.objects.get(pk=pk)
    posts = Post.objects.filter(folder=folder)
    data = posts.values()

    # comment, user정보를 보내줘야 할거 같음
    # 내정보 받아오기
    # user = User.objects.filter(pk=folder.folder_user.id)
    # user_data = serializers.serialize('json', user)

    # comments = []
    # for post in posts:
    #     comments.append(post.comments.all())
    # comments_data = serializers.serialize('json',comments)

    # questions user
    # a = User.objects.get(pk=question_post.user.id)
    # question_comments 개수

    # ctx = {
    #     'data': data,
    #     'user': user_data,
    #     'comments': comments_data,
    # }

    return JsonResponse(list(data), safe=False)


@csrf_exempt
def solved_folder_posts(request, pk):
    folder = Folder.objects.get(pk=pk)
    posts = Post.objects.filter(folder=folder)
    data = posts.values()

    return JsonResponse(list(data), safe=False)


@csrf_exempt
def framework_folder_posts(request, pk):
    folder = Folder.objects.get(pk=pk)
    posts = Post.objects.filter(folder=folder)
    data = posts.values()

    return JsonResponse(list(data), safe=False)


# ---------질문 모음
@csrf_exempt
def questions_lang_folder(request, pk):
    host = get_object_or_404(User, pk=pk)
    folder = QuestionFolder.objects.filter(folder_user=host, folder_kind="language")
    data = folder.values()

    return JsonResponse(list(data), safe=False)


def questions_lang_post(request, pk):
    folder = QuestionFolder.objects.get(pk=pk)
    posts = QuestionPost.objects.filter(question_folder=folder)
    data = posts.values()
    return JsonResponse(list(data), safe=False)


def questions_framework_folder(request, pk):
    host = get_object_or_404(User, pk=pk)
    folder = QuestionFolder.objects.filter(folder_user=host, folder_kind="framework")
    data = folder.values()

    return JsonResponse(list(data), safe=False)


def questions_framework_post(request, pk):
    folder = QuestionFolder.objects.get(pk=pk)
    posts = QuestionPost.objects.filter(question_folder=folder)
    data = posts.values()

    return JsonResponse(list(data), safe=False)


# 한번 누르면 follow, 두번 누르면 unfollow
def follow(request, host_pk):
    # 여기서 오는 pk는 내가 follow하려는 사람의 pk임
    # TODO post 상황과 get 상황 나눠야함!!!
    me = request.user
    host = get_object_or_404(User, pk=host_pk)

    if me.user_following.filter(pk=host_pk).exists():
        # 삭제
        me.user_following.remove(host)
        host.user_followed.remove(me)
    else:
        # 나의 following에 pk 추가
        me.user_following.add(host)
        # host의 follower에 나 추가
        host.user_followed.add(me)
        host_alarm = Alarm.objects.create(
            user=host, reason=me.user_nickname + " 님이 나를 팔로우합니다."
        )

    return redirect("users:my_page", host_pk)


def account_detail(request, pk):
    host = get_object_or_404(User, pk=pk)
    # 모래
    my_sand = Sand.objects.filter(user=host).order_by("-id")
    my_sand_sum = my_sand.aggregate(Sum("amount"))
    sands = serializers.serialize("json", my_sand)
    if my_sand_sum["amount__sum"] == None:
        my_sand_sum = 0
    else:
        if int(my_sand_sum["amount__sum"]) < 2000:
            host.user_level = 0
        elif int(my_sand_sum["amount__sum"]) < 7000:
            host.user_level = 1
        elif int(my_sand_sum["amount__sum"]) < 18000:
            host.user_level = 2
        else:
            host.user_level = 3
    ctx = {
        "host": host,
        "my_all_sands": my_sand,  # sand 모든 object list
        "my_sand_sum": my_sand_sum,  # 현재까지 sand 총합
    }
    return render(request, template_name="users/account_detail.html", context=ctx)


@permission_classes([IsAuthenticated])
class ChangeDesc(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangedescSerializer
    """context = {}
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        new_desc = request.POST.get("new_desc")
        user.user_profile_content = new_desc
        user.save()
        return redirect("users:account_detail", user.id)
    return redirect("users:account_detail", user.id)
"""


@permission_classes([IsAuthenticated])
class ChangeNicknameApi(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangeNicknameSerializer
    # if queryset.objects.filter(user_nickname=name):
    # raise Exception("중복된 닉네임이 있습니다.")

    """context = {}
    if request.method == "POST":
        new_nickname = request.POST.get("new_nickname")
        user = get_object_or_404(
            User, pk=pk
        )  # 내 계정 고치기는 페이지가 host = 접속한 사람이여야만 보이게 해야함! (front)
        if User.objects.filter(user_nickname=new_nickname):
            context.update({"error": "이미 존재하는 별명입니다."})

        else:
            user.user_nickname = new_nickname
            user.save()
            return redirect("users:account_detail", user.id)
    return redirect("users:account_detail", user.id)
"""


# 비밀번호 변경 함수
@permission_classes([IsAuthenticated])
class ChangepasswordView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    """def post(self, request, pk, *args, **kwargs):
        context = {}
        current_password = request.POST.get("origin_password")
        user = get_object_or_404(User, pk=pk)
        print(check_password(current_password, str(user.password)))
        print(current_password, user.password)
        if check_password(current_password, user.password):
            new_password = request.POST.get("new_password")
            password_confirm = request.POST.get("password_confirm")
            if new_password == password_confirm and len(new_password) >= 8:
                user.set_password(new_password)
                user.save()
                # backend 인자 추가
                # login(
                #   request,
                #  user,
                # backend="django.contrib.auth.backends.ModelBackend",
                # )
                return Response({"user": user.data}, status=status.HTTP_200_OK)
            else:
                return Response(
                    {"error": "새로운 비밀번호를 다시 확인해주세요."},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR,
                )
        else:
            return Response(
                {"error": "현재 비밀번호가 일치하지 않습니다."},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
"""


@permission_classes([IsAuthenticated])
class ChangeImgView(generics.RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangeimageSerializer

    """user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        new_img = request.FILES.get("new_img", None)
        if new_img:
            # 원래 이미지 삭제
            if user.user_profile_image != "../static/image/profile_img.jpg":
                user.user_profile_image.delete()
            # 새이미지로 바꿈
            user.user_profile_image = new_img
            user.save()
    return redirect("users:account_detail", user.id)
"""


# ________________________________________________ alarm ________________________________________________
# @csrf_exempt
class AlarmAPI(APIView):
    def get(self, request, *args, **kwargs):
        me = User.objects.get(id=kwargs.get("pk"))  # 누구의 alarm인지
        my_alarm = Alarm.objects.filter(user=me)  # 주인의 alarm 모두 가져오기
        serializer = AlarmSerailzer(my_alarm, many=True)
        # not_check_alarm = serializer.filter(is_checked=False)  # 그중 False인애들 가져와서
        data = serializer.data
        # for alarm in my_alarm:
        #     alarm.is_checked = True
        #     alarm.save()

        return Response(data)


# new code
class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        email = request.data["email"]
        username = request.data["username"]

        if User.objects.filter(email=email, username=username).exists():
            user = User.objects.get(email=email, username=username)
            # uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
            # token = PasswordResetTokenGenerator().make_token(user)
            current_site = get_current_site(request=request).domain
            # relativeLink = reverse(
            # "users:password-reset-confirm",
            # kwargs={"uidb64": uidb64, "token": token},
            # )
            absurl = "http://localhost:3000/password_reset_submit"  # current_site + relativeLink
            user_get = User.objects.get(username=username)
            print(user_get)
            temp = random.randrange(10000, 50000)
            user_get.temp = temp
            user_get.save()
            print(user_get.temp)
            email_body = (
                "안녕하세요, \n 아래 링크를 눌러 인증번호를 입력한후 비밀번호를 변경하세요\n"
                + absurl
                + "\n 인증번호 : "
                + str(temp)
                + "\n"
            )
            data = {
                "email_body": email_body,
                "to_email": user.email,
                "email_subject": "비밀번호 변경",
            }

            Util.send_email(data)

            return Response(
                {"success": "비밀번호 변경 링크를 보냈습니다."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"Fail": "아이디 또는 이메일이 틀렸습니다. 다시 입력해주세요 "},
                status=status.HTTP_400_BAD_REQUEST,
            )


# class PasswordTokenCheckAPI(generics.GenericAPIView):
#     def get(self, request, uidb64, token):
#         try:
#             id = smart_str(urlsafe_base64_decode(uidb64))
#             user = User.objects.get(id=id)

#             if not PasswordResetTokenGenerator().check_token(user, token):
#                 return Response(
#                     {"error": "토큰이 맞지 않습니다. 새로운 토큰을 발행해주세요"},
#                     status=status.HTTP_401_UNAUTHORIZED,
#                 )

#             return Response(
#                 {
#                     "success": True,
#                     "message": "Credentials Valid",
#                     "uidb64": uidb64,
#                     "token": token,
#                 },
#                 status=status.HTTP_200_OK,
#             )

#         except DjangoUnicodeDecodeError as identifier:
#             if not PasswordResetTokenGenerator().check_token(user):
#                 return Response(
#                     {"error": "토큰이 유효하지 않음. 새로운 토큰 발행해주세요"},
#                     status=status.HTTP_401_UNAUTHORIZED,
#                 )


# class SetNewPasswordAPIView(generics.GenericAPIView):
#     serializer_class = SetNewPasswordSerializer

#     def patch(self, request):
#         serializer = self.serializer_class(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         return Response(
#             {"success": True, "message": "비밀번호 변경 성공"}, status=status.HTTP_200_OK
#         )

# Alarm 읽었다고 체크 할 수 있는 Alarm update
class UpdateAlarmAPIView(generics.RetrieveUpdateAPIView):
    queryset = Alarm.objects.all()
    serializer_class = AlarmUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer, *args, **kwargs):
        target_alarm = get_object_or_404(Alarm, pk=self.kwargs['pk'])

        if target_alarm.is_checked == False:
            target_alarm.is_checked = True

        target_alarm.save()
        serializer.save(is_checked = target_alarm.is_checked)
