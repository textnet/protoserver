# protoserver
Textnet server prototype in Python.


## Technology stack: flask

    easy_install flask
    pip install pymmd

## Run locally

    python app.py

## Implemented feature set

* rudimentary filesystem:
    * address fragments by `~tags` (file names treated as tags)
    * find collections of fragments with same set of tags
    * `~publish` folders to ~namespace/path
* rudimentary publisher:
    * lookup for published document
    * render text from multimarkdown

## Feature set to implement

* rudimentary composer
    * `~include`
    * `~attach`
* rudimentary publisher to HTML
    * render image collections and serve images
    * render attaches and serve attaches
* rudimentary shared spaces
    * `~import`
    * `~library`
* offline/P2P hygiene  
    * fully shared spaces
    * cache
    * version control
    * merge and conflict resolution


## Textnet markup

    ~tags: #tag1, #tag2, #tag3
    ~include: #tag #intersected with other tag
    ~include: #image (optional parameters) — возможно отдельная команда?
    ~attach: #tag1 #tag2
    ~publish: namespace/path
    ~import: namespace/path #optional #tags
    ~library: namespace/path #optional #tags
