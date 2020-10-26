# -*- coding: utf-8 -*-
"""esg_scraping

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ZOIJFTdrQ2hmwy1gwsO6vXfXqfyemRkp
"""
from esg_env.config import HOST, PASSWORD, USERNAME, DATABASE

'''!pip -q install wikipedia
!pip -q install pymysql
!pip install selenium'''

import pymysql
import pandas as pd
import numpy as np
import wikipedia as wp
import re
from bs4 import BeautifulSoup
import requests
from datetime import date
import time
from selenium import webdriver
from selenium.webdriver import ActionChains
import config

options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
# open it, go to a website, and get results
driver = webdriver.Chrome('chromedriver',options=options)


def GetCompaniesESG():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    driver = webdriver.Chrome('chromedriver', options=options)
    wiki = wp.page("List_of_S%26P_500_companies").html().encode("UTF-8")
    df = pd.read_html(wiki)[0]

    companies = df.iloc[:, [0, 1, 3, 4]]
    results = []

    for index, row in companies.iterrows():
        company = row.values.tolist()[0]
        url = 'https://finance.yahoo.com/quote/' + company + '/sustainability?p=' + company
        text = requests.get(url).text
        soup = BeautifulSoup(text, 'html.parser')

        esg_score = soup.find("div", {"class": "Fz(36px) Fw(600) D(ib) Mend(5px)"})
        esg_risk = soup.find("div", {"class": "Fz(s) Fw(500) smartphone_Pstart(4px)"})
        esg_percentile = soup.find("span", {
            "Bdstarts(s) Bdstartw(0.5px) Pstart(10px) Bdc($seperatorColor) Fz(12px) smartphone_Bd(n) Fw(500)"})
        each_esg_score = soup.findAll("div", {"D(ib) Fz(23px) smartphone_Fz(22px) Fw(600)"})
        controversy_comment = soup.find("span", {
            "Bdstarts(s) Bdstartw(0.5px) Pstart(5px) Mstart(5px) Bdc($seperatorColor) Fz(s) Fw(b)"})
        controversy_level = soup.find("div", {"D(ib) Fz(36px) Fw(500)"})

        if esg_score is not None:
            esg_score = float(esg_score.text)
        else:
            esg_score = None
        if esg_risk is not None:
            esg_risk = esg_risk.text
        else:
            esg_risk = None
        if esg_percentile is not None:
            esg_percentile = esg_percentile.text
        else:
            esg_percentile = None
        # environment_risk, social_risk, governance_risk
        if each_esg_score is not None and each_esg_score != []:
            environment_risk = float(each_esg_score[0].text)
            social_risk = float(each_esg_score[1].text)
            governance_risk = float(each_esg_score[2].text)
        else:
            environment_risk = None
            social_risk = None
            governance_risk = None
            # controversy_comment
        if controversy_comment is not None:
            controversy_comment = controversy_comment.text.replace(' Controversy level', '')
        else:
            controversy_comment = None

        # self controversy level
        if controversy_level is not None:
            controversy_level = float(controversy_level.text)
        else:
            esg_percentile = None
        # peer controversy level
        driver.get(url)
        time.sleep(0.5)
        try:
            move_to_element_location = driver.find_element_by_xpath(
                '//*[@id="Col1-0-Sustainability-Proxy"]/section/div[2]/div[2]/div/div/div/div[2]/div/div[1]')
            ActionChains(driver).move_to_element(move_to_element_location).perform()
            data_in_the_bubble = driver.find_element_by_xpath('//*[@id="dropdown-menu"]/div[3]/div[3]/div')
            hover_data = data_in_the_bubble.get_attribute("innerHTML")
            matches = re.findall("\d+(?:\.\d+)?", hover_data)
            peer = float(matches[0])
        except:
            peer = None
        execution_date = date.today()

        result = row.values.tolist() + [esg_score, esg_risk, esg_percentile, environment_risk, social_risk,
                                        governance_risk, controversy_comment, controversy_level, peer, execution_date]

        results.append(result)
    return results

def GetESGInMysql():
    db = pymysql.connect(host=HOST, port=3306, user=USERNAME,
                         password=PASSWORD, database=DATABASE, charset='utf8')
    cursor = db.cursor()
    esgs = GetCompaniesESG()
    sql = "INSERT INTO esg_company (Symbol,Security_name,GICS_Sector,GICS_Sub_Industry,ESG_Score,ESG_Risk,ESG_Percentile,Environment_Risk,Social_Risk,Governance_Risk,Controversy_comment,Controversy_level,Peer_Controversy_level,execution_date) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"  # 插入语句
    timebegin = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())  # record the begin time for find the error

    try:
        cursor.executemany(sql, esgs)
        db.commit()
        print(timebegin + "success")
    except:
        db.rollback()
        print(timebegin + "fail！")

    cursor.close()
    db.close()


'''# record the scraping
time1=time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
print("start scraping"+time1)
# Run scraping every day.
schedule.every().day.at('8:00').do(GetESGInMysql) 
# Check the processing, while good, run script.
while True:
    schedule.run_pending()
    time.sleep(1)    '''