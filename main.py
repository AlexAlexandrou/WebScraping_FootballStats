from scrape import *
from locals import *

if __name__ == "__main__":

    # Combine scrape and offline dictionaries into a single dictionary
    funcs_dict.update(funcs_dict_offline)


    print('WELCOME TO FOOTBALL STATS \n\n\n')
    print('Below are the functions you can use: \n')

    selection = ''
    # Display home menu to user
    while selection.casefold() != 'N'.casefold():
        
        print('\n')
        [print(key,':',value,'\n') for key, value in funcs_dict.items()]
        selection = input('\nPlease select the number of the function you want to use (Enter N to quit program):  ')
        if selection.casefold() == 'N'.casefold():
            # end program if input is N
            break
        elif not selection.isdigit() or int(selection) > len(funcs_dict):
            # Ask input again if not 'N' or number
            print('ERROR: Unkown command.\n')
            continue
        
        # Call selected function
        for key, value in funcs_dict.items():
            if selection == str(key):
                print(f'\nSelected the "{value}" function.\n')
                locals()[f'{value}']()
                break
    
    print('\nProgram ended.\n')
                
