def get_and_load_dictionary(input):
    import requests, json
    return json.loads(requests.get(input).text)

def sama_sorter(result_dictionary, gganbu_dictionary):
    moonsama_list = []
    exosama_list = []
    gromlinvip_list = []
    moonsama_count = 0
    exosama_count = 0
    gromlinvip_count = 0
    for player in result_dictionary.keys():
        if result_dictionary.get(player).get("stone")*5%1 == 0:
            gromlinvip_list.append(player)
            gromlinvip_count = gromlinvip_count + 1
        elif result_dictionary.get(player).get("stone") >= gganbu_dictionary.get("stone")*10 and result_dictionary.get(player).get("wood") >= gganbu_dictionary.get("wood")*10 and result_dictionary.get(player).get("iron") >= gganbu_dictionary.get("iron")*10 and result_dictionary.get(player).get("gold") >= gganbu_dictionary.get("gold")*10:
            moonsama_list.append(player)
            moonsama_count = moonsama_count + 1
        else:
            exosama_list.append(player)
            exosama_count = exosama_count + 1
    total = moonsama_count + exosama_count + gromlinvip_count
    print("Total Players: " + str(total))
    print("Moonsamas: " + str(moonsama_count))
    print("Exosamas: " + str(exosama_count))
    print("Gromlins/VIPS: " + str(gromlinvip_count))
