#Beautiful Soup Script
from bs4 import BeautifulSoup
import csv

with open('Question Plans.html', 'r') as f:
    doc = f.read()

#Requires pythons default parser because lxml fails to parse the large table.
soup = BeautifulSoup(doc, 'html.parser')

#Empty list to store the tuples.
rows = []

#The fields of the data tuples.
header = ('Attachment', 'Question Page Link', 'Question Title', \
        'Question Plan Link', 'First Name', 'Last Name', 'Class', \
        'Keystone Title', 'Keystone Link', 'Mentor')

#This function evaluates true only for the <tr> table rows with Question d
def isrow(tag):
    if tag.name == u'tr':
        if tag.parent.parent.name == u'table' and \
                tag.parent.parent.has_attr('summary'): 
            return True
#Returns a tuple with all of the relevant info from a given <td> question.
def extract(rowtag):
    columns = rowtag.contents
    #Is there an attachment on the Question page?
    if columns[0].contents == []:
        attach = 'No'
    else:
        attach = 'Yes'

    #The question name and link
    q = columns[1].table.tbody.tr.td
    qpage = unicode(q.a['href'])
    qname = unicode(q.a.contents[0])

    #Question plan link, if there is one.
    if columns[2].string == None:
        qlink = 'N/A'
    else:
        qlink = unicode(columns[2].a['href'])

    #First Name
    fname = unicode(columns[3].string)

    #Last Name
    lname = unicode(columns[4].string)

    #Grad Year
    year = unicode(columns[5].string)

    #Keystone title
    kname = unicode(columns[6].string)

    #Keystone link
    if columns[7].string == None:
        klink = 'N/A'
    else:
        klink = unicode(columns[7].a['href'])
    #Mentor name
    mentor = unicode(columns[8].string)

    return (attach, qpage, qname, qlink, fname, \
            lname, year, kname, klink, mentor)


#Finds the first (header) row of the table.
rowone = soup.find('tr', { 'class' : 'ms-viewheadertr'})

#Iterates through each row of the table and calls extract.
for sibling in rowone.next_siblings:
    rows.append(extract(sibling))

with open('output.csv', 'w') as csvfile:
    planwriter = csv.writer(csvfile, dialect='excel')
    planwriter.writerow(header)
    for row in rows:
        seq = [elem.encode('utf-8', 'replace') for elem in row]
        planwriter.writerow(seq)


