# Plassets

Planet assets.

## Important notes

1. this will create a tempfile sqlite database, which will be cleared after every run (there is no persistence between runs; you'll need to manually invoke ```create_app``` with a different sqlite location if you'd like persistence; see ```__main__.py```)
2. the ```X-User: admin``` header is **required** for creating a new asset (you cannot "authentication" by omitting the header) <sup>(not that there actually *is* any authentication)</sup>
3. All endpoints require/emit json. The asset creation endpoint will attempt to coerce post data to json, so you do not need to set its mimetype to ```application/json```.

## Installation

From within a (virtual)env of your choosing:

```
    git clone https://github.com/badg/plassets
    cd plassets
    pip install .
```

If you want to run the test suite, you will need to ```pip install .[test]```.
Actually, depending on your version of pip, you may need to instead run
```pip install -e .[test]```.

## Use

To run, from same (virtual)env invoke:

```
    python -m plassets [--host -H host] [--port -p port]
```

The easiest way to add assets is using the built-in, extremely, absurdly,
ridiculously, laughably simple html page served from the base route. Assuming
you are running on the default localhost:8080, simply start the app and use
a browser to navigate to ```127.0.0.1:8080/``` and you'll see a page that lets
you add assets. The page does an ajax request, automatically adding the X-User
header for you.

Otherwise, you will need to ```POST``` json to the ```/assets/v1/``` endpoint
like this:

```json
{
    "name": "fooz",
    "type": "satellite",
    "class": "dove",
    "details": {}
}
```

This is the only endpoint that mutates state. **For all requests,** a status
code of 200 indicates success, and an HTTP error code indicates failure.

Every other endpoint is fairly self-explanatory, and returns json:

```
    GET     /assets/v1/                     List all assets.
    POST    /assets/v1/                     Create a new asset.
    GET     /assets/v1/<name>               Get a single asset, by its name
    GET     /assets/v1/sat/                 Get only satellites
    GET     /assets/v1/sat/dove             Get only Dove satellites
    GET     /assets/v1/sat/rapideye         Get only RapidEye satellites
    GET     /assets/v1/ant/                 Get only antennae
    GET     /assets/v1/ant/dish/            Get only dish antennae
    GET     /assets/v1/ant/yagi/            Get only yagi antennae
```

# Implementation & design notes

The general strategy here is to start small with room to breathe. So, design
decisions that acquire lots of inertia once deployed (for example: the choice
to use a URL-versioned API) are made in such a way that they can be easily
expanded in the future. However, design decisions that can be changed fairly
freely (for example: using a single file flask app instead of dedicated files
for routes, no blueprint usage, etc) are left for future refactoring.

Assets are currently completely immutable (including their details). Because
they were defined in the spec as an additional feature, asset details are
optional -- this has the downside of creating a potentially inconsistent state
in the database, but is simulating backwards compatibility with an existing API
that didn't implement details.

As a further note on details: the asset store is implemented as a single table
for all assets. The details are implemented as an internal json blob. However,
depending on the specifics of the database (in particular, nosql vs RDBS) and
the number of asset types and classes, it may very well be justified to
migrate to using a dedicated table for every asset class.

In general, the despite using sqlite under the hood, the system was designed as
if it were using nosql (sqlite was only chosen for demo purposes, to make the
reviewer's life easier when running). Since the asset details were listen in
the spec as an extra, I chose to implement them as if they were an in-progress
part of the spec (in terms of the larger fictional context of the app) as
opposed to being an exhaustively-defined, mature spec for every asset type and
class within the asset store. Were that the case, I would approach the overall
architecture with dedicated models for each asset type and class (I would still
use a flat store for the assets themselves though).

The simulated nosql design architecture also has the effect that the asset name
is used directly as the primary key, instead of assigning each a unique ID
programmatically and giving the name an index.

Finally: note that the filter strategy cannot conflict with the asset name,
since asset names must be at least 4 characters.

# Side notes

+ This is tested against py3k5 and py2k7
+ Within docs, there's a jawas_plassets file, that is part of an API experiment for an as-yet-unreleased microservice framework (think: flask competitor for py3.5 native async/await)
