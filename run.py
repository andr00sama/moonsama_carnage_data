from inputs import raw_result_array, raw_gganbu_array
from functions import get_and_load_dictionary, sama_sorter

for week in range (48,56):
    week_index = week - 17
    print("Week Number: " + str(week))
    gganbu_dictionary = get_and_load_dictionary(raw_gganbu_array[week_index])
    result_dictionary = get_and_load_dictionary(raw_result_array[week_index])
    sama_sorter(result_dictionary, gganbu_dictionary)
    print(" ")
