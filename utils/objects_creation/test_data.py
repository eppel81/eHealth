# -*- coding: utf-8 -*-

PAYMENT_NONCES = {
        'amex': 'fake-valid-amex-nonce',
        'visa': 'fake-valid-visa-nonce',
        'paypal': 'fake-paypal-future-nonce'
    }

DOCTORS = [
    {
        'username': 'doctor1',
        'email': 'doctor1@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Azcona',
        'last_name': 'Guerra',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._GUERRA_AZCONA_pu7zytO.jpg',
    },
    {
        'username': 'doctor2',
        'email': 'doctor2@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Castell',
        'last_name': 'Gomez',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._CASTELL_GÓMEZ_37HKDDc.jpg',
    },
    {
        'username': 'doctor3',
        'email': 'doctor3@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Federico',
        'last_name': 'Castillo',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._DEL_CASTILLO_DÍEZ.jpg',
    },
    {
        'username': 'doctor4',
        'email': 'doctor4@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Freire',
        'last_name': 'Torres',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._FREIRE_TORRES.jpg',
    },
    {
        'username': 'doctor5',
        'email': 'doctor5@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Mora',
        'last_name': 'Sanz',
        'city_id': 1,
        'country_id': 2,
        'gender': True,
        'timezone_id': 212,
        'photo': 'photo/DR._MORA_SANZ.jpg',
    },
    {
        'username': 'doctor6',
        'email': 'doctor6@mail2tor.com',
        'password': 'zaq123',
        'first_name': 'Villar',
        'last_name': 'Riu',
        'city_id': 1,
        'country_id': 2,
        'gender': False,
        'timezone_id': 212,
        'photo': 'photo/DRA._VILLAR_RIU.jpg',
    }
]

PATIENTS = [
    {
        'username': 'patient1',
        'email': 'patient1@gmail.com',
        'password': 'zaq123',
        'first_name': 'Meike',
        'last_name': 'Ritter',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient1.jpg'
    },
    {
        'username': 'patient2',
        'email': 'patient2@gmail.com',
        'password': 'zaq123',
        'first_name': 'Ferdinand',
        'last_name': 'Lang',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient2.jpg'
    },
    {
        'username': 'patient3',
        'email': 'patient3@gmail.com',
        'password': 'zaq123',
        'first_name': 'Luise',
        'last_name': 'Breuer',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient3.jpg'
    },
    {
        'username': 'patient4',
        'email': 'patient4@gmail.com',
        'password': 'zaq123',
        'first_name': 'Brad',
        'last_name': 'Sullivan',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient4.jpg'
    },
    {
        'username': 'patient5',
        'email': 'patient5@gmail.com',
        'password': 'zaq123',
        'first_name': 'Leonard',
        'last_name': 'Beck',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient5.jpg'
    },
    {
        'username': 'patient6',
        'email': 'patient6@gmail.com',
        'password': 'zaq123',
        'first_name': 'Perry',
        'last_name': 'Pearson',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient6.jpg'
    },
    {
        'username': 'patient7',
        'email': 'patient7@gmail.com',
        'password': 'zaq123',
        'first_name': 'Gabriel',
        'last_name': 'Omahony',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient7.jpg'
    },
    {
        'username': 'patient8',
        'email': 'patient8@gmail.com',
        'password': 'zaq123',
        'first_name': 'Karen',
        'last_name': 'Murphy',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient8.jpg'
    },
    {
        'username': 'patient9',
        'email': 'patient9@gmail.com',
        'password': 'zaq123',
        'first_name': 'Katherine',
        'last_name': 'Warren',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient9.jpg'
    },
    {
        'username': 'patient10',
        'email': 'patient10@gmail.com',
        'password': 'zaq123',
        'first_name': 'Jay',
        'last_name': 'Spencer',
        'country_id': 2,
        'timezone_id': 180,
        'photo': 'photo/patient10.jpg'
    }
]


NOTES = [
    {
        'anamnesis': 'AP:. F - B:-Amigdalectomía. Talasemia minor. Jaquecas '
                     'frecuentes en tratamiento con Carbapacemina y par l columna '
                     'Artrotec. No alergias conocidas. AF:. 21,1,13 EA:: '
                     '.Cuadro de dolor epigastrico que irradia todo el abdomen. '
                     'No cede con la ingesta y sy lo hace cuando vomita. Esta en '
                     'tratamiento con Movicol. 11,2,13: BREATH TEST 7,57 Positivo. '
                     'ECOGRAFIA ABDOMINAL: Sin alteraciones. 22,4,13: BREATH TEST: 15,3 '
                     'Positivo. 20,5,13: cuádruple terapia. 21,10,13: BREATH TEST: 0,9 Negativo. '
                     '3,3,15: Cuadro de descomposición y vómitos , con presencia '
                     'de moco en heces. Suxidina0,1,1, BREATH TEST ANALISIS DE HECES. ',
        'exploration': '',
        'diagnosis': 'Gastritis helicobacter +',
        'additional_tests': '',
        'treatment': 'Triple terapia',
        'public_notes': ''
    },
    {
        'anamnesis': 'las trae ahora de la SS y parece que son negativos y '
                     'patrece que la han pedido lo de la capsula endoscopica por '
                     'fin EXPL persiste el timpanismo llamativi mas en el '
                     'flanco izqdo pendiente de la capsula pongo Kreon y dieta sin gluten',
        'exploration': '',
        'diagnosis': '',
        'additional_tests': '',
        'treatment': '',
        'public_notes': ''
    },
    {
        'anamnesis': 'Cuñado de Dr. Titi Consulta por aenmia ferropénica. '
                     'Le hicieron una polipectomía por colotomia hace 4-5 '
                     'años M. Calwero en el Rosario. Artrtia¡s gotosa, '
                     'EPOC (bronquitis asmática), Ahora Hb 8,2 con Fe de 14 y '
                     'ferritina de 15',
        'exploration': 'Epigastralgia. Resto igual',
        'diagnosis': '',
        'additional_tests': 'Colono + gastro con sedación',
        'treatment': '',
        'public_notes': ''
    }
]

TEST_FILES = [
    {
        'file': 'files/emedicaltest1@gmail.com/UAT MANOMETRIA PRUEBA_CbVJXds.docx',
        'conclusions': 'Esfinter esofágico inferior normotenso, asimétrico con '
                        'disfunción por relajaciones ausentes. Motilidad de '
                        'cuerpo esofágico con peristalsis conservada dentro de '
                        'la normalidad. Esfinter esofágico superior levemente '
                        'hipotenso con buena función.'
    },
    {
        'file': 'files/emedicaltest1@gmail.com/Clinic Report.docx',
        'conclusions': 'probable angioma hepático. Diverticulosis en '
                        'marco cólico. Resto en el informe'
    }
]

RECORD_FILES = [
    {
        'file': 'files/emedicaltest1@gmail.com/Clinic Report.docx',
        'conclusions': 'Esfinter esofágico inferior normotenso, asimétrico con '
                        'disfunción por relajaciones ausentes. Motilidad de '
                        'cuerpo esofágico con peristalsis conservada dentro de '
                        'la normalidad. Esfinter esofágico superior levemente '
                        'hipotenso con buena función.'
    },
    {
        'file': 'files/emedicaltest1@gmail.com/UAT MANOMETRIA PRUEBA_CbVJXds.docx',
        'conclusions': 'probable angioma hepático. Diverticulosis en '
                        'marco cólico. Resto en el informe'
    }
]