from django.shortcuts import render
import os
import cv2
from PIL import Image
import glob
import sys
import pandas as pd

sys.path.append(r'D:\.Time\models\real_time_models')

import fitbit_api

folder_path = r'D:\.Time\temp data\static/'
csv_path = r'D:\.Time\temp data\file1.csv'

def get_all_images():
    img_list = glob.glob(f"{folder_path}*.jpg") + glob.glob(f"{folder_path}*.png") + glob.glob(f"{folder_path}*.jpeg")
    img_names = []
    for img in img_list:
        img_name = os.path.basename(img)
        img_names.append(img_name)

    try:
        df = pd.read_csv(csv_path)
        print(df)
        img_names_pd = df['Image_Name'].to_list()
        img_res_pd = df['Result'].to_list()

        f_list = []
        for i in range(len(img_names_pd)):
            f_list.append([img_names_pd[i], img_res_pd[i] ])
        print(f_list)

    except:
        f_list = None

    return f_list

def home(request):
    context = {'home' : 'active'}
    return render(request, 'web_app/home.html', context)

def about(request):
    context = {'about' : 'active'}
    return render(request, 'web_app/about.html', context)

def run(request):

    img_names = get_all_images()

    if request.method == 'POST':
        my_file = request.FILES['myfile']
        image = Image.open(my_file)
        image.save(folder_path+my_file.name)
        img_names = get_all_images()

    context = {
        'run' : 'active',
        'image_list': img_names
    }

    return render(request, 'web_app/run.html', context)

def parse_data(data):

    l_list = []

    for i in data:
        l_list.append([ i['time'], i['value'] ])

    return l_list

def real_time(request):

    l_list = [ [0,0], [1,1], [2,2] ]

    if request.method == 'POST':
        user_id = request.POST.get('user_id','')
        user_token = request.POST.get('user_token')
        print(user_id)
        print(user_token)
        data = fitbit_api.heart_rate(user_id, user_token, None, debug=False)
        l_list = parse_data(data)
        # fitbit_api.get_activity(user_id, user_token, None, debug=True)

    context = {
        'real_time': 'active',
        'l_list': l_list,
        'img': ['heart_rate.png']
    }


    return render(request, 'web_app/real_time.html', context)
