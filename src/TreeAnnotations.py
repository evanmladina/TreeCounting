import requests

ZENODO_TREES_URL = 'https://zenodo.org/record/3765872'
ZENODO_TREE_SHAPEZIPFILE_URL = "https://zenodo.org/record/3765872/files/shapefiles.zip"
ZENODO_TREE_ANNOTATIONS_BY_SITE = {"SJER":"https://zenodo.org/record/3765872/files/SJER_2019.csv",
"ABBY":"https://zenodo.org/record/3765872/files/ABBY_2019.csv",
"BART":"https://zenodo.org/record/3765872/files/BART_2019.csv",
"BLAN":"https://zenodo.org/record/3765872/files/BLAN_2019.csv",
"BONA":"https://zenodo.org/record/3765872/files/BONA_2019.csv",
"CLBJ":"https://zenodo.org/record/3765872/files/CLBJ_2019.csv",
"CUPE":"https://zenodo.org/record/3765872/files/CUPE_2018.csv",
"DEJU":"https://zenodo.org/record/3765872/files/DEJU_2019.csv",
"DELA":"https://zenodo.org/record/3765872/files/DELA_2019.csv",
"DSNY":"https://zenodo.org/record/3765872/files/DSNY_2019.csv",
"GUAN":"https://zenodo.org/record/3765872/files/GUAN_2018.csv",
"HARV":"https://zenodo.org/record/3765872/files/HARV_2019.csv",
"HEAL":"https://zenodo.org/record/3765872/files/HEAL_2019.csv",
"HOPB":"https://zenodo.org/record/3765872/files/HOPB_2019.csv",
"JERC":"https://zenodo.org/record/3765872/files/JERC_2019.csv",
"JORN":"https://zenodo.org/record/3765872/files/JORN_2019.csv",
"KONZ":"https://zenodo.org/record/3765872/files/KONZ_2019.csv",
"LAJA":"https://zenodo.org/record/3765872/files/LAJA_2018.csv",
"LENO":"https://zenodo.org/record/3765872/files/LENO_2019.csv",
"MLBS":"https://zenodo.org/record/3765872/files/MLBS_2018.csv",
"MOAB":"https://zenodo.org/record/3765872/files/MOAB_2019.csv",
"NIWO":"https://zenodo.org/record/3765872/files/NIWO_2019.csv",
"NOGP":"https://zenodo.org/record/3765872/files/NOGP_2019.csv",
"OAES":"https://zenodo.org/record/3765872/files/OAES_2019.csv",
"OSBS":"https://zenodo.org/record/3765872/files/OSBS_2019.csv",
"REDB":"https://zenodo.org/record/3765872/files/REDB_2019.csv",
"RMNP":"https://zenodo.org/record/3765872/files/RMNP_2018.csv",
"SCBI":"https://zenodo.org/record/3765872/files/SCBI_2019.csv",
"SERC":"https://zenodo.org/record/3765872/files/SERC_2019.csv",
"SOAP":"https://zenodo.org/record/3765872/files/SOAP_2019.csv",
"SRER":"https://zenodo.org/record/3765872/files/SRER_2019.csv",
"TALL":"https://zenodo.org/record/3765872/files/TALL_2019.csv",
"TEAK":"https://zenodo.org/record/3765872/files/TEAK_2019.csv",
"WLOU":"https://zenodo.org/record/3765872/files/WLOU_2019.csv",
"WOOD":"https://zenodo.org/record/3765872/files/WOOD_2019.csv",
"WREF":"https://zenodo.org/record/3765872/files/WREF_2019.csv",
"YELL":"https://zenodo.org/record/3765872/files/YELL_2019.csv"}

def getAnnotationURL(selection):
    if selection.upper() == 'ALL':
        return ZENODO_TREE_SHAPEZIPFILE_URL
    else:
        return ZENODO_TREE_ANNOTATIONS_BY_SITE[selection.upper()]


def downloadAnnotation(selection, downloadFilePath):
    if (selection.upper() == 'ALL'):
        print("Don't currently support getting all shape files\n")
        return
    url = getAnnotationURL(selection) + '?download=1'
    data = requests.get(url,timeout=5)
    with open(downloadFilePath, 'wb') as f:
       f.write(data.content)
    