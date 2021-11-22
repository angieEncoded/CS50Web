def processUnorderedLists(entry):
    # console.log(repr(entry))
    startingLines = []
    endingLines = []
    existingText = []
    replacementText = []

    # There doesn't seem to be a way to conditionally capture the end of the string
    # AND capture all the data inside. Since I don't need the contents here, I am 
    # letting it go and noting it here in case I come back to this again
    openers = re.compile(r'(\r\n\r\n|^|\r\r|\n\n)([\-\*\+])(.*$)?')

    openersMatches = openers.finditer(entry)
    for item in openersMatches:
        # console.log(f"Openers Matches {item}")
        # console.log(item.group(3))
        startingLines.append(item.start())      

    closers = re.compile(r'(^|\s*)[\-\*\+](.*)(\r\n\r\n|\r\r|\n\n|$)')
    closersMatches = closers.finditer(entry)
    for item in closersMatches:
        # console.log(f"Closer matches: {item}")
        endingLines.append(item.end())  

    # Now I have the start and end of each one and can slice that from entry
    for index, item in enumerate(startingLines):
        entrySlice = entry[startingLines[index]:endingLines[index]]
        # console.log(entrySlice)
        # put the text somewhere we can get it later
        existingText.append(entrySlice)

        # Get all the line items from the 'mini' list and process them into line items
        listPattern = re.compile(r'^([" "]*)([\-\*\+])(.*)', re.MULTILINE)
        listMatches = listPattern.finditer(entrySlice)
        
        previousSpaces = 0
        currentSpaces = 0
        openOrderedLists = []
        # get the length, see notes for more information
        holdingCell = sum(1 for _ in listPattern.finditer(entrySlice))
        
        for index, item in enumerate(listMatches):
            # console.log(item)
            # set up a couple variables to hold extra data
            prefix = ""
            suffix = ""
            # get the spaces in the item
            currentSpaces = len(item.group(1))
            # console.log(currentSpaces)
            # console.log(previousSpaces)

            # If current spaces > previous spaces we need to open a ul
            if currentSpaces > previousSpaces and currentSpaces != 0:
                openOrderedLists.append(1)
                prefix = prefix + f"<ul>"
                
            # if current spaces is < previous spaces and there is still an unordered list in the array, we need to close the ul
            if currentSpaces <= previousSpaces and len(openOrderedLists) > 0:
                openOrderedLists.pop()
                prefix = prefix + f"</ul>"


            # Handle an edge case where we need to close more than one ul
            if currentSpaces == 0 and len(openOrderedLists) > 0:
                # have to loop over the remaining items in the list if we somehow dropped to a top level entry
                for _ in openOrderedLists:
                    openOrderedLists.pop()
                    prefix = prefix + "</ul>"

            # Edge case when we have nothing left but still need to close a ul see notes at top
            if index == (holdingCell - 1)  and len(openOrderedLists) > 0:
                # console.log("This was true")
                suffix = "</ul>"


            previousSpaces = currentSpaces

            completeItem = f"{prefix}<li>{item.group(3).strip()}</li>{suffix}"
            # console.log(completeItem)
            entrySlice = entrySlice.replace(item.group(0).strip(), completeItem)
            # console.log(enstrySlice)


        replacementText.append(entrySlice)


    # finally wrap the whole thing in a ul and send it back
    for index, _ in enumerate(existingText):
        # console.log(index)
        fullentry = f"\n<ul>\n{replacementText[index]}\n</ul>\n"
        entry = entry.replace(existingText[index], fullentry)

    return entry
                                
