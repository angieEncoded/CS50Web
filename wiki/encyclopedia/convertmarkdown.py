from os import replace
import re
from . import angie
console = angie.Console()

    # This took me a good week to solve. At least, the unordered list part did. In the end, it's probably not as efficient as
    # the official solution, but it gets the job done and was fun to work on. 


    # How would I convert it myself?
    # using this as a guide
    # https://www.markdownguide.org/basic-syntax/
    # Would need to support the following
    # Headings 
    # #, ##, ###, ####, #####
    # Boldface text
    # **Some content in here **
    # Unordered lists
    # -, + or *
    # links
    # [link identifier](https://actuallink.com)
    # paragraphs
    # separated by a blank line

    # used https://regex101.com/ to learn and build the regexes

    # NOTE0001
    # I ran into a lot of problems with this trying to build a regex with
    # regex101.com and this stack overflow post pointed me in the right direction with how to
    # manage the carriage returns and etc. That site must have a linux backend and I am 
    # developing in a windows environment, so I get a \r\n not just a \r
    # https://stackoverflow.com/questions/20056306/match-linebreaks-n-or-r-n
    # closers = re.compile(r'(\s*|^)([-|*|+])(.*)($|\r\n\r\n)')
    # Annnnnnd then, I ended up not going this route anyway and doing something completely different. LOL
    # Leaving the note anyway, might need to remember the carraige returns etc at some point in the future

    # NOTE0002
    # I wanted to test later on for when we hit the end of the entries, but these iterables don't know
    # their length. This stackoverflow post suggested this approach
    # holdingCell = sum(1 for _ in entriesToProcess.finditer(entrySlice))
    # https://stackoverflow.com/questions/3347102/python-callable-iterator-size
    # which does ultimately get me what I want. It iterates over my slice with a placeholder for the variable
    # since it doesn't matter and won't be accessed, and gives me the sum of the entries. 
    



def convertIt(entry):
    
    # it looks like python isn't async, so this will be fine. Nice to not have to worry about async for a minute.
    processedEntry = processUnorderedLists(entry)
    processedEntry = processHeaderData(processedEntry)
    processedEntry = processBoldText(processedEntry)
    processedEntry = processLinks(processedEntry)
    processedEntry = processParagraphs(processedEntry)
    return processedEntry




# PROCESS HEADERS
#===================================================
def processHeaderData(entry):

    # The first () will match all the hashes
    # Then I want any number of characters after that except for a newline
    hashTagsPattern = re.compile(r'^([#]{1,6})(\s{1})(.*)$', re.MULTILINE)
    hashMatches = hashTagsPattern.finditer(entry)

    # group 0 is my whole thing
    # group 1 is my first set of matches
    # group 2 is my second

    # Now I have all the target data
    for item in hashMatches:
        # console.log(item)
        # get the length and then strip the whitespace
        # so I know what kind of header to substitute
        numberOfHashes = len(item.group(1).strip())
        # console.log(numberOfHashes)
        
        # there is a "\n" in the 2nd group position......
        # So get the target data from the third group.
        targetText = item.group(3).strip()
        # console.log()

        # Set up the text I want to return - ran into a weird issue with this
        # If I didn't use strip() to clean it up, it would not format this 
        # string correctly. 
        # console.log(f"<h{numberOfHashes}> {targetText} </h{numberOfHashes}>")
        replacement = f"<h{numberOfHashes}> {targetText} </h{numberOfHashes}>"

        # now replace that part of the string with my new string
        # ran into the same problem here with stripping the whitespace causing it to behave strangely when it cut the text
        # entry = entry.replace(item.group(0).strip(), replacement)
        entry = entry.replace(item.group(0), replacement)
    return entry


# PROCESS BOLDFACE TEXT
#===================================================
def processBoldText(entry):
    # process the bolldface
    # match exactly two asterisks before and after any amount of text
    boldfacePattern = re.compile(r'([*]{2})([^\*]+)([*]{2})')
    boldfaceMatches = boldfacePattern.finditer(entry)

    for item in boldfaceMatches:
        # console.log(item)
        # get just the text
        targetText = item.group(2)
        # console.log(targetText)

        # set up the replacement
        replacement = f"<strong> {targetText} </strong>"  

        # replace the whole thing with the new string
        # removing the strip from all of them, see the unordered list and headers entries for notes on a bug
        entry = entry.replace(item.group(0), replacement)
    return entry

    





# PROCESS LINKS
#===================================================
def processLinks(entry):
    # [I am a link Identifier](https://google.com)
    # get my links - with a REALLY ugly regex.
    linkPattern = re.compile(r'(\[)([^\]]+)(\])(\()([^\)]+)(\))')
    linkMatches = linkPattern.finditer(entry)
    for item in linkMatches:

        # This group is my link text
        # console.log(item.group(2))
        linkText = item.group(2)
        # And this is my link
        # console.log(item.group(5))
        linkUrl = item.group(5)

        newLink = f"<a href='{linkUrl}' target='_blank'>{linkText}</a>"

        # now we can replace group 0 with my link
        # removing the strip from all of them, see the unordered list and headers entries for notes on a bug
        entry = entry.replace(item.group(0), newLink)
    return entry



# PROCESS PARAGRAPHS
#===================================================
def processParagraphs(entry):

    # get the whitespace pattern, if I grab the cr\lf cr\lf and then the first word, then everything to the new line that should get me what i need
    paragraphPattern = re.compile(r'(\r\n)(\w+.+)')
    paragraphMatches = paragraphPattern.finditer(entry)

    # I need to see what the heck this pattern should be... \r\n\r\n
    # console.log(repr(entry))

    for item in paragraphMatches:
        # console.log(item)
        # console.log(item.group(2))
        paragraph = f"<p>{item.group(2).strip()}</p>"
        # removing the strip from all of them, see the unordered list and headers entries for notes on a bug
        entry = entry.replace(item.group(0), paragraph)
        
    return entry

# PROCESS UNORDERED LISTS
#===================================================
def processUnorderedLists(entry):

    # Make a copy of entry to read from - I ran into this with one of the CS50 projects as well
    # I think it was the one where we had to pixelate an image, and my code was 'correct' in that it 
    # did the things it should have, but my results weren't correct because every time it ran, it 
    # altered the original image and that threw off my next iteration of the code. Same thing happened here
    # and it took me a good hour and 3 mile walk to realize why some of my lines were just... cut off and all funky. 
    entryToReadFrom = entry


    # Find all the possible entries
    allEntries = re.compile(r'^([" "]*)([\-\*\+])(.*)', re.MULTILINE)
    entryMatches = allEntries.finditer(entry)
    lastEnd = 0
    batches = []
    currentBatch = [None, None]
    
    # Read over all the entries and get the locations to slice them out 
    for item in entryMatches:
        # console.log(item)

        # on the first run through, I know I have to start a new batch with the start number
        if lastEnd == 0:
            # console.log(f"Last end is true, adding {item.start()} to curent batch")
            currentBatch[0] = item.start() # set the first position of current batch to start
            currentBatch[1] = item.end() # set the current end to deal with edge case of last item
            lastEnd = item.end() # update lastEnd to the end of that item
            continue

        # If the start of this entry is only 1 past the start of the previous
        # set the new end to that item and continue - we are not done looking
        if item.start() == lastEnd + 1:
            # console.log(f"item.start is equal to one more than last end, making lastEnd {item.end()}")
            # console.log(lastEnd)
            lastEnd = item.end()
            currentBatch[1] = item.end() # make sure that we are putting and end into the batch
            continue

        # If item start is greater than that, we are on to a new batch
        # Note that this IS much less forgiving than the markdown2 package. I am expecting 
        # very well-formed markdown with this approach. When comparing the results from markdown2
        # to my results, it seemed like that package was a lot more forgiving of many things, including
        # matching up headers and allowing spaces between some lis. I prefer a more strict approach. 
        if item.start() > lastEnd + 1:
            # console.log(f"item in third {item}")
            # console.log(lastEnd)
            # console.log(f"item.start is greater than 1+ last end, completing batch")
            currentBatch[1] = lastEnd # set the end of the batch
            batches.append(currentBatch) # push the current batch to all batches
            currentBatch = [None, None] # reset the current batch
            currentBatch[0] = item.start() # set the new batch's start location
            currentBatch[1] = item.end() # deal with the edge case
            lastEnd = item.end() # update the lastEnd variable


    # push the last item into the array
    batches.append(currentBatch)

    # iterate over the batches and slice the text for processing
    for batch in batches:
        # console.log(batch)

        # grab the slice of text
        entrySlice = entryToReadFrom[batch[0]:batch[1]] # read from my copy, NOT the original I am altering or my text locations will not be correct
        entryCopy = entrySlice # Hold an unchanged copy somewhere so we can find it in the entry later
        
        # Now we get to read the list items in the mini-batch
        entriesToProcess = re.compile(r'^([" "]*)([\-\*\+])(.*)', re.MULTILINE) # Grab the current items to process
        entriesMatches = entriesToProcess.finditer(entrySlice)
        

        previousSpaces = 0
        currentSpaces = 0
        openLists = 0
        holdingCell = sum(1 for _ in entriesToProcess.finditer(entrySlice)) # SEE NOTE0002

        for index, item in enumerate(entriesMatches):
            # console.log(item.group(0))
            prefix = ""
            suffix = ""
            currentSpaces = len(item.group(1)) 

            if currentSpaces == 0 and openLists == 0: # we don't need to do anything to prefix or suffix
                pass 

            if currentSpaces > previousSpaces: # Open up an unordered list
                openLists = openLists + 1
                prefix = prefix + "<ul>\n"

            if currentSpaces <= previousSpaces and openLists > 0: # Close the previous unordered list
                openLists = openLists - 1
                prefix = prefix + "</ul>\n"
            
            if currentSpaces == 0 and openLists > 0: # Edge case where we drop back and have a bunch to close
                for _ in range(openLists):
                    openLists = openLists - 1
                    prefix = prefix + "</ul>\n"

            if index == (holdingCell - 1)  and openLists > 0: # Edge case when we have nothing left but still need to close a ul
                openLists = openLists - 1
                suffix = suffix + "</ul>"

        
            previousSpaces = currentSpaces # rotate the spaces
            completeItem = f"{prefix} <li> {item.group(3)} </li> {suffix}" # compile the complete item
            # console.log(completeItem)
            # ran into a weird bug here, stripping the whitespace caused it to be confused about what to replace when items
            # had the same verbiage. I tracked the breakdown between this line and creating the full entry. 
            # entrySlice = entrySlice.replace(item.group(0).strip(), completeItem)
            entrySlice = entrySlice.replace(item.group(0), completeItem)
            

        fullentry = f"\n<ul>\n{entrySlice}\n</ul>\n" # Wrap the whole thing in a UL
        # console.log(fullentry)
        entry = entry.replace(entryCopy, fullentry) # replace the text in the entry
    return entry
                                
