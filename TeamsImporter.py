from dotenv import dotenv_values 
from tqdm import tqdm
import requests

config = dotenv_values(".env")

# Auth token
token = 'Token ' + config['TOKEN']

# the url of where the data will be pushed, for the teams is in the format /api/v1/tournaments/{tournemt}/teams
url = config['BASE_URI'] + '/api/v1/tournaments/' + config['TOURNAMENT_SLUG'] + '/teams'

# the url to get all the institutions, /api/v1/institutions
urlInst = config['BASE_URI'] + '/api/v1/institutions'

# link of the participants category, in this case the category is called 'iniciado' the other is called 'geral'
iniciado = config['INICIADOS_URL']
geral = config['OPEN_URL']

# link of the breaks category, in this case the category is called 'iniciado' the other is called 'geral'
breakIniciado = config['INICIADOS_BREAK_URL']
breakGeral = config['INICIADOS_BREAK_URL']


institutionDict = {}

def main():
    
    # A list of all participants
    with open('participants.txt', 'r', encoding='utf-8') as fp:
        participants = fp.read().splitlines()

    # A list in order with the emails of each participant1
    with open('emails.txt', 'r', encoding='utf-8') as fp:
        emails = fp.read().splitlines()

    # The list of type of break that each team is participanting, only support one time of break for each team
    # Categories should be done beforehand
    with open('Breaks.txt', 'r', encoding='utf-8') as fp:
        breaks = fp.read().splitlines()

    # Respective sociecty/insititue of each team, can be done to each participant only the first will be used
    with open('Sociedades.txt', 'r', encoding='utf-8') as fp:
        societies = fp.read().splitlines()
    # The list of each team name
    with open('TeamNames.txt', 'r', encoding='utf-8') as fp:
        teamNames = fp.read().splitlines()

    # A list for each participant if it is starting to debate now 'Iniciated'
    with open('Iniciado.txt', 'r', encoding='utf-8') as fp:
        iniciado = fp.read().splitlines()

    print(len(participants))

    # Check if all files have the same lenght, sanity check
    if not all(len(l) == len(participants) for l in iter([emails, breaks, societies, teamNames, iniciado])):
        print("The files dont't have the same lenght")
        return -1

    # Load all the possible institute
    load_inst()

    pbar = tqdm(total=len(participants), desc='Loading teams')

    i = 0
    while i < len(participants):
        r = requests.post(url=url,
                          headers={
                            'Authorization': token,
                            'Content-type': 'application/json'
                          },
                          json={
                            "reference": teamNames[i],
                            "short_reference": teamNames[i][:35],
                            "code_name": teamNames[i],
                            "institution": getInstitutionUrl(societies[i].lower()),
                            "speakers": [
                                {
                                    "name": participants[i],
                                    "email": emails[i],
                                    "categories": [
                                        mapIniciado(iniciado[i])
                                    ],
                                },
                                {
                                    "name": participants[i+1],
                                    "email": emails[i+1],
                                    "categories": [
                                        mapIniciado(iniciado[i+1])
                                    ],
                                }
                            ],
                            "use_institution_prefix": 'false',
                            "break_categories": [
                                mapBreak(breaks[i])
                            ],
                             "institution_conflicts": [
                                getInstitutionUrl(societies[i].lower())
                            ]
                          })
    
        if r.status_code != 201:
            print("Something went wrong! on iteration {}".format(i))
            print("status Code = \"{}\"".format(r.status_code))
            print(r.reason)
            print("Aborting! Some data might already have been imported")
            return
    
        i=i+2
        pbar.update(2)
    print("All Done")

def mapIniciado(cat):
    if (cat == 'SIM'):
        return iniciado
    return geral


def mapBreak(cat):
    if (cat == 'INICIADO'):
        return breakIniciado
    return breakGeral

def load_inst():
    r = requests.get(url=urlInst, headers={
        'Authorization': token
    })
    
    for i in r.json():
        institutionDict[i['code'].lower()] = i['url']

    # print(institutionDict)

def getInstitutionUrl(inst):
    if inst in institutionDict:
        return institutionDict[inst]
    return institutionDict['narnia']

if __name__ == '__main__':
    main()