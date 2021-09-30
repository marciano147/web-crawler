
from bs4 import BeautifulSoup
import requests
import pandas as pd 


headers ={
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36'
}
baseurl = 'https://www.feedipedia.org/'
r = requests.get('https://www.feedipedia.org/content/feeds?category=All')
soup = BeautifulSoup(r.content, 'html.parser')
feedlist = soup.find_all('span', class_='field-content')
# all links of feeds
feedlinks = []
for item in feedlist:
   for link in item.find_all('a', href=True ):
    feedlinks.append(baseurl+link['href'])

# funtion to strip text if it exists
def textstripp(extracted):
    if (extracted):
        return extracted.text.strip() 
    else:
        return 'there doesnt exist'

# fucntion to strip text and split if it exitss
def textsplittrip(extracted):
    if (extracted):
        return extracted.text.strip().split(';') 
    else:
        return 'there doesnt exist'

def fixtext(extracted):
    if(extracted == 'there doesnt exist' or  extracted == 'Doesnt exist'):
        return 'Doesnt exist'
    if (extracted == 'This type of animal does not eat this food' ) :
        return 'This type of animal does not eat this food'
    rumi = ' ' 
    for item in extracted.find_all('p'):
      rumi = rumi + item.text + '\n' + '\n'
    return(rumi)


def animaleater(extracted):
    if (extracted):
        return extracted
    else:
        return 'This type of animal does not eat this food'


def exists(extracted):
    if (extracted):
        return extracted
    else:
        return 'Doesnt exist'

def justforh4(extracted):
    if(extracted == 'there doesnt exist' or  extracted == 'Doesnt exist'):
        return 'Doesnt exist'
    if (extracted == 'This type of animal does not eat this food' ) :
        return 'This type of animal does not eat this food'
    rumi = ' ' 
    for item in extracted:
      rumi = rumi + item.text + '\n' + '\n'
    return(rumi)
    
feedlist = []
# testlink = 'https://www.feedipedia.org/node/275'
for link in feedlinks:
    r2 = requests.get(link, headers=headers)
    soup2 = BeautifulSoup(r2.content, 'html.parser')
# name of feed
    namefo = textstripp(soup2.find('h1', class_='art-postheader'))
    if(namefo == 'there doesnt exist'):
      continue
    # print(namefo)
    # common names of feed
    comom = textsplittrip(soup2.find("div", attrs={'class':'field-item even', 'property':'schema:about'} ))
    # synonims of feed
    synonimss = textstripp((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-synonyms-display field-type-computed field-label-abovec'})))

    # description of feed
    description = fixtext(exists(soup2.find("div", attrs={'class':'field-item even', 'property':'schema:description'} ))).strip()


    # this is the references of feed
    try:
        references = (soup2.find('table', attrs={'class':'views-table cols-0'}))
        referencelist = []
        for item in references.find_all('tr'):
            name = (item.find_all('a')[0]).text
            link = item.find_all('a')[1]['href'] if len(item.find_all('a')) > 1 else 'no link'
            referencelist.append([name, link])
    except:
        referencelist = 'No References'
    
    # this is the related feeds
    relatedfeeds = soup2.find('div', attrs={ 'class':'field field-name-field-datasheet-list field-type-viewfield field-label-abovec'})
    relatedfeedlist = []
    for item in relatedfeeds:
      for link in item.find_all('a'):
       relatedfeedlist.append(link.string + '  ' + baseurl+link['href'] )

    # this is the chemicals components
    table = soup2.find_all('tr', attrs={'class':'tableheader'})
    tableheade=[]       
    for item in table:
        tableheade.append(item.text.split('\n')[0])
    # all rrelevant tables
    try:
     chemicals = (soup2.find('table', attrs={'style':'width:100%;'}))
    # a different and more organized way which, I coulndt get 100%
    # All_values = dict.fromkeys(tableheade, [])
     All_values = dict.fromkeys(tableheade, " ")
     currentvals= " "
     for item in chemicals.find_all('tr'):
         if (item('td')[0].text in tableheade ):
               currentheader = item('td')[0].text
               All_values[currentheader] =  All_values[currentheader] + 'This is the description of numbers by order: Unit, Avg, SD: standard deviation, Min, Max, Nb: number of values ' + '\n'
               continue  
         for index, val in enumerate(item('td')):
             if(index == 7):
                  continue
             if(val.text == '\xa0' or val.text == 'None' ):
                 currentvals = currentvals + '(No Value)' + ', '
                 continue
             if(val.string):
                 currentvals = currentvals + val.string + ', '
             else : 
                currentvals = currentvals + '(No Value)' + ', '
                continue
         currentvals = currentvals[:-2]
         All_values[currentheader] = All_values[currentheader] +'\n' + currentvals + '.' + '\n'
         currentvals = " "
    except:
        chemicals = 'No Table available'
    # nutritional attributes
    nutritional = fixtext(exists((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-nutrition-display field-type-computed field-label-abovec'})))).strip()
    # potential constraints 
    Potentialcomstraints = fixtext(exists((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-caution-display field-type-computed field-label-abovec'})))).strip() 
    # How affects animals
    horses  = justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-horses-display field-type-computed field-label-abovec'}))))).strip()
    ruminants = justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-ruminants-display field-type-computed field-label-abovec'}))))).strip()
    pigs= justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-pigs-display field-type-computed field-label-abovec'}))))).strip()
    poultry = justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-poultry-display field-type-computed field-label-abovec'}))))).strip()
    rabbit = justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-rabbits-display field-type-computed field-label-abovec'}))))).strip()
    otherspecies =justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-other-display field-type-computed field-label-abovec'}))))).strip()
    fish = justforh4(animaleater(((soup2.find("div", attrs={'class':'field-items even', 'class':'field field-name-field-fishes-display field-type-computed field-label-abovec'}))))).strip()
    AnimalsWhoeat = {
        'Horses and Donkets': horses,
        'Ruminants' : ruminants,
        'Pigs': pigs,
        'Poultry': poultry,
        'Rabbits' : rabbit,
        'Fish' : fish,
        'Other Species' : otherspecies 

    }

    Feed = {
        'name': namefo,
        'references' : referencelist,
        'common names' : comom,
        'Synonyms' : synonimss,
        'Related feeds' : relatedfeedlist,
        'Description': description,
        'Chemicals content' : All_values,
        'Animals which eat this': AnimalsWhoeat,
        'Nutritional attributes' : nutritional,
        'Potential Comstraints' : Potentialcomstraints
        }

    feedlist.append(Feed)
   

df = pd.DataFrame(feedlist) 
df.to_csv('feedipedia.csv', index=False)
df.to_csv('feedipediaFalse.csv', index=False, header=False)

    # not in use
    # for header in tableheade:
    #  print(header)
    #  print(All_values[header])
            


    # this is used to take off the title word from it
    # titlename = ((soup2.find_all("div", attrs={'class':'field-label' })))
    # alltitles = ' '
    # for item in titlename:
    #  alltitles = alltitles + ' ' + item.text
    # print(alltitles)
            


  
