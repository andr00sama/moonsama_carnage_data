import tiny 
import utils 

# create frequency table
def frequency_table(vals):
    hist = {}
    get = hist.get
    for i in vals:
        hist[i] = get(i, 0) + 1
    return hist