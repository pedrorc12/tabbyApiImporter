# tabbyApiImporter

A simple importer for the tabby cat tabulation software

## How to use it

## set up

First you copy the .env.template to the .env and change the variables acordinly.

for the open and "inicado" category you can curl the `/api/v1/tournaments/{slug}/speaker-categories` (or the `/api/v1/tournaments/{slug}/break-categories` for the break categories) to see the options.

you can download all the necessary dependecies with `pip install -r requirements.txt`

after the env variables were set up you can run the main.py script the options are: 
```bash
  --setup         create all the necessary files
  --cleanup       clear all the created files
  --import-teams  import all the teams
  --import-adj    import all the adjudicators
```
Run the script with `python main.py --setup` to create the necessary txt
files then put in each file the information necessary the order is important the line of each file should match the line of other files for example:
| participants.txt | email.txt              | Sociedades.txt | ... |   |
|------------------|------------------------|----------------|-----|---|
| participantA     | participantA@email.com | SdDUP          |     |   |
| participantB     | participantB@email.com | SdDUP          |     |   |
| ...              | ...                    | ...            |     |   |

#### Breaks file 
In the breaks file if the team is 'inicado' write "INICIADO" in caps, if is not type anything else.

#### Inicado file
In Inicado.txt file write "SIM" if the participants is 'inicado' if is not write anything else.

## Import the Teams

To import the teams simply run `python main.py --import-teams`

## Import the Adjudicators

To import the teams simply run `python main.py --import-adj`

### clean up 

After everything is done you can run `python main.py --cleanup` to clear the files

## Troubleshoting

### 403
If you get 403 forbidden certified that the token is valid

### 500
You may get a 500 error if you try to import a team that is already there, in this case clear the database and try again