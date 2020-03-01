'''
this will take URL or a list of URLs, will get the pages on the URLs and will return a list of:
words with their frequency of occurence
used on those pages
'''
import requests, bs4, re, time, validators, json, pprint

def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, bs4.Comment):
        return False
    return True

def text_from_html(body):
    soup = bs4.BeautifulSoup(body, 'html.parser')
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts)  
    return u" ".join(t.strip() for t in visible_texts)

def extractor(url, levelNow):
	words = dict()

	pagedata = requests.get(url)
	text = text_from_html(pagedata.text)
	cleanpagedata = bs4.BeautifulSoup(pagedata.text, 'html.parser')

	text = ''.join([i if ord(i) < 128 else ' ' for i in text])
	for word in text.split(" "): 
	        if word not in ["[","]","{","}","(",")","\\","|","/","-"]:
		        if word in words: 
		            words[word] = words[word] + 1
		        else: 
		            words[word] = 1

	words = sorted(words.items(), key=lambda x: x[1], reverse=True)
	draft_response = dict()
	draft_response["submitted_URL"] = url
	draft_response["title"]= cleanpagedata.title.string
	draft_response["depthLevel"] = levelNow
	draft_response["words"] = words

	return draft_response


response=dict()
response["submissions"]=["https://news.ycombinator.com/", "https://gist.github.com/superfeedr/364100", "http://www.ram.org/ramblings/philosophy/spam/spammers.html"]
level = 0
response["responses"]=[]

for url in response["submissions"]:
	response["responses"].append(extractor(url, 0))

output = open("output.json", "w+")
json.dump(response,output, indent=4)
output.close()
