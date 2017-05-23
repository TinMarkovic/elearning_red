## Installation

'''
pip install -r piprequirements
cd elearning_red
cp elearning_red/settings_default.txt elearning_red/settings.py
nano elearning_red/settings.py # Set up DB config
python manage.py migrate
python manage.py loaddata elearning/fixtures/init.json
python manage.py runserver
'''


## Requirements

elearning projekt za ExtensionEngine Spring Camp, crveni tim "Shrubbery"

Zahtjevi:
- 3 nivoa korisnika: Student, Profesor, Administrator

ADMIN: Mora imati mogućnost kreirati druge korisnike

STUDENT: Mora biti u mogućnosti registrirati i logirati se, pristupit listi kolegija na koje je upisan i moći se sam upisati.

PROFESOR: Upisuje, ispisuje i mijenja studente u kolegijima, te programima.

- struktura Kolegija:

Profesor pristupa točci za izradu kolegija

Kolegij je sastavljen od SEKCIJA koje sadrže BLOKOVE sadržaja

Početni je zahtjev imanje četri različita bloka sadržaja:

HTML, Video, Slika, Kviz

(+ Program, koji sadrži više kolegija, i kolegiji 

mogu biti u više programa, nekakav logički skup kolegija)

- Stvaranje sadržaja mora biti jednostavno za profesora (npr. drag&drop)

- Neki osnovni zahtjevi za poglede:

STUDENT dashboard:

	Link za dodavanje na različite kolegije

	Lista svih upisanih kolegija

PROFESOR dashboard:

	Popis kolegija (u njegovoj kontroli)

	Link na dodavanje novih kolegija (CMS)

	Student management (za dodavanje na kolegije)
