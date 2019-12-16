###
### This is a pretty useless tool that everytime I start my computer will tell
### me what food my school will serve.
###
import webFetch, datetime, json, string, random

### Return the day of the week as an integer, where Monday is 0 and Sunday is 6. (Copy pasta from docs)
weekday = datetime.datetime.today().weekday()
STD_ERROR = "__ERROR__"

def convert(link):
	where = link.find('?')
	url = ""
	#correctDomainCheck = url.find("onyolo.com")
	#if correctDomainCheck > 14 or correctDomainCheck < 0:
	#	return (" E1", STD_ERROR)
	#del correctDomainCheck
	if where < 0:
		if link.find("/message") > 0:
			url = link[:link.find("/message")] + "?w=x"
			return (link, url)
		else:
			return (" E2", STD_ERROR)
	url = link[:where] + "?w=x"
	link = link[:where] + "/message"
	return (link, url)

def newCookie():
	### Generates a new cookie.
	cookie = ''.join(random.choices(string.ascii_letters + string.digits, k=22))
	return cookie

def refresh_header(url, cookie, size):
	header = {
		"Accept": "application/json, text/plain, */*",
		"Accept-Encoding": "gzip, deflate, br",
		"Accept-Language": "en-US,en;q=0.5",
		"Connection": "keep-alive",
		"Content-Length": str(57 + int(size) + 1),
		"Content-Type": "application/json;charset=utf-8",
		"Cookie": f"popshow-temp-id={cookie}",
		"DNT":"1",
		"Host": "onyolo.com",
		"id=": str(cookie),
		"Cache-Control": "no-cache",
		"Referer": url,
		"User-Agent": "Mozilla/5.0 (X11; Windows NT 6.1; rv:60.0) Gecko/20100101 Firefox/60.0"
	}
	return header

def getDay(str_day = "Måndag"):
	r = webFetch.Fetch("https://skolmaten.se/storsjo-gymnasiet/")
	relevant = r.getAfter(f'<span class="weekday">{str_day}</span>', 900)
	relevant = relevant.split('<div class="date">', 1)[0]
	food = ""
	try:
		food = r.getBetween(relevant, "<span>", "</span>")
	except:
		try:
			food = r.getBetween(relevant, '<div class="items"><p class="reason">', "</p></div>")
		except:
			exit()
	date = r.getBetween(relevant, '<span class="date">','</span>')
	date = f"{str_day} ({date})"
	return (f"Mat idag, {date} är : {food}")

if __name__ == "__main__":

	rv = ""
	if weekday == 0: rv = getDay()
	elif weekday == 1: rv = getDay("Tisdag")
	elif weekday == 2: rv = getDay("Onsdag")
	elif weekday == 3: rv = getDay("Torsdag")
	elif weekday == 4: rv = getDay("Fredag")
	else: exit()
	cookie = newCookie()
	target, url = convert("https://onyolo.com/wrOgsAF9rT?w=testing".strip())
	if url == STD_ERROR:
		print("Convertion error!" + target)
		exit()
	payload = {"text":f"{rv}","cookie":f"{cookie}", "wording":"x"}
	header = refresh_header(url, cookie, len(rv))
	r = webFetch.requests.post(target, data=json.dumps(payload), headers=header)
	exit()
