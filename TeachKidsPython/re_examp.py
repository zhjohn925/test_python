#  https://docs.python.org/3/library/re.html
#    re.match()
#    re.search()
#    re.findall()
#    re.split()
#    re.sub()
#    re.compile()


result = re.search(r'Analytics', 'AV Analytics Vidhya AV')
print result.group(0)
#Output:
#Analytics

result = re.findall(r'AV', 'AV Analytics Vidhya AV')
print result
#Output:
#['AV', 'AV']

# re.split(pattern, string, [maxsplit=0])
result=re.split(r'y','Analytics')
result
#Output:
#['Anal', 'tics']

result=re.split(r'i','Analytics Vidhya')
print result
#Output:
#['Analyt', 'cs V', 'dhya'] #It has performed all the splits that can be done by pattern "i".

result=re.split(r'i','Analytics Vidhya',maxsplit=1)
result
#Output:
#['Analyt', 'cs Vidhya']

result=re.sub(r'India','the World','AV is largest Analytics community of India')
result
#Output:
#'AV is largest Analytics community of the World'

# re.compile(pattern, repl, string)
pattern=re.compile('AV')
result=pattern.findall('AV Analytics Vidhya AV')
print result
result2=pattern.findall('AV is largest analytics community of India')
print result2
#Output:
#['AV', 'AV']
#['AV']
