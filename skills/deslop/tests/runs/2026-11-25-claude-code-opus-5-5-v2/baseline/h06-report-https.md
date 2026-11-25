People put a lot of trust in a `.gov` address. They expect a government website to be secure and reliable, and they assume that what they read there is official. When they send information through one of these sites, especially personal information, they expect it to arrive safely and to go only to the government.

With today's Internet and today's browsers, **HTTPS** (`https://`) is the best way to make sure information is reliable and gets sent securely.

So 18F's policy is to **use HTTPS for every .gov website we make**. 18F is an in-house technology team that builds things for other parts of the U.S. federal government. We're committed to deploying HTTPS on every website we release.

The decision was easy. Strong encryption helps both our visitors and the agencies we work with:

* **Security.** HTTPS guarantees that visitors are reaching the official website. Nobody else can tamper with the page or swap in a different one. Users are protected from being hijacked or having their information stolen. Our government partners are protected from being impersonated or used as a vehicle for attack.
* **Privacy.** Internet traffic is easy to intercept and easy to correlate, and no browsing data is truly insensitive. HTTPS keeps a visitor's browsing private by encrypting web pages, URLs, cookies, and HTTP headers.
* **Speed.** Encryption lets us use modern protocols like [SPDY](https://developers.google.com/speed/spdy/), an extension to HTTPS that [makes websites load much faster](https://thethemefoundry.com/blog/why-we-dont-use-a-cdn-spdy-ssl/). Most modern browsers support SPDY, and [Twitter, Google, and Facebook](http://www.wired.com/2013/03/facebook-spdy/) use it today. SPDY requires encryption. It's also the basis for the upcoming [HTTP/2](https://http2.github.io/), which will require encryption to support visitors on modern browsers.

HTTPS also keeps us in line with **search engine best practices**, since [Google's search algorithms now prefer encrypted websites](http://googlewebmastercentral.blogspot.com/2014/08/https-as-ranking-signal.html).

These benefits apply to all of our applications at all times, not only when passwords or personal information are involved. If we use HTTPS everywhere, we never have to build a boundary around the "sensitive" parts of an application or decide where that boundary belongs.

The UK's Government Digital Service came to the same conclusion. Its [digital standards for the UK government](https://www.gov.uk/service-manual) [require HTTPS](https://www.gov.uk/service-manual/domain-names/https.html).
