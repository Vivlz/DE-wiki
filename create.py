import csv
import string
import os
from dotenv import load_dotenv

from mwcleric import AuthCredentials
from mwcleric import WikiggClient

#Note: rate limit only allows for 47 pages to be created/updated at a time

class Creator:
    summary = 'Creating new pages from data file'
    
    def __init__(self):
        #load_dotenv()
        #username = os.getenv("USERNAME")
        #password = os.getenv("PASSWORD")
        #credentials = AuthCredentials(username=username,password=password)
        # the following login has been changed to edit gg.wiki.gg rather than sorcererbyriver.wiki.gg
        # gg.wiki.gg is our sandbox wiki that anyone may edit for any reason to test scripts
        # so while you are testing your code, you can leave this as-is and view changes at gg.wiki.gg
        # then change it to your wiki afterwards
        #self.site = WikiggClient('discoelysium', credentials=credentials)

        credentials = AuthCredentials(user_file="me")
        # the following login has been changed to edit gg.wiki.gg rather than sorcererbyriver.wiki.gg
        # gg.wiki.gg is our sandbox wiki that anyone may edit for any reason to test scripts
        # so while you are testing your code, you can leave this as-is and view changes at gg.wiki.gg
        # then change it to your wiki afterwards
        self.site = WikiggClient('discoelysium', credentials=credentials)


    def run(self):
        # open an existing file for reading -
        csvfile = open('character_index.csv', newline='')

        # make a new variable - table - for Python's CSV reader object -
        table = csv.reader(csvfile)
        
        iter = 0
        for row in table:
            wikitext = '{{Example character infobox'

            if iter == 0:
                iter += 1
                continue
   
            data = {
                "Title": str(row[1]),
                "Speaking Name": str(row[2]),
                "AKA": str(row[3]),
                "Role": str(row[4]),
                "Affiliation": str(row[6]),
                "In-Game Location": str(row[7]),
                "First Appeatance": str(row[8]),
                "Age": str(row[10]),
                "Nationality": str(row[11]),
                "Ethnicity": str(row[12]),
                "Prerelease": str(row[14]),
                "Original Release": str(row[15]),
                "Final Cut": str(row[16])
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
