'''
this will take URL or a list of URLs, will get the pages on the URLs and will return a list of:
*links
*emails
*IPs
used on those pages
'''
import requests, bs4, re, time, validators, json, pprint

most_common_types = ["jpg","jpeg","png","gif","css","js","html","ico","gif","pdf","doc","docx", "rar", "tar", "gz", "7z", "zip"]

def extractor(url, levelNow):
	draft_response = dict()
	draft_response["submitted_URL"] = url

	draft_response["depthLevel"] = levelNow
	draft_response["title"]=""
	draft_response["totalURLs"]=""
	draft_response["totalDomains"]=""
	draft_response["totalIPs"]=""
	draft_response["totalEmails"]=""
	draft_response["URLs"]=[]
	draft_response["Domains"]=[]
	draft_response["IPs"]=[]
	draft_response["Emails"]=[]

	pagedata = requests.get(url)
	cleanpagedata = bs4.BeautifulSoup(pagedata.text, 'html.parser')

	draft_response["title"]= cleanpagedata.title.string

	for url in re.findall("(?:(?:https?|ftp):\\/\\/)?[\\w/\\-?=%.]+\\.[\\w/\\-?=%.]+", str(pagedata.text)):
		domain = url.split("//")[-1].split("/")[0].split('?')[0]
		if domain.split(".")[-1] not in most_common_types and '-' not in domain.split(".")[-1] and len(domain.split(".")[0]) != 1:
			if validators.domain(domain):
				if domain not in draft_response["Domains"]:
					draft_response["Domains"].append(domain)

			if validators.url(url):
				if url not in draft_response["URLs"]:
					draft_response["URLs"].append(url)

	for ip in re.findall("([0-9]+\\.[0-9]+\\.[0-9]+\\.[0-9]+)", str(pagedata.text)):
		if validators.ipv4(ip):
			if ip not in draft_response["IPs"]:
				draft_response["IPs"].append(ip)

	for email in re.findall("([a-zA-Z0-9._-]+@[a-zA-Z0-9._-]+\\.[a-zA-Z0-9_-]+)", str(pagedata.text)):
		if validators.email(email):
			if email not in draft_response["Emails"]:
				draft_response["Emails"].append(email)
	    
	draft_response["totalURLs"]=len(draft_response["URLs"])
	draft_response["totalDomains"]=len(draft_response["Domains"])
	draft_response["totalIPs"]=len(draft_response["IPs"])
	draft_response["totalEmails"]=len(draft_response["Emails"])

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
