# hugo-resizer
Script to resize images for the static site generator Hugo

## Overview
Finds images that are used in a [Hugp](https://hugo.io) static site and creates smaller versions that can more easily be used with html
elements like `srcset`.

The script assumes your posts are layed out as follows:
```
└───content
    └───post
        ├───arc-reactor
        │   └───images
        ├───beer-pong
        │   └───img
        └───flashlight
            └───images
```

And will put the generated images in their own folders:
```
└───content
    └───post
        ├───arc-reactor
        │   └───images
        │       ├───1080
        │       ├───300
        │       └───600
        ├───beer-pong
        │   └───img
        │       ├───1080
        │       ├───300
        │       └───600
        └───flashlight
            └───images
                ├───1080
                ├───300
                └───600
```

## Usage
Run from the same directory that the `hugo` command would normally be run for the site.

Currently don't have command line options set up, so configuration is done in the script.

The `processes` variable configures how many processes to run in parallel. Set this to how many cores your CPU has.
