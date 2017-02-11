
import os,sys

if not sys.version_info[0]==2:
	print("Wrong Python Version. Use Python 2.*")
	raise SystemExit

import qrcode
import httplib
import urlparse
from PIL import Image

def unshorten_url(url):
    parsed = urlparse.urlparse(url)
    h = httplib.HTTPConnection(parsed.netloc)
    h.request('HEAD', parsed.path)
    response = h.getresponse()
    if response.status/100 == 3 and response.getheader('Location'):
        return response.getheader('Location')
    else:
        return url

HEADER = '\033[95m'
OKBLUE = '\033[94m'
OKGREEN = '\033[92m'
WARNING = '\033[93m'
FAIL = '\033[91m'
ENDC = '\033[0m'

pathname = os.path.dirname(sys.argv[0])
fullpath = os.path.abspath(pathname) 

print(OKGREEN+"Enter the URL"+ENDC+" which is contained in the QRCode\nthat the Cardboard App doesn't accept "+WARNING+"(\"goo.gl/...\", including \"http(s)\",\nbut not \"www\") (HTTPS will be HTTP then)"+ENDC+" or type \"exit\"")

falscheURL = True

wrongURLprinted = False
while falscheURL:


	url = str(raw_input())
	
	if url.lower() == "exit":
		print("Thank you for using.\n Good Bye!")
		raise SystemExit
	if "https" in url.lower():
		url = url.replace("https","http")
		print url

	if not url.lower().startswith("http://"):
		print(FAIL+"Wrong URL because it doesn't start with http*://"+ENDC)
		print("\n\nTry again or type \"exit\" for exit...\n\n")
#		raise SystemExit
	elif not "goo.gl" in url.lower():
		print(FAIL+"Wrong URL because no goo.gl"+ENDC)
		print("\n\nTry again or type \"exit\" for exit...\n\n")
#		raise SystemExit

		
	else:
		
		try:
			url = unshorten_url(url)
			#print("unshortenedurl: "+url)
			splittedUrl = url.split('?')

			if not "?p=" in url.lower():
				print(FAIL+"Wrong URL because no ?p"+ENDC)
				wrongURLprinted = True
				raise
				
			if not "google.com/cardboard/cfg" in url.lower():
				print(FAIL+"Wrong URL because no cardboard/cfg"+ENDC)
				wrongURLprinted = True
				raise
						
		except:
			if not wrongURLprinted:
				print(FAIL+"Wrong URL"+ENDC)
			print("\n\nTry again or type \"exit\" for exit...\n\n")
		else:
			falscheURL=False
try:
	correctedUrl="http://google.com/cardboard/cfg?"+splittedUrl[1]
	print("The corrected URL is: "+correctedUrl)
	fehler = True
	while fehler:
		print("Should I create a QR code? (y/N) (Overwrites exiting \"Cardboard_URL.png\"")
		doQRcode = str(raw_input())
		if doQRcode.lower() == "y":
			fehler = False
			##Create QR Code
			img = qrcode.make(correctedUrl)
			img.save("Cardboard_URL.png")
			print("QR Code created. It can be found at "+fullpath+"/Cardboard_URL.png")
			print("Do you want to open it now? (y/N)")
			showQRCode= str(raw_input())
			print("Thank you for using.\n Good Bye!")
			if showQRCode.lower()=="y":
				img.show()
			else:
				raise SystemExit

		elif doQRcode.lower() == "n":
			fehler = False
			print("Thank you for using.\n Good Bye!")
			raise SystemExit
		else:
			print(FAIL+"Wrong input. Try again."+ENDC)
except IndexError:
	print(FAIL+"Wrong URL"+ENDC)
	raise SystemExit

##http://google.com/cardboard/cfg?p=CgxIZWlzZSBNZWRpZW4SD1ZSLVBhcHBlIERlbHV4ZR13vh89JY_CdT0qEAAASEIAAEhCAABIQgAASEJYADW8dBM9OggK16M-AAAAAFAAYAA

##goo.gl/zJqbwJ
