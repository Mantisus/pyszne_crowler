A small experimental web scraping project.

The target site is https://www.pyszne.pl

Task is to get contact details of all restaurants in Poland

The target site uses Cloudflare protection with rather poor settings. The pages protected by Cloudflare can be bypassed with correct headers and httpx.

Another feature of the site is the switch to cw-api.takeaway for internal product pages. For cw-api.takeaway pages, the user agent validator is poorly implemented. The use of invalid useragents avoids the protection of IP - User Agent mapping constraint checks. But increased server load will result in IP restriction of requests. Hence one way to develop IP connectivity.

Script can be accelerated using proxy, but avoid unnecessary load on site if you don't have to.

Navigation pages are cached because they are rarely changed data. But there is no caching for the regions page, because this content changes more often.

If you plan to use the script for research or learning, please use url_cache decorator for request function. This will consume more than 30 gigabytes of disk space, but you won't create an increased load on the target site.

One aim of the experiment is to create a fully asynchronous script, the synchronisation of execution is done by checking the number of tasks in the event pool.
A small experimental web scraping project.

The target site is https://www.pyszne.pl

Task is to get contact details of all restaurants in Poland

The target site uses Cloudflare protection with rather poor settings. The pages protected by Cloudflare can be bypassed with correct headers and httpx.

Another feature of the site is the switch to cw-api.takeaway for internal product pages. For cw-api.takeaway pages, the user agent validator is poorly implemented. The use of invalid useragents avoids the protection of IP - User Agent mapping constraint checks. But increased server load will result in IP restriction of requests. Hence one way to develop IP connectivity.

Script can be accelerated using proxy, but avoid unnecessary load on site if you don’t have to.

Navigation pages are cached because they are rarely changed data. But there is no caching for the regions page, because this content changes more often.

If you plan to use the script for research or learning, please use url_cache decorator for request function. This will consume more than 30 gigabytes of disk space, but you won’t create an increased load on the target site.

One aim of the experiment is to create a fully asynchronous script, the synchronisation of execution is done by checking the number of tasks in the event pool.
