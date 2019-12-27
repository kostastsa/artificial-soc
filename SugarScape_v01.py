import matplotlib.pyplot as plt
import matplotlib as mpl
import scipy as sp
import random as rnd
from pylab import meshgrid
from matplotlib import cm
from matplotlib.pyplot import pause as pause



def f(x, mu, sigma):
    return 10*sp.exp(-((x[0]-mu[0])**2+(x[1]-mu[1])**2)/sigma**2)



class Space:
    ''' The Sugarscape of our simulation. The various attributes and methods defined may vary. The indexing
    of the places in the sugarscape follows the convention of labelling matrix elements. The origin is in the
    upper left corner of the map and position [i,j] means i places down, j places right.
    '''


    def __init__(self, capacity):
        self.capacity = capacity
        self.sugarscape = sp.copy(capacity)
        self.size = len(capacity)
        self.agent_map = sp.zeros([len(capacity), len(capacity)])

        

    # Growback Rule (should make it more efficient)
    def growback(self, alpha):
            for i in range(self.size):
                for j in range(self.size):
                    self.sugarscape[i,j] = min(self.capacity[i,j], self.sugarscape[i,j] + alpha)
            


class Agent:
    ''' An Agent is an object with the following attributes:

        - metabolism : how much sugar the agent consumes each tick
        - vision : how far the agent can see in the four principal directions
        - position : its position in the sugarscape is an array of its coordinates.
                     we follow the convention of matrix indexing to denote position,
                     therefore position [i,j] means i positions down j positions right, the
                     origing being in the upper left corner of our map.
        - sex : M , F
        - wealth : the amount of sugar the agent has in its possession
    '''

    
    def __init__(self, size):
        ''' This initializer creates an Agent object with certain attributes. The variable scape
            is a 'copy' of the sugarscape capacity matrix. The Agent interacts with the sugarscape
            through this variable.
        '''
        self.size = size
        self.position = sp.array([rnd.randint(0, size - 1), rnd.randint(0, size - 1)])
        self.metabolism = rnd.randint(1, 3)
        self.vision = rnd.randint(1, 6)
        self.sex = rnd.choice(['M', 'F'])
        self.wealth = 0


    # Movement Rule
    def movement(self, scape):
        ''' The Movement Rule of the Agents : they look as far as their vision permits in the
            four principal directions, throw out occupied cells and randomly go to the cell with
            the most sugar that is the closest.

            The SugarScape has the topology of a torus, and this is implemented in this function.
        '''
        dir_north = sp.array([-1,0])
        dir_east = sp.array([0,1])
        dir_south = sp.array([1,0])
        dir_west = sp.array([0,-1])
        

        sugar_north = [scape.sugarscape[self.position[0] - v , self.position[1]] for
                            v in range(1, self.vision + 1)]

        agents_north = [scape.agent_map[self.position[0] - v , self.position[1]] for
                            v in range(1, self.vision + 1)]

        sugar_east = [scape.sugarscape[self.position[0],
                                                 (self.position[1] + v)%(scape.size)]
                            for v in range(1, self.vision + 1)]

        agents_east = [scape.agent_map[self.position[0],
                                                 (self.position[1] + v)%(scape.size)]
                            for v in range(1, self.vision + 1)]

        sugar_south = [scape.sugarscape[(self.position[0] + v)%(scape.size)
                                                   , self.position[1]]
                            for v in range(1, self.vision + 1)]
        
        agents_south = [scape.agent_map[(self.position[0] + v)%(scape.size)
                                                   , self.position[1]]
                            for v in range(1, self.vision + 1)]

        sugar_west = [scape.sugarscape[self.position[0], self.position[1] - v ] for
                            v in range(1, self.vision + 1)]

        agents_west = [scape.agent_map[self.position[0], self.position[1] - v ] for
                            v in range(1, self.vision + 1)]

        north_rank = sp.array(sugar_north) - 1000*sp.array(agents_north)
        east_rank = sp.array(sugar_east) - 1000*sp.array(agents_east)
        south_rank = sp.array(sugar_south) - 1000*sp.array(agents_south)
        west_rank = sp.array(sugar_west) - 1000*sp.array(agents_west)
        


        options = {(tuple(dir_north), sp.argmax(north_rank)) : max(north_rank),
                   (tuple(dir_east), sp.argmax(east_rank))   : max(east_rank),
                   (tuple(dir_south), sp.argmax(south_rank)) : max(south_rank),
                   (tuple(dir_west), sp.argmax(west_rank))   : max(west_rank)}

        

        keys = list(options.keys())
        values = list(options.values())
        max_ind = [i for i in range(len(values)) if values[i]==max(values)]
        best_options = {keys[i]:values[i] for i in max_ind}
        best_opt_keys = list(best_options.keys())
        argmaxes = [i[1] for i in best_opt_keys]
        min_argmax_ind = [i for i in range(len(argmaxes)) if argmaxes[i] == min(argmaxes)]
        move_tuple = rnd.choice([best_opt_keys[i] for i in min_argmax_ind])
        move_dir = sp.array(move_tuple[0])
        move_dist = move_tuple[1] + 1
        scape.agent_map[self.position[0], self.position[1]] = 0
        self.position = self.position + move_dist*move_dir
        self.position = [i%self.size for i in self.position]
        scape.agent_map[self.position[0], self.position[1]] = 1


        
            
    def metabolize(self, scape):
        pos = self.position
        self.wealth += scape.sugarscape[pos[0],pos[1]] - self.metabolism
        scape.sugarscape[pos[0],pos[1]] = 0
        


   
size = 100
x = sp.arange(0,size)
y = sp.arange(0,size)
X,Y = meshgrid(x,y)

##CAP = sp.array([[f([i,j], [0.5*size , 0.5*size], 0.4*size) for i in range(size)]
##               for j in range(size)]) + \
##       sp.array([[f([i,j], [0.5*size, 0.5*size], 0.4*size) for i in range(size)]
##               for j in range(size)])

hills = [(rnd.random()*size, rnd.random()*size) for i in range(20)]
CAP_LIST = [sp.array([[f([i,j], mu, 0.07*size) for i in range(size)]
               for j in range(size)]) for mu in hills]

CAP = sum(CAP_LIST) + sp.ones([size, size])

##CAP = 4*sp.ones([size, size])



S = Space(CAP)
Z = S.sugarscape


Agents = [Agent(S.size) for i in range(100)]

##Agents = []
##for i in range(30):
##    for j in range(30):
##        Agents.append(Agent(S.size , sp.array([i, j])))

for a in Agents:
    S.agent_map[a.position[0], a.position[1]] = 1
    

cmap = cm.binary
Z.astype(int)

wealth_matrix0 = []
population = []

for i in range(1,100):
    fig, ax = plt.subplots()
    ax.xaxis.tick_top()
    plt.gca().invert_yaxis()
    cm = ax.pcolormesh(Z, cmap = cmap)
    fig.colorbar(cm)
    ax.spy(S.agent_map , marker = 'o', markersize = 2)
    
    fig.show()
    pause(0.1)
    plt.close()

    population.append(len(Agents))

 
    S.growback(1)
    for a in sp.random.permutation(Agents):
        a.metabolize(S)
        a.movement(S)
        if a.wealth <= 0:
            S.agent_map[a.position[0] , a.position[1]] = 0
            Agents.remove(a)

    


plt.plot(population)
plt.show()

















            
