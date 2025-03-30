import csv
import string
import os
from dotenv import load_dotenv

from mwcleric import AuthCredentials
from mwcleric import WikiggClient

#actually not used, just here for reference
WIKITEXT = """{{Example character infobox
|title={{PAGENAME}}

|sections=General Info, Game Info, Biography, Voice Acting

|General Info=Title,Speaking Name,AKA,Role
|Game Info=Affiliation, In-Game Location, First Appearance
|Biography=Age, Nationality, Ethnicity 
|Voice Acting=Pre-Release, Original Release, Final Cut 

|Title = {title}
|Speaking Name = {s_name}
|AKA = {aka}
|Role ={role}

|Affiliation = {aff}
|In-Game Location = {location}
|First Appearance = {appearance}

|Age = {age}
|Nationality = {nationality}
|Ethnicity ={ethnicity})

|Prerelease = {pre_release}
|Original Release={og_release}
|Final Cut = {final_cut}}}
"""

class Creator:
    summary = 'Creating new pages from data file'

    def __init__(self):
        credentials = AuthCredentials()
        # the following login has been changed to edit gg.wiki.gg rather than sorcererbyriver.wiki.gg
        # gg.wiki.gg is our sandbox wiki that anyone may edit for any reason to test scripts
        # so while you are testing your code, you can leave this as-is and view changes at gg.wiki.gg
        # then change it to your wiki afterwards
        self.site = WikiggClient('test', credentials=credentials)


    def run(self):
        # open an existing file for reading -
        csvfile = open('character_index_test.csv', newline='')

        # make a new variable - table - for Python's CSV reader object -
        table = csv.reader(csvfile)
        wikitext = '{{Example character infobox'
        iter = 0
        for row in table:

            if iter == 0:
                iter += 1
                continue
            
            data = {
                "title": str(row[1]),
                "s_name": str(row[2]),
                "aka": str(row[3]),
                "role": str(row[4]),
                "aff": str(row[6]),
                "location": str(row[7]),
                "appearance": str(row[8]),
                "age": str(row[10]),
                "nationality": str(row[11]),
                "ethnicity": str(row[12]),
                "pre_release": str(row[14]),
                "og_release": str(row[15]),
                "final_cut": str(row[16])
            }

            for key,value in data.items():
                if value == "":
                    continue
                wikitext += "\n"
                wikitext += "|" + str(key) + " = " + str(value)

            wikitext += "}}"

            #print(wikitext)

            page_name = row[0]
            page = self.site.client.pages[page_name]
            page_text = wikitext

            print(page)

            # this is the general form for saving a page
            # the page is a Page object gotten from site.client.pages[page_name]
            # page_text is the text you want to save
            # summary is the edit summary to use
            page.save(page_text, summary=self.summary)

        csvfile.close()

if __name__ == '__main__':
    Creator().run()
