#Teemu Pöytäniemi, Niklas Nystad
import sys
import time
import heapq
import copy

#class implemets one state and it has all functions which are needed to manipulate states
class State:

    #static variable for size of matrix
    size=[]

    #constuctor which creates public variables for class
    def __init__(self, matrix_form, map_form):

        #state is stored as a vector and a map
        self.matrix_form = matrix_form
        self.map_form = map_form


        self.parent = None
        self.state_move=[]

        self.current_cost = 0
        self.heuristic_cost = 0
        self.total_cost = 0

    # greater than method, this method is needed to sort the openlist
    def __gt__(self, other):

        if self.total_cost != other.total_cost:
            return self.total_cost > other.total_cost
        else:

            return self.current_cost > other.current_cost


    #  == operator, needed to compair the states
    def __eq__(self, other):

        return self.matrix_form == other.matrix_form

    #only for printing the state
    def __str__(self):
        return str(self.matrix_form)





    #checks if the is free to move left
    #@param car's name, key to the map
    #@return bool
    def free_to_move_left(self, name):


        position_matrix=self.map_form[name]
        x=position_matrix[0]


        if x==0:
            return True

        for i in range(0,x):

            if self.matrix_form[ position_matrix[1] ][i] != "__":
                return False

        return True

    #checks if the car is free to move right
    #@param car's name, key to the map
    #@return bool
    def free_to_move_right(self, name):

        position_matrix=self.map_form[name]

        x = position_matrix[0]+1

        size= State.size[0]


        if x>size:
            return True
        for i in range(x, size):

            if self.matrix_form[ position_matrix[1] ][i] != "__":
                return False

        return True

    #this method creates all possible states from current states
    #@return list of all possible states, list of prices and list of moved cars
    def get_possible_moves(self):


        possible_states=[]
        possible_prices=[]
        possible_car_move=[]

        moves=0
        empty_lane=False

        for key in self.map_form:

            if any([self.free_to_move_right(key), self.free_to_move_left(key)]):


                for line in range( State.size[1])  :

                    for column in  range( State.size[0] ):


                        if self.matrix_form[line][column] == "__":
                            moves+=1

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

                        else:
                            break

                    if empty_lane==True:

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

                        possible_states.append(self.create_state(key,[column, pos[1]] ))
                        possible_car_move.append(key)
                        possible_prices.append(2)

                    else:
                        break

                for column in  range( pos[0]+1, State.size[0] ):


                    if self.matrix_form[pos[1]][column] == "__":
                        moves+=1

                        possible_states.append(self.create_state(key,[column, pos[1]] ))
                        possible_car_move.append(key)
                        possible_prices.append(1)


                    else:
                        break


        return possible_states, possible_prices, possible_car_move


    #creates a new state from other
    #@param name of moved car to create a new state, car's new location
    #@return new State object
    def create_state(self, name, new_location):

        #have to create deep copy from private cariables
        new_map=copy.deepcopy(self.map_form)
        new_matrix=copy.deepcopy(self.matrix_form)

        current_location=list(self.map_form[name])

        new_matrix[current_location[1]][current_location[0]]="__"
        new_matrix[new_location[1]][new_location[0]]=name



        new_map[name]=new_location

        return State(new_matrix, new_map)





# This class implements A* algorit
class Astar:
    #constructor creates private variables start state and goal state
    def __init__(self, start_state, goal_state):


        self.__start_state=start_state
        self.__goal_state=goal_state


    #A* algorit
    #openlist is implemented as a heap, so sorting algorit is heap sort
    def run_Astar(self):


        openlist=[]
        closedlist=[]


        expansions=0

        start=self.__start_state
        openlist.append(start)
        heapq.heapify(openlist)

        kierrokset=1

        while openlist:


            process= heapq.heappop(openlist)
            print(kierrokset, "valittu tila ", process)
            kierrokset+=1

            if process == self.__goal_state:
                self.__goal_state=process
                return expansions



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
                        #print(expanded_state.total_cost , expanded_state, "h ",expanded_state.heuristic_cost)
                        heapq.heappush(openlist,expanded_state)




        return False



    #update states costs
    #@param adj is a neibhour state, current state, price to move between states, the car which has been moved
    #@return void
    def update_state(self, adj, current, price, car  ):

        adj.current_cost=current.current_cost+price
        adj.parent=current
        adj.heuristic_cost=self.heuristic(adj)
        adj.state_move=[car, price]
        adj.total_cost=adj.current_cost+adj.heuristic_cost


    #creates output files
    #@param time consumed to calculate the task, expansions
    #@return void but creates files extension.info and extension.plan if not excist allready
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




    #heirstic function, calculates the distance assuming that you can move cars
    # throw others and if the car in the goal state is not at the end of lane you
    #can push it to its place with price 3
    #@param State object
    def heuristic(self, current_stat):

        heuristic_cost=0
        current_state=current_stat.map_form


        for key in current_state:
            car_pos=current_state[key]
            car_goal=self.__goal_state.map_form[key]
            x_change=car_pos[0]-car_goal[0]
            y_change=car_pos[1]-car_goal[1]


            if y_change !=0:
                if self.__goal_state.free_to_move_right(key):
                    heuristic_cost+=4
                else:
                    heuristic_cost+=3
            else:
                if x_change < 0 :
                    heuristic_cost += 1
                elif x_change >0:
                    heuristic_cost += 2
        #print( current_state," __  ",heuristic_cost)
        return heuristic_cost








#main function which is called when the program starts
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




#reads the file
#@param: file name
#@return State object(first time called init state, last time goal state), first row as a list
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


    lines.pop(0)

    for i in range(len(lines)):
        line=lines[i]
        line.strip()
        line_vec=line.split()
        matrix.append(line_vec)

        for e in range(len(line_vec)):
            hasmap[line_vec[e]]=[e,i]


    hasmap.pop("__", None)


    return State(matrix, hasmap), first_row



if __name__=="__main__":
    main()
