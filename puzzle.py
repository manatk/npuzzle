import math
def LoadFromFile(filepath):
    input = open(filepath, "r")
    all_lines = input.readlines()

    #check to make sure that the n is a valid integer
    try:
        n = int(all_lines[0].strip())
        if n <= 0:
            print("N IS NEGATIVE")
            return None
    except:
        print("N IS INVALID")
        return None
    all_lines.pop(0)

    #make sure that you have n rows
    if len(all_lines) != n:
        return None

    #list for the data structure representation
    list = []
    found_hole = False

    for i in all_lines:
        i = i.strip()
        i = i.split('\t')

        #check to make sure that the row has valid length
        if is_valid_row(i,n) == False:
            #print("INVALID ROW")
            return None

        #append each element in the file to the list
        for x in i:
            if x == "*":
                if found_hole == False:
                    list.append(0)
                    found_hole = True
                else:
                    print("MORE THAN ONE HOLE")
                    return None
            elif is_valid_entry(x, n) == False:
                print("INVALID ENTRY")
                return None
            else:
                if int(x) in list:
                    print(list)
                    print(x)
                    print("REPEAT INTEGER")
                    return None
                list.append(int(x))
        #I tried to do this as a list comprehension, couldn't figure out exact syntax
        #list = list + [int(x) for x in i if x != '*' else x = 0]

    if (found_hole == False):
        print("NO HOLE FOUND")
        return None
    return(list)

def check_type(list):
    for i in list:
        print(type(i))

#returns whether the row has n elements
def is_valid_row(i,n):
    if len(i) != n:
        print("INVALID ROW")
        return False

#returns whether the element is valid
def is_valid_entry(x,n):
    if (x.isdigit() == False):
        return False
    x = int(x)
    if (x < 1 or x > math.pow(n,2) - 1):
        return False
    return True

#print state as a game board representation
def debug_state(state):
    n = int(math.sqrt(len(state)))
    row = ""
    n_count = 0
    for i in state:
        row = row + " " + str(i)
        if (n_count % n) == n-1:
            print(row)
            row = ""
        n_count = n_count + 1

#compute all the neighbors
def ComputeNeighbors(state):
    n = math.sqrt(len(state))
    index = state.index(int(0))
    neighbor_list = []

    if index == 0:
        neighbor_list.append(swap(state, index, index+1))
        neighbor_list.append(swap(state, index, index+n))

    elif index == n-1:
        neighbor_list.append(swap(state, index, index-1))
        neighbor_list.append(swap(state, index, index+n))

    elif index < n-1:
        neighbor_list.append(swap(state, index, index-1))
        neighbor_list.append(swap(state, index, index+n))
        neighbor_list.append(swap(state, index, index+1))

    elif (index != (n)*(n-1)) and (index % n == 0):
        neighbor_list.append(swap(state, index, index-n))
        neighbor_list.append(swap(state, index, index+n))
        neighbor_list.append(swap(state, index, index+1))

    elif index == (n)*(n-1):
        neighbor_list.append(swap(state, index, index-n))
        neighbor_list.append(swap(state, index, index+1))

    elif (index % n == n-1) and (index < math.pow(n,2)-1):
        neighbor_list.append(swap(state, index, index-1))
        neighbor_list.append(swap(state, index, index+n))
        neighbor_list.append(swap(state, index, index-n))

    elif index == math.pow(n,2)-1:
        neighbor_list.append(swap(state, index, index-1))
        neighbor_list.append(swap(state, index, index-n))

    elif (index > n*(n-1)) and (index < math.pow(n,2)-1):
        neighbor_list.append(swap(state, index, index-n))
        neighbor_list.append(swap(state, index, index-1))
        neighbor_list.append(swap(state, index, index+1))

    else:
        neighbor_list.append(swap(state, index, index-n))
        neighbor_list.append(swap(state, index, index+n))
        neighbor_list.append(swap(state, index, index-1))
        neighbor_list.append(swap(state, index, index+1))

    return neighbor_list

#swap two tiles
def swap(state, index, pos2):
    pos2 = int(pos2)
    temp = list(state[:])
    temp[index] = temp[pos2]
    moved = temp[pos2]
    temp[pos2] = 0
    temp = tuple(temp)
    return (moved, temp)

#get the goal state
def get_goal(state):
    goal = list(range(1, len(state))) + [0]
    return tuple(goal)

#compare current state to goal state
def is_goal(state):
    goal = tuple(list(range(1, len(state))) + [0])
    return (state == goal)

#backtrack from parents dictionary
def backtrack(parents, end_state):
    state = tuple(end_state)
    backtrack = []
    backtrack.append(end_state)
    value = parents[tuple(state)]
    changes = []

    while value != None:
        changes.append((changed(value, backtrack[-1])))
        backtrack.append(value)
        value = parents[tuple(value)]

    changes.reverse()
    return(changes)

#returns which tile was changed
def changed(state_1, state_2):
    for i in range(0,len(state_1)):
        if state_1[i] != state_2[i]:
            if state_1[i] != 0:
                return str(state_1[i])
            return str(state_2[i])

#get which row the hole is in
def get_row(state):
    index = state.index(int(0))
    n = int(math.sqrt(len(state)))
    return(int(index / n))

#determine whether the puzzle is solvable
def is_solvable(state):
    n = math.sqrt(len(state))
    if n % 2 == 1:
        if get_inversions(state) % 2 == 0:
            return True
        return False
    else:
        hole_row = get_row(state)
        #print ((n - 1 - hole_row) % 2)
        inversions = get_inversions(state)
        #on even rows backwards
        if ((n - 1 - hole_row)) % 2 == 1 and inversions % 2 == 1:
            return True
        #on odd rows backwards
        if ((n - 1 - hole_row) % 2 == 0) and (inversions % 2 == 0):
            return True
        return False

#breadth first search
def BFS(state):
    if is_solvable(state) == False:
        print("UNSOLVABLE")
        return None
    frontier = [(state)]
    discovered = set(tuple(state))
    parents = {tuple(state): None}
    #make sure still have items left in the frontier to explore
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(tuple(current_state))
        #if at goal state, return tile list
        if is_goal(current_state) == True:
            return backtrack(parents, current_state)
        for neighbor in ComputeNeighbors(current_state):
            if tuple(neighbor[1]) not in discovered:
                #add node to the end of the frontier
                frontier.append(neighbor[1])
                discovered.add(tuple(neighbor[1]))
                parents[tuple(neighbor[1])] = tuple(current_state)
    #if puzzle is not solvable, return none
    return None

def DFS(state):
    if is_solvable(state) == False:
        print("UNSOLVABLE")
        return None
    frontier = [(state)]
    discovered = set(tuple(state))
    parents = {tuple(state): None}
    while len(frontier) != 0:
        current_state = frontier.pop(0)
        discovered.add(tuple(current_state))
        if is_goal(current_state) == True:
            return backtrack(parents, current_state)
        for neighbor in ComputeNeighbors(current_state):
            if tuple(neighbor[1]) not in discovered:
                #add node to the start of the frontier
                frontier.insert(0, neighbor[1])
                discovered.add(tuple(neighbor[1]))
                parents[tuple(neighbor[1])] = tuple(current_state)
    print("UNSOLVABLE")
    return None

def BidirectionalSearch(state):
    if is_solvable(state) == False:
        print("UNSOLVABLE")
        return None

    goal = get_goal(state)
    f_frontier = [state]
    b_frontier = [goal]

    discovered_forward = set([state])
    discovered_backward = set([goal])

    parents_forward = {state: None}
    parents_backward = {goal: None}

    #make sure still have items left to explore
    while len(f_frontier) != 0 and len(b_frontier) != 0:
        current_state_forward = f_frontier.pop(0)
        current_state_backward = b_frontier.pop(0)

        discovered_forward.add(tuple(current_state_forward))
        discovered_backward.add(tuple(current_state_backward))

        intersection = discovered_backward.intersection(discovered_forward)
        intersection = list(intersection)

        #found intersecting elements, meaning completed the path
        if len(intersection) > 0:
            intersection_point = next(iter(intersection))
            forward_path = backtrack(parents_forward, intersection_point)
            back_path = list(reversed(backtrack(parents_backward, intersection_point)))
            return forward_path + back_path

        for (neighbor_state_forward) in ComputeNeighbors(current_state_forward):
            if tuple(neighbor_state_forward[1]) not in discovered_forward:
                f_frontier.append(neighbor_state_forward[1])
                discovered_forward.add(neighbor_state_forward[1])
                parents_forward[tuple(neighbor_state_forward[1])] = tuple(current_state_forward)

        #checking the intersection again in case forward search created an intersection point
        intersection = discovered_backward.intersection(discovered_forward)
        if len(intersection) > 0:
            intersection_point = next(iter(intersection))
            forward_path = backtrack(parents_forward, intersection_point)
            back_path = list(reversed(backtrack(parents_backward, intersection_point)))
            return forward_path + back_path

        for (neighbor_state_backward) in ComputeNeighbors(current_state_backward):
            if tuple(neighbor_state_backward[1]) not in discovered_backward:
                b_frontier.append(neighbor_state_backward[1])
                discovered_backward.add(tuple(neighbor_state_backward[1]))
                parents_backward[tuple(neighbor_state_backward[1])] = tuple(current_state_backward)

    return None

#to test whether a puzzle is solvable, calculate the number of inversions.
def get_inversions(state):
    n = int(math.sqrt(len(state)))
    inversions = 0;
    for i in range (0, n*n-1):
        for x in range (i+1, n*n):
            #print(state[i])
            #print(state[x])
            if (state[i] and state[x] != 0) and (state[i] > state[x]):
                #print(state[i])
                #print(state[x])
                inversions = inversions + 1
    return inversions


def main():
    output = LoadFromFile("test_input.txt")
    #print(output)
    if output == None:
        print("Invalid Input")
        return None

    list = tuple(output)
    #n = output[1]
    #check_type(list)
    #debug_state(list)
    #print("COMPUTER NEIGHBORS", ComputeNeighbors(list))
    #is_goal(list)
    #is_goal(list)
    print("DFS", DFS(list))
    #print("LEN DFS", len(DFS(list)))
    #print("DFS", DFS(list))
    print("BDS", BidirectionalSearch(list))
    #print("BDS LEN", len(BidirectionalSearch(list)))
    #print(len(BidirectionalSearch(list)))
    #print(changed((1, 2, 0, 3), (1, 2, 3, 0)))
    print("BFS", (BFS(list)))
    #print(len(BFS(list)))
    #print(get_inversions(list))
    #print(get_row(list))
    #print(is_solvable(list))
    #print("BDS", BidirectionalSearch(list))


if __name__ == "__main__":
    main()
