import insights
import helpers
import time
import json
def main():
    pass
    start_time = time.time()

    """
    avoid calling init_db_data() again if possible (takes over 1 minute right now).
    it is really not expected to be used often at all (literally only when we first ever create db or 
    maybe if data becomes corrupted or we mess up on some insertions).
    """ 
    

    # helpers.init_db_data() 

    end_time = time.time()

    execution_time = end_time - start_time
    print("Execution time:", execution_time)

if __name__ == "__main__":
    main()