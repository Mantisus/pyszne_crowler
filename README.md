A small experimental web scraping project.

The target site is https://www.pyszne.pl

The task is to get the contact details of all restaurants in Poland.

The target site uses Cloudflare protection with rather poor settings. The Cloudflare-protected pages can be bypassed with correct headers and httpx.

Another feature of the site is the switch to cw-api.takeaway for internal product pages. For cw-api.takeaway pages, the user agent validator is poorly implemented. The use of invalid useragents bypasses the protection of the IP-user-agent mapping constraint checks. However, increased server load will result in IP restriction of requests. So one way to develop IP connectivity.

Scripts can be accelerated using a proxy, but avoid unnecessary load on the site if you don't need to.

Navigation pages are cached because they are rarely modified data. However, there is no caching for the regions page as this content changes more frequently.

If you plan to use the script for research or learning, please use the url_cache decorator for the request function. This will consume more than 30 gigabytes of disk space, but you won't increase the load on the target site.

One goal of the experiment is to create a fully asynchronous script, synchronising execution by checking the number of tasks in the event pool.
