####################################################################
#  grocery_utils.py                                                #
#  Name: Alysha Pursley                                            #
#  Date: July 18, 2025                                             #
#  Description:                                                    #
#    Contains helper functions for sorting and searching           #
####################################################################

####################################################################
#  Sort items alphabetically                                       #
#  Prints each item in A–Z order with its frequency count          #
####################################################################
def sort_alpha(freq_data):
    for item in sorted(freq_data):
        print(f"{item}: {freq_data[item]}")

####################################################################
#  Sort items by highest frequency                                 #
#  Sorts from most to least sold then prints each item and count   #
####################################################################
def sort_by_freq(freq_data):
    sorted_items = sorted(
        freq_data.items(),
        key=lambda x: x[1],
        reverse=True
    )
    for item, freq in sorted_items:
        print(f"{item}: {freq}")

####################################################################
#  Search for a specific item                                      #
#  Checks dictionary and prints frequency or not found message     #
####################################################################
def search_item(freq_data, item_name):
    item = item_name.lower()
    if item in freq_data:
        print(f"{item}: {freq_data[item]}")
    else:
        print("Item not found.")
