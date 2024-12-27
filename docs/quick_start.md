---
layout: page
title: Quick Start
permalink: /qstart/
nav_order: 3
---

# Getting Started 

This guide offers a brief overview on running the simulation software. This has been adapted from the MAXe repository. 

## Cloning the Repository

The first step in running the simulation is to clone the market-sim repository. It is important that `--recurse-submodules` is used here, due to a series of submodules nested within the broader market-sim repo (MAXe, and within MAXe, PyBind). 

```
git clone <link> --recurse-submodules 
```

In the event that `--recurse-submodules` was not used in the initialization of the repo, one can update the submodules by running the following:

```
git submodule update
```

## Building the Executable

Before attempting to run the simulation, it is helpful to build and compile to ensure a certain level of basic functionality. Building the simulation is done by creating a build directory in the MAXe directory, and building from there. 

```
cd maxe
mkdir build
cd build
cmake ../
cmake --build .
```

If all goes well, some compiling should occur, error free. 

## Running a Simulation

The MAXe repository includes a handful of default agent types. These can be used to demonstrate the basic process of running a simulation. 

This tutorial simulates a market in which there are two agents: a seller and a buyer. The seller "wakes up" at a pre-specified interval and sells a given number of shares at a predetermined price. The buyer is alerted when orders are placed, wakes up to buy the shares being sold. 

 > Note: there is no concept of finite resources in this simulation. This must be implemented at the agent level. This simply demonstrates the transaction mechanism, and the process of building and running a simulation. 

 

