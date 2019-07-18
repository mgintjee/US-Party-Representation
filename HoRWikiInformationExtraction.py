#####################################
## HoR Wiki Information Extraction ##
## Created On: 07.17.19            ## 
## Updated On: 07.17.19            ##
#####################################

# Other Imports
import requests
from bs4 import BeautifulSoup

# My Imports
import HoRWikiStateInformation

# Static Globals
HoR_WIKI_URL =  "https://en.wikipedia.org/wiki/List_of_current_members_of_the_United_States_House_of_Representatives"
TBODY_TAG = "tbody"
TR_TAG = "tr"
TH_TAG = "th"
TD_TAG = "td"
TD_DISTRICT_INDEX = 0
TD_PARTY_INDEX = 3
ELEMENT_TABLE_ID = "votingmembers"
DEMOCRATIC_KEY = "Democratic"
REPUBLICAN_KEY = "Republican"
INDEPENDENT_KEY = "Independent"

def main():
    information = ExtractInfoFromHoRWiki()
    for key in information.keys():
        print(information[key].ToString())

def ExtractInfoFromHoRWiki():
    extractedDictOfStateInformation = dict()
    html = ExtractHtmlFromUrl(HoR_WIKI_URL)
    table = ExtractTableFromHtml(html)
    rows = ExtractRowsFromTable(table)
    dictOfStateInformation = dict()

    stateIndex = 0
    for row in rows:
        data = ExtractDataFromRow(row)
        index = 0
        state = ""
        party = ""
        
        for datum in data:
            if (index == TD_DISTRICT_INDEX):
                state = datum.text.strip("\n")
                state = ExtractStateFromDistrict(state)
                
            elif(index == TD_PARTY_INDEX):
                party = datum.text.strip("\n")
                
            index += 1

        if ( state == ""):
            continue
        
        if (state in dictOfStateInformation.keys()):
            if (party in dictOfStateInformation[state].keys()):
                dictOfStateInformation[state][party] += 1
            else:
                dictOfStateInformation[state][party] = 1
                
        else:
                dictOfStateInformation[state] = dict()
                dictOfStateInformation[state][party] = 1
                
    for key in dictOfStateInformation.keys():
        seatsDemocratic = 0
        seatsRepublican = 0
        seatsIndependent = 0
        
        if(DEMOCRATIC_KEY in dictOfStateInformation[key].keys()):
            seatsDemocratic = dictOfStateInformation[key][DEMOCRATIC_KEY]
            
        if(REPUBLICAN_KEY in dictOfStateInformation[key].keys()):
            seatsRepublican = dictOfStateInformation[key][REPUBLICAN_KEY]
            
        if(INDEPENDENT_KEY in dictOfStateInformation[key].keys()):
            seatsIndependent = dictOfStateInformation[key][INDEPENDENT_KEY]
            
        StateInformation = HoRWikiStateInformation.StateInformation(key, seatsDemocratic, seatsRepublican, seatsIndependent)
        extractedDictOfStateInformation[key] = StateInformation
            
    return extractedDictOfStateInformation
    
def ExtractHtmlFromUrl(url):
    request = requests.get(url)
    html = BeautifulSoup(request.text, "html.parser")
    return html

def ExtractTableFromHtml(html):
    table = html.find("table", {"id": ELEMENT_TABLE_ID})
    return table

def ExtractRowsFromTable(table):
    rows = table.find_all(TR_TAG)
    return rows

def ExtractDataFromRow(row):
    data = row.find_all(TD_TAG)
    return data

def ExtractStateFromDistrict(district):
    counter = 0
    for char in district:
        if( IsNumeric(char)):
            break
        else:
            counter += 1
    return district[:counter]

def IsNumeric(char):
    numbers = "0123456789"
    return (char in numbers)

if __name__ == "__main__":
    main()