# 6.0002 Problem Set 2 Fall 2020
# Graph Optimization
# Name:
# Collaborators:
# Time:


# This file contains a set of data structures to represent the graphs 
# that you will be using for this pset.

class Node():
    """Represents a node in the graph"""

    def __init__(self, name):
        """ 
        Initializes  an instance of Node object.

        Parameters: 
        name - object representing the name of the node             
        """
        self.name = str(name)

    def get_name(self):
        """ 
        Returns: 
        str, representing the name of the node 
        """
        return self.name

    def __str__(self):
        """ 
        This is the function that is called when print(node) is called.

        Returns: 
        str, humanly readable reprsentation of the node
        """
        return self.name

    def __repr__(self):
        """ 
        Formal string representation of the node

        Returns: 
        str, the name of the node.
        """
        return self.name

    def __eq__(self, other):
        """ 
        This is function called when you use the "==" operator on nodes

        Parameters:
        other - Node object to compare against 

        Returns: 
        bool, True is self == other, false otherwise
        """
        if not isinstance(other, Node):
            return False
        return self.name == other.name

    def __ne__(self, other):
        """ 
        This is function called when you used the "!=" operator on nodes

        Parameters:
        other - Node object to compare against 

        Returns: 
        bool, True is self != other, false otherwise
        """
        return not self.__eq__(other)

    def __hash__(self):
        """
        Returns: 
        Hash of the node. This function is necessary so that Nodes can be 
        used as keys in a dictionary, Nodes are immutable
        """
        return self.name.__hash__()


# PROBLEM 1: Implement this class based on the given docstring.
class DirectedRoad():
    """Represents a road (edge) with a travel time (weight)"""

    def __init__(self, src_node, dest_node, travel_time, road_type, traffic_multiplier = 1):
        """ 
        Initialize src, dest, travel_time, and road_type for the DirectedRoad class
        
        Parameters: 
        src: Node, representing the source node
        dest: Node, representing the destination node
        travel_time: float, representing the time travelled between the src and dest
        road_type: str, representing the type of road of the edge
        traffic_multiplier: float, representing how much to multiply travel_time in the case of traffic
        The traffic multiplier will always be at least 1.
        """
        self.src = src_node
        self.dest = dest_node
        self.travel_time = travel_time
        self.road_type = road_type
        self.traffic_multiplier = traffic_multiplier
        
    def get_source_node(self):
        """ 
        Getter method for DirectedRoad

        Returns: 
        Node, representing the source node 
        """
        return self.src
        
    def get_destination_node(self):
        """ 
        Getter method for DirectedRoad

        Returns: 
        Node, representing the destination node 
        """
        return self.dest

    def get_road_type(self):
        """ 
        Getter method for DirectedRoad

        Returns:
        str, representing the road type of the road
        """
        return self.road_type

    def get_travel_time(self, has_traffic = False):
        """ 
        Gets the travel_time for this road. In traffic conditions:
        - multiply the time it takes to travel on a road by its traffic multiplier

        Paramater:
        has_traffic - bool, True if there is traffic, False otherwise  
        
        Returns: 
        float, representing the time to travel from the source node to the destination node
        """
        if has_traffic:
            return self.travel_time * self.traffic_multiplier
        else:
            return self.travel_time


    def __str__(self):
        """ 
        Function that is called when print() is called on a DirectedRoad object.
        
        Returns: 
        str, with the format 'src -> dest takes travel_time minute(s) via road_type road with traffic multiplier traffic_multiplier' 
        
        Note: For the total time assume normal traffic conditions
        """
        return (f'{self.src.get_name()} -> {self.dest.get_name()} takes ' +
                f'{self.get_travel_time()} minute(s) via {self.get_road_type()} road ' +
                f'with traffic multiplier {self.traffic_multiplier}')
    
    def __hash__(self):
        return self.__str__().__hash__()

# PROBLEM 1: Implement methods of this class based on the given docstring.
# DO NOT CHANGE THE FUNCTIONS THAT HAVE BEEN IMPLEMENTED FOR YOU.
class RoadMap():
    """Represents a road map -> a directed graph of Node and DirectedRoad objects"""

    def __init__(self):
        """
        Initalizes a new instance of RoadMap.
        """
        self.nodes = set()
        self.nodes_to_roads = {}  # must be a dictionary of Node -> list of roads starting at that node

    def __str__(self):
        """
        Function that is called when print() is called on a RoadMap object.
        
        Returns: 
        str, representation of the RoadMap.  
        """
        road_strs = []
        for roads in self.nodes_to_roads.values():
            for road in roads:
                road_strs.append(str(road))
        road_strs = sorted(road_strs)  # sort alphabetically
        return '\n'.join(road_strs)  # concat road_strs with "\n"s between them

    def get_reachable_roads_out_of_node(self, node, restricted_roads): 
        """
        Get the roads out of Node node, excluding roads whose types are in restricted_roads
        Param: 
            node: Node
            find reachable roads out of this node 
            
            restricted_roads: List of strings (types of roads) 
            road types that cannot be traveled on 
            
        Return: 
            A new list of all the roads that start at given node, 
            whose types are not in restricted_roads. 
            Empty list if the node is not in the graph.
        """
        roads = []
        
        # Uses list comprehension to list roads(values) from the node(key) if they aren't a restricted type
        if node in self.nodes:
            roads = [x for x in self.nodes_to_roads[node] if x.get_road_type() not in restricted_roads]
        return roads

    def get_all_nodes(self):
        """
        Return:
        a COPY of all nodes in the RoadMap. Does not modify self.nodes
        """
        return self.nodes.copy()

    def contains_node(self, node):
        """ 
        Param: 
        node Node object
        
        Return: 
        True, if node is in the graph. False, otherwise.
        """
        return node in self.nodes

    def insert_node(self, node):
        """ 
        Adds a Node object to the RoadMap.
        Raises a ValueError if it is already in the graph.

        Param: 
        node object
        """
        if node in self.nodes:
            raise ValueError('Duplicate node')
            
        # Adds node to both node list and the road dictionary
        else:
            self.nodes.add(node)
            self.nodes_to_roads[node] = []

    def insert_road(self, road):
        """ 
        Adds a DirectedRoad instance to the RoadMap.
        Raises a ValueError if either of the nodes associated with the road is not in the graph.

        Param: 
        road, DirectedRoad object
        """
        src = road.get_source_node()
        dest = road.get_destination_node()
        
        # Checks if both nodes have been added to the graph first
        if not (src in self.nodes and dest in self.nodes):
            raise ValueError('Node not in graph')
        
        # Adds roads to road dictionary
        self.nodes_to_roads[src].append(road)
            
