import re
from . import angie
console = angie.Console()

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
    # four spaces or one tab


def convertIt(entry):
    # send it into the header converter
    # it looks like python isn't async, so this will be fine
    processedEntry = processHeaderData(entry)
    processedEntry = processBoldText(processedEntry)
    


    

    
    
    return processedEntry








def processHeaderData(entry):
    #PROCESS HEADER DATA
    #===================================================
    # The first () will match all the hashes
    # Then I want any number of characters after that except for a newline
    hashTagsPattern = re.compile(r'((\n|^)#{1,6})(.*)')
    hashMatches = hashTagsPattern.finditer(entry)

    # group 0 is my whole thing
    # group 1 is my first set of matches
    # group 2 is my second

    # Now I have all the target data
    for item in hashMatches:

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
        entry = entry.replace(item.group(0).strip(), replacement)
    # END PROCESS HEADER DATA
    #===================================================
    
    return entry


def processBoldText(entry):
    # process the bolldface
    # match exactly two asterisks before and after any amount of text
    boldfacePattern = re.compile(r'([*]{2})(.*)([*]{2})')
    boldfaceMatches = boldfacePattern.finditer(entry)
    
    for item in boldfaceMatches:

        # get just the text
        targetText = item.group(2)

        # set up the replacement
        replacement = f"<strong> {targetText} </strong>"  

        # replace the whole thing with the new string
        entry = entry.replace(item.group(0).strip(), replacement)
    
    return entry

    
    