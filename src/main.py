import insights
import helpers
import time
import asyncio

def main():
    pass
    start_time = time.time()
    # insights.attendance_counter(0,20)
    print(helpers.get_data_by_gameid("2023-01-15"))

    end_time = time.time()

    execution_time = end_time - start_time
    print("Execution time:", execution_time)

if __name__ == "__main__":
    main()