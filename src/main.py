import queueing_system

def run():
    test = queueing_system.Queue(100, 5, 10, 11)
    test.run_simulation()


if __name__ == "__main__":
    #try:
        run()
    #except BaseException as ex:
    #    print(f"[ERROR]: something went totally wrong: {ex}")
