import sys


def heuristic(current, goal):

    pass


def main():
    start_file =sys.argv[1]
    goal_file=sys.argv[2]
    start=read_file(start_file)
    goal=read_file(goal_file)
    current_cost=[]
    current_route=[]




def read_file(filename):
    file=open(filename, "r")
    lines=file.readlines()
    file.close()
    hasmap={}
    matrix= []
    first_row=lines[0]
    lines.pop(0)

    for i in range(len(lines)):
        line=lines[i]
        line.strip()
        line_vec=line.split()

        for e in range(len(line_vec)):
            hasmap[line_vec[e]]=[e,i]


    for line in lines:
        line.strip()
        line_vec= line.split()
        matrix.append(line_vec)

    print(hasmap)
    return matrix

main()
