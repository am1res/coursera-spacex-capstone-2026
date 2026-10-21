from pathlib import Path
import requests
url="https://en.wikipedia.org/w/index.php?title=List_of_Falcon_9_and_Falcon_Heavy_launches&oldid=1027686922"
r=requests.get(url,timeout=45)
r.raise_for_status()
Path(__file__).with_name("wikipedia_snapshot.html").write_bytes(r.content)
print("Downloaded the course historical Wikipedia revision",len(r.content),"bytes")
