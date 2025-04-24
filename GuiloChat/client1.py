import httpx


with httpx.Client() as client:
    r = client.get("http://localhost:7003/paulo")

print(r.text)