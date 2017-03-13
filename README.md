# Plassets

Planet assets.

## Installation and use

From within a (virtual)env of your choosing:

```
    git clone https://github.com/badg/plassets
    cd plassets
    pip install .
```

If you want to run the test suite, you will need to ```pip install .[test]```.

To run, from same (virtual)env invoke:

```
    python -m plassets [--host -H host] [--port -p port]
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

# Side notes

+ This is tested against py3k5 and py2k7
+ Within docs, there's a jawas_plassets file, that is part of an API experiment for an as-yet-unreleased microservice framework (think: flask competitor for py3.5 native async/await)

# Scratchpad:

    >>> from plassets.plassets import db
    >>> db.create_all()
