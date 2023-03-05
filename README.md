A small experimental web scraping project.

The target site is https://www.pyszne.pl

The task is to get the contact details of all restaurants in Poland.

The target site uses Cloudflare protection with rather poor settings. The Cloudflare-protected pages can be bypassed with correct headers and httpx.

Another feature of the site is the switch to cw-api.takeaway for internal product pages. For cw-api.takeaway pages, the user agent validator is poorly implemented. The use of invalid useragents bypasses the protection of the IP-user-agent mapping constraint checks. However, increased server load will result in IP restriction of requests. So one way to develop IP connectivity.

Scripts can be accelerated using a proxy, but avoid unnecessary load on the site if you don't need to.

Navigation pages are cached because they are rarely modified data. However, there is no caching for the regions page as this content changes more frequently.

If you plan to use the script for research or learning, please use the url_cache decorator for the request function. This will consume more than 30 gigabytes of disk space, but you won't increase the load on the target site.

One goal of the experiment is to create a fully asynchronous script, synchronising execution by checking the number of tasks in the event pool.


# TODO

Based on traffic analysis of the mobile app, we can retrieve data about the restaurant using the following queries

https://pl-cdn.citymeal.com/ws/6.15/getrestaurantdata/{key}/en
https://pl-cdn.citymeal.com/ws/6.15/getrestaurantdatacheckout/{key}/en

with headers

```python
headers = {
    "Platform": "androidtablet",
    "Appname": "Pyszne.pl",
    "Appversion": "8.30.0",
    "Systemversion": "33;8.30.0",
    "Accept-Encoding": "gzip, deflate",
    "User-Agent": "okhttp/4.10.0",
}
```

The current problem is getting restaurant data through the api of the mobile app. They use a key with an md5 cache based on other keys. Perhaps there are some sort of salts. We need to determine an algorithm

sample

``python
url = "https://pl.citymeal.com/androidtablet/at.php/?"

data = var0=09024b6dd1e8770cda58bb27229f98ac&var1=getrestaurants&var2=&var3=180&var4=52.2380508&var5=20.9856886&var6=en&var7=0&var8=1&var10=0&version=5.40&systemversion=33%3B8.30.08.30.0&appname=Pyszne.pl&language=en

headers = """Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Content-Length: 209
Accept-Encoding: gzip, deflate
User-Agent: okhttp/4.10.0""
```
