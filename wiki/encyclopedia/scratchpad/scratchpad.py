





        # listPattern = re.compile(r'^([' ']*)([-|*|+])(.*)', re.MULTILINE)
        


        # set up some helper variables to keep track of whether we need to open 
        # an unordered list for indentation
 





            # console.log(item)


            # How many spaces does the line have
            currentSpaces = len(item.group(1))
            # console.log(currentSpaces)
            



            




            # console.log(f"Holding cell is:{holdingCell}")
            # console.log(f"Index is :{index}")





            # all other items just need to be wrapped in an LI - prefix will be empty
            # suffix handles an edge case where an unordered list needs to be closed at the end
            # of a complete list
            # console.log(item.group(2))
            completeItem = f"{prefix}<li>{item.group(3).strip()}</li>{suffix}"
            entrySlice = entrySlice.replace(item.group(0).strip(), completeItem)
            # console.log(completeItem)
        # dump my processed data into the array
        
           


    # and finally the entire entryslice needs to be wrapped in a ul, replaced in the larger string, and returned
    # I put all the processed text into twin arrays because I kept mutating the string and messing up my lists

        # console.log(existingText[index])
        # console.log(fullentry)




  

    # console.log(entry)


        # openers = re.compile(r'(\r\n\r\n|^)([-|*|+])(.*)')
    #\r\n\r\n- LAST LIST START AND END
    # find all the starts