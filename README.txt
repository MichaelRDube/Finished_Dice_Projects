Author:  Michael Dube

Instructions for use:

Plug in USB camera.  This project uses a Logitech MXBRIO.

If not already run, navigate to the directory which holds
die-rolling projects and run install_setup.sh
(sudo ./install_setup.sh).

MAKE SURE TO FULLY RESTART THE COMPUTER, or permissions
may not be granted by install.sh as intended.

This should install any libraries needed for the project
on Ubuntu Linux and configure the camera settings to match
training conditioins.

These installations will be made inside a virtual
environment.  This virtual environment must be activated
before using scripts.  While in the directory that holds
the myenv directory, enter:
"source myenv/bin/activate"
and the virtual environment will be active in that terminal
until deactivated, or until the terminal closes.
When the virtual environment is active, it should say
"(myenv)" all the way to the left of the current terminal
line.

Each of the following scripts is slightly unique according
to which die is being evaluated.
Simply navigate to the appropriate die folder and run each
script as directed, according to what is needed.

reset.py-
    For any given die shape, before attempting to run any
    other script, set up project directory by navigating to
    project directory and running reset.py (python3 reset.py).
    This will ensure that all necessary files and directories
    exist.
    Any time the User would like to return database and its
    cache to its original empty state, reset.py may be run.
    This will return any pictures in the project's
    'processed_images' directory to 'captured_images',
    ensuring no accidental loss of images.
    Any values kept in dice.db will be lost, however, and
    therefore, any corrections to roll identifications will
    also be lost.
    If the User would like to start over with no images, the
    images may be deleted manually from 'captured_images'
    after running reset.py.
    If the User is experiencing issues after deleting items
    or directories, they should attempt to run reset.py, as
    this will likely return the project to its intended state.

manual_roll.py-
    To roll a die and take pictures of the rolls manually,
    the User may run manual_roll.py (python3 manual_roll.py).
    The camera will stream its video for the benefit of the
    User while manual_roll.py runs.
    The User may press the Space Bar to take a picture of the
    roll, and q to exit the script.
    Any pictures taken this way will be automatically named
    according to die type + index, and saved in 'captured_images'.
    To avoid saving over existing images, this index will start
    1 higher than the highest indexed image in 'captured_images'
    AND 'processed_images'.

auto_roll.py-
    To roll a die and take pictures of the rolls automatically,
    the User may run auto_roll.py (python3 auto_roll.py).  The
    python script will attempt to connect to the Arduino and
    begin rolling the die.  After a random number of shakes, the
    box will be still for a moment as the script takes a picture
    of the die.  Once the picture has been taken, the box will
    repeat the process indefinitely.
    The User may at any time press Ctrl+C in whichever terminal
    window has been running auto_roll.py to stop the rolling
    process and exit the program.
    Note that the box may not stop shaking right away, as the
    Arduino does not receive the command to stop.  Simply wait
    until the box stops moving completely, and it will be safe
    to move.
    Any pictures taken by auto_roll.py will be automatically named
    according to die type + index, and saved in 'captured_images'.
    To avoid saving over existing images, this index will start
    1 higher than the highest indexed image in 'captured_images'
    AND 'processed_images'.
    
dump.py-
    To identify digits present in images kept in 'captured_images',
    the User may run dump.py (python3 dump.py).
    Any digit identified in an image will be logged in dice.db.
    dice.db holds information on the path to the corresponding image,
    value, confidence, and flagged status of each digit.
    A digit will be flagged if the identification is below a certain
    confidence, or (for projects that make use of
    Digit_Identifier_Model.pt) if the digit does not appear on that
    die, (i.e., a 13 identified on a D8).
    It is worth noting that this extends to the maximum of each die.
    For example, we know that for our dice, though a D8 contains
    the value 8, the digit '8' does not appear on the die.
    Therefore, any '8' identified on our D8 is likely something
    else entirely and should be flagged.
    Identifications for any impossible digits are flagged and
    logged in dice.db as value 0 to make them easier to find
    in the GUI.
    After dump.py makes its identifications, moves pictures from
    'captured_images' to 'processed_images', and enters its roll
    information into dice.db, it will generate a small error report.
    This error report includes paths to each image that has been
    flagged, the total number of flagged items, and which
    identified digits have been flagged.

TheGUI.py-
    To review roll information and view images of each roll,
    the User may run TheGUI.py (python3 TheGUI.py).
    dice.db must exist and be non-empty in order to properly
    use TheGUI.py.  If the User runs TheGUI.py while it does
    not exist or is empty, the window will not fully open,
    and the User will be informed of the error in the terminal.
    If this error is encountered, the User may enter anything
    into the terminal in order to exit the script.
    If dice.db exists and is non-empty, upon opening, TheGUI.py
    will fetch all information on rolls currently kept in dice.db,
    hold this information in a list, and display the image and
    information of the first roll in dice.db.
    It is worth noting that the index of each roll is not derived
    from its index in dice.db, but its index in the list, as held
    by TheGUI.py.
    Since information from the database is fetched in order of its
    index in dice.db, the indeces SHOULD match.
    However, if the User resets the database and reprocesses with
    new data, the order of insertions in dice.db may be different,
    resulting in a different index in dice.db for any given roll.
    This is unlikely to become a problem.
    Displayed below the image of each roll is the path to the
    current image, the value of the digit identified, and whether
    or not the image has been flagged for further review.
    Buttons:
        Previous-  Moves to the previous roll in list.  If
        current index is at the first roll, this button will do
        nothing.
        
        Next-  Moves to the next roll in the list.  If current
        index is at the last roll, this button will do nothing.
        
        Jump-  Moves to the roll with the index matching the one
        in the text box directly below Jump button (to be
        specified by the User).

        Previous Flagged-  Moves to the previous roll marked as
        flagged in the list.  If no flagged rolls exist before
        the current index, this button will do nothing.
        
        Next Flagged-  Moves to the next roll marked as flagged
        in the list.  If no flagged rolls exist after the current
        index, this button will do nothing.

        <- (Previous of Value)-  Moves to the previous roll with
        identified value matching the one specified in the
        'Next of Value' text box (to be specified by User).  If no
        rolls match this value before the current index, this
        button will do nothing.
        
        -> (Next of Value)-  Moves to the next roll with identified
        value matching the one specified in the 'Next of Value'
        text box (to be specified by User).  If no rolls match
        this value after the current index, this button will do
        nothing.
            (Reminder:  impossible rolls are stored in dice.db as
            value 0 for easy value searching.)

        Refresh-  Fetches information from dice.db and updates
        list of rolls held by TheGUI.py, in case of entry of new
        data .  The User will stay on their current index.

        Make Correction-  If the User finds an incorrect
        identification, they may enter the correct value in the
        'Digit Identified:' text box and press the Make Correction
        button.  This will change the value in dice.db and remove
        the flagged status.
            (If the database contains a correctly identified digit
            that has been flagged, since the correct value should
            already be displayed, the User may simply press the
            Make Correction button to remove the flagged status.)
            
        Delete-  If the User finds any image of a roll that is
        visually unclear to the point of being unable to make a
        manual correction, this image should likely be removed
        from the dataset.  The User may press the Delete button
        to drop it from the records kept in dice.db.
            (Note that this will not delete the picture from the
            dataset, in case the User makes a mistake or changes
            their mind.  To completely remove the picture itself,
            the User should find that particular image in that
            project's 'processed_images' directory and delete it
            manually after deleting it from the database using
            the GUI.)
            
to_csv.py-
    Once the User has acquired sufficient images of rolls, logged
    them into dice.db with dump.py, and made the necessary
    corrections to the flagged entries via TheGUI.py, the User may
    run to_csv.py (python3 to_csv.py) to move the tally of rolls
    in dice.db to a csv file (roll_tally.csv) for easy statistics.
    Upon being activated, to_csv.py will issue the User a reminder
    to make any necessary corrections before continuing.  to_csv.py
    will execute after the User presses Enter, unless the script is
    terminated early.  The User may delay pressing Enter to open a 
    different terminal and make necessary corrections with
    TheGUI.py. (reminder to activate the virtual environment
    by typing "source myenv/bin/activate" on a new terminal before
    attempting to run any scripts contained by Finished_Dice_Projects,
    or some scripts may not work properly).  Alternatively, the User
    may make their corrections after proceeding with to_csv.py and
    run to_csv.py again after the corrections have been made.  This
    will overwrite any out-of-date data in roll_tally.csv.
            
