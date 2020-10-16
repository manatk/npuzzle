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

def debug_state(state, n):
    row = ""
    n_count = 0
    for i in state:
        row = row + str(i)
        if (n_count % n) == n-1:
            print(row)
            row = ""
        n_count = n_count + 1

def compute_neighbors(state, n):
    print(state)
    index = state.index(int(0))
    neighbor_list = []
    print("INDEX IS" , index)

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
    temp = state[:]
    temp[index] = temp[pos2]
    #print(temp[pos2])
    temp[pos2] = 0
    return temp

def isGoal(state):
    print(state)
    goal = (sorted(state))
    return (state == goal)

def main():
    output = read_input()
    if output == None:
        print("invalid input")
        return None
    list = output[0]
    n = output[1]
    #check_type(list)
    #debug_state(list, n)
    print(compute_neighbors(list, n))
    #isGoal(list)

if __name__ == "__main__":
    main()
