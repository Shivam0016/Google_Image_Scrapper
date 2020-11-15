from flask import Flask,render_template,request
from bs4 import BeautifulSoup
from selenium import webdriver
import time
import os
import requests

app=Flask(__name__)

DRIVER_PATH='./chromedriver'
SEARCH_TERM=""
IMAGE_COUNT=5


def search_and_download():
    counter=1
    with webdriver.Chrome(executable_path=DRIVER_PATH) as wd:
        global SEARCH_TERM, IMAGE_COUNT

        target_folder=os.path.join('./images','_'.join(SEARCH_TERM.split(" ")))

        if not os.path.exists(target_folder):
            os.makedirs(target_folder)

        k="https://www.google.com/search?q={0}&tbm=isch".format(SEARCH_TERM)
        print(SEARCH_TERM,"-->",k)
        wd.get(k)
        thumbnail_images=wd.find_elements_by_css_selector("img.Q4LuWd")


        for single_thumbnail in thumbnail_images[:IMAGE_COUNT]:
            single_thumbnail.click()
            time.sleep(2)

            actual_image=wd.find_elements_by_css_selector("img.n3VNCb")
            for image in actual_image:
                if image.get_attribute('src') and 'http' in image.get_attribute('src'):
                    im=image.get_attribute('src')
                    material=requests.get(im).content

                    f=open(os.path.join(target_folder,'jpg'+'_'+str(counter)+'.jpg'),'wb')
                    f.write(material)
                    f.close()

                    counter += 1
@app.route('/',methods=['GET','POST'])
def index():

    if request.method=="POST":
        global SEARCH_TERM,IMAGE_COUNT
        SEARCH_TERM= request.form["search_term"]
        IMAGE_COUNT=int(request.form["count"])
        search_and_download()
        return "Downloaded..."

    else:
        return render_template('index.html')

if __name__=="__main__":
    app.run(debug=True)