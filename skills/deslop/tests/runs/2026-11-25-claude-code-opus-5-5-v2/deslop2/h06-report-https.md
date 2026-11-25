The `.gov` in government websites carries a lot of weight. Citizens expect government websites to be secure, trustworthy, and reliable. Citizens expect anything they read on a `.gov` website to be official, and they expect any information they submit to that website, especially personal information, to be sent safely and only to the government.

On today's Internet, in today's web browsers, HTTPS (`https://`) offers the strongest guarantee of reliable information and secure transmission.

That's why 18F's policy is to **use HTTPS for every .gov website we make**.  18F is an in-house government technology team that builds things for the rest of the U.S. federal government, and we're committed to deploying HTTPS across all of our released websites.

Deciding to use HTTPS everywhere was not difficult. Strong encryption benefits our visitors and our government partners by providing:

* **A secure connection.** HTTPS guarantees that visitors are connecting to the official website, and not getting a page that's been tampered with or replaced entirely by someone else. This protects users from being hijacked or having their information stolen, and protects our government partners from being impersonated or used as a vehicle for attack.
* **A private connection.** Internet traffic is easily intercepted and easily correlated. There is no such thing as insensitive browsing data. By using HTTPS, a visitor's browsing activity is kept private. Web pages, URLs, cookies, and HTTP headers are all encrypted.
* **A fast connection.** Encryption allows us to use modern protocols like [SPDY](https://developers.google.com/speed/spdy/), an extension to HTTPS that [greatly speeds up website loading](https://thethemefoundry.com/blog/why-we-dont-use-a-cdn-spdy-ssl/). SPDY is widely supported by modern browsers, and used today by [Twitter, Google, and Facebook](http://www.wired.com/2013/03/facebook-spdy/). SPDY requires encryption, and is the basis for the upcoming [HTTP/2](https://http2.github.io/), which will require encryption to support visitors on modern browsers.

Finally, using HTTPS lets us adhere to search engine best practices, as [Google's search algorithms now prefer encrypted websites](http://googlewebmastercentral.blogspot.com/2014/08/https-as-ranking-signal.html).

These properties are useful for all of our applications, all of the time, not just when passwords or personal information are involved. By simply deploying HTTPS all of the time, we don't have to engineer a boundary around "sensitive" parts of the application, or judge where those lines should be drawn.

Our friends across the pond in the Government Digital Service have come to the same conclusion, and [require HTTPS](https://www.gov.uk/service-manual/domain-names/https.html) in their [digital standards for the UK government](https://www.gov.uk/service-manual).
