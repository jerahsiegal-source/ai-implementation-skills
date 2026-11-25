Express is a fast, minimalist web framework for [node](http://nodejs.org) that doesn't impose a particular way of doing things.

```js
const express = require('express')
const app = express()

app.get('/', function (req, res) {
  res.send('Hello World')
})

app.listen(3000)
```

## Installation

Express is a [Node.js](https://nodejs.org/en/) module published on the [npm registry](https://www.npmjs.com/).

You need Node.js 0.10 or later. If you don't have it yet, [download and install Node.js](https://nodejs.org/en/download/) first.

Then install Express with [`npm install`](https://docs.npmjs.com/getting-started/installing-npm-packages-locally):

```bash
$ npm install express
```

For more detail, see [our installing guide](http://expressjs.com/en/starter/installing.html).

## Features

  * Robust routing
  * Built for high performance
  * Very high test coverage
  * HTTP helpers (redirection, caching, etc.)
  * A view system that works with 14+ template engines
  * Content negotiation
  * An executable for generating apps quickly

## Docs & Community

  * [Website and Documentation](http://expressjs.com/) ([website repo](https://github.com/expressjs/expressjs.com))
  * [#express](https://webchat.freenode.net/?channels=express) on freenode IRC
  * [GitHub Organization](https://github.com/expressjs): official middleware and modules
  * [Wiki](https://github.com/expressjs/express/wiki)
  * [Google Group](https://groups.google.com/group/express-js): discussion
  * [Gitter](https://gitter.im/expressjs/express): support and discussion

**Tip:** If you're upgrading, read [Migrating from 3.x to 4.x](https://github.com/expressjs/express/wiki/Migrating-from-3.x-to-4.x) and [New features in 4.x](https://github.com/expressjs/express/wiki/New-features-in-4.x).

### Security Issues

To report a security vulnerability in Express, see [Security Policies and Procedures](Security.md).

## Quick Start

The fastest way to start is to generate an app with the [`express(1)`](https://github.com/expressjs/generator) executable.

Install the executable. Its major version matches the Express major version:

```bash
$ npm install -g express-generator@4
```

Create the app:

```bash
$ express /tmp/foo && cd /tmp/foo
```

Install dependencies:

```bash
$ npm install
```

Start the server:

```bash
$ npm start
```

Then open http://localhost:3000.

## Philosophy

Express aims to give you small, robust tools for HTTP servers. That makes it a good fit for single-page apps, websites, hybrids, and public HTTP APIs.

Express doesn't make you use any particular ORM or template engine. It supports over 14 template engines through [Consolidate.js](https://github.com/tj/consolidate.js), so you can quickly put together the framework that fits your project.
