# Analytics

Analytics is a side project for the site. While I was building the site while following along a tutorial that I had come across, I decided to expand the function of decorators being used in the site, to move from just routing to doing some analytical tracking. The site passes a trace id between pages, and will keep track of the page loads by that page. This offers features like:
 - Error Tracking: when the site loads an error page, it starts a trace, and then follows the user back to the main page to see where they meant to go
 - Departure Tracking: determine what pages/links a user is most likely to go to after loading a specific page
 - Arrival Tracking: determine what pages on the site a user is most likely to arrive from
 - Site Tracing: follow users through the site, to determine which paths of the site are most active
 - Page Activity: follow the pages that are getting the most page loads

It is worth noting that none of this is client side (yet?), so it works even if the client has Javascript disabled. It does not keep any identifying information except pages visited (the site doesn't even use login). 

The site now has a "View Your Trace" page, so you can see what the site is tracking. It shows the trace information, and a list of their page views. The next step is to paginate the views (already pretty well set, because I have the example)
