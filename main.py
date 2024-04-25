import argparse
import importlib
import os

parser = argparse.ArgumentParser(description='Script for importing data in into tabbycat')

parser.add_argument('--setup', action='store_true', help='create all the necessary files') 
parser.add_argument('--cleanup', action='store_true', help='clear all the created files') 
parser.add_argument('--import-teams', action='store_true', help='import all the teams') 
parser.add_argument('--import-adj', action='store_true', help='import all the adjudicators') 

args = parser.parse_args()

file_paths = [
        'adj.txt',
        'adjEmail.txt',
        'adjInst.txt',
        'Breaks.txt',
        'emails.txt',
        'Iniciado.txt',
        'participants.txt',
        'Sociedades.txt',
        'TeamNames.txt',
    ]

def main():

    if args.setup:
        create_files()
    elif args.import_teams:
        import_teams()
    elif args.import_adj:
        import_adj()
    elif args.cleanup:
        cleanup()
    else:
        print("Nothing to do goodbye :)")

    return 1

def create_files():
    for file in file_paths:
        try:
            with open(file, 'w') as file:
                pass  # pass statement does nothing, so it creates an empty file
        
            print(f"Empty text file '{file}' created successfully.")
        
        except Exception as e:
            print(f"Error occurred: {e}")

def import_teams():
    try:
        teams_importer = importlib.import_module("TeamsImporter")
        teams_importer.main()
    except Exception as e:
        print(f"Error occurred: {e}")

def import_adj():
    try:
        adj_importer = importlib.import_module("AdjImporter")
        adj_importer.main()
    except Exception as e:
        print(f"Error occurred: {e}")

def cleanup():
    for file in file_paths:

        try:
            if os.path.exists(file):
                os.remove(file)
                print(f"File '{file}' deleted successfully.")
            else:
                print(f"File '{file}' does not exist.")
        except Exception as e:
            print(f"Error occurred: {e}")

if __name__ == '__main__':
    main()