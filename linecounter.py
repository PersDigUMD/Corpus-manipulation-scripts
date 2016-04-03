'''
Created on Dec 27, 2015

@author: Elijah Cooke
'''

import sys, os
import xml.etree.ElementTree as ET
import csv
try:
    from lxml import etree , objectify
    print("running with lxml.etree")
except ImportError:
    try:
        # Python 2.5
        import xml.etree.cElementTree as etree
        print("running with cElementTree on Python 2.5+")
    except ImportError:
        try:
            # Python 2.5
            import xml.etree.ElementTree as etree
            print("running with ElementTree on Python 2.5+")
        except ImportError:
            try:
                # normal cElementTree install
                import cElementTree as etree
                print("running with cElementTree")
            except ImportError:
                try:
                    # normal ElementTree install
                    import elementtree.ElementTree as etree
                    print("running with ElementTree")
                except ImportError:
                    print("Failed to import ElementTree from any known place")
    
def listFiles(rootdir):
    result = []
    print('Searching {0} ...'.format(rootdir))
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            p = os.path.join(root,f)
            result.append(os.path.abspath(p))
    print('Found {0} files in the specified directory tree.'.format(len(result)))
    return result                

def countlines(file):
    endinghold = ""
    parser = etree.XMLParser(remove_pis=True)
    tree = etree.parse(file,parser)
    root = tree.getroot()
    words = 0
    lines = 0
    text = ""
    ns = {"xml":"http://www.tei-c.org/ns/1.0"}
    if "divan" in file:
        for urn in root.findall("xml:text/xml:body/xml:div", namespaces = ns):
            for genre in urn.findall("xml:div",namespaces = ns):
                for poem in genre.findall("xml:div",namespaces = ns):
                    for b in poem.findall("xml:l",namespaces = ns):
                        lines = lines + 1
                        if (b[0].text):
                            print(b[0].text)
                            words = words + len(b[0].text.split())
                        if (b[1].text):
                            words = words + len(b[1].text.split())
    else:
        print(file)
        for urn in root.findall("xml:text/xml:body/xml:div", namespaces = ns):
            if (urn.find("xml:div", namespaces = ns)):
                if (urn.find("xml:div", namespaces = ns).get("subtype")=="chapter"):
                    for chapter in urn.findall("xml:div",namespaces = ns):
                        for page in chapter.findall("xml:div",namespaces = ns):
                            for b in page.findall("xml:l",namespaces = ns):
                                lines = lines + 1
                                if (b[0].text):
                                    print(b[0].text)
                                    text = text + b[0].text + "\t"
                                    words = words + len(b[0].text.split())
                                if (b[1].text):
                                    print(b[1].text )
                                    text = text + b[1].text + "\n"
                                    words = words + len(b[1].text.split())
                else:
                    if (urn.find("xml:div", namespaces = ns).get("subtype")=="page"):
                        for page in urn.findall("xml:div",namespaces = ns):
                            for b in page.findall("xml:l",namespaces = ns):
                                lines = lines + 1
                                if (b[0].text):
                                    words = words + len(b[0].text.split())
                                if (b[1].text):
                                    words = words + len(b[1].text.split())
            else:
                for b in urn.findall("xml:l",namespaces = ns):
                    lines = lines + 1
                    if (b[0].text):
                        words = words + len(b[0].text.split())
                    if (b[1].text):
                        words = words + len(b[1].text.split())
    outputname = file.split('/home/elijah/Desktop/PDLcorpus-master/data',1)[1]
    f = open("shahname.txt","w")
    f.write(text)
    return (outputname, words, lines)
def main():
    files = listFiles(sys.argv[1])
    words = 0
    lines = 0
    outfile = open("output.csv", 'w')
    writer = csv.writer(outfile,delimiter='\t')
    for f in files:
        if "~" in f:
            continue
        if "_cts_" in f:
            continue
        data = countlines(f)
        writer.writerow(data)
        words = words + data[1]
        lines = lines + data[2]
    print ("word count: " + str(words))
    print ("Line count: " + str(lines))
    outfile.close()    
main()
