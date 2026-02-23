# Plan i Priprema za Timesheet Aplikaciju

## (A) CHECKLIST - Šta TI treba da uradiš PRE nego što počnemo sa radom

### 1. Setup Development Okruženja
- [ ] Instaliraj **Node.js** (LTS verzija, npr. 20.x ili novija) - potrebno za ReactJS
- [ ] Instaliraj **Python** (verzija 3.9 ili novija) - potrebno za backend
- [ ] Instaliraj **Git** (ako već nemaš) - za verzionisanje koda
- [ ] Instaliraj **Visual Studio Code** ili drugi editor (ako već nemaš)
- [ ] Proveri da li radi `npm` i `python` u terminalu

### 2. Kreiranje GitHub Repozitorijuma (opciono, ali preporučeno)
- [ ] Kreiraj novi GitHub repozitorijum (može biti privatni)
- [ ] Daj mi pristup repozitorijumu (ili mi pošalji link ako ćeš da radim preko forka)
- [ ] Alternativa: ako ne koristiš GitHub, reci mi kako želiš da delimo kod

### 3. Kreiranje PostgreSQL Baze Podataka
- [ ] Odaberi managed PostgreSQL provajdera:
  - **Vercel Postgres** (najjednostavnije ako već koristiš Vercel)
  - **Neon** (besplatni tier, dobar za development)
  - **Supabase** (besplatni tier, lako za setup)
- [ ] Kreiraj novu bazu podataka
- [ ] Zabeleži **connection string** (format: `postgresql://user:password@host:port/database`)
- [ ] Testiraj konekciju (možeš koristiti neki PostgreSQL klijent kao pgAdmin ili DBeaver)

### 4. Kreiranje Vercel Naloga (za Frontend)
- [ ] Kreiraj nalog na **Vercel** (vercel.com) - besplatno
- [ ] Poveži GitHub nalog sa Vercelom (ako koristiš GitHub)
- [ ] Zabeleži Vercel nalog i pristupne podatke

### 5. Odluke o Backend Hostingu
- [ ] Odaberi jedan od sledećih opcija za backend hosting:
  - **Render** (render.com) - besplatni tier, automatski deploy iz GitHub-a
  - **Railway** (railway.app) - besplatni tier, jednostavno
  - **Fly.io** (fly.io) - besplatni tier, dobar za Python
- [ ] Kreiraj nalog na odabranom servisu
- [ ] Zabeleži pristupne podatke

### 6. Priprema Podataka za Aplikaciju
- [ ] **Lista imena za radio buttons**: Pripremi listu imena osoba koje će koristiti aplikaciju
  - Primer: ["Marko", "Ana", "Petar", "Jovana"]
  - Format: jednostavna lista stringova
- [ ] **Odluka o formatu Hours polja**:
  - Da li sme decimalno (npr. 4.5 sati)?
  - Ili samo celi brojevi (npr. 4, 5, 8)?
  - Maksimalna vrednost (npr. 24 sata)?
- [ ] **Odluka o formatu Date polja**:
  - Format prikaza (npr. DD/MM/YYYY ili YYYY-MM-DD)?
  - Da li dozvoljavamo prošle datume? Buduće datume?
  - Da li treba default vrednost (današnji datum)?

### 7. Environment Variables Priprema
- [ ] Pripremi listu environment varijabli koje će biti potrebne:
  - `DATABASE_URL` - connection string za PostgreSQL
  - `BACKEND_URL` - URL backend API-ja (biće poznat nakon deploy-a)
  - (Ostale varijable ću ti reći nakon što vidim specifične potrebe)

---

## (B) INFORMACIJE I ODLUKE koje su mi POTREBNE od tebe

### 1. Credentials i Connection String-ovi
- [ ] **PostgreSQL Connection String** (format: `postgresql://user:password@host:port/database`)
  - VAŽNO: Ne šalji mi ovo preko javnog kanala! Koristićemo environment variables
  - Možeš mi reći kako želiš da ga podelimo (npr. preko GitHub Secrets, ili direktno u Vercel/Render dashboard-u)

### 2. Lista Imena za Radio Buttons
- [ ] **Lista imena** (kao niz stringova):
  - Primer: `["Marko", "Ana", "Petar", "Jovana"]`
  - Ili mi reci da li će lista biti dinamička (dodaje se iz baze) ili statička

### 3. Validacione Odluke
- [ ] **Hours polje**:
  - [ ] Decimalno ili samo celi brojevi?
  - [ ] Maksimalna vrednost (npr. 24)?
  - [ ] Minimalna vrednost (npr. 0.5 ili 1)?
- [ ] **Date polje**:
  - [ ] Format prikaza (DD/MM/YYYY ili YYYY-MM-DD)?
  - [ ] Dozvoljeni prošli datumi? (DA/NE)
  - [ ] Dozvoljeni budući datumi? (DA/NE)
  - [ ] Default vrednost = današnji datum? (DA/NE)
- [ ] **Project polje**:
  - [ ] Slobodan unos (text input) ili dropdown lista?
  - [ ] Ako je dropdown, koja je lista projekata?
- [ ] **Description polje**:
  - [ ] Maksimalna dužina teksta? (npr. 500 karaktera)
  - [ ] Obavezno polje ili opciono?

### 4. Backend Hosting Odluka
- [ ] **Koji hosting servis si odabrao?**
  - Render / Railway / Fly.io / Drugo (navedi)
- [ ] **Da li imaš nalog i pristup?**

### 5. Deployment Strategija
- [ ] **Da li želiš da deploy-ujemo odmah nakon što napravim kod?**
  - Ili prvo testiranje lokalno?
- [ ] **Da li želiš da ja postavim environment variables na hosting servisima?**
  - Ili ćeš ti to uraditi (trebaću ti connection string-ovi)?

### 6. CSV Export Funkcionalnost
- [ ] **Format CSV export-a:**
  - [ ] Koje kolone treba da budu u CSV-u? (sve iz baze ili neke specifične?)
  - [ ] Format datuma u CSV-u?
  - [ ] Da li treba filtriranje po datumu/ime/projektu?
  - [ ] Ili jednostavno: svi podaci iz baze?

### 7. Dodatne Funkcionalnosti (opciono za MVP)
- [ ] **Da li želiš nešto dodatno za MVP?**
  - Validacija na frontendu?
  - Loading spinner tokom submit-a?
  - Error handling poruke?
  - Ili samo osnovna funkcionalnost?

---

## (C) PREDLOG STRUKTURE PROJEKTA

```
Timesheet app/
│
├── timesheet_front/          # ReactJS Frontend
│   ├── public/               # Statički fajlovi (index.html, favicon, itd.)
│   ├── src/
│   │   ├── components/        # React komponente
│   │   │   ├── TimesheetForm.jsx    # Glavna forma za unos podataka
│   │   │   └── SuccessMessage.jsx   # Poruka nakon uspešnog submit-a
│   │   ├── services/         # API pozivi ka backend-u
│   │   │   └── api.js        # Axios/fetch funkcije za API
│   │   ├── utils/            # Pomoćne funkcije
│   │   │   └── validation.js # Validacija formi
│   │   ├── App.jsx           # Glavna React komponenta
│   │   ├── index.js          # Entry point
│   │   └── index.css         # Globalni stilovi
│   ├── package.json          # NPM dependencies
│   ├── .env.local            # Environment variables (ne commit-uje se)
│   ├── .gitignore
│   └── vercel.json           # Vercel konfiguracija (opciono)
│
├── timesheet_back/           # Python Backend
│   ├── app/
│   │   ├── __init__.py
│   │   ├── main.py           # FastAPI/Flask aplikacija, glavni entry point
│   │   ├── models.py         # Database models (SQLAlchemy ili raw SQL)
│   │   ├── database.py       # Database konekcija i setup
│   │   ├── schemas.py        # Pydantic schemas za validaciju (ako FastAPI)
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── timesheet.py  # POST /timesheet endpoint
│   │       └── export.py     # GET /export endpoint (CSV)
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables (ne commit-uje se)
│   ├── .gitignore
│   └── README.md             # Backend dokumentacija
│
├── .gitignore                # Globalni gitignore
├── README.md                 # Glavna dokumentacija projekta
└── Timesheet_App_Specification.pdf
```

### Objašnjenje Strukture:

#### **timesheet_front/** (ReactJS)
- **public/**: Statički fajlovi koje Vercel servira direktno
- **src/components/**: React komponente (forma, poruke, itd.)
- **src/services/**: Funkcije za komunikaciju sa backend API-jem
- **src/utils/**: Pomoćne funkcije (validacija, formatiranje)
- **package.json**: Lista NPM paketa (React, Axios, itd.)
- **.env.local**: Environment varijable (BACKEND_URL, itd.)

#### **timesheet_back/** (Python)
- **app/main.py**: Glavna FastAPI/Flask aplikacija, definiše API rutе
- **app/models.py**: Database modeli (tabela timesheets)
- **app/database.py**: Setup PostgreSQL konekcije
- **app/schemas.py**: Pydantic modeli za validaciju request/response (FastAPI)
- **app/routes/**: API endpoint-i (POST /timesheet, GET /export)
- **requirements.txt**: Python paketi (FastAPI/Flask, psycopg2, itd.)
- **.env**: Environment varijable (DATABASE_URL)

---

## (D) PREDLOG TEHNOLOGIJA I DEPLOYMENT OPCIJE

### Frontend Tehnologije
- **ReactJS** (najnovija stabilna verzija)
- **Axios** ili **Fetch API** za HTTP pozive
- **React Hooks** (useState, useEffect) za state management
- **CSS Modules** ili **Tailwind CSS** (opciono, za stilizovanje)
- **Vercel** za hosting (automatski deploy iz GitHub-a)

### Backend Tehnologije
- **FastAPI** (preporučeno) ili **Flask**
  - FastAPI: moderno, brzo, automatska dokumentacija
  - Flask: jednostavnije, lakše za početnike
- **psycopg2** ili **asyncpg** za PostgreSQL konekciju
- **SQLAlchemy** (opciono) za ORM, ili raw SQL queries
- **Pydantic** (za FastAPI) za validaciju podataka
- **python-dotenv** za učitavanje environment varijabli

### Database
- **PostgreSQL** (managed)
- **Preporučeni provajderi:**
  1. **Vercel Postgres** ⭐ (najjednostavnije ako već koristiš Vercel)
     - Integrisano sa Vercel ekosistemom
     - Besplatni tier: 256 MB storage
     - Automatski backup
  2. **Neon** ⭐ (najbolji za development)
     - Besplatni tier: 0.5 GB storage
     - Serverless PostgreSQL
     - Brz setup
  3. **Supabase** (dobra alternativa)
     - Besplatni tier: 500 MB storage
     - Dodatne funkcionalnosti (auth, storage) ako zatreba kasnije

### Backend Hosting Opcije

#### 1. **Render** ⭐ (preporučeno za početak)
- **URL**: render.com
- **Besplatni tier**: Da (sa ograničenjima)
- **Pros**: 
  - Automatski deploy iz GitHub-a
  - Besplatni SSL sertifikat
  - Jednostavno setup
  - Podrška za Python
- **Cons**: 
  - Aplikacija "spava" nakon 15 min neaktivnosti (prvi request sporiji)
  - Ograničenja na besplatnom tier-u
- **Cena**: Besplatno (ili $7/mesec za web service bez sleep-a)

#### 2. **Railway**
- **URL**: railway.app
- **Besplatni tier**: Da ($5 kredita/mesec)
- **Pros**:
  - Brz deploy
  - Dobra podrška za Python
  - Lako dodavanje PostgreSQL baze
- **Cons**:
  - Ograničen kredit na besplatnom tier-u
- **Cena**: Besplatno ($5 kredita) ili $5/mesec minimum

#### 3. **Fly.io**
- **URL**: fly.io
- **Besplatni tier**: Da
- **Pros**:
  - Globalna distribucija
  - Dobra podrška za Python
  - Brz
- **Cons**:
  - Malo kompleksniji setup
- **Cena**: Besplatno (sa ograničenjima) ili pay-as-you-go

### Deployment Workflow

1. **Frontend (Vercel)**:
   - Push koda na GitHub
   - Poveži GitHub repozitorijum sa Vercel
   - Vercel automatski detektuje React projekat
   - Dodaj environment variable: `REACT_APP_BACKEND_URL`
   - Deploy se dešava automatski

2. **Backend (Render/Railway/Fly.io)**:
   - Push koda na GitHub
   - Poveži GitHub repozitorijum sa hosting servisom
   - Postavi environment variable: `DATABASE_URL`
   - Postavi build command: `pip install -r requirements.txt`
   - Postavi start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT` (FastAPI) ili `gunicorn app.main:app` (Flask)
   - Deploy se dešava automatski

3. **Database (Vercel Postgres/Neon/Supabase)**:
   - Kreiraj bazu preko dashboard-a
   - Kopiraj connection string
   - Dodaj u environment variables backend-a
   - (Prvo ću kreirati migration script za kreiranje tabele)

---

## ZAKLJUČAK

**Nakon što završiš checklist iz sekcije (A) i odgovoriš na pitanja iz sekcije (B), ja mogu da krenem sa implementacijom bez blokera.**

**Prioritetne informacije koje mi trebaju odmah:**
1. PostgreSQL connection string
2. Lista imena za radio buttons
3. Odluke o validaciji (hours, date format)
4. Backend hosting izbor

**Ostalo može da sačeka, ali ovo je minimum za početak.**

