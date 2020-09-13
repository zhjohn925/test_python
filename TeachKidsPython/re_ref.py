# https://www.analyticsvidhya.com/blog/2015/06/regular-expression-python/
# https://docs.python.org/3/library/re.html

# Operators 	         Description
#    . 	                  Matches with any single character except newline ‘\n’.
#    ? 	                  match 0 or 1 occurrence of the pattern to its left
#    + 	                  1 or more occurrences of the pattern to its left
#    * 	                  0 or more occurrences of the pattern to its left
#    \w 	                Matches with a alphanumeric character whereas \W (upper case W) matches non alphanumeric character.
#    \d 	                Matches with digits [0-9] and /D (upper case D) matches with non-digits.
#    \s 	                Matches with a single white space character (space, newline, return, tab, form) and \S (upper case S) 
#                            matches any non-white space character.
#    \b 	                boundary between word and non-word and /B is opposite of /b
#    [..] 	              Matches any single character in a square bracket and [^..] matches any single character not in square bracket
#    \ 	                  It is used for special meaning characters like \. to match a period or \+ for plus sign.
#    ^ and $ 	            ^ and $ match the start or end of the string respectively
#    {n,m} 	              Matches at least n and at most m occurrences of preceding expression if we write it as {,m} then 
#                            it will return at least any minimum occurrence to max m preceding expression.
#    a| b 	              Matches either a or b
#    ( ) 	                Groups regular expressions and returns matched text
#    \t, \n, \r 	        Matches tab, newline, return


########################################################
# Problem 1: Return the first word of a given string
########################################################

# Solution-1  Extract each character (using “\w“)

import re
result=re.findall(r'.','AV is largest Analytics community of India')
print result
#Output:
#['A', 'V', ' ', 'i', 's', ' ', 'l', 'a', 'r', 'g', 'e', 's', 't', ' ', 'A', 'n', 'a', 'l', 'y', 't', 
#'i', 'c', 's', ' ', 'c', 'o', 'm', 'm', 'u', 'n', 'i', 't', 'y', ' ', 'o', 'f', ' ', 'I', 'n', 'd', 'i', 'a']

result=re.findall(r'\w','AV is largest Analytics community of India')
print result
#Output:
#['A', 'V', 'i', 's', 'l', 'a', 'r', 'g', 'e', 's', 't', 'A', 'n', 'a', 'l', 'y', 't', 'i', 'c', 's', 'c', 
#'o', 'm', 'm', 'u', 'n', 'i', 't', 'y', 'o', 'f', 'I', 'n', 'd', 'i', 'a']


# Solution-2  Extract each word (using “*” or “+“)

result=re.findall(r'\w*','AV is largest Analytics community of India')
print result
#Output:
#['AV', '', 'is', '', 'largest', '', 'Analytics', '', 'community', '', 'of', '', 'India', '']

result=re.findall(r'\w+','AV is largest Analytics community of India')
print result
Output:
['AV', 'is', 'largest', 'Analytics', 'community', 'of', 'India']


#  Solution-3 Extract each word (using “^“)

result=re.findall(r'^\w+','AV is largest Analytics community of India')
print result
#Output:
#['AV']

result=re.findall(r'\w+$','AV is largest Analytics community of India')
print result
#Output:
#[‘India’]

########################################################
# Problem 2: Return the first two character of each word
########################################################

#  Solution-1  Extract consecutive two characters of each word, excluding spaces (using “\w“)

result=re.findall(r'\w\w','AV is largest Analytics community of India')
print result
#Output:
#['AV', 'is', 'la', 'rg', 'es', 'An', 'al', 'yt', 'ic', 'co', 'mm', 'un', 'it', 'of', 'In', 'di']

#  Solution-2  Extract consecutive two characters those available at start of word boundary (using “\b“)

result=re.findall(r'\b\w.','AV is largest Analytics community of India')
print result
#Output:
#['AV', 'is', 'la', 'An', 'co', 'of', 'In']


########################################################
# Problem 3: Return the domain type of given email-ids
########################################################

#  Solution-1  Extract all characters after “@”

result=re.findall(r'@\w+','abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz') 
print result 
#Output: ['@gmail', '@test', '@analyticsvidhya', '@rest']

result=re.findall(r'@\w+.\w+','abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz')
print result
#Output:
#['@gmail.com', '@test.in', '@analyticsvidhya.com', '@rest.biz']

#   Solution – 2 Extract only domain name using “( )”

result=re.findall(r'@\w+.(\w+)','abc.test@gmail.com, xyz@test.in, test.first@analyticsvidhya.com, first.test@rest.biz')
print result
#Output:
#['com', 'in', 'com', 'biz']

########################################################
# Problem 4: Return date from given string
########################################################

result=re.findall(r'\d{2}-\d{2}-\d{4}','Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009')
print result
#Output:
#['12-05-2007', '11-11-2011', '12-01-2009']

result=re.findall(r'\d{2}-\d{2}-(\d{4})','Amit 34-3456 12-05-2007, XYZ 56-4532 11-11-2011, ABC 67-8945 12-01-2009')
print result
#Output:
#['2007', '2011', '2009']

########################################################
# Problem 5: Return all words of a string those starts with vowel
########################################################

#  Solution-1  Return each words
result=re.findall(r'\w+','AV is largest Analytics community of India')
print result
#Output:
#['AV', 'is', 'largest', 'Analytics', 'community', 'of', 'India']

#  Solution-2  Return words starts with alphabets (using [])
result=re.findall(r'[aeiouAEIOU]\w+','AV is largest Analytics community of India')
print result
#Output:
#['AV', 'is', 'argest', 'Analytics', 'ommunity', 'of', 'India']

#  Solution-3 Above you can see that it has returned “argest” and “ommunity” from the mid of words. 
#      To drop these two, we need to use “\b” for word boundary.
result=re.findall(r'\b[aeiouAEIOU]\w+','AV is largest Analytics community of India')
print result 
#Output:
#['AV', 'is', 'Analytics', 'of', 'India']

result=re.findall(r'\b[^aeiouAEIOU]\w+','AV is largest Analytics community of India')
print result
#Output:
#[' is', ' largest', ' Analytics', ' community', ' of', ' India']

#Above you can see that it has returned words starting with space. To drop it from output, 
#include space in square bracket[].
result=re.findall(r'\b[^aeiouAEIOU ]\w+','AV is largest Analytics community of India')
print result
#Output:
#['largest', 'community']


########################################################
# Problem 6: Validate a phone number (phone number must be of 10 digits and starts with 8 or 9) 
########################################################
import re
li=['9999999999','999999-999','99999x9999']
for val in li:
 if re.match(r'[8-9]{1}[0-9]{9}',val) and len(val) == 10:
     print 'yes'
 else:
     print 'no'
#Output:
#yes
#no
#no

########################################################
# Problem 7: Split a string with multiple delimiters
########################################################
import re
line = 'asdf fjdk;afed,fjek,asdf,foo' # String has multiple delimiters (";",","," ").
result= re.split(r'[;,\s]', line)
print result
#Output:
#['asdf', 'fjdk', 'afed', 'fjek', 'asdf', 'foo']

# We can also use method re.sub() to replace these multiple delimiters with one as space ” “.
import re
line = 'asdf fjdk;afed,fjek,asdf,foo'
result= re.sub(r'[;,\s]',' ', line)
print result
#Output:
#asdf fjdk afed fjek asdf foo

########################################################
# Problem 8: Retrieve Information from HTML file
########################################################
#Sample HTML file (str)
#<tr align="center"><td>1</td> <td>Noah</td> <td>Emma</td></tr>
#<tr align="center"><td>2</td> <td>Liam</td> <td>Olivia</td></tr>
#<tr align="center"><td>3</td> <td>Mason</td> <td>Sophia</td></tr>
#<tr align="center"><td>4</td> <td>Jacob</td> <td>Isabella</td></tr>
#<tr align="center"><td>5</td> <td>William</td> <td>Ava</td></tr>
#<tr align="center"><td>6</td> <td>Ethan</td> <td>Mia</td></tr>
#<tr align="center"><td>7</td> <td HTML>Michael</td> <td>Emily</td></tr>

result=re.findall(r'<td>\w+</td>\s<td>(\w+)</td>\s<td>(\w+)</td>',str)
print result
#Output:
#[('Noah', 'Emma'), ('Liam', 'Olivia'), ('Mason', 'Sophia'), ('Jacob', 'Isabella'), ('William', 'Ava'), ('Ethan', 'Mia'), ('Michael', 'Emily')]

#You can read html file using library urllib2 (see below code)
import urllib2
response = urllib2.urlopen('')
html = response.read()





