# Network Analysis

# Generate Network

To investigate the relationship between energy consumption and greenhouse gas emission, we bin the variables - gas_mcf and gas_lb_ghg into 50 bins which represent the 50 different levels and store the binning number as nodes in the network. The weight is generated according to the count of rows with the same two nodes. Therefore, if a city has natural gas consumption level a and greenhouse gas emission level b, the weight of a and b increments 1. We can identify the relationship between natural gas consumption and greenhouse gas emission according to the clusterings generated. The data set is used to build graph is stored in network.csv.

# Statistics Information 

Compute some statistics about the graph, including:
Type: DiGraph
Number of nodes: 50
Number of edges: 694
Average in degree:  13.8800
Average out degree:  13.8800
Node, Degree
1, 27
2, 29
3, 30
4, 32
5, 33
6, 34
7, 33
8, 35
9, 34
10, 37
11, 38
12, 38
13, 37
14, 39
15, 37
16, 40
17, 38
18, 40
19, 38
20, 38
21, 39
22, 41
23, 40
24, 38
26, 42
25, 40
27, 39
28, 35
29, 36
30, 31
31, 31
32, 26
33, 25
34, 26
35, 25
36, 21
37, 12
38, 14
39, 14
40, 13
41, 12
42, 13
43, 8
44, 13
45, 10
46, 10
47, 5
48, 6
49, 8
50, 8
Number of nodes in full network:  50
Number of edges in full network:  694
Number of connected components: 1
The density of nodes is:  0.283265306122449
The number of triangles in graph is:  4165.0
The averages for the centralities is:  0.5665306122448979
The length of largest connected component in the graph:  50

# Clustering Analysis

The clustering coefficient is:  {1: 0.5719063545150501, 2: 0.5573065902578797, 3: 0.564, 4: 0.5520833333333334, 5: 0.5498915401301518, 6: 0.5426829268292683, 7: 0.5531453362255966, 8: 0.5324427480916031, 9: 0.5458248472505092, 10: 0.5356536502546689, 11: 0.532051282051282, 12: 0.5256821829855538, 13: 0.5211864406779662, 14: 0.5015128593040847, 15: 0.5254668930390493, 16: 0.4928263988522238, 17: 0.48562300319488816, 18: 0.4728183118741059, 19: 0.48165869218500795, 20: 0.4678111587982833, 21: 0.46676737160120846, 22: 0.4389416553595658, 23: 0.4542203147353362, 24: 0.43450479233226835, 26: 0.40295629820051415, 25: 0.4434907010014306, 27: 0.42220543806646527, 28: 0.3980952380952381, 29: 0.39057507987220447, 30: 0.4084158415841584, 31: 0.42945544554455445, 32: 0.37681159420289856, 33: 0.3959731543624161, 34: 0.3925233644859813, 35: 0.3665338645418327, 36: 0.3205882352941177, 37: 0.4318181818181818, 38: 0.29444444444444445, 39: 0.2857142857142857, 40: 0.25, 41: 0.22727272727272727, 42: 0.2358490566037736, 43: 0.19642857142857142, 44: 0.1509433962264151, 45: 0.2159090909090909, 46: 0.26136363636363635, 47: 0.3333333333333333, 48: 0.42857142857142855, 49: 0.32142857142857145, 50: 0.21428571428571427}

The modularity of unweight graph is 0.2023527062734512.
