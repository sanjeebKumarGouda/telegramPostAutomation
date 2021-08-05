# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 10:22:57 2021

@author: Sanjeeb
"""


from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import datetime
import sys
from os.path import isfile, join
from os import listdir
import os
from df2gspread import df2gspread as d2g
from selenium.webdriver.common.action_chains import ActionChains


##### Reading in Google Spreadsheets
def read_google_spreadsheet(sheet_name,worksheet_name,column_list):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Sanjeeb\Desktop\Gramoday\7fbPosting\Google_Spreadsheet_Data-a1102009ecbb.json", scope)
#   creds = ServiceAccountCredentials.from_json_keyfile_name('C:\Users\Sud\Downloads\sudwhatsapp\Whatsapp-df6ca9484ba5.json', scope)
    client = gspread.authorize(creds)
    price_sheet = client.open(sheet_name).worksheet(worksheet_name)
    price_values = price_sheet.get_all_values()
    price_df = pd.DataFrame(price_values[1:], columns = column_list)
    return price_df

##### Writing in Google Spreadsheets
def write_to_google_spreadsheet(sheet_name,df,spreadsheet_key):
    scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
    creds = ServiceAccountCredentials.from_json_keyfile_name(r"C:\Users\Sanjeeb\Desktop\Gramoday\7fbPosting\Google_Spreadsheet_Data-a1102009ecbb.json", scope)
    client = gspread.authorize(creds)
    wks_name = sheet_name
    d2g.upload(df, spreadsheet_key, wks_name, credentials=creds,start_cell = 'A1',row_names=False)
    
    
if __name__ == "__main__":
    
    my_date = datetime.date.today().weekday()
    date_today = datetime.date.today()
    print(date_today)
    #print(my_date)
    l1 = [0,1,2,3,4,5,6]
    l2 = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
    week_day_dict = dict(zip(l1,l2))
    #print(week_day_dict)
    print(week_day_dict[my_date])

    PATH = "C:\Program Files (x86)\chromedriver.exe"
    #options = Options()
    ##### Handling of Allow Pop Up In Facebook
    options = Options()
    options.add_argument("--disable-infobars")
    options.add_argument("start-maximized")
    #options.add_argument("--headless")
    options.add_argument("--disable-extensions")

    # Pass the argument 1 to allow and 2 to block
    options.add_experimental_option("prefs", { 
        "profile.default_content_setting_values.notifications": 2 
    })

    driver = webdriver.Chrome(chrome_options=options, executable_path=PATH)
    driver.get('https://web.telegram.org/k/')
    owner_name = "Sanjeeb"
    print("Waiting 35 sec to scan QR code for LogIN")
    time.sleep(35)
    
    
    ## Identifying the groups to be posted on
    df_combined = read_google_spreadsheet("Social_Media_Groups","groupDescr",["groupID","groupName","platform","is_gramoday_group (1/0)","dateOfAddition (YYYY-MM-DD)","groupURL","#groupMembers","groupCropCategory","groupCommodity","groupState","groupOccupation","groupLanguage","addedBy","groupEntrantID","dayOfPosting","postCaption","isPosted (1/0)"])
    groupPosting_monitoring_df = read_google_spreadsheet("Team KPI Metrics","groupPosting_monitoring",["dateOfPosting","addedBy","platform","groupCropCategory","groupCommodity","#Impressions"])
    df_combined = df_combined[df_combined["platform"] == "telegram"]
    df_combined = df_combined[(df_combined["addedBy"] == owner_name) & (df_combined["dayOfPosting"] == week_day_dict[my_date])]
    print(df_combined.head(10))
    group_list = list(df_combined["groupName"])

    group_language_dict = pd.Series(df_combined["groupLanguage"].values,index = df_combined["groupName"]).to_dict()
    # group_url_dict = pd.Series(df_combined["groupURL"].values,index = df_combined["groupName"]).to_dict()
    postCaption_dict = pd.Series(df_combined["postCaption"].values,index = df_combined["groupName"]).to_dict()
    category_dict = pd.Series(df_combined["groupCropCategory"].values,index = df_combined["groupName"]).to_dict()
    commodity_dict = pd.Series(df_combined["groupCommodity"].values,index = df_combined["groupName"]).to_dict()
    impression_dict = pd.Series(df_combined["#groupMembers"].values,index = df_combined["groupName"]).to_dict()
    # group_dict = pd.Series(df_combined["groupName"].values,index = df_combined["groupName"]).to_dict()
    lst_combine = []
    
    for groups in group_list:
        language = group_language_dict[groups].lower()
        commodity = commodity_dict[groups].lower()
        category = category_dict[groups].lower()
        # url = group_url_dict[groups]
        impression = impression_dict[groups]
        try:
            # Clicking search botton
            search_box = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-left']/div[1]/div[1]/div[1]/div[2]/input[1]")))
            search_box.click()
            search_box.send_keys(groups)
            
            # Group click
            group_click = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//body[1]/div[2]/div[1]/div[1]/div[1]/div[1]/div[2]/div[2]/div[2]/div[1]/div[1]/div[1]/div[1]/div[1]/ul[1]/li[1]/div[1]")))
            group_click.click()
            
            # click message box
            messageBox_click = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[1]/div[6]/div[1]/div[1]")))
            messageBox_click.click()
            # report = "It is a test onion message\nThis is newline of test onion message"
            report = postCaption_dict[groups]
            for part in report.split('\n'):
                messageBox_click.send_keys(part)
                ActionChains(driver).key_down(Keys.SHIFT).key_down(Keys.ENTER).key_up(Keys.SHIFT).key_up(Keys.ENTER).perform()
            #messageBox_click.send_keys(Keys.ENTER)
            
            # click Attachment
            attachment = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//body/div[@id='page-chats']/div[@id='main-columns']/div[@id='column-center']/div[1]/div[1]/div[4]/div[1]/div[1]/div[6]/div[2]")))
            attachment.click()
            
            # click Photo/Video
            photo_click = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//span[contains(text(),'Photo or Video')]")))
            # webdriver.ActionChains(driver).move_to_element(photo_click).click(photo_click).perform()
            driver.execute_script("arguments[0].click();", photo_click)
            
            # Uploading Photo
            key = str(category + "_" + commodity + "_" + language)
            exe_dict = {"vegetables_potato_hindi":"vegetables_potato_hi", "vegetables_potato_english":"vegetables_potato_en", 
                        "vegetables_onion_hindi":"vegetables_onion_hi", "vegetables_onion_english":"vegetables_onion_en",
                        "vegetables_all_hindi":"vegetables_all_hi", "vegetables_all_english":"vegetables_all_en"}
            i = exe_dict[key]
            path = "C:\\Users\\Sanjeeb\\Downloads\\push_messages_new\\{0}\\{1}\\{2}\\{3}.exe"
            print(path.format(category,commodity, language, i))
            #time.sleep(20)
            os.system(path.format(category,commodity, language, i))
            
            print("Waiting for 10 sec to attach file\n")
            time.sleep(10)
            
            
            # click SEND button
            click_send = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"/html/body/div[5]/div/div[1]/button/div")))
            print("POST button found\n")
            driver.execute_script("arguments[0].click();", click_send)
            # webdriver.ActionChains(driver).move_to_element(click_send).click(click_send).perform()
            
            print("Waiting for 20 sec after clicking POSt botton\n")
            time.sleep(20)
            print("Congratulation you automated Telegram Post!!!")
            lst = [date_today, owner_name, "telegram", category, commodity, impression]
            lst_combine.append(lst)
            
        
        except Exception as e:
            print("Could not send to group")
            print(e)
            
    df_append = pd.DataFrame(lst_combine, columns=["dateOfPosting","addedBy","platform","groupCropCategory","groupCommodity","#Impressions"])
    df1 = df_append.groupby(["dateOfPosting","addedBy","platform","groupCropCategory","groupCommodity"])
    df1.sum().to_csv(r"C:\Users\Sanjeeb\Desktop\Gramoday\8tgPosting\impression.csv")
    df1 = pd.read_csv(r"C:\Users\Sanjeeb\Desktop\Gramoday\8tgPosting\impression.csv")
    
    groupPosting_monitoring_df_updated = pd.concat([groupPosting_monitoring_df, df1])
    groupPosting_monitoring_df_updated = groupPosting_monitoring_df_updated.reset_index(drop=True)
    groupPosting_monitoring_df_updated.drop_duplicates(inplace=True)
    write_to_google_spreadsheet("groupPosting_monitoring",groupPosting_monitoring_df_updated,"1CuMsHfynafgUVvd-2dRATKg6K79hW7oaqBaTzgHJQ4o")
    
    driver.quit()