import queueing_system

def run():
    test = queueing_system.Queue(100000, 1, 1, 20)
    rho = test.arrival_rate / test.service_rate
    #test.run_simulation()
    #time, means = test.find_stationary_waiting_mean(40000)
    w = test.calculate_waiting_mean(100000)
    #test.draw_graph(time, means)
    print(f'Середній час чекання в черзі: {w}')
    print(f'Теоретичний середній час чекання в черзі: {rho / (test.service_rate - test.arrival_rate)}')
    #test.draw_graph(time, waitings)
    #print(f'Theoretical P_k = {test.find_theoretical_P(5)}')
   # print(f'P_k = {test.find_P(N = 5)}')
    #print(test.I_n)
    #print(f'Theoretical P_k = {(1- test.arrival_rate / test.service_rate)*(test.arrival_rate / test.service_rate)**5}')



if __name__ == "__main__":
    #try:
        run()
    #except BaseException as ex:
    #    print(f"[ERROR]: something went totally wrong: {ex}")
