import numpy as np


class Queue:

    runtime : float
    simulation_time : float
    next_arrival_time : float
    num_servers : int
    servers_data : list
    queue_len : int
    arrival_rate : float
    service_rate : float
    

    def __init__(self, simulation_time : float, num_servers : int, arrival_rate : float, service_rate : float) -> None:

        self.simulation_time = simulation_time
        self.num_servers = num_servers
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.runtime = 0
        self.queue_len = 0
        
        self.servers_data = []
        self.servers_data.append(0)
        for _ in range(self.num_servers):
            self.servers_data.append(float('inf'))

    
    def arrival_time(self) -> float:
        return np.random.exponential(1 / self.arrival_rate)
    
    
    def service_time(self) -> float:
        return np.random.exponential(1 / self.service_rate)       

    
    def run_simulation(self) -> None:
        self.next_arrival_time = self.arrival_time()
        time = 0
        count = 1

        print(self.servers_data)
        print(self.next_arrival_time)

        while time <= self.simulation_time:
            index_next_free_server = np.argmin(self.servers_data[1:]) + 1
            next_free_server = self.servers_data[index_next_free_server]

            #print(index_next_free_server)

            if self.next_arrival_time < next_free_server:
                time += self.next_arrival_time

                if self.servers_data[0] == self.num_servers:
                    self.servers_data[0] = self.num_servers

                    for i in range(1,self.num_servers+1):
                        self.servers_data[i] -= self.next_arrival_time

                    self.queue_len += 1

                elif self.servers_data[0] < self.num_servers:
                    self.servers_data[0] += 1

                    free_server_index = next(i for i,v in enumerate(self.servers_data) if v == float('inf'))

                    for i in range(1,self.num_servers+1):
                        if i == free_server_index:
                            continue
                        
                        self.servers_data[i] -= self.next_arrival_time
                    
                    self.servers_data[free_server_index] = self.service_time()
                
                self.next_arrival_time = self.arrival_time()


            elif self.next_arrival_time > next_free_server:
                time += next_free_server

                self.next_arrival_time -= next_free_server

                if self.queue_len:
                    self.servers_data[0] = self.num_servers
                    
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
            

            print(f'iteration: {count}')
            print(self.servers_data)
            print(self.next_arrival_time)
            print(self.queue_len)
            print()
            count += 1