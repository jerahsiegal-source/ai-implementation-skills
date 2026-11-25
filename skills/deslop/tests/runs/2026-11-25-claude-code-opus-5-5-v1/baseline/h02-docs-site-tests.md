[About a year ago](https://18f.gsa.gov/2014/11/17/taking-control-of-our-website-with-jekyll-and-webhooks/) we moved this site fully onto Jekyll and brought our blog over from Tumblr. That gave us more freedom, and it meant we could edit our content on GitHub. Readers have sent us quite a few pull requests since then, fixing typos and optimizing images. But as the blog got more complicated, we started making mistakes that were hard to spot before publishing. So we worked out a way to catch many of them before they reach your browser.

Because our site's code lives on GitHub, we can hook it up to continuous integration (CI) services that check our work before we publish. Plenty of open source projects use CI to test their code. We use it to test our content. We use Travis CI, though there are many other options. Until recently, our only test was building the site and seeing whether the build succeeded.

A build catches some high-level errors, but not all of them. We added `html-proofer` to our tests. It checks internal links and validates the HTML on every generated page. That catches more, but it's still a bit like a chainsaw: it gets through the material quickly and misses the small stuff. Say a post was missing the `authors` field in its frontmatter. Every test would pass, and the page would go out without a byline. We wouldn't notice until we'd merged the content and previewed it on our staging server.

Checking things by hand is the worst, especially when a computer could do it for you. So we wrote the `jekyll_frontmatter_tests` gem. It's pretty simple, and it catches problems like this before we publish. It compares each post to a "schema" that lists which frontmatter fields should exist and how their values should be formatted. Here's how to install it and set it up to test a Jekyll site's posts.

We recommend typing each command yourself instead of copying and pasting.

## Installation

Add `jekyll_frontmatter_tests` to the `jekyll-plugins` section of your `_config.yml`, then run `gem install jekyll_frontmatter_tests`. After that, `jekyll --help` should list a new command called `test`. For reference, here are [18f.gsa.gov's `_config.yml`](https://github.com/18F/18f.gsa.gov/blob/staging/_config.yml) and [`Gemfile`](https://github.com/18F/18f.gsa.gov/blob/staging/Gemfile).

## Configuration

Next, make a "schema" file in a directory called `deploy/tests/schema`. If that directory doesn't exist yet, run `mkdir -p deploy/tests/schema` from the root of your Jekyll directory. Then create a file called `_posts.yml` by running `touch deploy/tests/schema/_posts.yml`.
