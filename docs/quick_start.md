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

### A brief overview of project structure
There are two main folders relevant to running simulations: `market-sim/agent code` and `market-sim/simulations`. 

Generally speaking, the `market-sim/agent code` folder should contain all code necessary for agents to function. This might include the basic scripts describing their behavior. It also might include files that contain beleifs about assets, etc. 

The `market-sim/simulations` directory should contain XML files that specify the simulation. 

When building the program, all of these files are copied into the appropriate directory where the simulation will use them. They are separated at this level purely for the sake of organization. 

### Simulation overview 

This tutorial simulates a market in which there are two agents: a seller and a buyer. The seller "wakes up" at a pre-specified interval and sells a given number of shares at a predetermined price. The buyer is alerted when orders are placed, wakes up to buy the shares being sold. 

 > Note: there is no concept of finite resources in this simulation. This must be implemented at the agent level. This example only demonstrates the transaction mechanism and the process of building and running a simulation. 

 The behvaior of two agents in this simulation have been scripted in Python by the authors of MAXe. They have been included here by default in the `market-sim/agent code` directory. It is recommended to look over these files, if only to get an idea of how agent behavior is typically structured. 

 Agent characteristics are passed to the simulation via xml files. An example, used for running this particular simulation, can be found in `market-sim/simulations`

 ### Running the simulation
 
Running the simulation involves three steps:
- Ensuring that agent files have been appropriately initialized. This involves navigating to directory `market-sim/maxe/build` and running ```cmake ../```. 
- Building the simulation. From `market-sim/maxe/build` run ```cmake --build .```
- Executing the simulation. from `market-sim` run ```Python3 simulate.py [simulation filename]``` In this case, replace `[simulation filename]` with `SellerBuyerExample.xml`

