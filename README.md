# Project Atlas
Michigan Technological University CS 3141 Team Software Project for Creating Fictional City Maps.

## Usage
I'll let you know when there is code to use...

## [Documentation](https://classdb.it.mtu.edu/~mjschwen/docs/atlas/index.html)
Use the link above to see the formal documentation on the inner works of Atlas.

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
This will put the new webpages in `/docs/build/html/`.

## Libraries
We will be using [NetworkX](https://networkx.org/) to represent a graph and [numpydoc](https://numpydoc.readthedocs.io/en/latest/index.html) to generate documentation.
We also use [SciPy](https://docs.scipy.org/doc/scipy/reference/index.html) to generate convex hulls and Voronoi diagrams
```
pip install networkx
pip install numpydoc
```
