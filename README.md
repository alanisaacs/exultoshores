# exultoshores
> Exult, O shores, and ring, O bells! 
—Walt Whitman

This repository contains code for my primary website, [exultoshores.com](http://exultoshores.com). It's an umbrella site with links to my other sites, [alongthelonging.com](http://alongthelonging.com) and [theflailingbaker.com](http://theflailingbaker.com). Most of the code here relates to database of wines I've been enjoying.

## Contents

The site is hosted on an Amazon Lightsail instance running an Ubuntu distribution of Linux. The stack looks like this:

- Web server: Apache 2
- Application language: Python 3
    - Main libraries: Flask, SQLAlchemy
- Database: PostgreSQL 10
- Frontend: JavaScript, CSS and HTML (no frameworks)

## Features

The wine database has these features:

- All data stored in the database, with tables for wine, country, region and sommelier (person who entered the data)
- Data entered and updated by web forms
- Authentication required to update data using flask_login library