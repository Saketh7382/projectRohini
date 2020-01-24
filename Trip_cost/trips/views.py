from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Trip, Transaction
import django.utils.timezone as tz
import numpy as np
import pandas as pd

def index(request):
    trips = Trip.objects.all()
    context={
        'trips' : trips
    }
    return render(request, 'index3.html', context)

def insert_trip(request):
    return render(request, 'insert.html')

def insert_trip_value(request):
    if request.method == 'POST':
        trip_name = request.POST['trip_name']
        description = request.POST['description']
        members_data = request.POST['members']
        members = list(members_data.split(','))
        # print(members)

        t = Trip(trip_name=trip_name, description=description, date=tz.localtime(), members=members)
        t.save()

        trips = Trip.objects.all()
        context={
            'trips' : trips
        }
        # return render(request, 'index3.html', context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        # return render(request, 'insert.html')

def delete_trip(request, trip_id):
        # trip_id = request.POST['delete_value_trip']

        Trip.objects.filter(id=trip_id).delete()

        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def insert_trans_value(request, trip_id):
    if request.method == 'POST':
        print(trip_id)
        trip = Trip.objects.get(id=trip_id)
        # print(trip)
        amt_from = request.POST['amt_from']
        amount_to_data = request.POST['amount_to']
        amount_to = list(amount_to_data.split(','))
        amount = request.POST['amount']
        trans = Transaction(trip_name=trip, amt_from=amt_from, amount_to=amount_to, amount=amount)
        trans.save()
        # trip = Trip.objects.all()[-1]
        # trans.Trip.add(trip)

        # trans = Transaction.objects.filter(trip_name_id=trip_id)
        # context = {
        #     "trans" : trans
        # }
        # return render(request, 'insert_trans.html',context)
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    else:
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def delete_trans(request, trip_id, trans_id):
    print(trip_id)
    # trans_id = request.POST['delete_value_trans']
    Transaction.objects.filter(id=trans_id).delete()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def trip_expand(request, trip_id):
    # trip = Trip.objects.get()
    trans = Transaction.objects.filter(trip_name_id=trip_id)
    trip = Trip.objects.filter(id=trip_id)
    context = {
        "trip_name":trip,
        "trans" : trans
    }
    return render(request, 'insert_trans.html', context)

def analysis_trans(request, trip_id):
    data = Transaction.objects.filter(trip_name_id=trip_id)
    data2 = Transaction.objects.filter(trip_name_id=trip_id)
    # print("Trans")
    # print(type(trans))
    # print(trans[0])
    # print(trans)
    trip = Trip.objects.get(id=trip_id)
    names = trip.members
    # print(type(xnames))
    # print(xnames)
    matrix = np.zeros([len(names),len(names)])
    # names = ['A','B','C','D']
    df = pd.DataFrame(matrix, index=names, columns=names)

    matrix = data_to_matrix(df,data,names)
    analysis1 = analysis_1(matrix,names)

    analysis2 = analysis_2(matrix,names)

    analysis3 = analysis_3(matrix,names)

    context = {
        'transactions' : data2,
        'names' : names,
        'analysis1' : analysis1,
        'analysis2' : analysis2,
        'analysis3' : analysis3
    }
    # print(matrix)
    return render(request, 'analysis.html', context)

def data_to_matrix(df,data,names):
    for row in data:
        amt_from = row.amt_from
        amt_to = row.amount_to
        amount = row.amount
        for col in amt_to:
            df[col][amt_from] += amount//len(amt_to)
    return df
def analysis_1(mat, names):
    a1 = []
    for name in names:
        a1.append((name,mat[name][name]))
        #print(name+" : "+str(mat[name][name]))
    return a1

#spend by him
def analysis_2(mat, names):
    a2 = []
    for name in names:
        amt = 0
        for itr in names:
            amt += mat[itr][name]
        a2.append((name,amt))
        # print(name+" : "+str(amt))
    return a2

#amount that has needs to be given to others
def analysis_3(mat, names):
    a3 = []
    for name in names:
        for itr in names:
            if mat[itr][name] != 0 and itr!=name:
                # print(itr+"->"+name+" : "+str(mat[itr][name]))
                a3.append([itr,name,mat[itr][name]])
    return a3
