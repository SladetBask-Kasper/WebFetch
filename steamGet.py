from webFetch import *
import re, urllib.parse
def rm_spaces(x): return re.sub(r"\s+", "", x)

STD_LISTING_URL = "https://steamcommunity.com/market/listings/730/"

URLS = ["https://steamcommunity.com/market/listings/730/AWP%20%7C%20Dragon%20Lore%20%28Battle-Scarred%29",
"https://steamcommunity.com/market/listings/730/Glock-18%20%7C%20Water%20Elemental%20%28Factory%20New%29",
"https://steamcommunity.com/market/listings/730/P90%20%7C%20Asiimov%20%28Factory%20New%29",
"https://steamcommunity.com/market/listings/730/StatTrak%E2%84%A2%20Glock-18%20%7C%20Water%20Elemental%20%28Factory%20New%29",
"https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Redline%20%28Battle-Scarred%29",
"https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Predator%20%28Battle-Scarred%29",
"https://steamcommunity.com/market/listings/730/AK-47%20%7C%20Asiimov%20%28Battle-Scarred%29",
"https://steamcommunity.com/market/listings/730/AK-47%20%7C%20The%20Empress%20%28Battle-Scarred%29",
"https://steamcommunity.com/market/listings/730/AWP%20%7C%20PAW%20%28Factory%20New%29",
"https://steamcommunity.com/market/listings/730/AWP%20%7C%20Asiimov%20%28Well-Worn%29",
"https://steamcommunity.com/market/listings/730/AWP%20%7C%20Redline%20%28Well-Worn%29"]

def removeAsciiValues(txt): return str(urllib.parse.unquote(
	txt.split(STD_LISTING_URL,1)[1]))

def valutaTranslation(txt):
	txt = txt.replace(",--€", " Euro").replace("--€", " Euro").replace("€",
		" Euro").replace("zł", " Polsk Zloty").replace("$", "").replace("kr", " kr").replace("USD",
		" USD").replace("₴", " Ukrainian Hryvnia").replace("pуб",
		" Rysk Rubel").replace("000", " 000").replace("₸", " Kazakstansk Tenge")
	if "¥" in txt:
		txt = txt.replace("¥","") + " Yen"
	elif "CDN$" in txt:
		txt = txt.replace("CDN$", "") + " Kanadensisk Dollar"
	elif "P" in txt:
		txt = txt.replace("P", "") + " Peso"
	elif "Rp" in txt:
		txt = txt.replace("Rp", "") + " Nya Rupiah"#Indonesisk Rupie
	elif "HK" in txt:
		txt = txt.replace("HK", "") + " Hongkongdollar"
	elif txt[0] == "R":
		try:
			tmp = int(txt[1])
		except:
			pass
		else:
			txt = txt.replace("R", "") + " Sydafrikansk Rand"
	return txt

def getSteamItem(url):
	getRequest = Fetch(url)
	x = ""
	try:
		x = getRequest.getAfter('<span class="market_table_value">', 103)
	except IndexError:
		return "IndexError"
	final = rm_spaces(x[-15:])
	if "<" in final:
		final = final.split("<", 1)[0]
	final = valutaTranslation(final.replace(".", ","))
	return final

output = ""
for i in URLS:
	if not i == 1:
		x = removeAsciiValues(i)
		y = getSteamItem(i)
		z = " [{}]{}{}\n".format(x, " "*((55-len(x))+1), y)
		output += z
		print(z, end="")
