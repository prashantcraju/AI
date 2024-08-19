# Prashant Raju
# pcr2120

from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource

class Puzzle:
    
    def __init__(self, initial_state):
        self.list = []
        self.set = set()
        self.list.append(initial_state)
        self.set.add(initial_state.config)

    def add_front(self, state):
        self.list.insert(0, state)
        self.set.add(state.config)

    def add_back(self, state):
        self.list.append(state)
        self.set.add(state.config)
    
    def add_weight(self, state):
        self.list.append(state)
        self.set.add(state.config)
        self.list.sort(key=lambda x: x.full_cost, reverse=True)
    
    def weight_update(self, state):
        for lstate in self.list:
            if lstate.config == state.config:
                lstate.full_cost = state.full_cost
                break
        self.list.sort(key=lambda x: x.full_cost, reverse=True)
    
    def has(self, state):
        return state.config in self.set
    
    def pop(self):
        state = self.list.pop()
        self.set.remove(state.config)
        return state
    
    def popSmallest(self):
        state = self.list.pop()
        self.set.remove(state.config)
        self.list.sort(key=lambda x: x.full_cost, reverse=True)
        return state
    
    def len(self):
        return len(self.list)
    
    def is_empty(self):
        return self.len() == 0
    
#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n         = n
        self.cost      = cost
        self.parent    = parent
        self.action    = action
        self.config    = config
        self.children  = []
        self.dimension = n
        self.full_cost = -1

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)
        
    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[3*i : 3*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.empty_row == 0:
            return None

        else:
            blank_index = int(self.empty_row * self.n + self.empty_column)
            goal = blank_index - self.n
            new_configuration = list(self.config)
            new_configuration[blank_index], new_configuration[goal] = new_configuration[goal], new_configuration[blank_index]
            return PuzzleState(tuple(new_configuration), self.n, parent=self, action="Up", cost=self.cost + 1)
        
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.empty_row == self.n - 1:
            return None

        else:
            blank_index = int(self.empty_row * self.n + self.empty_column)
            goal = int(blank_index + self.n)
            new_configuration = list(self.config)
            new_configuration[blank_index], new_configuration[goal] = new_configuration[goal], new_configuration[blank_index]
            return PuzzleState(tuple(new_configuration), self.n, parent=self, action="Down", cost=self.cost + 1)
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.empty_column == 0:
            return None

        else:
            blank_index = int(self.empty_row * self.n + self.empty_column)
            goal = blank_index - 1
            new_configuration = list(self.config)
            new_configuration[blank_index], new_configuration[goal] = new_configuration[goal], new_configuration[blank_index]
            return PuzzleState(tuple(new_configuration), self.n, parent=self, action="Left", cost=self.cost + 1)


    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.empty_column == self.n - 1:

            return None

        else:
            blank_index = int(self.empty_row * self.n + self.empty_column)
            goal = blank_index + 1
            new_configuration = list(self.config)
            new_configuration[blank_index], new_configuration[goal] = new_configuration[goal], new_configuration[blank_index]
            return PuzzleState(tuple(new_configuration), self.n, parent=self, action="Right", cost=self.cost + 1)

    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

    def isEqual(self, state):
        return self.config == state.config

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput(state, nodes_expanded, deepest):
    
    path_to_goal = []
    state_holder = state
    
    while state_holder.parent != None:
        path_to_goal.insert(0, state_holder.action)
        state_holder = state_holder.parent
        
        file = open("output.txt", "w")
        file.write("path_to_goal: {}\n".format(path_to_goal))
        file.write("cost_of_path: {}\n".format(state.cost))
        file.write("nodes_expanded: {}\n".format(nodes_expanded))
        file.write("search_depth: {}\n".format(state.cost))
        file.write("max_search_depth: {}\n".format(deepest))
        file.write("running_time: {}\n".format(time.time() - start_time)
        file.write("max_ram_usage: {}\n".format(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss/1000.0, '.3f'))
        file.close()
        
        return
    
def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    
    start = Puzzle(initial_state)
    seen = set()

    nodes_expanded = 0
    deepest = 0
    
    while not start.is_empty():
        state = start.pop()
        seen.add(state.config)

        if test_goal(state):
            write_output(state, nodes_expanded, deepest)
            break

        if len(state.children) == 0:
            children = state.expand()
            
        nodes_expanded += 1

        for child in children:

            if start.has(child):
                continue

            if child.config in seen:
                continue

            if child.cost > deepest:
                deepest = child.cost

            start.add_front(child)

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    
    start = Puzzle(initial_state)
    seen = set()

    # stats
    nodes_expanded = 0
    deepest = 0
    
    while not start.is_empty():
        state = start.pop()
        seen.add(state.config)

        if test_goal(state):
            write_output(state, nodes_expanded, deepest)
            break

        if len(state.children) == 0:
            children = reversed(state.expand())
            
            nodes_expanded += 1

        for child in children:

            if start.has(child):
                continue

            if child.config in seen:
                continue

            if child.cost > deepest:
                deepest = child.cost

            start.add_back(child)

def A_star_search(initial_state):
    """A * search"""

    start = Puzzle(initial_state)
    seen = set()

    nodes_expanded = 0
    deepest = 0
    
    while not start.is_empty():
        state = start.popSmallest()
        
    seen.add(state.config)
    
    if test_goal(state):
            write_output(state, nodes_expanded, deepest)
            break

    if len(state.children) == 0:
            children = reversed(state.expand())
            nodes_expanded += 1

    for child in children:
        if child.config in seen:
            continue

    child.full_cost = calculate_total_cost(child)

    if start.has(child):
        start.weight_update(child)
        continue

    if child.cost > deepest:
        deepest = child.cost

    start.add_weight(child)

            
def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    
    return state.cost + calculate_manhattan_dist_block(state)
    
def calculate_manhattan_dist_block(state):
    """calculate the manhattan distance of a state"""

    result = 0
    
    for block, idx in enumerate(state.config):
        if idx == 0:
            continue
        result += calculate_manhattan_dist(idx, block, state.n)

    return result

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    
    avenue = value % n
    street = int(value/n)
    avenue_goal = idx % n
    street_goal = int(idx/n)

    return abs(avenue_goal - avenue_goal) + abs(street_goal - street_goal)
    
def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    
    return puzzle_state.config == (0,1,2,3,4,5,6,7,8)

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments!")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
