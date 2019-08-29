"""
FILE: TreeProfiler.py
AUTHOR: Matteo Miceli
USERNAME: 18910854
UNIT: COMP1002 Data Structures and Algorithms
PURPOSE: Menu interface for utilising tree implementations
REFERENCE: When a reference was used it was given in the function docstring
COMMENTS:
REQUIRES: Makes use of fileIO.py, which handles file input and output of the
          stock exchange data, and dsaTrees.py, which handles the
          implementation of the tree data structures. dsaTrees.py contains the tree
          data structures and shares.py contains the Share object class.
          Also the sys module, from the Python Standard Library.
Last Mod: 04/06/2019
"""

import sys
import os
from dsaTrees import *



class Menu:
    """
    TREEPROFILER.PY USAGE INFORMATION

    DESCRIPTION
    The TreeProfiler.py program has been designed to compare and assist
    reporting on Binary Search Trees, B-Trees and 2,3,4-Trees using
    Australian Stock Exchange (ASX) historical data found, which can be found
    at: https://www.asxhistoricaldata.com/

    The program operates in three modes depending on the command line
    parameters passed via the terminal:

    MODES
    (1) User documentation mode:
        The mode currently being used to display this information. Describes
        the required command line parameters to operate the program. The
        absence of command line parameters following 'TreeProfiler.py' will
        launch this mode.

    (2) Interactive testing environment mode:
        Provides user with a menu whereby they can:
           - Load new data either from csv or serialised binary file
             into one of three tree implementations:
              (a) Binary Search Tree
              (b) A B-Tree with the option to vary the number of keys per node
              (c) 2,3,4-Tree

        - Quit the program

        Additionally, once valid data is loaded into a tree the user can also:
           - Perform find, insert and delete operations on the tree

           - Produce statistics on the tree, including:
               (a) Size: Number of elements in the tree
               (b) Height: The number of levels within the tree, based on the
                           longest path
               (c) Balance: Measure of the tree's balance as a percentage
               (d) Insertion time: Average time to insert one share
               (e) Deletion time: Average time to delete one share
               (f) Find time: Average time to find a share
               (g) Sort time: Average time to traverse list in-order

           - Save the tree as text output in sorted order or a serialised
             binary file

    (3) Profiling mode
        Allows the user to use command line arguments to the TreeProfiler.py
        program to input the choice of tree, data size and input file. This
        mode is useful to output only the statistics (specified above) to
        assist in reporting on, and comparing, the tree implementations.

    ARGUMENTS (passed via the command line)
        -i  Enables interactive user mode

        -p  Executes profiling mode
            If -p is enabled then the following arguments are also required in
            the following format (see usage examples below):

            -p [tree] [data size] [input file] [input file type]
                tree - the choice of tree implementation:
                   bs         Binary Search tree
                   bt[nKeys]  B-Tree with the number of keys per node [nKeys]
                              which must be an odd integer >= 3
                   234t       2,3,4-Tree

                data size - the maximum number of shares allowed in the tree
                            which must be between 1 and 10000 (inclusive)

                input file - path to the required input file

                input file type - 'csv' or 'bin' (binary/pickle)

    USAGE EXAMPLES
    (1)     "python3 TreeProfiler.py"
            Launches user documentation mode

    (2)     "python3 TreeProfiler.py -i"
            Launches interactive testing environment mode

    (3)     "python3 TreeProfiler.py -p bt5 250 sharesdata.csv csv
            Executes profiling mode and generates statistics on sharesdata.csv
            using a B-Tree with max 250 shares and 5 keys per node.
    """

    def __init__( self, treePtr = None ):
            """
            NAME: init method
            PURPOSE: initialises an object as an instance of the TreeProfiler
                        class.
            IMPORTS: sys.argv - a list of arguments entered by the user at the
                            command line to indicate their desired program
                            mode
                     treePtr - a pointer to a TreeProfiler object where the
                               selected tree and all of its data will be
                               stored and operated on
            EXPORTS: None.
            ASSERTIONS:
                Pre: argv contains the correct and valid arguments as per the
                        usage information for the TreeProfiler program.
                Post: None
            REMARKS: No references used to write method.
            """
            self.argv = sys.argv
            self.treePtr = treePtr

            if self.treePtr is None:
                raise Exception( "A TreeProfiler object must be passed as an "
                                 "argument in order for this program to work."
                                 "Please see TreeProfiler.py documentation "
                                 "for further information." )




    def runProgram( self ):
        """
        NAME: runProgram
        PURPOSE: Wrapper method to run _selectMode method.
        IMPORTS: self - the instance of the Menu class
        EXPORTS: None
        ASSERTIONS:
            Pre: The object exists and is valid
            Post: None
        REMARKS: No references used to write method. I chose to use a wrapper
                 method since the user should not need to access the methods
                 used to execute the tree operations.
        """
        self._selectMode()




    def _selectMode( self ):
        """
        NAME: _selectMode
        PURPOSE: Private method which takes the user's second command line
                 argument (the user's desired operating mode) and executes the
                 method corresponding to the mode.
        IMPORTS: self - the instance of the Menu class
        EXPORTS: None.
        ASSERTIONS:
            Pre: self.argv contains correct and valid arguments as per the
                 usage information for the TreeProfiler program.
            Post: None.
        REMARKS: No references used to write method. If the user incorrectly
                 enters command line arguments in a way that is not outlined
                 as in the TreeProfiler.py documentation an exception will be
                 thrown because without correct arguments the program cannot
                 operate correctly.
        """

        if len( self.argv ) == 1:
            print( self.__doc__ )

        elif self.argv[1] == "-i" :
            print( "\n---------------------------------------------------" )
            print("INTERACTIVE USER MODE")
            print( "---------------------------------------------------" )
            self._mainMenu()

        # checks that parameters given for profiling mode are correct
        elif self.argv[1] == "-p" and len(self.argv) == 6:
            try:
                assert( ( self.argv[2] == "bs" or
                          self.argv[2] == "234t" or
                          self.argv[2][:2] == "bt" ) )
                if self.argv[2][:2] == "bt":
                    int(self.argv[2][2:])
                    assert(int(self.argv[2][2:]) % 2 != 0)
                self.argv[3] = int(self.argv[3])
                assert( self.argv[3] > 0 and self.argv[3] <= 10e6 )
                assert( self.argv[5] == 'csv' or self.argv[5] == 'bin')
            except:
                raise MenuException( "Incorrect command line arguments given "
                "for profiling mode.\nRun TreeProfiler.py without arguments "
                "for usage information." )
            else:
                self.treePtr._profileTree(self.argv[2:])

        else:
            raise MenuException( "Incorrect command line arguments given. "
                "Run TreeProfiler.py without arguments for usage\n"
                "information." )




    def _mainMenu( self ):
        """
        NAME: _mainMenu
        PURPOSE: Private method called when user selects interactive mode.
                 Prints menu options related to tree operations to the screen.
                 Only once the user has loaded data can they access tree
                 operations.
        IMPORTS: self - the instance of the Menu class
        EXPORTS: None.
        ASSERTIONS:
            Pre: None.
            Post: The user selected a valid option from the menu choices.
        REMARKS: No references used.
        """

        print( "\nMAIN MENU:" )
        if self.treePtr.tree is None:
            print( "   (1)  - Load new data" )

        else:
            print( "   (1)  - Load new tree\n"
                   "   (2)  - Tree find\n"
                   "   (3)  - Tree insert\n"
                   "   (4)  - Tree delete\n"
                   "   (5)  - Tree statistics\n"
                   "   (6)  - Save tree" )
        print( "   (0)  - Quit" )

        validChoice = False
        while validChoice is False:
            choice = input( "Choice: " )

            try:
                choice = int(choice)

                if self.treePtr.tree is not None:
                    if choice in range( 0, 7 ):
                        validChoice = True
                else:
                    if choice in range(0, 2):
                        validChoice = True

            except ValueError:
                print( "Invalid choice entered. Please enter the number\n"
                       "(as an integer) corresponding to your desired\n"
                       "choice.\n" )

        if choice == 1:
            self._loadDataMenu()
            self._mainMenu()
        elif choice == 2:
            self._treeFindMenu()
            self._mainMenu()
        elif choice == 3:
            self._treeInsertMenu()
            self._mainMenu()
        elif choice == 4:
            self._treeDeleteMenu()
            self._mainMenu()
        elif choice == 5:
            self._treeStatsMenu()
            self._mainMenu()
        elif choice == 6:
            self._saveTreeMenu()
            self._mainMenu()
        elif choice == 0:
            print( "\n---------------------------------------------------" )
            print( "GOODBYE" )
            print( "---------------------------------------------------\n" )




    def _loadDataMenu( self ):
        """
        NAME: _loadDataMenu
        PURPOSE: A private method for displaying a menu to load data from CSV
                 or binary files as a linked list of Share objects. Data is
                 loaded in the TreeProfiler._loadData method and if data is
                 loaded successfully the program progresses to the
                 Menu._loadTreeMenu() method for csv files,
                 else it returns to the Menu._mainMenu().
        IMPORTS: self - the instance of the Menu class
        EXPORTS: None.
        ASSERTIONS:
            Pre: The file type to be loaded will exist and be valid.
            Post: self.shares will contain valid Share objects.
        REMARKS: No references used.
        """
        print( "\n---------------------------------------------------" )
        print( "LOAD DATA FROM FILE" )
        print( "---------------------------------------------------" )
        print( "Select file input type:" )
        print( "   (1)   - CSV file\n"
               "   (2)   - Serialised binary (pickle) file\n"
               "   (0)   - Return to main menu" )

        fileType = False
        while fileType is False:
            fileChoice = input( "Choice: " )

            try:
                fileChoice = int( fileChoice )

                if fileType in range(0, 3):
                    fileType = fileChoice

            except ValueError:
                print( "Invalid choice entered. Please enter the number\n"
                       "(as an integer) corresponding to your desired\n"
                       "choice.\n" )
        print( "\n---------------------------------------------------" )

        if ( fileType == 1 ) or ( fileType == 2 ):
            self.treePtr._loadData( fileType )

            if fileType == 1:
                print( "---------------------------------------------------" )
                self._loadTreeMenu()

        print( "---------------------------------------------------" )




    def _loadTreeMenu( self ):
        """
        NAME: _loadTreeMenu
        PURPOSE: A private method for displaying a menu for the user to choose
                 which tree implementation to load their csv data into. The
                 program will continue to the TreeProfiler._loadTree() method,
                 where the tree will be loaded.
        IMPORTS: self - the instance of the Menu class
        EXPORTS: None.
        ASSERTIONS:
            Pre: The user has loaded ASX share data into a linked list of
                 Share objects.
            Post: Within the TreeProfiler object, the linked list
                  containing the Share objects no longer exists and a tree has
                  been implemented using this data instead.
        REMARKS: No references used.
        """
        print( "Select tree data structure type to use:" )
        print( "   (1)   - Binary Search Tree\n"
               "   (2)   - B-Tree\n"
               "   (3)   - 2,3,4-Tree\n"
               "   (0)   - Return to main menu" )

        numKeys = None
        treeChoice = False
        while treeChoice is False:
            treeType = input( "Choice: " )

            try:
                treeType = int( treeType )

                if treeType in range(0, 4):
                    treeChoice = treeType

            except ValueError:
                print( "Invalid choice entered. Please enter the number\n"
                    "(as an integer) corresponding to your desired\n"
                    " choice.\n" )

            if treeType == 2:
                validNum = False
                while validNum is False:
                    numKeys = input("Enter number of keys per node (must be greater than 3 and odd): ")

                    try:
                        numKeys = int(numKeys)

                        if numKeys <= 3:
                            print("\tNumber must be greater than 3.")
                            if numKeys % 2 == 0:
                                print("\tNumber must be odd.")

                        else:
                            validNum = True
                    except:
                        pass

        if treeChoice != 0:
            self.treePtr._loadTree( treeChoice, numKeys )




    def _treeFindMenu( self ):
        """
        NAME: _treeFindMenu
        PURPOSE: In interactive mode the user can input the ticker of a share
                 that is loaded into the tree. If found, the share information
                 is printed to the screen.
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: None.
        ASSERTIONS:
            Pre: The ticker is inserted in the correct format and the ticker
                 is within the tree.
            Post: The ticker was found. Returned to main menu.
        REMARKS: No refs used.
        """

        print( "\n---------------------------------------------------" )
        key = input( f"Enter the share ticker (T) and date corresponding to the share\n"
                      "you wish to find in the format TTTYYYYMMDD e.g. A2B20190513: " )
        try:
            key = key.upper()
            assert(key.isalnum() is True or key.isalpha() is True)
            assert(len(key) == 11)
        except:
            print("Share ticker format is three characters with capital letters e.g. 'AXT' or 'B2Y'\n"
                  "and date must be in format YYYYMMDD." )

        try:
            if self.treePtr.type == "bs":
                share = self.treePtr.tree.find(key)
            elif self.treePtr.type == "234t":
                share = self.treePtr.tree.find(key)[1].value
            else:
                share = self.treePtr.tree.find(key)[1].value
        except KeyNotFoundTreeError:
            print( f"Key {key} not found in the tree." )
        else:
            print( f"\t{share}" )




    def _treeInsertMenu( self ):
        """
        NAME: _treeInsertMenu
        PURPOSE: Lets the user enter the information of a share to be loaded
                 into an existing tree
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: A share object to the tree.
        ASSERTIONS:
            Pre: The ticker of the share is not already present in the tree.
            Post: The share was inserted correctly into the tree.
        REMARKS: No references used.
        """
        print( "\n---------------------------------------------------" )
        print( "Insert a share: " )

        s = Share()
        while s.ticker is None:
            s.ticker = input( "\tEnter share ticker: ")
        while s.date is None:
            s.date = input( "\tEnter share date: ")
        while s.openP is None:
            s.openP = input( "\tEnter share opening price: ")
        while s.closeP is None:
            s.closeP = input( "\tEnter share closing price: ")
        while s.highP is None:
            s.highP = input( "\tEnter share highest price: ")
        while s.lowP is None:
            s.lowP = input( "\tEnter share lowest price: ")
        while s.volume is None:
            s.volume = input( "\tEnter share volume: ")

        try:
            self.treePtr.tree.insert(s.ticker+s.date, s)
        except TreeNodeError:
            print( f"Key '{s.ticker}' already exists in tree." )

        print( "\n---------------------------------------------------" )




    def _treeDeleteMenu( self ):
        """
        NAME: _treeDeleteMenu
        PURPOSE: In interactive mode, the user can eneter the ticker of a
                 share they wish to delete from the tree.
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: None.
        ASSERTIONS:
            Pre: The ticker/share is in the tree
            Post: The share was removed from the tree
        REMARKS: No references used
        """

        print( "\n---------------------------------------------------" )
        key = input( f"Enter the share ticker (T) and date corresponding to the share\n"
                      "you wish to find in the format TTTYYYYMMDD e.g. A2B20190513: ")

        try:
            key = key.upper()
            assert(key.isalnum() == True)
            assert(len(key) == 11)
            self.treePtr.tree.delete(key)
            print("Ticker deleted successfully")
        except AssertionError:
            print("Ticker format must be three capital letters followed by the date e.g. AXT20190514")
        except KeyNotFoundTreeError:
            print("Key not found.")

        print( "\n---------------------------------------------------" )


    def _treeStatsMenu( self ):
        """
        NAME: _treeStatsMenu
        PURPOSE: The Menu class never intended to directly access tree data.
                 This method displays the graphical portion of the menu to
                 display the trees statistics, handled by TreeProfiler._treeStats
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: None.
        ASSERTIONS:
            Pre: The tree exists and is implemented correctly
            Post: None
        REMARKS:None
        """
        print( "\n---------------------------------------------------" )
        print( "TREE STATISTICS " )
        print( "---------------------------------------------------" )

        self.treePtr._treeStats()

        print( "---------------------------------------------------" )




    def _saveTreeMenu( self ):
        """
        NAME: _saveTreeMenu
        PURPOSE: In interactive mode, gives the user a menu to select which
                 output file type to export the tree into.
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: None
        ASSERTIONS:
            Pre: None
            Post: The user made a valid choice
        REMARKS: None
        """
        print( "\n---------------------------------------------------" )
        print( "SAVE TREE TO FILE" )
        print( "---------------------------------------------------" )
        print( "Select file input type:" )
        print( "   (1)   - CSV file\n"
               "   (2)   - Serialised binary (pickle) file\n"
               "   (0)   - Return to main menu" )

        fileType = False
        while fileType is False:
            fileChoice = input( "Choice: " )

            try:
                fileChoice = int( fileChoice )

                if fileType in range(0, 3):
                    fileType = fileChoice

            except ValueError:
                print( "Invalid choice entered. Please enter the number\n"
                       "(as an integer) corresponding to your desired\n"
                       "choice.\n" )
        print( "\n---------------------------------------------------" )

        if ( fileType == 1 ) or ( fileType == 2 ):
            fileName = input("Enter output file name: ")
            self.treePtr._saveTree( fileType, fileName )

        print( "---------------------------------------------------" )



class TreeProfiler:
    """
    The TreeProfiler class interacts with the fileIO and dsaTrees modules and
    their associated classes and methods. The output of interacting with these
    modules (the user's chosen tree implementation and a temporarily stored
    linked list), are stored by an object of this class.
    """

    def __init__( self ):
        """
        NAME: init method
        PURPOSE: initialises an object as an instance of the TreeProfiler
                    class.
        IMPORTS: None.
        EXPORTS: self.shares - a linked list containing objects
                               of type Share, loaded from the input file
                 self.tree - the user's chosen tree data structure
                 self.type - a string indicating the type of tree to be
                             profiled e.g. "bs", "bt" or "234t" (see usage
                             documentation)
                 self.profileKeys - a linkedlist containing random keys from
                                    the stored tree used to generate statistics
                                    on the find and delete methods of the tree
        ASSERTIONS:
            Pre: argv contains the correct and valid arguments as per the
                    usage information for the TreeProfiler program.
            Post: None
        REMARKS: No references used to write method.
        """

        self.shares = None
        self.tree = None
        self.type = None
        self.profileDelKeys = dsaLL()
        self.profileFindKeys = dsaLL()



    def _loadData( self, fileChoice ):
        """
        NAME: _loadData
        PURPOSE: A private method to load data from a CSV file into
                 a linked list stored by the TreeProfiler object.
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: self.shares - the linked list containing the Share objects
        ASSERTIONS:
            Pre: The user has a valid file to load the Share objects from.
            Post: A linked list containing the loaded Share objects exists at
                  self.shares
        REMARKS: No references used.
        """
        if fileChoice == 1:
            self.shares = FileIO.readSharesCSV()
        else:
            self.tree = FileIO.readSharesPickle()




    def _loadTree( self, treeType=None, numKeys=None ):
        """
        NAME: _loadTree
        PURPOSE: A private method to load the Share objects from the linkedList
                 into the user's desired tree implementation.
        IMPORTS: self - the instance of the TreeProfiler class
                 treeType - an integer passed by the Menu._loadTreeMenu
                            corresponding to the user's tree chosen tree type
        EXPORTS: self.tree - the implemented tree structure
                             containing the sorted Share objects
        ASSERTIONS:
            Pre: self.shares contains valid Share objects stored in a linkedList
            Post: self.tree contains a valid tree implementation correctly
                  sorted by ticker. The self.shares linked
                  list no longer exists and its value is None.
        REMARKS: No references used.
        """

        if self.shares is not None:

            # Binary Search Tree
            if treeType == 1 or (self.type is not None and self.type == "bs"):
                self.tree = BinaryTree()
                if self.type is None:
                    self.type = "bs"

            # B-Tree
            elif treeType == 2 or (self.type is not None and self.type[:2] == "bt"):
                if numKeys is not None:
                    self.tree = BTree(numKeys + 1)
                else:
                    self.tree = BTree(int(self.type[2:]) + 1)

                if self.type is None:
                    self.type = "bt"

            # 2,3,4-Tree
            elif treeType == 3 or (self.type is not None and self.type == "234t"):
                self.tree = BTree(4)
                if self.type is None:
                    self.type = "234t"

            for shareObj in range( self.shares.count ):
                share = self.shares.removeFirst()
                self.tree.insert( share.ticker+share.date, share )

        else:
            raise MenuException( "Unable to create tree since share data\n"
                                 "not present. Reload data from file to\n"
                                 "proceed.\n" )

        self.shares = None




    def _treeStats( self ):
        """
        NAME: _treeStats
        PURPOSE: Interacts with the tree and generates height, balance, size
                 and insert/delete/find/sort times
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: None
        ASSERTIONS:
            Pre: The tree exists and is implemented correctly
            Post: The given statistics are accurate
        REMARKS: None
        """

        n = self.tree.size
        tree = self.tree
        insTime = round(tree.insTime, 5)
        delTime = round(tree.delTime, 5)
        findTime = round(tree.findTime, 5)
        sortTime = round(tree.sortTime, 5)
        height = tree.height()
        balance = tree.balance()
        print( f"\tTree size: {n} shares")
        print( f"\tHeight: {height} levels")
        print( f"\tBalance: {balance}%")
        print( f"\tInsertion time: {insTime}" )
        print( f"\tDeletion time: {delTime}" )
        print( f"\tFind time: {findTime}" )
        print( f"\tSort time: {sortTime}" )
        print("\n\nNote: In interactive mode if the loaded tree has not had\n")
        print("      any shares deleted or has not been written to file, then Deletion and Sort time will be 0.")



    def _saveTree( self, fileType, fileName ):
        """
        NAME: _saveTree
        PURPOSE: Interacts with the FileIO class to save the tree to csv or
                 binary
        IMPORTS: self - the instance of the TreeProfiler class
                 fileType - 1 (csv) or 2 (binary/pickle)
                 fileName - output file name
        EXPORTS: A csv or binary file to the users given directory
        ASSERTIONS:
            Pre: The file type and name are valid and can be read/written
            Post: The file exists and is valid
        REMARKS: None
        """

        if fileType == 1:
            FileIO.writeSharesCSV(self.tree, fileName)
        else:
            FileIO.writeSharesPickle(self.tree, fileName)



    def _profileTree( self, args ):
        """
        NAME: _profileTree
        PURPOSE: Executes profiling mode. If the user selects profiling mode
                 from the command line then their arguments are passed from
                 the menu class, their chosen implemented with the data from
                 the input file and the output statistics saved to TreeProfilerOutput.log
                 Additional runs are appended to this file to generate a dataset.
        IMPORTS: self - the instance of the TreeProfiler class
        EXPORTS: TreeProfilerOutput.log file
        ASSERTIONS:
            Pre: All arguments entered are valid, program has write access
            Post: The stats methods were executed successfully and the output
                  file is valid and accurate
        REMARKS: None
        """

        self.type = args[0]
        maxSize = args[1]
        inputFile = args[2]
        fileType = args[3]

        # Load the inputFile as a tree
        if fileType == "csv":
            self.shares = FileIO.readSharesCSV(inputFile, maxSize, message=0)
            self._loadTree()
        else:
            self.tree = FileIO.readSharesPickle(inputFile, message=0)

        # Perform random find, delete, sort operations to generate stats
        tree = self.tree
        height = tree.height()
        balance = tree.balance()
        size = self.tree.size

        i = 0
        for share in self.tree:
            i = i % 10
            if i == 4:
                self.profileDelKeys.insertLast(share)
            if i == 5:
                self.profileFindKeys.insertLast(share)
            i += 1


        for share in self.profileDelKeys:
            #print(f"Attempting to delete:{share.ticker}")
            self.tree.delete(share.ticker+share.date)

        for share in self.profileFindKeys:
            #print(f"Attempting to find:{share.ticker}")
            self.tree.find(share.ticker+share.date)

        # write stats to output file
        insTime = round(tree.insTime, 5)
        delTime = round(tree.delTime, 5)
        findTime = round(tree.findTime, 5)
        sortTime = round(tree.sortTime, 5)

        if not os.path.exists("outputData"):
            os.mkdir("outputData")

        with open( 'outputData/TreeProfilerOutput.log', 'a+') as file:
            file.write( f"{self.type}, {maxSize}, {inputFile}, "
                        f"{size}, {height}, {balance}, "
                        f"{insTime}, {delTime}, {findTime}, {sortTime}\n" )

        print("Profile successfully outputted to outputData/TreeProfilerOutput.log")

"""
Error class design based on M. Valerie,
https://lms.curtin.edu.au/webapps/discussionboard/do/message?action=
list_messages&course_id=_91716_1&nav=discussion_board_entry&conf_id=
_271585_1&forum_id=_719480_1&message_id=_9197902_1
(Accessed on 23/05/2019)
"""
class Error( Exception ):
    """ Base class for exceptions in this module. Custom error classes writted
    as per python documentation:
    https://docs.python.org/3/tutorial/errors.html#user-defined-exceptions
    """
    pass

class MenuException( Error ):
    """
    Exception raised if user makes incorrect selection on menu items.

    Attribute:
        message --- explanation of the error
    """



# Main program
if __name__ == "__main__":
    """
    Since ASX data is provided sorted by each share's ticker name, sorting
    this into a binary search tree is completely degenerate and can therefore cause
    stack overflow.
    This sys.setrecursion function attempts to increase the recursion
    limit so that files with data on many shares load succesfully.
    (On systems I tested this program on, enabling this option prevented this issue
    from occurring)
    """
    sys.setrecursionlimit(10**6)

    # Create profiler object to store tree/data
    tree = TreeProfiler()
    # Pass the object to the Menu class so that it can point to it
    main = Menu(tree)
    # Execute the users command line arguments
    main.runProgram()
