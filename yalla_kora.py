import requests
from bs4 import BeautifulSoup
import csv


date =  input("Enter the date(MM/DD/YYYY): ") #"12/19/2022"

page = requests.get(f"https://www.yallakora.com/match-center/?date={date}")

def main(page):
    
    src = page.content # returns the byte code
    soup = BeautifulSoup(src, "lxml") #(byte code, parser) convert the code to be displayed in html view
    
    # Get championships divs 
    championships = soup.find_all("div", {"class" : "matchCard"}) # take only the classes of match card (tagtype, {filter})
    match_details = []
    
    def get_match_info(championchips):
        
        champ_title = championchips.find("h2").text.strip() # we used find() because we search for one element
        
        # contents() return list of childs for the div and we search for the element in the order
        # we used index of 1 because index of 0 is a space
        # champ_title = championchips.contents[1].find("h2").text.strip()
        
        all_matches = championchips.find_all("li") # return all the list items in the given championship
        
        no_of_matches = len(all_matches)
        
        
        
        for i in range(no_of_matches):
            
            # Get teams names
            team_A = all_matches[i].find("div", {"class":"teams teamA"}).find("p").text.strip()        
            team_B = all_matches[i].find("div", {"class":"teams teamB"}).find("p").text.strip()        
            
            # Get the score
            match_res = all_matches[i].find('div', {'class':"MResult"}).find_all('span', {'class':"score"})
            score = f" {match_res[1].text.strip()} - {match_res[0].text.strip()}"
            
            # Get Match Time
            
            time = all_matches[i].find('div', {'class':"MResult"}).find('span', {'class': 'time'}).text.strip()
                
            # Get Match Channel
            channel = all_matches[i].find('div', {'class':"channel icon-channel"}) 
            if channel is None:
                channel = "غير معروفة"
            else:
                channel = channel.text.strip()
            
            # Get the round or the week
            
            week = all_matches[i].find('div', {'class':"date"}).text.strip()
            
            match_details.append({
                "البطولة" : champ_title,
                "الجولة / الأسبوع" : week,
                "الفريق أ" : team_A,
                "الفريق ب" : team_B,
                "ميعاد المباراة" : time,
                "النتيحة" : score,
                "القناة" : channel
            })
            
            
            
        
    for i in range(len(championships)):
        
        get_match_info(championships[i])
        
    keys = list(match_details[0].keys())
    
    with open(r"D:\Programming\Web Scraping\matches.csv", "w" ,encoding="utf-8-sig" ,newline='') as output:
        dict_writer = csv.DictWriter(output, fieldnames=keys)
        dict_writer.writeheader()
        
        dict_writer.writerows(match_details)
        print("process done")

main(page)