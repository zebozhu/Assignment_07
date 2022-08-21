#------------------------------------------#
# Title: Assignment06_Starter.py
# Desc: Working with classes and functions.
# Change Log: (Who, When, What)
# DBiesinger, 2030-Jan-01, Created File
# Zebo Zhu, 14Aug2022, Modified File
# Zebo Zhu, 20Aug2022, Added error handling
#------------------------------------------#

import pickle

# -- DATA -- #
strChoice = '' # User input
lstTbl = []  # list of lists to hold data
dicRow = {}  # list of data row
strFileName = 'CDInventory.dat'  # data storage file
# strFileName = 'CDList.dat'  # uncomment this line to test the invalid file name error handling
objFile = None  # file object

# 
# -- PROCESSING -- #
class DataProcessor:
    
    @staticmethod
    def load_table(newSong): 
        """Function to load user input data to a dictionary in a table

        Args:
            newSong (Tuple): A tuple of the user inputs (ID, CD, Artist Name)

        Returns:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime
        """
        # intID = int(strID)
        dicRow = {'ID': int(newSong[0]), 'Title': newSong[1], 'Artist': newSong[2]}
        lstTbl.append(dicRow)
        return lstTbl
        
    @staticmethod 
    def delete_data(intIDDel, table):
        """Function to delete a song in a table based on user ID selection

        Args:
            intIDDel (int): user selection of the CD ID number
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        intRowNr = -1
        blnCDRemoved = False
        for row in lstTbl:
            intRowNr += 1
            if row['ID'] == intIDDel:
                del lstTbl[intRowNr]
                blnCDRemoved = True
                break
        if blnCDRemoved:
            print('The CD was removed')
        else:
            print('Could not find this CD!')

class FileProcessor:
    """Processing the data to and from text file"""

    @staticmethod
    def read_file(file_name):
        """Function to manage data ingestion from a binary file to a list of dictionaries

        Reads the data from a binary file identified by file_name into a 2D table
        (list of dicts) table one line in the file represents one dictionary row in table.

        Args:
            file_name (string): name of file used to read the data from
            
        Returns:
            None.
        """
        # table.clear()  # this clears existing data and allows to load data from file
        with open(file_name, 'rb') as objFile:
            pickle.load(objFile)
         
        # objFile = open(file_name, 'r')

        # for line in objFile:
        #     data = line.strip().split(',')
        #     dicRow = {'ID': int(data[0]), 'Title': data[1], 'Artist': data[2]}
        #     table.append(dicRow)
        # objFile.close()

    @staticmethod
    def write_file(file_name, table):
        """Function to write data from a list of dictionaries to a binary file

        Reads the data from a 2D table (list of dicts) table one line in the file represents one dictionary row in table.
        to a binary file identified by file_name

        Args:
            file_name (string): name of file used to read the data from
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime

        Returns:
            None.
        """
        # objFile = open(file_name, 'w')
        with open(file_name, 'wb') as objFile:
            # for row in table:
            #     lstValues = list(row.values())
            #     lstValues[0] = str(lstValues[0])
                # objFile.write(','.join(lstValues) + '\n')
            pickle.dump(table, objFile)
            # objFile.close()


# -- PRESENTATION (Input/Output) -- #

class IO:
    """Handling Input / Output"""

    @staticmethod
    def print_menu():
        """Displays a menu of choices to the user

        Args:
            None.

        Returns:
            None.
        """

        print('Menu\n\n[l] load Inventory from file\n[a] Add CD\n[i] Display Current Inventory')
        print('[d] delete CD from Inventory\n[s] Save Inventory to file\n[x] exit\n')

    @staticmethod
    def menu_choice():
        """Gets user input for menu selection

        Args:
            None.

        Returns:
            choice (string): a lower case sting of the users input out of the choices l, a, i, d, s or x

        """
        choice = ' '
        while choice not in ['l', 'a', 'i', 'd', 's', 'x']:
            choice = input('Which operation would you like to perform? [l, a, i, d, s or x]: ').lower().strip()
        print()  # Add extra space for layout
        return choice

    @staticmethod
    def show_inventory(table):
        """Displays current inventory table


        Args:
            table (list of dict): 2D data structure (list of dicts) that holds the data during runtime.

        Returns:
            None.

        """
        print('======= The Current Inventory: =======')
        print('ID\tCD Title (by: Artist)\n')
        for row in table:
            print('{}\t{} (by:{})'.format(*row.values()))
        print('======================================')

    @staticmethod
    def new_song(strID, strTitle, stArtist):
        """Prompt user to enter a new song


        Args:
            strID (string): ID number of the song
            strTitle (string): Title of the song
            stArtist (string): Artist of the song

        Returns:
            strID (string): ID number of the song
            strTitle (string): Title of the song
            stArtist (string): Artist of the song


        """
        strID = input('Enter ID: ').strip()
        strTitle = input('What is the CD\'s title? ').strip()
        stArtist = input('What is the Artist\'s name? ').strip()
        return strID, strTitle, stArtist

# 1. When program starts, read in the currently saved Inventory
objFile = open(strFileName,'w+')
objFile.close()
# FileProcessor.read_file(strFileName)

# 2. start main loop
while True:
    # 2.1 Display Menu to user and get choice
    IO.print_menu()
    strChoice = IO.menu_choice()

    # 3. Process menu selection
    # 3.1 process exit first
    if strChoice == 'x':
        break
    # 3.2 process load inventory
    if strChoice == 'l':
        print('WARNING: If you continue, all unsaved data will be lost and the Inventory re-loaded from file.')
        strYesNo = input('type \'yes\' to continue and reload from file. otherwise reload will be canceled: ')
        if strYesNo.lower() == 'yes':
            print('reloading...')
            try:
                FileProcessor.read_file(strFileName)
            except:
                print('File does not exist, please check the file name!')
            IO.show_inventory(lstTbl)
        else:
            input('canceling... Inventory data NOT reloaded. Press [ENTER] to continue to the menu.')
            IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.3 process add a CD
    elif strChoice == 'a':
        # 3.3.1 Ask user for new ID, CD Title and Artist
        strID = ''
        strTitle =''
        stArtist =''
        newSong = IO.new_song(strID, strTitle, stArtist)

        # 3.3.2 Add item to the table
        DataProcessor.load_table(newSong)
        print('New song has been successfully added to the inventory')
        # IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.4 process display current inventory
    elif strChoice == 'i':
        IO.show_inventory(lstTbl)
        continue  # start loop back at top.
    # 3.5 process delete a CD
    elif strChoice == 'd':
        # 3.5.1 get Userinput for which CD to delete
        # 3.5.1.1 display Inventory to user
        IO.show_inventory(lstTbl)
        # 3.5.1.2 ask user which ID to remove
        try: 
            intIDDel = int(input('Which ID would you like to delete? ').strip())
            # 3.5.2 search thru table and delete CD
            DataProcessor.delete_data(intIDDel, lstTbl)
            IO.show_inventory(lstTbl)
        except: 
            print('Invalid input! Please check your selection!')
            print()
        continue  # start loop back at top.
    # 3.6 process save inventory to file
    elif strChoice == 's':
        # 3.6.1 Display current inventory and ask user for confirmation to save
        IO.show_inventory(lstTbl)
        strYesNo = input('Save this inventory to file? [y/n] ').strip().lower()
        # 3.6.2 Process choice
        if strYesNo == 'y':
            # 3.6.2.1 save data
            print()
            print('writing data to file...')
            try:
                FileProcessor.write_file(strFileName, lstTbl)
            except:
                print('Invalid file name or table, please check and re-enter!')
            IO.show_inventory(lstTbl)
        else:
            input('The inventory was NOT saved to file. Press [ENTER] to return to the menu.')
        continue  # start loop back at top.
    # 3.7 catch-all should not be possible, as user choice gets vetted in IO, but to be save:
    else:
        print('General Error')




