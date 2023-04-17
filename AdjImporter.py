import requests

token = ''
url = ''
urlInst = ''

institutionDict = {}

baseScore = 2.5

def main():
    with open('adj.txt', 'r', encoding='utf-8') as fp:
        adj = fp.read().splitlines()

    with open('adjEmail.txt', 'r', encoding='utf-8') as fp:
        emails = fp.read().splitlines()

    with open('adjInst.txt', 'r', encoding='utf-8') as fp:
        societies = fp.read().splitlines()

    print(len(adj))

    # Check if all files have the same lenght, sanity check
    if not all(len(l) == len(adj) for l in iter([emails, societies])):
        print("The files dont't have the same lenght")
        return -1

    load_inst()

    
    i = 0
    while i < len(adj):
        r = requests.post(url=url,
                          headers={
                            'Authorization': token,
                            'Content-type': 'application/json'
                          },
                          json={
                            "name": adj[i],
                            "email": emails[i],
                            "institution": getInstitutionUrl(societies[i].lower()),
                            "base_score": baseScore,
                            "institution_conflicts": [
                                getInstitutionUrl(societies[i].lower())
                            ],
                            "team_conflicts": [],
                            "adjudicator_conflicts": [],
                        })
    
        i=i+1
        if r.status_code != 201:
            print("Something went wrong!")
            print("status Code = \"{}\"".format(r.status_code))
            print(r.text)
            print("Aborting! Some data might already have been imported")
            return
    
    
    print("All Done")

def load_inst():
    r = requests.get(url=urlInst, headers={
        'Authorization': token
    })
    
    for i in r.json():
        institutionDict[i['code'].lower()] = i['url']

def getInstitutionUrl(inst):
    return institutionDict[inst]

if __name__ == '__main__':
    main()