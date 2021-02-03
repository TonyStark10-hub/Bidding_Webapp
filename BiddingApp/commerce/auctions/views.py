from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    
    all_items=list_item.objects.all()
    empty=False
    if len(all_items)==0:
        empty=True
    return render(request,'auctions/activelist.html',{
        'items':all_items,
        'empty':empty
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url='/login')
def create_listing(request):
    if request.method=='POST':
        item = list_item()

        item.seller=request.user.username
        item.title=request.POST.get('title')
        item.description=request.POST.get('description')
        item.catagory=request.POST.get('catagory')
        item.starting_bid=request.POST.get('starting_bid')
        
        if request.POST.get('image_link'):
            item.image=request.POST.get('image_link')
        else:
            item.image="https://www.aust-biosearch.com.au/wp-content/themes/titan/images/noimage.gif"
        
        item.save()

        all_items=list_item.objects.all()
        empty=False
        if len(all_items)==0:
            empty=True
        return render(request,'auctions/activelist.html',{
            'items':all_items,
            'empty':empty
        })
    else:
        return render(request,'auctions/create.html')
def active_listing(request):

    all_items=list_item.objects.all()
    empty=False
    if len(all_items)==0:
        empty=True
    return render(request,'auctions/activelist.html',{
        'items':all_items,
        'empty':empty,
    })

@login_required(login_url='/login')   
def viewlisting(request,item_id):
    
    if request.method == "POST":
        item=list_item.objects.get(id=item_id)
        newbid=int(request.POST.get('newbid'))
        comments=comment.objects.filter(item_id=item_id)

        if item.starting_bid>=newbid:
            return render(request,'auctions/viewlisting.html',{
                'item':item,
                'message':'Your bid should be higher than the current bid',
                'msg_type':"danger",
                'comments':comments

            })
        else:
            item.starting_bid=newbid
            item.save()
            bidob=bid.objects.filter(item_id=item_id)
            if bidob:
                bidob.delete()
            newob=bid()
            newob.user=request.user.username
            newob.newbid=newbid
            newob.title=item.title
            newob.item_id=item_id
            newob.save()
            item=list_item.objects.get(id=item_id)
            return render(request,'auctions/viewlisting.html',{
                'item':item,
                'message':'bid added succesfully',
                'msg_type':'success',
                'commrnts':comments


            })
    else:
        item=list_item.objects.get(id=item_id)
        added=watchlist.objects.filter(user=request.user.username,item_id=item_id)
        comments=comment.objects.filter(item_id=item_id)
        return render(request,'auctions/viewlisting.html',{
            'item':item,
            'added':added,
            'comments':comments
        })

@login_required(login_url='/login')
def addtowatchlist(request,item_id):

    obj=watchlist.objects.filter(user=request.user.username,item_id=item_id)
    comments=comment.objects.filter(item_id=item_id)

    if obj:
        obj.delete()
        item=list_item.objects.get(id=item_id)
        added=watchlist.objects.filter(user=request.user.username,item_id=item_id)
        return render(request,'auctions/viewlisting.html',{
            'item':item,
            'added':added,
            'message':'Item has been removed from your watchlist',
            'msg_type':'success',
            'comments':comments

        })
    else:
        obj= watchlist()
        obj.item_id=item_id
        obj.user=request.user.username
        obj.save()
        item=list_item.objects.get(id=item_id)
        added=watchlist.objects.filter(user=request.user.username,item_id=item_id)
        return render(request,'auctions/viewlisting.html',{
            'item':item,
            'added':added,
            'comments':comments
        })

@login_required(login_url='/login')
def addcomment(request,item_id):

    obj=comment()
    obj.item_id=item_id
    obj.user=request.user.username
    obj.content=request.POST.get('newcomment')
    obj.save()

    comments=comment.objects.filter(item_id=item_id)
    item=list_item.objects.get(id=item_id)
    added=watchlist.objects.filter(user=request.user.username,item_id=item_id)
    return render(request,'auctions/viewlisting.html',{
        'item':item,
        'added':added,
        'comments':comments
    })

@login_required(login_url='/login')
def watchlist_view(request):
    watchlist_items=watchlist.objects.filter(user=request.user.username)
    items=[]
    for item in watchlist_items:
        entity=list_item.objects.get(id=item.item_id)
        items.append(entity)

    return render(request,'auctions/watchlist.html',{
        'items':items
    })

@login_required(login_url='/login')    
def catagory(request,cat):
    
    items=list_item.objects.filter(catagory=cat)

    return render(request,'auctions/catagory.html',{
        'items':items
    })

@login_required(login_url='/login')    
def catagories(request):

    return render(request,'auctions/catagories.html')

@login_required(login_url='/login')
def closebid(request,item_id):

    item=list_item.objects.get(id=item_id)
    highest_bid=bid.objects.get(newbid=item.starting_bid,item_id=item_id)
    highest_bidder=highest_bid.user
    winner_obj=winner()
    winner_obj.name=highest_bidder
    winner_obj.title=item.title
    winner_obj.seller=item.seller
    winner_obj.final_price=item.starting_bid
    winner_obj.save()

    
    comment_obj=comment.objects.filter(item_id=item_id)
    comment_obj.delete()
    watchlist_obj=watchlist.objects.filter(item_id=item_id)
    watchlist_obj.delete()
    item.delete()
    
    lst=winner.objects.filter(seller=request.user.username)
    return render(request,'auctions/closedbidslist.html',{
        'list':lst
    })

@login_required(login_url='/login')
def closedbidslist(request):
    
    lst=winner.objects.filter(seller=request.user.username)
    return render(request,'auctions/closedbidslist.html',{
        'list':lst
    })

@login_required(login_url='/login')
def winnings(request):

    win_lst=winner.objects.filter(name=request.user.username)

    return render(request,'auctions/winninglst.html',{
        'list':win_lst
    })




    



