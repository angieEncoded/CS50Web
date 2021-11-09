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

    
    
    