
#pyinstaller --onefile -F --add-binary "C:\Python37\Scripts\chromedriver.exe";"." latest.py
print('Starting...')
import time
import requests
import pandas as pd
import os
import sys
import copy
import glob
import shutil
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:69.0) Gecko/20100101 Firefox/69.0',
'Accept': '*/*',
'Accept-Language': 'en-US,en;q=0.5',
'Accept-Encoding': 'gzip, deflate, br',
'X-Requested-With': 'XMLHttpRequest',
'Connection': 'keep-alive'}


def f7(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


df = pd.read_excel('Instagram_data_(id).xlsx')
df.dropna(axis=0, subset=['Instagram Name (city)'],inplace=True)
insta_links = list(df['Instagram Name (city)'])
# insta_links = f7(insta_links)
# df = df.set_index('Instagram Name (city)')
range_of_images = (input('Enter the range of images, for example 2,5: '))
range_of_images = tuple(int(x) for x in range_of_images.split(","))
range_of_images = list(range(range_of_images[0],range_of_images[1]+1))

insta_dict = {}
dict3 = {}

already_scraped = []
os.mkdir('instagram_images')
for index,insta_link in enumerate(insta_links):
    image_links = []
    insta_images_links = []
    insta_id = copy.deepcopy(insta_link)
    if 'http' in insta_link:
        insta_link = insta_link.split('.com/')[1].split('/')[0]   
    if insta_id not in already_scraped:
        print(f'Downloading images for {insta_link}...')
        res = requests.get(f'https://www.instagram.com/{insta_link}/',headers=headers)    
        try:
            total_posts = int(res.text.split('"edge_owner_to_timeline_media":{"count":')[1].split(',')[0])
            print(total_posts,'post(s) found.')
        except:
            print(insta_link,'instagram page not found.')
            insta_dict['Instagram Name (city)'] = insta_link
            plus_code = df.iloc[index]['Plus Code']
            category = df.iloc[index]['Category']
            insta_dict['Category'] = category
            insta_dict['Plus Code'] = plus_code
            dict3[index]=pd.DataFrame(insta_dict,index=[0])
            continue
        try:
            description = res.text.split('description":"')[1].split('"')[0].strip()
        except:
            description = ''
        try:
            description80 = description[:80]
        except:
            description80 = ''
        try:
            pp_link = res.text.split('"profile_pic_url":"')[1].split('"')[0].replace('\\u0026','&')
        except:
            pp_link = ''
        try:
            instagram_id = res.text.split('[{"logging_page_id":"profilePage_')[1].split('"')[0]
        except:
            instagram_id = ''

        required = range_of_images[-1]
        if total_posts < required:
            # print(f'The required range not available in {insta_link}. Total number of posts are {total_posts}.')
            required = total_posts

    else:
        # search all the existing jpg files including the insta_name and copy them to the new category folder
        imgs_already_downloaded = glob.glob('*/*/*.jpg')
        imgs_already_downloaded = [i for i in imgs_already_downloaded if insta_link in i]
        category = df.iloc[index]['Category']
        df_t = df4.set_index('Instagram Name (city)')

        description = df_t.loc[insta_link,'Full Description']
        description80 = df_t.loc[insta_link,'Description']
        instagram_id = df_t.loc[insta_link,'Instagram ID (city)']
        if not os.path.exists(f"instagram_images/{category}"):
            os.makedirs(f"instagram_images/{category}")
        copied = False
        for img in imgs_already_downloaded:
            img1 = img[img.rfind('\\')+1:]
            target = f"instagram_images/{category}/{img1}"
            try:
                shutil.copyfile(img,target)
                copied = True
            except:
                None
        print('Duplicate instagram ID.')
        if copied:
            print(f'Images for {insta_link} successfully copied to the {category} folder.')


    plus_code = df.iloc[index]['Plus Code']
    category = df.iloc[index]['Category']
    if type(plus_code) != str:
        if type(plus_code) == float:
            plus_code = str(plus_code)
        else:
            plus_code = plus_code[:1][0]
    try:
        plus_code = plus_code.split(',')[0]
    except:
        plus_code = ''
    insta_dict['Category'] = category
    insta_dict['Plus Code'] = plus_code
    insta_dict['Instagram Name (city)'] = insta_link
    insta_dict['Instagram ID (city)'] = instagram_id
    insta_dict['Instagram Profile Picture'] = f'{insta_link}_profile.jpg'
    insta_dict['Full Description'] = description
    insta_dict['Description'] = description80
    if not os.path.exists(f"instagram_images/{category}"):
        os.makedirs(f"instagram_images/{category}")
    if insta_id not in already_scraped:
        try:
            myfile = requests.get(pp_link,headers=headers)
            open(f'instagram_images/{category}/{insta_link}_profile.jpg', 'wb').write(myfile.content)
        except:
            None
        headers = {
            'authority': 'www.instagram.com',
            'accept': '*/*',
            'x-mid': 'pknpr8lprfzw1yo0ufk1sz6t6014f3lv68urp6hijbafc27p1jr',
            'x-ig-www-claim': '0',
            'x-requested-with': 'XMLHttpRequest',
            'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-csrftoken': 'W4Fh7nPyXyaWaDHtypOusHbFxSrRFazi',
            'x-ig-app-id': '1217981644879628',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': f'https://www.instagram.com/{insta_link}/',
            'accept-language': 'en-US,en;q=0.9',
        }

        params = (
            ('query_hash', '56a7068fea504063273cc2120ffd54f3'),
            ('variables', f'{{"id":"{instagram_id}","first":100}}'),
        )

        response = requests.get('https://www.instagram.com/graphql/query/', headers=headers, params=params)
        rs = response.json()['data']['user']['edge_owner_to_timeline_media']['edges']
        for r in rs:
            if r['node']['__typename'] == 'GraphImage':
                image_links.append(r['node']['display_url'])
        image_links = image_links[range_of_images[0]-1:range_of_images[-1]]
        for num,image_link in enumerate(image_links,start=1):
            while True:
                try:
                    myfile = requests.get(image_link,headers=headers)
                    break
                except:
                    time.sleep(2)
                    continue

            open(f'instagram_images/{category}/{insta_link}_{num}.jpg', 'wb').write(myfile.content)
            sys.stdout.write(".")
            sys.stdout.flush()
            insta_images_links.append((image_link))
            # insta_dict[f'image_{num}_link'] = image_link
            # if num in range_of_images:
            insta_dict[f'image_{num}_link'] = f'{insta_link}_{num}.jpg'
            dict3[index]=pd.DataFrame(insta_dict,index=[0])
            already_scraped.append(insta_id)
    else:
        for num in range(1,range_of_images[-1]+1):
            insta_dict[f'image_{num}_link'] = f'{insta_link}_{num}.jpg'
            try:
                dict3[index]=pd.DataFrame(insta_dict,index=[index])
            except:
                dict3[index]=pd.DataFrame(insta_dict)[:1]
    insta_dict = {}
    df4 = pd.concat(dict3.values(),axis=0,ignore_index=True,sort=True)
    print(f'\nImages downloading completed for {insta_link}.')
    maxi = []
    for i in dict3.values():
        maxi.append(i.shape)
    maxim = sorted(maxi,key=lambda x: x[1], reverse=True)[0]
    for i in dict3.keys():
        if dict3[i].shape == maxim:
            k = i
            break
    df4 = df4.reindex(columns=dict3[k].columns)
    df4.to_excel('instagram_images_links.xlsx',index=False)

df1 = pd.concat(dict3.values(), axis=0, ignore_index=True,sort=True)
maxi = []
for i in dict3.values():
    maxi.append(i.shape)
maxim = sorted(maxi,key=lambda x: x[1], reverse=True)[0]
for i in dict3.keys():
    if dict3[i].shape == maxim:
        k = i
        break
df1 = df1.reindex(columns=dict3[k].columns)
# df1['Plus Codes'] = df['Plus Codes'].str.split(',').str[0]
df1.to_excel('instagram_images_links.xlsx',index=False)
print('Instagram images links saved in excel file named as "instagram_images_links.xlsx".')
