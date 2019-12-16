###
### GetBank av Kasper EEDAT18A
### Får till vardera banks hemsida (Se "Källor") och hämtar infromation som 
### t.ex. ränta så att du är uppdaterad.
### Det tar ungefär fem sekunder att hämta allt och skriva resultaten till en fil.
###
### Använding:
### Metod 1: kör denna fil
### Metod 2: importera denna fil
### Använding vid import:
### res_espar, res_privkonto = get_swedbank()
### res_spar = get_icabank()
### res_spar, res_lån = get_forex()
### res_spar, res_xl, res_kid = get_dansk()
### res_spar, res_fram = get_hsb()
### res_spar, res_pers = get_lf()
###  * res = resultat
###

import requests
import codecs
from datetime import date, datetime

# Källor
SWEDBANK = "https://www.swedbank.se/privat/rantor-priser-och-kurser/rantor.html"
ICABANK  = "https://www.icabanken.se/kort-och-konto/vara-konton/sparkonto/"
FOREX    = "https://www.forex.se/spara"
DANSK_SK = "https://danskebank.se/privat/produkter/sparkonton/sparkonto"
DANSK_XL = "https://danskebank.se/privat/produkter/sparkonton/sparkonto-xl"
DANSK_KD = "https://danskebank.se/privat/produkter/sparkonton/sparkonto-barn"
HSB      = "https://www.handelsbanken.se/sv/privat/spara/sparformer/sparkonton-och-rantor"
LF       = "https://www.lansforsakringar.se/jamtland/privat/bank/bli-bankkund/aktuella-rantor-och-priser/"

# Global Vars
LOG_FILE = "räntor.log"
LOG_DIR  = "logs/"
log_content_buffer = ""

def write_log():
	global log_content_buffer

	log_content_buffer = "[{}]\n".format(str(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))) + log_content_buffer
	filename = LOG_DIR + str(datetime.now().strftime("%Y-%m-%d-")) + LOG_FILE
	
	with codecs.open(filename, 'w', encoding='utf8') as f:
		f.write(log_content_buffer)
def log(txt, v=True):
	global log_content_buffer
	log_content_buffer += txt + "\n"
	if v: print(txt)

###
### Gets swedbank ränta.
### Returns as tuple
### Usage:
### res_espar, res_privkonto = get_swedbank()
###
def get_swedbank():
	r = requests.get(SWEDBANK)
	webpage = str(r.text)# teststr
	strlen1 = 7
	strlen2 = 4
	r.close()
	split_word = '- Räntan på e-sparkonto är för närvarande'
	res_espar = str(webpage.split(split_word, 1)[1])[:strlen1].strip().replace(" ", "")

	split_word = "Ränta för närvarande:" 
	res_privkonto = str(webpage.split(split_word, 1)[1])[:strlen2].strip().replace(" ", "")
	return (res_espar, res_privkonto)

###
### Gets Ica Bankens ränta.
### Returns as string
### Usage:
### res_spar = get_icabank()
###
def get_icabank():
	r = requests.get(ICABANK)
	webpage = str(r.text)
	strlen = 13
	r.close()

	split_word = 'Vår bästa sparränta just nu:&nbsp;<span>' 
	res_spar = str(webpage.split(split_word, 1)[1])[:strlen].strip().replace(" ", "").replace("<span>", "").replace("</span>", "").replace("p", "%")
	return res_spar

###
### Gets forex ränta.
### Returns as tuple
### Usage:
### res_spar, res_lån = get_forex()
### res_sparkonto = get_forex()[0]
###
def get_forex():
	r = requests.get(FOREX)
	webpage = str(r.text)
	strlen = 23
	r.close()

	split_word =  'sparkonto har en sparr&#228;nta p&#229;' 
	split_word2 = " och hela "
	res = str(webpage.split(split_word, 1)[1])[:strlen].strip().replace(" %", "%").split(split_word2)
	res_spar = res[0]
	lan_kund = res[1]
	return (res_spar, lan_kund)

###
### Gets danske bank ränta.
### Returns as tuple
### Usage:
### res_spar, res_xl, res_kid = get_dansk()
### URL VARS:
### DANSK_SK
### DANSK_XL
### DANSK_KD
###
def get_dansk():
	strlen = 6 # alla har samma format på procent
	webpage = requests.get(DANSK_SK)
	sk = str(webpage.text)
	webpage = requests.get(DANSK_XL)
	xl = str(webpage.text)
	webpage = requests.get(DANSK_KD)
	kd = str(webpage.text)
	
	webpage.close()

	split_word1 =  'Upp till 100 000 kr</td><td style="text-align: left;">' # SK
	split_word2 = "Kontot har f.n en ränta på "
	split_word3 = "<p>Kontot har f.n en ränta på "
	res_spar = str(sk.split(split_word1, 1)[1])[:strlen].strip().replace(" %", "%")
	res_xl   = str(xl.split(split_word2, 1)[1])[:strlen].strip().replace(" %", "%")
	res_kid  = str(kd.split(split_word3, 1)[1])[:strlen].strip().replace(" %", "%")
	return (res_spar, res_xl, res_kid)

###
### Gets Hanelsbankens ränta.
### Returns as tuple
### Usage:
### res_spar, res_fram = get_hsb()
### 
def get_hsb():
	r = requests.get(HSB)
	webpage = str(r.text)
	strlen = 6
	r.close()

	split_word = """<td class="shb-text shb-cms-table__cell-align-left"><strong>Sparkonto</strong></td>
                      <td class="shb-text shb-cms-table__cell-align-left">0 kr</td>
                      <td class="shb-text shb-cms-table__cell-align-left">Ingen</td>
                      <td class="shb-text shb-cms-table__cell-align-left">Rörlig ränta: """
	split_word2 = """<td class="shb-text shb-cms-table__cell-align-left"><strong>Framtidskonto</strong></td>
                      <td class="shb-text shb-cms-table__cell-align-left">0 kr</td>
                      <td class="shb-text shb-cms-table__cell-align-left">1 år</td>
                      <td class="shb-text shb-cms-table__cell-align-left">Rörlig ränta: """
	res_spar = str(webpage.split(split_word, 1)[1])[:strlen].strip().replace(" ", "")
	res_fram = str(webpage.split(split_word2, 1)[1])[:strlen].strip().replace(" ", "")
	return (res_spar, res_fram)

###
### Gets Länsförsäkringar ränta.
### Returns as tuple
### Usage:
### res_spar, res_pers = get_lf()
### 
def get_lf():
	r = requests.get(LF)
	webpage = str(r.text)
	strlenr = 122
	strlen = 5
	r.close()

	split_word2 = "<caption>R&#228;nta och avgift sparkonto</caption>"
	split_word = "<caption>R&#228;nta och avgift privatkonto</caption>"
	res_priv = str(webpage.split(split_word, 1)[1])[:strlenr].strip().replace(" %", "%").replace(" ", "")[-strlen:]
	res_spar = str(webpage.split(split_word2, 1)[1])[:strlenr].strip().replace(" %", "%").replace(" ", "")[-strlen:]

	return (res_spar, res_priv)
if __name__ == "__main__":

	log("Swedbank:")
	res_espar, res_privkonto = get_swedbank()
	log("\tResultat E-sparkonto : \"" + res_espar + "\"")
	log("\tResultat Privatkonto : \"" + res_privkonto + "\"")
	log("\n")

	log("Ica Banken:")
	log("\tResultat Sparkonto : \"" + get_icabank() + "\"")
	log("\n")

	log("FOREX Bank:")
	res_spar, lan_kund = get_forex()
	log("\tResultat Sparkonto : \"" + res_spar + "\"")
	log("\tResultat Lån kund  : \"" + lan_kund + "\"")
	log("\n")

	log("Danske Bank:")
	res_spar, res_xl, res_kid = get_dansk()
	log("\tResultat Sparkonto   : \"" + res_spar + "\"")
	log("\tResultat SparkontoXL : \"" + res_xl + "\"")
	log("\tResultat Barnkonto   : \"" + res_kid + "\"")
	log("\n")

	log("Handelsbanken:")
	res_spar, res_fram = get_hsb()
	log("\tResultat Sparkonto     : \"" + res_spar + "\"")
	log("\tResultat Framtidskonto : \"" + res_fram + "\"")
	log("\n")


	log("Länsförsökringar:")
	res_spar, res_priv = get_lf()
	log("\tResultat Privatkonto : \"" + res_priv + "\"")
	log("\tResultat Sparkonto   : \"" + res_spar + "\"")

	write_log()
