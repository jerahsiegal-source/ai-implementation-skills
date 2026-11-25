[About a year ago](https://18f.gsa.gov/2014/11/17/taking-control-of-our-website-with-jekyll-and-webhooks/) we converted this site to run fully on Jekyll and migrated our blog from Tumblr. When we did that we gained some freedom and the ability to edit our content on GitHub. We’ve received quite a few pull requests from readers to fix typos and optimize images. As our blog got more complicated, we started making mistakes that were hard to catch before publishing. So we came up with a way to catch many of those errors, before they end up in your browser.

One advantage of hosting our site’s code on GitHub is we can integrate with continuous integration (CI) services to check our work before we publish. Many open source projects use a CI to run various tests on their code. We use it to run tests on our content. We use Travis CI but there are many others out there. Until recently, the only test we ran was building the site to know if it was successful.

Just building the site caught a few high-level errors but not all. We added the `html-proofer` to our test suite, which checks internal links and validates the HTML on every generated page. This helps us catch more errors but is still kind of like a chainsaw: It tears through the material but misses detail-level problems. If a post was missing the `authors` field in the frontmatter, for example, all the tests would pass but the generated page would be missing a byline. This is the kind of error we wouldn’t catch until we merged the content into the site and previewed it on our staging server.

Manually inspecting things is the worst, especially when you can make a computer to do it for you. This is why we wrote the `jekyll_frontmatter_tests` gem. It’s pretty simple and helps us catch problems like this before we publish. It works by comparing our posts to a “schema” that describes which fields should exist in the frontmatter and how their values should be formatted. Let’s walk through installation and setup for testing a Jekyll site’s posts.

For these instructions, we recommend typing in each of the commands, not copy-pasting.

## Installation

Install it by adding `jekyll_frontmatter_tests` to your `_config.yml` in the `jekyll-plugins` section and then `gem install jekyll_frontmatter_tests`. Once installed, you should have an extra command called `test` when you run `jekyll --help`. Here’s what [18f.gsa.gov’s `_config.yml`](https://github.com/18F/18f.gsa.gov/blob/staging/_config.yml), and [`Gemfile`](https://github.com/18F/18f.gsa.gov/blob/staging/Gemfile) look like.

## Configuration

Next, create a “schema” file in a directory called `deploy/tests/schema`. If you don’t have that directory, you can make it by running `mkdir -p deploy/tests/schema` from the root of your Jekyll directory. Then create a file called `_posts.yml`. You can do this by running `touch deploy/tests/schema/_posts.yml`.
