import profile #
from django.shortcuts import render, redirect #
from django.views.generic import TemplateView, DeleteView #
from user_app.models import Friendship, Avatar #
from post_app.models import Album #
from post_app.models import Post #
from django.urls import reverse_lazy #
from django.shortcuts import get_object_or_404 #
from django.contrib.auth.models import User #
from user_app.models import Profile

#
class FriendsView(TemplateView):
    template_name = "friends/friends.html" #
    #
    def get_context_data(self, **kwargs): 
        context = super(FriendsView, self).get_context_data(**kwargs) #
        profile = Profile.objects.get(user = self.request.user) #
        context["all_recommended"] = Profile.objects.filter().exclude(user = self.request.user) #
        context["all_friends"] = Friendship.objects.filter(accepted = True) #
        context["all_requests"] = Friendship.objects.filter(profile2 = profile, accepted = False) #
        context["all_avatars"] = Avatar.objects.all() #
        context["current_user"] = Profile.objects.get(user = self.request.user) #
        author_avatars = {} #
        #
        for author in Profile.objects.all(): #
            avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first() #
            author_avatars[author.id] = avatar #
        context["author_avatars"] = author_avatars #
        return context #
    #
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists(): #
            return redirect("registration") #
        else:   #
            return super().dispatch(request, *args, **kwargs) #
            
    
    
#
class AllFriendsView(TemplateView):
    template_name = "all_friends/all_friends.html" #
    #
    def get_context_data(self, **kwargs):
        context = super(AllFriendsView, self).get_context_data(**kwargs) #
        context["all_friends"] = Friendship.objects.filter(accepted = True) #
        context["all_avatars"] = Avatar.objects.all() #
        context["current_user"] = Profile.objects.get(user = self.request.user) #
        author_avatars = {} #
        for author in Profile.objects.all(): #
            avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first() #
            author_avatars[author.id] = avatar #
        context["author_avatars"] = author_avatars #
        return context #
    #
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists(): #
            return redirect("registration") #
        else:  #
            return super().dispatch(request, *args, **kwargs) #
#
class RequestView(TemplateView):
    template_name = "all_requests/requests.html" #
#
    def get_context_data(self, **kwargs):
        context = super(RequestView, self).get_context_data(**kwargs) #
        profile = Profile.objects.get(user = self.request.user) #
        context["all_requests"] = Friendship.objects.filter(profile2 = profile, accepted = False) #
        context["all_avatars"] = Avatar.objects.all() #
        author_avatars = {} #
        for author in Profile.objects.all(): #
            avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first() #
            author_avatars[author.id] = avatar #
        context["author_avatars"] = author_avatars #
        return context #
    #
    def dispatch(self, request, *args, **kwargs): 
        if not Profile.objects.filter(user_id = request.user.id).exists(): #
            return redirect("registration") #
        else: #
            return super().dispatch(request, *args, **kwargs) #
#
class RecommendedView(TemplateView):
    template_name = "recommended/recommended.html" #
    #
    def get_context_data(self, **kwargs):
        context = super(RecommendedView, self).get_context_data(**kwargs) #
        context["all_recommended"] = Profile.objects.filter().exclude(user = self.request.user) #
        context["all_avatars"] = Avatar.objects.all() #
        author_avatars = {} #
        for author in Profile.objects.all(): #
            avatar = Avatar.objects.filter(profile=author, shown=True, active=True).first() #
            author_avatars[author.id] = avatar #
        context["author_avatars"] = author_avatars #
        return context #
    #
    def dispatch(self, request, *args, **kwargs): 
        if not Profile.objects.filter(user_id = request.user.id).exists(): #
            return redirect("registration")#
        else: # 
            return super().dispatch(request, *args, **kwargs) #
#
class FriendProfileView(TemplateView):
    template_name = 'friend_profile/friend_profile.html' #
    def get_context_data(self, **kwargs): #
        context = super(FriendProfileView, self).get_context_data(**kwargs) #
        friend_pk = self.kwargs['friend_pk'] #
        friend_user = User.objects.get(id = friend_pk) # 
        profile_id = Profile.objects.get(user_id = friend_pk) #
        context['friend'] = Profile.objects.get(user_id = friend_pk) #
        context['avatar'] = Avatar.objects.filter(profile = profile_id).first() #
        context['all_avatars'] = Avatar.objects.all() #
        context['all_posts'] = Post.objects.filter(author_id = profile_id.pk).all().order_by('-id') #
        context["posts_count"] = Post.objects.filter(author_id = profile_id.pk).count() #
        context['current_request'] = Friendship.objects.filter(profile1= Profile.objects.get(user = friend_user), profile2 =Profile.objects.get(user = self.request.user)).union(Friendship.objects.filter(profile2= Profile.objects.get(user = friend_user), profile1 =Profile.objects.get(user = self.request.user))).first()
        context['all_views'] = Post.objects.none() #
        context['all_albums'] = Album.objects.filter(author = profile_id) #
        for post in Post.objects.filter(author = profile_id): #
            context['all_views'] = context['all_views'] | post.views.all() #
        context["my_friends"] = Friendship.objects.filter(profile2 = profile_id, accepted = True).union(Friendship.objects.filter(profile1 = profile_id, accepted = True))
        return context #
    #
    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user_id = request.user.id).exists():#
            return redirect("registration") #
        else: #
            return super().dispatch(request, *args, **kwargs) #
#
def delete_request(request, pk):
    current_user = Profile.objects.get(user_id = request.user.id) #
    friend_user = Profile.objects.get(user_id = pk) #
    if Friendship.objects.filter(profile1_id = request.user.pk, profile2 = friend_user): #
        Friendship.objects.get(profile1 = current_user, profile2 = friend_user).delete() #
    if Friendship.objects.filter(profile2 = current_user, profile1 = friend_user): # 
        Friendship.objects.get(profile2 = current_user, profile1 = friend_user).delete() #
    return redirect("main_friends") #
#
def delete_recommended(request, pk):
    rejected_user = User.objects.get(id = pk) #
    return redirect("main_friends") #
#
def delete_friend(request, pk):
    current_user = Profile.objects.get(user_id = request.user.id) #
    friend_user = Profile.objects.get(user_id = pk)#
    if Friendship.objects.filter(profile1 = current_user, profile2 = friend_user): #
        Friendship.objects.get(profile1 = current_user, profile2 = friend_user).delete() #
    if Friendship.objects.filter(profile2 = current_user, profile1 = friend_user): #
        Friendship.objects.get(profile2 = current_user, profile1 = friend_user).delete() #
    return redirect("main_friends") #
#
def confirm_friend(request, pk):    
    current_profile = Profile.objects.get(user_id = request.user.id) #
    friend_profile = Profile.objects.get(user_id = pk) #
    current_user = User.objects.get(id = request.user.id) #
    friend_user = User.objects.get(id = pk)#
    request = Friendship.objects.get(profile1=friend_profile, profile2=current_profile) #
    request.accepted = True #
    request.save() #
    return redirect("main_friends") #
#
def request_to_user(request, pk):
    current_user = Profile.objects.get(user_id = request.user.id) #
    request_user = Profile.objects.get(user_id = pk) #
    if len(Friendship.objects.filter(profile1 = current_user, profile2 = request_user)) == 0 and len(Friendship.objects.filter(profile1 = request_user, profile2 = current_user)) == 0: #
        Friendship.objects.create(profile1 = current_user, profile2 = request_user, accepted = False) #
    return redirect("main_friends") #