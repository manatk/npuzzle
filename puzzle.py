import math
def read_input():
    input = open("test_input.txt", "r")
    all_lines = input.readlines()
    n = int(all_lines[0].strip())
    all_lines.pop(0)
    if len(all_lines) != n:
        return None
    list = []
    for i in all_lines:
        i = i.strip()
        i = i.split('\t')
        #check to make sure that the row has valid length
        if isValid(i,n) == False:
            return None
        for x in i:
            if x == "*":
                list.append(0)
            else:
                list.append(int(x))
        #list = list + [int(x) for x in i if x != '*' else x = 0]
    return(list, n)

def check_type(list):
    for i in list:
        print(type(i))

def isValid(i,n):
    if len(i) != n:
        return False

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

def compute_neighbors(state):
    n = math.sqrt(len(state))
    #print(state)
    index = state.index(int(0))
    neighbor_list = []
    #print("INDEX IS" , index)

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

def swap(state, index, pos2):
    pos2 = int(pos2)
    temp = state[:]
    temp[index] = temp[pos2]
    moved = temp[pos2]
    #print(temp[pos2])
    temp[pos2] = 0
    return (moved, temp)

def isGoal(state):
    goal = list(range(1, len(state))) + [0]
    #print(goal)
    return (state == goal)

def backtrack(parents, end_state):
    state = tuple(end_state)
    backtrack = []
    backtrack.append(end_state)
    value = parents[tuple(state)]

    while value != None:
        backtrack.append(value)
        value = parents[tuple(value)]

    backtrack.reverse()
    print("BACKTRACK IS" , backtrack)
    return backtrack


def BFS(state):
    frontier = [(state)]
    discovered = set(tuple(state))
    parents = {tuple(state): None}
    while len(frontier) != 0:
        #print ("Fronter is ", frontier)
        current_state = frontier.pop(0)
        #(debug_state(current_state))
        #print("")
        discovered.add(tuple(current_state))
        if isGoal(current_state) == True:
            print("HERE")
            return backtrack(parents, current_state)
        for neighbor in compute_neighbors(current_state):
            #print(neighbor)
            if tuple(neighbor[1]) not in discovered:
                frontier.append(neighbor[1])
                discovered.add(tuple(neighbor[1]))
                parents[tuple(neighbor[1])] = tuple(current_state)

def DFS(state):
    frontier = [(state)]
    discovered = set(tuple(state))
    parents = {tuple(state): None}
    while len(frontier) != 0:
        #print ("Fronter is ", frontier)
        current_state = frontier.pop(0)
        #(debug_state(current_state))
        #print("")
        discovered.add(tuple(current_state))
        if isGoal(current_state) == True:
            print("HERE")
            return backtrack(parents, current_state)
        for neighbor in compute_neighbors(current_state):
            #print(neighbor)
            if tuple(neighbor[1]) not in discovered:
                frontier.insert(0, neighbor[1])
                discovered.add(tuple(neighbor[1]))
                parents[tuple(neighbor[1])] = tuple(current_state)

def main():
    output = read_input()
    if output == None:
        print("invalid input")
        return None
    list = output[0]
    n = output[1]
    #check_type(list)
    #debug_state(list)
    #print(compute_neighbors(list))
    #isGoal(list)
    #isGoal(list)
    DFS(list)
    BFS(list)


if __name__ == "__main__":
    main()
