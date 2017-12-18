import sys
import time
import heapq
import copy

class State:

    #static variable for size of matrix
    size=[]

    def __init__(self, matrix_form, map_form):

        self.matrix_form = matrix_form
        self.map_form = map_form


        self.parent = None
        self.state_move=[]

        self.current_cost = 0
        self.heuristic_cost = 0
        self.total_cost = 0

    # greater than method
    def __gt__(self, other):

        return self.total_cost > other.total_cost

    #  == operator
    def __eq__(self, other):

        return self.matrix_form == other.matrix_form

    def __str__(self):
        return str(self.matrix_form)






    def free_to_move_left(self, name):
    #    print(name,"   nimi")
    #    print(self.map_form)
    #    print(self.matrix_form)

        position_matrix=self.map_form[name]
        x=position_matrix[0]

    #    print("x ",x,"y  ", position_matrix[1])
        if x==0:
            return True

        for i in range(0,x):
            #print([self.matrix_form[ i ][position_matrix[1]], i , position_matrix[1]])
            if self.matrix_form[ position_matrix[1] ][i] != "__":
                return False

        return True

    def free_to_move_right(self, name):

        position_matrix=self.map_form[name]

        x = position_matrix[0]+1

        size= State.size[0]

        #print([size,x])
        if x>size:
            return True
        for i in range(x, size):
            #print("silmukassa")
            if self.matrix_form[ position_matrix[1] ][i] != "__":
                return False

        return True

    def get_possible_moves(self):

    #    print(self.free_to_move_right("C1"), "oikea")
    #    print(self.free_to_move_left("C1"), "vasen")
        possible_states=[]
        possible_prices=[]
        possible_car_move=[]

        moves=0
        empty_lane=False

        for key in self.map_form:

            if any([self.free_to_move_right(key), self.free_to_move_left(key)]):
                #print("vapaa liikkuun ",key)

                for line in range( State.size[1])  :

                    for column in  range( State.size[0] ):


                        if self.matrix_form[line][column] == "__":
                            moves+=1
                        #    print("key", key, "line", line, "colums", column)
                            possible_states.append(self.create_state(key,[column, line] ))
                            possible_car_move.append(key)
                            if line != self.map_form[key][1]:
                                possible_prices.append(3)

                            elif  line == self.map_form[key][1] and column==0:
                                possible_prices.append(3)
                            else:
                                possible_prices.append(2)

                            if column==State.size[0]-1:
                                empty_lane=True
                            #set_state.add(self.create_state(key,[column, line] ))
                        else:
                            break

                    if empty_lane==True:
                        #print("tyhjärivi")
                        empty_lane=False
                        continue


                    for column2 in range(State.size[0]-1, -1, -1):

                        if self.matrix_form[line][column2] == "__":
                            moves+=1

                            possible_states.append(self.create_state(key,[column2, line] ))
                            possible_car_move.append(key)

                            if line != self.map_form[key][1]:
                                possible_prices.append(4)

                            elif  line == self.map_form[key][1] and column==0:
                                possible_prices.append(4)
                            else:
                                possible_prices.append(1)

                        else:
                            break


            else:

                pos= self.map_form[key]

                for column in  range( pos[0]-1,0,-1 ):


                    if self.matrix_form[pos[1]][column] == "__":
                        moves+=1
                    #    print("key", key, "line", line, "colums", column)
                        possible_states.append(self.create_state(key,[column, pos[1]] ))
                        possible_car_move.append(key)
                        possible_prices.append(2)

                    else:
                        break

                for column in  range( pos[0]+1, State.size[0] ):


                    if self.matrix_form[pos[1]][column] == "__":
                        moves+=1
                    #    print("key", key, "line", line, "colums", column)
                        possible_states.append(self.create_state(key,[column, pos[1]] ))
                        possible_car_move.append(key)
                        possible_prices.append(1)


                    else:
                        break


        return possible_states, possible_prices, possible_car_move



    def create_state(self, name, new_location):

        new_map=copy.deepcopy(self.map_form)
        new_matrix=copy.deepcopy(self.matrix_form)

        current_location=list(self.map_form[name])
        #new_matrix=list(self.matrix_form)
        new_matrix[current_location[1]][current_location[0]]="__"
        new_matrix[new_location[1]][new_location[0]]=name


        #new_map=dict(self.map_form)
        new_map[name]=new_location

        return State(new_matrix, new_map)






class Astar:
    def __init__(self, start_state, goal_state):


        self.__start_state=start_state
        self.__goal_state=goal_state


    def run_Astar(self):


        openlist=[]
        closedlist=[]

        expansions=0

        start=self.__start_state
        openlist.append(start)

        while openlist:
            process= min(openlist)

            if process == self.__goal_state:
                self.__goal_state=process
                return expansions


            openlist.remove(process)
            closedlist.append(process)

            expanded, prices, cars =process.get_possible_moves()
            expansions+= len(prices)

            for expanded_state in expanded:

                if expanded_state not in closedlist:

                    if expanded_state in openlist:
                        if expanded_state.current_cost> process.current_cost + prices[expanded.index(expanded_state)]:
                            self.update_state(expanded_state ,process ,prices[expanded.index(expanded_state)], cars[expanded.index(expanded_state)])

                    else:
                        self.update_state( expanded_state ,process,prices[expanded.index(expanded_state)], cars[expanded.index(expanded_state)] )
                        openlist.append(expanded_state)




        return False




    def update_state(self, adj, current, price, car  ):

        adj.current_cost=current.current_cost+price
        adj.parent=current
        adj.heuristic_cost=self.heuristic(adj)
        adj.state_move=[car, price]
        adj.total_cost=adj.current_cost+adj.heuristic_cost


    def get_path(self, time, expansions):

        total_cost=0
        total_length=0
        plan_matrix=[]


        print(self.__goal_state)
        previous=self.__goal_state
        while previous != self.__start_state:
            location=previous.map_form[previous.state_move[0]]
            previous_location=previous.parent.map_form[previous.state_move[0]]

            line=','+str(previous.state_move[0])+',L'+str(previous_location[1])+' '+\
            'P'+str(previous_location[0])+',L'+str(location[1])+' P'+str(location[0])+','+str(previous.state_move[1])

            plan_matrix.append(line)
            total_cost+=previous.state_move[1]
            previous=previous.parent
            print(previous)
            total_length +=1

        #print(self.__start_state)
        plan_matrix=list(reversed(plan_matrix))

        for i in range(len(plan_matrix)):
            plan_matrix[i]=str(i+1)+plan_matrix[i]
        print(plan_matrix)
        plan_file=open('extension.plan','w')
        for item in plan_matrix:
            plan_file.write("{}\n".format(item))

        plan_file.close()
        information_file=open('extension.info','w')
        information_file.write('Step length: '+str(total_length)+'\n')
        information_file.write('Running time (seconds): ' + str(time)+'\n')
        information_file.write('Total cost: '+str( total_cost)+'\n')
        information_file.write('Expansions: '+str( expansions)+'\n')
        information_file.close()
        print("total cost ", total_cost, "total length", total_length)
        return




    def heuristic(self, current_state):

        heuristic_cost=0
        current_state=current_state.map_form

        for key in current_state:
            car_pos=current_state[key]
            car_goal=self.__goal_state.map_form[key]
            x_change=car_pos[0]-car_goal[0]
            y_change=car_pos[1]-car_goal[1]


            if y_change !=0:
                if self.__goal_state.free_to_move_right(key):
                    heuristic_cost=+4
                else:
                    heuristic_cost+=3
            else:
                if x_change < 0 :
                    heuristic_cost += 1
                elif x_change >0:
                    heuristic_cost += 2

        return heuristic_cost









def main():
    start_time=time.time()

    start_file =sys.argv[1]
    goal_file=sys.argv[2]

    start_state, size =read_file(start_file)
    goal_state, size  =read_file(goal_file)


    State.size=size

    astar=Astar(start_state, goal_state)

    expansion= astar.run_Astar()

    if expansion==False:
        print("no solution found")
        return
    end_time=time.time()
    consumed_time=end_time-start_time
    time_2_decimal=format(consumed_time, '.2f')

    astar.get_path(time_2_decimal, expansion)
    print("time ",time_2_decimal,"expands", expansion)





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

    #print(first_row)
    lines.pop(0)

    for i in range(len(lines)):
        line=lines[i]
        line.strip()
        line_vec=line.split()
        matrix.append(line_vec)

        for e in range(len(line_vec)):
            hasmap[line_vec[e]]=[e,i]


    hasmap.pop("__", None)
    #print(hasmap)

    return State(matrix, hasmap), first_row


def write_files(result):
    pass

if __name__=="__main__":
    main()
