import numpy as np
from progress.bar import Bar
import matplotlib.pyplot as plt


class Queue:

    runtime : float
    simulation_time : float
    next_arrival_time : float
    num_servers : int
    servers_data : list
    queue_len : int
    arrival_rate : float
    service_rate : float
    I_n : int
    customer_data : dict
    

    def __init__(self, simulation_time : float, num_servers : int, arrival_rate : float, service_rate : float) -> None:

        self.simulation_time = simulation_time
        self.num_servers = num_servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.runtime = 0
        self.queue_len = 0
        self.I_n = 0
        
        self.servers_data = []
        self.customer_data = {}
        self.servers_data.append(0)
        for _ in range(self.num_servers):
            self.servers_data.append(float('inf'))

    
    def arrival_time(self) -> float:
        return np.random.exponential(1/self.arrival_rate)
    
    
    def service_time(self) -> float:
        return np.random.exponential(1/self.service_rate)       

    
    def run_simulation(self, runtime, N : int = 0, find_p : bool = False,) -> None:
        self.next_arrival_time = self.arrival_time()
        time = 0
        count = 1

        exceeded_flag = False
        #bar = Bar('Processing', max=10000)

        """
        print(self.servers_data)
        print(self.next_arrival_time)
        print(f'Час, який пройшов: {time}')
        print()
        """
    
        while time <= runtime:
            #print(time)
            index_next_free_server = np.argmin(self.servers_data[1:]) + 1
            next_free_server = self.servers_data[index_next_free_server]         

            #print(index_next_free_server)

            if self.next_arrival_time < next_free_server:
                prev_time = time
                time += self.next_arrival_time

                customer_id = len(self.customer_data) + 1
                self.customer_data[customer_id] = {}

                if self.servers_data[0] == self.num_servers:
                    self.servers_data[0] = self.num_servers

                    self.customer_data[customer_id]['arrival_time'] = time
                    self.customer_data[customer_id]['start_service_time'] = prev_time + next_free_server

                    for i in range(1,self.num_servers+1):
                        self.servers_data[i] -= self.next_arrival_time

                    self.queue_len += 1

                elif self.servers_data[0] < self.num_servers:

                    self.servers_data[0] += 1

                    self.customer_data[customer_id]['arrival_time'] = time
                    self.customer_data[customer_id]['start_service_time'] = time

                    index_next_free_server = next(i for i,v in enumerate(self.servers_data) if v == float('inf'))

                    for i in range(1,self.num_servers+1):
                        if i == index_next_free_server:
                            continue
                        
                        self.servers_data[i] -= self.next_arrival_time
                    
                    self.servers_data[index_next_free_server] = self.service_time()
                
                self.next_arrival_time = self.arrival_time()


            elif self.next_arrival_time > next_free_server:
                time += next_free_server

                self.next_arrival_time -= next_free_server


                """
                tmp = list(self.customer_data.items())
                min_value_key = ''
                min_value = 0

                for j in range(1, len(tmp)):
                    if not(tmp[j][1]['start_service_time']):
                        min_value_key = tmp[j][0]
                        min_value = tmp[j][1]['arrival_time']
                        break

                for i in range(1, len(tmp)):
                    if min_value > tmp[i][1]['arrival_time'] and not(tmp[i][1]['start_service_time']):
                        min_value = tmp[i][1]['arrival_time']
                        min_value_key = tmp[i][0]
                
                """

                if self.queue_len:
                    self.servers_data[0] = self.num_servers

                #    self.customer_data[min_value_key]['start_service_time'] = time
                    
                    for i in range(1,self.num_servers+1):
                        if i == index_next_free_server:
                            continue

                        self.servers_data[i] -= next_free_server
                    
                    self.servers_data[index_next_free_server] = self.service_time()
                    self.queue_len -= 1
                    
                else:
                    self.servers_data[0] -= 1

                    for i in range(1,self.num_servers+1):
                        if i == index_next_free_server:
                            continue

                        self.servers_data[i] -= next_free_server

                    self.servers_data[index_next_free_server] = float('inf')
                

            """
            print(f'iteration: {count}')
            print(self.servers_data)
            print(f'Наступна заявка надійде через: {self.next_arrival_time}')
            print(f'Розмір черги: {self.queue_len}')
            print(f'Час, який пройшов: {time}')
            print(self.customer_data)
            print()
            count += 1
            """
            
            if find_p and self.num_servers + self.queue_len > N:
                exceeded_flag = True
                break

            #bar.next()
        
        #bar.finish()
                

        if not(exceeded_flag):
            self.I_n += 1


    def find_stationary_waiting_mean(self, runtime):
        time = range(0, runtime, 100)
        
        waiting_times = []
        waiting_mean = 0

        bar = Bar('Processing', max=len(time))

        for i in time:
            waiting_mean = self.calculate_waiting_mean(i)

            waiting_times.append(waiting_mean)

            self.reset()
            bar.next()
        
        bar.finish()

        return time, waiting_times
    

    def calculate_waiting_mean(self, runtime):
        self.run_simulation(runtime)

        waiting_time = 0
        customers_count = 0
        waiting_mean = 0
        tmp = list(self.customer_data.items())
        #print(self.customer_data)

        for j in range(len(tmp)):
            if tmp[j][1]['start_service_time']:
                waiting_time += tmp[j][1]['start_service_time'] - tmp[j][1]['arrival_time']
                customers_count += 1

        #print(waiting_time)
        #print(customers_count)

        if customers_count:
            waiting_mean = waiting_time / customers_count

        return waiting_mean


    def draw_graph(self, arguments, values):
        plt.plot(arguments, values)
        plt.xlabel('Simulation time')
        plt.ylabel('Waiting time mean')
        plt.title("Mean wating time graph")
        plt.show()


    def find_P(self, N : int):
        l = 0
        L = 10**6

        bar = Bar('Processing', max=L)

        while l < L:
            self.run_simulation(N, find_p = True)
            l += 1
            bar.next()
        
        bar.finish()

        return self.I_n / L


    def reset(self):
        self.runtime = 0
        self.queue_len = 0
        self.I_n = 0
        
        self.servers_data = []
        self.customer_data = {}
        self.servers_data.append(0)
        for _ in range(self.num_servers):
            self.servers_data.append(float('inf'))

    
    def find_theoretical_P_losses(self, N : int):
        P_0 = 0
        rho = self.arrival_rate / self.service_rate

        for i in range(N+1):
            P_0 += rho ** i / np.math.factorial(i)

        P_0 = 1 / P_0

        P_N = P_0 * rho ** N / np.math.factorial(N)

        return P_N

    
    def find_theoretical_P(self, N : int):
        P_0 = 0
        rho = self.arrival_rate / self.service_rate

        for i in range(self.num_servers):
            P_0 += rho ** i / np.math.factorial(i)
        
        P_0 += rho ** self.num_servers / (np.math.factorial(self.num_servers) * (1 - (rho / self.num_servers)))

        if N >= 1 and N <= self.num_servers:
            P_N = P_0 * rho ** N
        elif N > self.num_servers:
            P_N = P_0 * ((rho / self.num_servers) ** N) * (self.num_servers ** self.num_servers / np.math.factorial(self.num_servers))

        return P_N