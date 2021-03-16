# Project Atlas
Michigan Technological University CS 3141 Team Software Project for Creating Fictional City Maps.

## Usage
I'll let you know when there is code to use...

## [Documentation](https://mjschwenne.github.io/atlas/)
Use the link above to see the formal documentation on the inner works of Atlas.

How to build the documentation:

Add new classes to the documentation by running the following command in the terminal.
```
/atlas/docs> sphinx-apidoc -o ./source ../src/Frontend
/atlas/docs> sphinx-apidoc -o ./source ../src/Backend
```
Then add the name of the new `.rst` file to `index.rst` in alphabetic order.
Build the documentation
```
/atlas/docs> make clean
/atlas/docs> make html
```
This will put the new webpages in `/documentation/build/html/`.

Next, copy all the files from `/documentation/build/html` to `/docs/`, which is where Github pages will look for them.
Now, apparently Github pages does *not* like directories which start with an underscore, so be sure to refactor `/_static/` and `/_source/` to remove the underscore.
Finally, commit to the repo, and the documentation will be updated.

## Libraries
We will be using [NetworkX](https://networkx.org/) to represent a graph and [numpydoc](https://numpydoc.readthedocs.io/en/latest/index.html) to generate documentation.
We also use [SciPy](https://docs.scipy.org/doc/scipy/reference/index.html) to generate convex hulls and Voronoi diagrams
```
pip install networkx
pip install numpydoc
```
