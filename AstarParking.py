import sys
import time
import heapq

class State:

    #static variable for size of matrix
    size=[]

    def __init__(self, matrix_form, map_form):

        self.matrix_form = matrix_form
        self.map_form = map_form


        self.parent = None

        self.current_cost = 0
        self.heuristic_cost = 0
        self.total_cost = 0

    # greater than method
    def __gt__(self, other):

        return self.total_cost > other.total_cost

    #  == operator
    def __eq__(self, other):

        return self.matrix_form == other.matrix_form

    def free_to_move_left(self, position_matrix):

        x=position_matrix[0]-1

        if x<0:
            return True

        for i in range(0,x):
            if self.matrix_form[ position_matrix[1] ][i] != "__":
                return False

        return True

    def free_to_move_right(self, position_matrix):

        x = position_matrix[0]+1

        size=self.matrix_form[0].size()-1

        if x>size:
            return True
        for i in range(x, size):
            if self.matrix_form[ position_matrix[1] ][i] != "__":
                return False

        return True

    def get_possible_moves(self):

        possible_states=[]

        for key in self.map_form:

            if self.free_to_move_right() or self.free_to_move_left():

                for line_vec in range self.matrix_form:

                    for car in line_vec:

                        if car == "__":
                            




        #saman rivin paikan vaihdokset

        nimi="a"
        paikka=[2,1]

        #vasempaan
        x=paikka[0]-1
        #mahdolliset paikat vasempaan

        for i in range(x,0,-1):
            if self.matrix_form[paikka[1]][i]="__":
                #create new state
            else:
                break









class Astar:
    def __init__(self, start_state, goal_state):


        self.__openlist=[]
        heapq.heapify(self.__openlist)
        self.__closed=[]
        #self.__cells=[]
        self.__start_state=start_state
        self.__goal_state=goal_state







    def __get_path(self):
        pass




    def heuristic(self, current_state):

        heuristic_cost=0

        for key in current_state:
            car_pos=current_state[key]
            car_goal=self.__final_map[key]
            x_change=car_pos[0]-car_goal[0]
            y_change=car_pos[1]-car_goal[1]

            if x_change < 0 :
                heuristic_cost += 1
            elif x_change >0:
                heuristic_cost += 2
            elif x_change ==0 and y_change !=0:
                heuristic_cost += 1

            if y_change !=0:
                heuristic_cost += 1

        return heuristic_cost


    def run_Astar(self):
        pass

    def __get_legal_moves(self):
        pass




def main():
    start_time=time.time()

    start_file =sys.argv[1]
    goal_file=sys.argv[2]

    start_state, size =read_file(start_file)
    goal_state, size  =read_file(goal_file)

    State.size=size

    astar=Astar(start_state, goal_state)

    result= astar.run_Astar()

    wrire_files(result)

    #price= astar.heuristic(start_map)
    #print(price)




def read_file(filename):

    file=open(filename, "r")
    lines=file.readlines()
    file.close()

    hasmap={}
    matrix= []
    first_row=lines[0]
    first_row= first_row.strip()
    first_row=first_row.split()
    first_row= [int(s) for s in first_row]

    print(first_row)
    lines.pop(0)

    for i in range(len(lines)):
        line=lines[i]
        line.strip()
        line_vec=line.split()
        matrix.append(line_vec)

        for e in range(len(line_vec)):
            hasmap[line_vec[e]]=[e,i]

    print(hasmap)

    return State(matrix, hasmap), first_row


def wrire_files(result):
    pass

if __name__=="__main__":
    main()
