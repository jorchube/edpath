# edpath
Small command line utility for Elite:Dangerous players.

Compute the optimal order in whith a commander has to visit a series of systems in order to minimize time and costs. 

Currently uses the populated systems dump from [eddb.io](https://eddb.io) (Thank you for your work!)

### Usage:

```
$ edpath.py [-h] [-l [LIST [LIST ...]]] [-s [START [START ...]]] [-e [END [END ...]]] [--refresh] [--tests]

optional arguments:
  -h, --help            show this help message and exit
  -s [START [START ...]], --start [START [START ...]] Starting system for the route
  -e [END [END ...]], --end [END [END ...]]           Ending system for the route
  --refresh             Downloads the latest version of the systems database
                        before proceeding
  --tests               Run self tests

required arguments:
  -l [LIST [LIST ...]], --list [LIST [LIST ...]]      List of systems to compute the route
```

### Examples:

#1 - Compute the best route to visit a list of systems:
```
$> edpath.py -l achenar, beta caeli, sirius, sol    
 [edpath] ==============================
 [edpath]   1: SOL
 [edpath]   2: SIRIUS
 [edpath]   3: BETA CAELI
 [edpath]   4: ACHENAR
 [edpath] ------------------------------
 [edpath] Total distance: 179.63 Ly
 [edpath] ==============================
```
  

#2 - Compute the best route to visit a list of systems, specifying starting and ending systems:
```
$> edpath.py -l achenar, beta caeli, ceos, sirius, sol, sothis -s sol -e sirius
 [edpath] ==============================
 [edpath]   1: SOL
 [edpath]   2: CEOS
 [edpath]   3: SOTHIS
 [edpath]   4: BETA CAELI
 [edpath]   5: ACHENAR
 [edpath]   6: SIRIUS
 [edpath] ------------------------------
 [edpath] Total distance: 1239.27 Ly
 [edpath] ==============================
```
