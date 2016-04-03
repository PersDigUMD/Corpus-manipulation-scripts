'''
Created on Mar 15, 2016

@author: elijah
'''
import sys, os
import xml.etree.ElementTree as ET
from gc import garbage
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
    
correctauthors = {
            "abusaeed":"abusaid",
            "anvari":"anvari",
            "babaafzal":"babaafzal",
            "babataher":"babataher",
            "bahaee":"bahai",
            "bahar":"bahar",
            "bidel":"bidel",
            "eraghi":"eraghi",
            "farrokhi":"farrokhi",
            "ferdousi":"ferdowsi",
            "feyz":"feyz",
            "forooghi":"forughi",
            "ghaani":"ghaani",
            "gorgani":"gorgani",
            "hafez":"hafez",
            "hatef":"hatef",
            "helali":"helali",
            "hojviri":"hojviri",
            "iqbal":"eqbal",
            "jabali":"jabali",
            "jami":"jami",
            "kesayeek":"kasai",
            "haghani":"khaghani",
            "khajoo": "khaju",
            "khalili": "khalili",
            "khayyam": "khayyam",
            "khosro": "khosrow",
            "mahsati":"mahsati",
            "manoochehri": "manuchehri",
            "masood": "masud",
            "mohtasham": "mohtasham",
            "monshi":"monshi",
            "naserkhosro": "naserkhosrow",
            "nezami": "nezami",
            "obeyd": "obeyd",
            "orfi": "orfi",
            "ouhadi": "owhadi",
            "parvin": "parvin",
            "rahi": "rahi",
            "rashhe": "rashheh",
            "razi": "razi",
            "roodaki": "rudaki",
            "rumi_moulavi": "rumi_moulavi",
            "rumi": "rumi_moulavi",
            "moulavi": "rumi_moulavi",
            "saadi": "sadi",
            "saeb":"saeb",
            "salman": "salman",
            "sanaee": "sanai",
            "seyf": "seyf",
            "shabestari": "shabestari",
            "shahnematollah": "shahnematollah",
            "shahriar": "shahriar",
            "shater": "shater",
            "vahshi": "vahshi",
             }

correctworknames = {
                    "divan":    "divan",
                    "Divan":    "divan",
                   "30fasl":    "sifasl",
                   "sifasl":    "sifasl",
                   "asrarname":   "asrarnameh", 
                   "asrarnameh":    "asrarnameh",
                   "bayanolershad":    "bayanolershad",
                   "bisarname":    "bisarnameh",
                   "bisarnameh":    "bisarnameh",
                   "bolbolname":    "bolbolnameh",
                   "bolbolnameh":   "bolbolnameh",
                   "elahiname":    "elahinameh",
                   "elahinameh":    "elahinameh",
                   "fn":    "fotovvatnameh",
                   "fotovvatnameh": "fotovvatnameh",
                   "nan-halva":    "nanhalva",
                   "nanhalva":  "nanhalva",
                   "nan-paneer":    "nanpanir",
                   "nanpanir":  "nanpanir",
                   "shir-shekar":    "shirshekar",
                   "shirshekar":    "shirshekar",
                   "oshaghname":    "oshshaqnameh",
                   "oshshaqnameh":  "oshshaqnameh",
                   "shahname":    "shahnameh",
                   "shahnameh": "shahnameh",
                   "masnavi":    "masnavi",
                   "veysoramin":    "visuramin",
                   "visuramin": "visuramin",
                   "montasab":    "montasab",
                   "saghiname":    "saqinameh",
                   "saqinameh": "saqinameh",
                   "shahodarvish":    "shahudarvish",
                   "shahudarvish":  "shahudarvish",
                   "ouhadi":    "owhadi",
                   "owhadi":    "owhadi",
                   "kashfol-mahjoob":    "kashfolmahjub",
                   "kashfolmahjub": "kashfolmahjub",
                   "armaghan-hejaz":    "armaghanhejaz",
                   "armaghanhejaz":     "armaghanhejaz",
                   "asrar-khodi":    "asrarkhudi",
                   "asrarkhudi":    "asrarkhudi",
                   "javidname":    "javidnameh",
                   "javidnameh":    "javidnameh",
                   "pas-che-bayad-kard":    "paschehbayadkard",
                   "paschehbayadkard":  "paschehbayadkard",
                   "payam-mashregh":    "payammashreq",
                   "payammashreq":  "payammashreq",
                   "romooz-bikhodi":    "romuzbikhudi",
                   "romuzbikhudi":  "romuzbikhudi",
                   "zaboor-ajam":    "zaburajam",
                   "zaburajam": "zaburajam",
                   "7ourang":    "haftowrang",
                   "haftowrang":    "haftowrang",
                   "8behesht":    "hashtbehesht",
                   "hashtbehesht":  "hashtbehesht",
                   "ayeene-sekandari":    "ayinehsekandari",
                   "ayinehsekandari":   "ayinehsekandari",
                   "khosro-shirin":    "khosrowushirin",
                   "khosrowushirin":    "khosrowushirin",
                   "majnoon-leyli":    "majnunulayli",
                   "majnunulayli":  "majnunulayli",
                   "matlaolanvar":    "matlaolanvar",
                   "safarname":    "safarnameh",
                   "safarnameh":    "safarnameh",
                   "7peykar":    "haftpaykar",
                   "haftpaykar":    "haftpaykar",
                   "kheradname":    "kheradnameh",
                   "kheradnameh":   "kheradnameh",
                   "khosroandshirin":    "khosrowushirin",
                   "khosrowushirin":    "khosrowushirin",
                   "leyli-majnoon":    "layliumajnun",
                   "layliumajnun":  "layliumajnun",
                   "makhzanolasrar":    "makhzanolasrar",
                   "sharafname":    "sharafnameh",
                   "sharafnameh":   "sharafnameh",
                   "moosh-gorbe":    "mushgorbeh",
                   "mushgorbeh":    "mushgorbeh",
                   "oshaghname":    "oshshaqnameh",
                   "oshshaqnameh":  "oshshaqnameh",
                   "jaamejam":    "jamjam",
                   "jamjam":    "jamjam",
                   "mantegholoshagh":    "manteqoloshshaq",
                   "manteqoloshshaq":   "manteqoloshshaq",
                   "gouhar-e-eshgh":    "gowhareshq",
                   "gowhareshq":    "gowhareshq",
                   "mofrar":    "mofradat",
                   "mofradat":"mofradat",
                   "saghiname":    "saqinameh",
                   "saqinameh":"saqinameh",
                   "soughandname":    "suqandnameh",
                   "suqandnameh":"suqandnameh",
                   "boostan":    "bustan",
                   "bustan":"bustan",
                   "golestan":    "golestan",
                   "feraghname":    "feraqnameh",
                   "feraqnameh":"feraqnameh",
                   "jamkhor":    "jamshidukhurshid",
                   "jamshidukhurshid":"jamshidukhurshid",
                   "hadighe":    "hadiqeh",
                   "hadiqeh":"hadiqeh",
                   "tariq":    "tariq",
                   "golshaneraz":    "golshanraz",
                   "golshanraz":"golshanraz",
                   "kanzoqlhaghayegh":    "kanzolhaqayeq",
                   "kanzolhaqayeq":"kanzolhaqayeq",
                   "shahriar":    "shahriyar",
                   "shahriyar":"shahriyar",
                   "heydarbaba":    "haydarbaba1",
                   "haydarbaba1":"haydarbaba1",
                   "heydarbaba2":    "haydarbaba2",
                   "haydarbaba2":"haydarbaba2",
                   "farhad-shirin":    "farhadushirin",
                   "farhadushirin":"farhadushirin",
                   "khold-barin":    "kholdbarin",
                   "nazer-manzoor":    "nazerumanzur",
                   "nazerumanzur":"nazerumanzur",
                   "khosro-shirin2":"khosrowushirin2",
                   }

dateofdeath = {
                "abusaid":    "1049",
                "anvari":    "1189",
                "attar":    "1221",
                "babaafzal":    "1214",
                "babataher":    "1050",
                "bahai":    "1621",
                "bahar":    "1951",
                "bidel":    "1721",
                "eraghi":    "1289",
                "farrokhi":    "1038",
                "ferdowsi":    "1020",
                "feyz":    "1595",
                "forughi":    "1857",
                "ghaani":    "1854",
                "gorgani":    "1065",
                "hafez":    "1390",
                "hatef":    "1783",
                "helali":    "1589",
                "hojviri":    "1077",
                "eqbal":    "1938",
                "jabali":   "unkown",
                "jami":    "1492",
                "khaghani":    "1199",
                "khaju":    "1349",
                "khalili":    "1987",
                "khayyam":  "1131",
                "khosrow":    "1325",
                "mahsati":    "1160",
                "manuchehri":    "1049",
                "masud":    "1121",
                "mohtasham":    "1588",
                "monshi":    "1187",
                "naserkhosrow":    "1060",
                "nezami":    "1209",
                "obeyd":    "1370",
                "orfi":    "1591",
                "owhadi":    "1338",
                "parvin":    "1941",
                "rahi":    "1968",
                "rashheh":  "unkown",
                "razi":    "1627",
                "rudaki":    "941",
                "rumi_moulavi":    "1273",
                "sadi":    "1292",
                "saeb":    "1676",
                "salman":    "1376",
                "sanai":    "1131",
                "seyf":    "1348",
                "shabestari":    "1340",
                "shahnematollah":    "1431",
                "shahriar":    "1988",
                "shater":    "1937",
                "vahshi":    "1583",
             }

def listFiles(rootdir):
    result = []
    print('Searching {0} ...'.format(rootdir))
    for root, dirs, files in os.walk(rootdir):
        for f in files:
            p = os.path.join(root,f)
            result.append(os.path.abspath(p))
    print('Found {0} files in the specified directory tree.'.format(len(result)))
    return result                

def changefile(file,misswork):
    endinghold = ""
    parser = etree.XMLParser(remove_pis=True)
    tree = etree.parse(file,parser)
    root = tree.getroot()
    words = 0
    lines = 0
    filename = ""
    ns = {"xml":"http://www.tei-c.org/ns/1.0"}
    if "divan" in file:
        for urn in root.findall("xml:text/xml:body/xml:div", namespaces = ns):
            urn.set("n",changeurn(urn.get("n"),misswork))
            filename = newfilename(urn.get("n"),misswork)
            poemcount = 0
            for genre in urn.findall("xml:div",namespaces = ns):
                for poem in genre.findall("xml:div",namespaces = ns):
                    poemcount = poemcount + 1
                    poem.set("n", str(poemcount)) 
                    poem.set("genre",genre.get("n"))
                    for b in poem.findall("xml:l",namespaces = ns):
                        if (b[0].text):
                            b[0].text = normtext(b[0].text)
                        if (b[1].text):
                            b[1].text = normtext(b[1].text)
                    urn.append(poem)
                urn.remove(genre)
    else:
        for urn in root.findall("xml:text/xml:body/xml:div", namespaces = ns):
            urn.set("n",changeurn(urn.get("n"),misswork))
            filename = newfilename(urn.get("n"),misswork)
            if (urn.find("xml:div", namespaces = ns)):
                if (urn.find("xml:div", namespaces = ns).get("subtype")=="chapter"):
                    for chapter in urn.findall("xml:div",namespaces = ns):
                        for page in chapter.findall("xml:div",namespaces = ns):
                            for b in page.findall("xml:l",namespaces = ns):
                                if (b[0].text):
                                    b[0].text = normtext(b[0].text)
                                if (b[1].text):
                                    b[1].text = normtext(b[1].text)
                else:
                    if (urn.find("xml:div", namespaces = ns).get("subtype")=="page"):
                        for page in urn.findall("xml:div",namespaces = ns):
                            for b in page.findall("xml:l",namespaces = ns):
                                if (b[0].text):
                                    b[0].text = normtext(b[0].text)
                                if (b[1].text):
                                    b[1].text = normtext(b[1].text)
            else:
                for b in urn.findall("xml:l",namespaces = ns):
                    if (b[0].text):
                        b[0].text = normtext(b[0].text)
                    if (b[1].text):
                        b[1].text = normtext(b[1].text)
    for filedesc in root.findall("xml:teiHeader/xml:fileDesc", namespaces = ns):
        notesStmt = etree.SubElement(filedesc,"notesStmt")
        note = etree.SubElement(notesStmt,"note", subtype="dateOfDeath")
        note.text = authordateofdeath(filename)
    for title in root.findall("xml:teiHeader/xml:fileDesc/xml:titleStmt/xml:title", namespaces = ns):
        title.text = normwork(title.text,misswork)
    f = open(file,"w")
    textstring = etree.tostring(root, pretty_print=True).decode()
    f.write(textstring)
    f.close
    os.rename(file, os.path.dirname(file)+"/"+filename)
    return

#takes in an urn and corrects the speeling of the work identifier
def changeurn(urn,misswork):
    #splits out the textgroup part of the urn
    garbage, hold = urn.split("urn:cts:perslit:")
    #splits the work identifier into its parts
    hold = hold.split(".")
    #assigns the parts of the work identifier to specific variables and normilize the name
    author = normauthor(hold[0])
    work = normwork(hold[1],misswork)
    version = hold[2]
    newurn = "urn:cts:perslit:" + author + "." + work + "." + version
    return newurn

#creates the name for the new file with the correct spelling by using the urn
def newfilename(urn,misswork):
    #splits out the textgroup part of the urn
    garbage, hold = urn.split("urn:cts:perslit:")
    #splits the work identifier into its parts
    hold = hold.split(".")
    #assigns the parts of the work identifier to specific variables and normilize the name
    author = normauthor(hold[0])
    work = normwork(hold[1],misswork)
    version = hold[2]
    name = author + "." + work + "." + version + ".xml"
    return name
#takes an author as a string an checks it against the dictionary of authors and if found changes to the correct spelling
def normauthor(author):
    if author in correctauthors:
        newauthor = correctauthors[author]
        return newauthor
    else:
        return author
    
#takes an work as a string an checks it against the dictionary of work names and if found changes to the correct spelling
def normwork(work,misswork):
    if work in correctworknames:
        newwork = correctworknames[work]
        return newwork
    else:
        print(work +" not found")
        misswork.append(work)
        return work

#takes in a file name and splits it into its parts and returns the authors date of death from dateofdeath dictionary
def authordateofdeath(filename):
    hold = filename.split(".")
    author = hold[0]
    return dateofdeath[author]

#takes text as input and normalizes the text then outputs the new text
def normtext(otext):
    newtext = otext.replace(".","")
    newtext = newtext.replace("ِ","")
    newtext = newtext.replace("َ","")
    newtext = newtext.replace("؟","")
    newtext = newtext.replace("ْ","")
    newtext = newtext.replace("ٌ","")
    newtext = newtext.replace("ٍ","")
    newtext = newtext.replace("ً","")
    newtext = newtext.replace("ُ","")
    newtext = newtext.replace("ّ","")
    newtext = newtext.replace("ٓ","")
    newtext = newtext.replace("ٰ","")
    newtext = newtext.replace("ٔ","")
    newtext = newtext.replace("ء","")
    newtext = newtext.replace("؛","")
    newtext = newtext.replace("،","")
    return newtext
     
def main():
    misswork = []
    files = listFiles(sys.argv[1])
    for f in files:
        if "~" in f:
            continue
        if "_cts_" in f:
            continue
        changefile(f,misswork)
        print ("file "+f+" updated")
    print(list(set(misswork)))
main()
