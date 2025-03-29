import csv
import string

from mwcleric import AuthCredentials
from mwcleric import WikiggClient

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

    #def __init__(self):
        #credentials = AuthCredentials(user_file="me")
        # the following login has been changed to edit gg.wiki.gg rather than sorcererbyriver.wiki.gg
        # gg.wiki.gg is our sandbox wiki that anyone may edit for any reason to test scripts
        # so while you are testing your code, you can leave this as-is and view changes at gg.wiki.gg
        # then change it to your wiki afterwards
        #self.site = WikiggClient('test', credentials=credentials)


    def run(self):
        # open an existing file for reading -
        csvfile = open('character_index.csv', newline='')

        # make a new variable - c - for Python's CSV reader object -
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

            print(wikitext)

                
            

            #TODO: ignore empty rows and columns
            page_name = row[0]
            page = self.site.client.pages[page_name]
            page_text = WIKITEXT.format(
                
            )

            print(page)

            # this is the general form for saving a page
            # the page is a Page object gotten from site.client.pages[page_name]
            # page_text is the text you want to save
            # summary is the edit summary to use
            page.save(page_text, summary=self.summary)

        csvfile.close()

    @staticmethod
    def get_recipe_text(info):
        if len(info['ingredients']) == 0:
            # We could also choose to always return something here, and simply sometimes
            # have an empty |Recipe= parameter in the item infobox.
            # That would simplify the code a bit and not really cause any problems,
            # I just wanted to show a slightly more complex operation that you can simplify
            # rather than the other way around
            return ''
        # when doing string.format, {{ will be condensed down to {
        # so there are often a lot of { and } when you put wikitext here
        recipe_string = '{{{{RecipePart|item={ing}|quantity={q}}}}}'
        ingredients = ''.join(
            [recipe_string.format(ing=string.capwords(x['ingredient']), q=x['quantity']) for x in info['ingredients']])
        return f'|Recipe={ingredients}\n'

    def get_builds_into_text(self, item):
        for _, other in self.data.items():
            for ing in other['ingredients']:
                if ing['ingredient'] == item:
                    # as this string won't be in any string.format call, there is
                    # no need to escape the open & closing braces here
                    return '== Builds into ==\n{{BuildsInto}}'
        return ''


if __name__ == '__main__':
    Creator().run()
