from flask import Flask, request, flash, render_template, flash, redirect, url_for, session, Blueprint
from flask_session import Session
from app import *
import requests
from bs4 import BeautifulSoup
import json


flipkart = Blueprint('flipkart', __name__,url_prefix='/scrap/flipkart')


@flipkart.route("reviews/<string:pid>", methods=['POST', 'GET'])
def getReviews(pid):
    review = True
    reviews_text =[]
    reviews_title=[]
    for i in range(1):
        page = requests.get('https://www.flipkart.com/q/product-reviews/q?pid='+pid+'&page='+str(i))
        soup = BeautifulSoup(page.text, 'html.parser')
        pos1 = int(str(soup).find('\"readReviewsPage\":'))
        pos2 = int(str(soup).find('\"recentlyViewed\"'))
        string = '{'+str(soup)[pos1:pos2]+'}rk'
        string = string.replace("}}},}rk","}}}}")
        string = json.loads(string)
        string = string['readReviewsPage']['reviewsData']['product_review_page_default_1']['data']
        for s in string:
            reviews_title.append(s['value']['title'])
            reviews_text.append(s['value']['text'])

    reviews= zip(reviews_title,reviews_text)
    return render_template("flipkart.html",**locals())


@flipkart.route("results/<string:q>", methods=['POST', 'GET'])
def getResults(q):
    results = True
    p_name=[]
    p_url=[]
    p_id=[]
    page = requests.get('https://www.flipkart.com/search?q='+q)
    soup = BeautifulSoup(page.text, 'html.parser')
    string = soup.find('script', {'id':'jsonLD'}).text
    string = json.loads(string)
    string = string['itemListElement']
    for s in string:
        p_name.append(s['name'])
        p_url.append(s['url'])
        pos1 = str(s['url']).find('?pid=')
        pos2 = str(s['url']).find('&lid=')
        id = str(s['url'])[pos1:pos2]
        id = id.replace('?pid=','').replace('&lid=','')
        p_id.append(id)
    data = zip(p_name,p_id,p_url)

    return render_template('flipkart.html',**locals())


