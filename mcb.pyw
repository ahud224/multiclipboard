# saves and loads text to the clipboard
# usage: python mcb.pyw save <keyword> - saves keyword to the clipboard
#        python mcb.pyw <keyword> - loads the keyword from the clipboard
#        python mcb.pyw list - loads all keywords to the clipboard


import shelve, pyperclip, sys, threading

# create a loock object
lock = threading.Lock()

# create a shelf to store the clipboard contents
mcbShelf = shelve.open('mcb')

instructions = 'usage:\n  python mcb.pyw save <keyword>  -saves the keyword to the clipboard\n  python mcb.pyw <keyword>  -loads the keyword from the clipboard.\n  python mcb.pyw list   -lists all of the keywords'
executed = False # variable to track if item was copied to clipboard appropriately

# save content to clipboard
lock.acquire() # lock file
if len(sys.argv) == 3:
    if sys.argv[1].lower() == 'save':
        mcbShelf[sys.argv[2]] = pyperclip.paste()
        print('Saved to clipboard:',mcbShelf[sys.argv[2]])
        executed=True
    elif sys.argv[1].lower() == 'delete':
        if sys.argv[2] in mcbShelf:
            del mcbShelf[sys.argv[2]]
            print('Item deleted from clipboard:',mcbShelf[sys.argv[2]])
            executed=True
elif len(sys.argv) ==2:
    # list keywords and load content
    if sys.argv[1].lower() == 'list':
        pyperclip.copy(str(list(mcbShelf.keys())))
        print('Keys:',str(list(mcbShelf.keys())))
        executed=True
    elif sys.argv[1] in mcbShelf:
        pyperclip.copy(mcbShelf[sys.argv[1]])
        print('Loaded to clipboard:',mcbShelf[sys.argv[1]])
        executed=True
if executed == False:
    print('Invalid argument\n\n',instructions)
mcbShelf.close()
lock.release()


# next steps
#   method to delete all of items in shelf
#   how to open up the shelf without matching/listing all (i.e. open in a text editor, manipulate elsewhere)
#   add some error handling