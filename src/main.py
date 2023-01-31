import utils
import time
import json
import tiny 
import insights
import tkinter
import matplotlib
matplotlib.use( 'Agg' )
import numpy as np

def main():

    import matplotlib.pyplot as plt


    # start_time = time.time()
    # end_time = time.time()
    # execution_time = end_time - start_time
    # print("Execution time:", execution_time)

    # commented out because the below method fetches every endpoint from mcapi and stores it all locally
    # tiny.fetch_all_and_store()

    gameids = utils.carnage_dates()
    gameid = gameids[-1].date()
    data = tiny.get_data_by_gameid(gameid)
    
    lb_example = data[0]['data']['leaderboards']['leaderboards'][6]['leaderboard']
    lb_example_name = data[0]['data']['leaderboards']['leaderboards'][6]['itemId']

    pnames = [player['name'] for player in lb_example]
    pamounts = [player['amount'] for player in lb_example]     

    ft = insights.frequency_table(pamounts)

    # An "interface" to matplotlib.axes.Axes.hist() method
    n, bins, patches = plt.hist(x=pamounts, bins=11, color='#0504aa',
                                alpha=0.7, rwidth=0.85)
    plt.grid(axis='y', alpha=0.75)
    plt.xlabel('Value')
    plt.ylabel('Frequency')
    plt.title('My Very Own Histogram')
    plt.text(23, 45, r'$\mu=15, b=3$')
    maxfreq = n.max()
    # Set a clean upper y-axis limit.
    plt.ylim(ymax=np.ceil(maxfreq / 10) * 10 if maxfreq % 10 else maxfreq + 10)
    plt.savefig('figure.png')
    print(lb_example_name)
    print(bins)
    print(sum(n))

    # [print(pnames[i], pamounts[i]) for i in range(len(pnames))]

if __name__ == "__main__":
    main()