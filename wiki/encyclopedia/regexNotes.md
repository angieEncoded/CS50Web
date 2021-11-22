## General matching
- .     Any character except new line
- \d    digit
- \D    Not a digit
- \w    word character
- \W    not a word char
- \s    whitespace
- \S    Not a whitespace

## Anchors - 
- \b    Word boundary (whitespace or numeric character)
- \B    Not a word boundary
- ^     Beginning of a string
- $     End of a string


- []    Matches characters in brackets
- [^]   Matches characters NOT in the brackets


# Quantifiers
- *     0 or more
- +     1 or more
- ?     0 or one
- {3}   Exact number
- {3,4} Range of numbers

# scratchpad

  
      # PROCESS LI DATA
    #===================================================

    # now I need a pattern that looks for a newline or the start of the page
    # followed by a tab or any number of spaces
    # It looks like the other package generates nested lists when it
    # detects tab characters so I will have to do that as well
    lineItemsPattern = re.compile(r'(\n|^)(\t*?|\s*?)([\-\+\*])(.*)')
    lineItemMatches = lineItemsPattern.finditer(entry)
    
    
    for item in lineItemMatches:

        # need to somehow check whether there are \s characters 
        # because we need another ul for those
        
        console.log(repr(item.group(0).lstrip()))
        replaced = re.sub(r"\n\r", "", item.group(0))
        res = bool(re.search(r"^\s", replaced))
        console.log(res)

    
- This is an unordered list 
    - this is an indented unordered list which will need to be accounted for
        - this is a third indented list which i have to account for
+ This is also part of an indented unordered list
* and for some reason, so is this.
    
<ul>
    <li>This is an unordered list 
        <ul>
            <li>this is an indented unordered list which will need to be accounted for ##
                <ul>
                    <li>this is a third indented list which i have to account for</li>
                </ul>
            </li>
        </ul>
    </li>
    <li>This is also part of an indented unordered list ##</li>
    <li><p>and for some reason, so is this. ##</p></li>
    <li><p>I shouldn't have put this at the start that was bad form <strong>This is some boldface text</strong></p></li>
</ul>


 To apply a second repetition to an inner repetition, parentheses may be used. For example, the expression (?:a{6})* matches any multiple of six 'a' characters.

    (?:" "{4})*
 "<h1> H1 Regular Expressions Test </h1>\r\n<h2> H2 - - </h2>\r\n<h3> H3 * * </h3>\r\n<h4> H4 + + </h4> \r\n<h5> H5 </h5> \r\n<h6> H6 </h6> \r\n\r\nwhat is your problem????\r\n\r\n<h6> # This is not valid markdown and we should not process it but it looks like it does get processed by the other package soo... </h6>
 
 
 
 \r\n\r\n
 - This is an unordered list \r\n
    - this is an indented unordered list which will need to be accounted for ##\r\n
        - this is a third indented list which i have to account for\r\n
    + This is also part of an indented unordered list ##\r\n
    * and for some reason, so is this. ##\r\n\r\n
    
    * I shouldn't have put this at the start that was bad form 
 
 
 
 <strong> 
This is some boldface text </strong>\r\n\r\nMeanwhile, <a href='https://google.com'>I am a link Identifier</a>\r\nMeanwhile, <a href='https://www.google.com'>I am a link Identifier</a>\r\nMeanwhile, <a href='http://www.google.com'>I am a link Identifier</a>\r\n\r\nI am a simple paragraph with either 4 spaces or a tab character in front of me\r\n\r\nThis is another paragraph\r\n\r\n[This is a test]\r\n\r\n\r\n\r\n\r\n\r\n    "



    # First let's just match everything we want to match then figure out how to do look aheads and behinds


    # find a \r\n followed by a -, + or * for top level
    outerListPattern = re.compile(r'\r\n(-|\*|\+)[" "].+')
    outerListMatches = outerListPattern.finditer(entry)


    # inner list
    innerListPattern = re.compile(r'\r\n(?:" "{4})*(-|\*|\+)[" "].+')
    innerListMatches = innerListPattern.finditer(entry)

    console.log("======================================")
    for item in outerListMatches:
        console.log(item)

    console.log("======================================")
    for item in innerListMatches:
        console.log(item)


from shaky
    90tgffff3wpo20l
     fdddd22222222222222



<li> Top level unordered list with a -\r</li>\r\n    <li> this is an indented unordered list which will need to be accounted for\r</li>\r\n        <li> this is a third indented list which i have to account for\r</li>\r\n<li> Top level unordered list with a +\r</li>\r\n<li> Top level unordered list with a *</li>'


- Top level unordered list with a -
    - this is an indented unordered list which will need to be accounted for
        - this is a third indented list which i have to account for
+ Top level unordered list with a +
* Top level unordered list with a *

This is a paragraphs




# first convert all to line items
    listPattern = re.compile(r'(^(\s*)[-|*|+])(.*)', re.MULTILINE)
    listMatches = listPattern.finditer(entry)
    for item in listMatches:
        # console.log(item.group(2))
        li = f"<li>{item.group(3).strip()}</li>"
        entry = entry.replace(item.group(0).strip(), li)

    # Find the start of the unordered list with a lookbehind pattern
    outerPatternStart = re.compile(r'(?<!</li>\r\n)^<li>.*', re.MULTILINE)
    outerPatternStartMatches = outerPatternStart.finditer(entry)

    for item in outerPatternStartMatches:
        startingLi = f"<ul>{item.group(0).strip()}"
        entry = entry.replace(item.group(0).strip(), startingLi)



    # find the end of the unordered list with a lookahead pattern
    outerPatternEnd = re.compile(r'^.*</li>\r\n$', re.MULTILINE)
    outerPatternEndMatches = outerPatternEnd.finditer(entry)

    for item in outerPatternEndMatches:
        console.log(item)
        # endingLi = f"<ul>{item.group(0).strip()}"
        # entry = entry.replace(item.group(0).strip(), endingLi)

    # console.log(repr(entry))










    previousSpaces = 0
    currentSpaces = 0
    openOrderedLists = []


    for item in listMatches:
        
        listItemString = ""
        # The opening li should always have 0 spaces 
        currentSpaces = len(item.group(1))
        if currentSpaces == 0 and len(openOrderedLists) == 0:
            # Then we need to open a new unordered list
            listItemString = listItemString + '<ul>'

            # We need to keep track of the open ordered list
            openOrderedLists.append(1)

            # We need to put together the rest of the string and write the line item
            console.log(item.group(2))


        # set the previous spaces so we know where we are
        previousSpaces = currentSpaces

        

        console.log(item.group(1))

        # console.log(item.group(2))
        # li = f"<li>{item.group(3).strip()}</li>"
        # entry = entry.replace(item.group(0).strip(), li)








Some working regex stuff
    

<li>Top level unordered list with a -</li>\r\n
    <li>this is an indented unordered list which will need to be accounted for</li>\r\n
            <li>this is a third indented list which i have to account for</li>\r\n
            <li>Top level unordered list with a +</li>\r\n
            <li>Top level unordered list with a *</li>\r\n
            \r\n\r\n\r\n\r\n
            <p>Hello breaking paragraph</p>
            \r\n\r\n\r\n
            <li>Top level unordered list with a -</li>\r\n
                <li>this is an indented unordered list which will need to be accounted for</li>\r\n
                        <li>this is a third indented list which i have to account for</li>\r\n
                        <li>Top level unordered list with a +</li>\r\n
                        <li>Top level unordered list with a *</li>




 




            # We need to keep track of the open ordered list
            openOrderedLists.append(1)

            # We need to put together the rest of the string and write the line item
            console.log(item.group(2))


        # set the previous spaces so we know where we are
        previousSpaces = currentSpaces


        # console.log(item.group(2))
        li = f"<li>{item.group(3).strip()}</li>"
        entry = entry.replace(item.group(0).strip(), li)



    console.log(repr(entry))



    '- Top level unordered list FIRST START\r\n    - this is an indented unordered list which will need to be accounted for\r\n        - this is a third indented list which i have to account for\r\n+ Top level unordered list with a +\r\n* LAST ENTRY IN FIRST LIST\r\n\r\n'



    


            # in the case of the first indentation, half will be 2 and won't match to anything previous
            # if currentSpaces / 2 == 2 and len(openOrderedLists) == 0:
            #     openOrderedLists.append(1)
            #     replacement = f"<ul><li>{item.group(3).strip()}</li>"
            #     entrySlice = entrySlice.replace(item.group(0).strip(), replacement)

            # if the previous space is exactly half the current space, we need to 
            # open an unordered list
            # if previousSpaces == currentSpaces / 2 and currentSpaces > 0:
                # keep track of how many we have opened
                # openOrderedLists.append(1)
                # add the ul to the string 
                # replacement = f"<ul><li>{item.group(3).strip()}</li>"
                # entrySlice = entrySlice.replace(item.group(0).strip(), replacement)

            # If the current space is less than the previous space and we still have opened
            # unordered lists, we need to close them
            # if currentSpaces < previousSpaces and len(openOrderedLists) > 0:

                # remove the last opened unordered list
                # openOrderedLists.pop()
        # previousSpaces = currentSpaces

        # console.log(entrySlice)
        # console.log(entry[startingLines[index]])
        # write the whole thing back to the location in entry we sliced the list from
        # entry = entry[startingLines[index]] + entrySlice + entry[endingLines[index]]




'- Top level unordered list FIRST START\r\n    - this is an indented unordered list which will need to be accounted for\r\n        - this is a third indented list which i have to account for\r\n+ Top level unordered list with 
a +\r\n* LAST ENTRY IN FIRST LIST\r\n\r\n<p>Hello breaking paragraph</p>\r\n\r\n- Top level unordered list SECOND LIST START\r\n    - this is an indented unordered list which will need to be accounted for\r\n        - this is 
a third indented list which i have to account for\r\n+ Top level unordered list with a +\r\n    * LAST ENTRY IN SECOND LIST\r\n\r\n<p>And some other paragraph</p>\r\n\r\n\r\n- THIRD LIST START AND END
\r\n\r\n- Something is happening...'
