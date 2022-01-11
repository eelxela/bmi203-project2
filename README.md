![BuildStatus](https://github.com/eelxela/bmi203-project2/actions/workflows/test.yml/badge.svg)

# Project 2
Breadth-first search

# Assignment Overview
The purpose of this assignment is to get you comfortable working with graph structures and to implement a breadth-first search function to traverse the graph and find the shortest path between nodes.

# Assignment Tasks

## Coding Assessment
* Write a breadth-first search function (Write this code in the graph.py file)
	* If there's no end node, just return a list with the order of traversal
	* If there is an end node and a path exists, return a list of the shortest path
	* If there is an end node and a path does not exist, return None

## Software Development Assessment

* Write unit tests (in the test_bfs.py file) for your breadth first search
* Replace these instructions with a brief description of bfs in your forked repo
	
* Automate Testing with a [Github Actions](https://docs.github.com/en/actions)

	See blogposts below on helping set up github actions with pytest:
	
	* [post 1](https://blog.dennisokeeffe.com/blog/2021-08-08-pytest-with-github-actions)
	* [post 2](https://mattsegal.dev/pytest-on-github-actions.html)
	* Add "! [BuildStatus] (https://github.com/ < your-github-username > /Project2/workflows/Project2/badge.svg?event=push)" (update link and remove spaces) to the beginning of your readme file
	* Also refer to previous assignment for more in-depth help with GitHub actions

	Ensure that the github actions complete the following:
	* runs pytest

# Getting Started
To get started you will need to fork this repository onto your own github. You will then work on the code base from your own repo and make changes to it in the form of commits. 

# Reference Information
## Test Data
Two networks have been provided in an adjacency list format readable by [networkx](https://networkx.org/), is a commonly used python package for working with graph structures. These networks consist of two types of nodes:
* Faculty nodes 
* Pubmed ID nodes

However, since these are both stored as strings, you can treat them as equivalent nodes when traversing the graph. The first graph ("citation_network.adjlist") has nodes consisting of all BMI faculty members, the top 100 Pubmed papers *cited by* faculty, and the top 100 papers that *cite* faculty publications. Edges are directed and and edge from node A -> B indicates that node A *is cited by* node B. There are 5120 nodes and 9247 edges in this network.

The second network is a subgraph of the first, consisting of only the nodes and edges along the paths between the PIs of all your TAs. There are 30 nodes and 64 edges.

# Completing the assignment
Make sure to push all your code to github, ensure that your unit tests are correct, and submit a link to your github through the google classroom assignment.

# Grading

## Code (6 points)
* Breadth-first traversal works correctly (3)
* Traces the path from one faculty to another (2)
* Handles boundary cases (1)

## Unit tests (3 points)
* Output traversal for mini data set (1.5)
* Unit tests for cases that work and cases that don't (1.5)

## Style (1 points)
* Readable code with clear comments and method descriptions

