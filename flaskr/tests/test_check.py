import pytest
from flask import Flask
from datetime import datetime
import controllers.patientController as controller
from models import Patient, Hospital, Doctor, sparql
#from helper import db, app
from flask_mongoengine import MongoEngine
from run import seeder

score = 0
# Metodo para pre-tests, se ejecuta el inicio de cada test
# Crea la bbdd db_test la llena con los seeders y luego de ejeuctar el test borra la bbdd
@pytest.fixture(autouse=True)
def run_before_and_after_tests(tmpdir):
    """Fixture to execute asserts before and after a test is run"""
    # Setup: fill with any logic you want
    from flask_mongoengine import MongoEngine
    app = Flask("test_data")
    db = MongoEngine()
    db.disconnect(alias='default')
    app.config["MONGODB_SETTINGS"] = {
            "db": "db_test",
            "host": "mongodb://localhost/db_test",
            "port": 27017,
            "alias": "default",
    }
    db.init_app(app)
    db_name = db.get_db().name
    seeder(app)


    yield # this is where the testing happens

    # Teardown : fill with any logic you want
    db_collections_size = len(db.get_db().list_collection_names())
    assert db_name == "db_test"
    assert db_collections_size is 3

    # Confirmo con MongoEngine que la bbdd ha sido borrada    
    from mongoengine import connect
    db.disconnect(alias='default')
    db = connect(db_name)
    db.drop_database(db_name)
    db_collections_size= len(db.get_database(db_name).list_collection_names())
    assert db_collections_size is 0

def test_list_hospitals():
    all_hospitals = controller.show_hospitals()
    assert len(all_hospitals) == 5
    assert all_hospitals[0].id == "9f8a5c90-cf1a-4ca3-9dea-c6a94174ae69"
    assert all_hospitals[1].id == "b04fde75-59d8-457f-82b9-c25f2c64abfc"
    assert all_hospitals[2].id == "c5d7cbea-55a4-4809-9969-82b148032a0e"
    assert all_hospitals[3].id == "db6da10f-4ec4-468a-ad46-36a407480fa7"
    assert all_hospitals[4].id == "d2dc1154-1329-4e56-a5c3-8e88b63f3c4a"
    global score; score += 0.5 # Increase score

def test_filterHospitalsByCity():
    list_hospitals = controller.filterHospitalsByCity("Madrid")
    assert len(list_hospitals) == 2
    assert list_hospitals[0].id == "9f8a5c90-cf1a-4ca3-9dea-c6a94174ae69"
    assert list_hospitals[1].id == "c5d7cbea-55a4-4809-9969-82b148032a0e"
    global score; score += 0.5 # Increase score

def test_list_hospital_patients():
    hospital_id = "9f8a5c90-cf1a-4ca3-9dea-c6a94174ae69"
    list_patients = controller.list_hospital_patients(hospital_id)
    assert len(list_patients) == 3
    assert list_patients[0].id == "923ec756-87b7-4743-808b-795a04b6dd21"
    assert list_patients[1].id == "3a268172-6c5c-4d9b-8964-8b9a1e531af5"
    assert list_patients[2].id == "508fb53c-c212-453f-ab17-cf56049f5a2c"
    global score; score += 1 # Increase score

# def test_show_hospital():
#     hospital_id = "9f8a5c90-cf1a-4ca3-9dea-c6a94174ae69"
#     result=controller.show_hospital(hospital_id)
#     assert result is not None
#     global score; score += 2 # Increase score

def test_read_patient():
    patient_id="3a268172-6c5c-4d9b-8964-8b9a1e531af5"
    patient = controller.read_patient(patient_id)
    assert patient.id == patient_id
    assert patient.name == "Juan"
    assert patient.surname == "Rodriguez"
    assert patient.dni == "123123"
    global score; score += 1 # Increase score

def test_create_patient():
    hospital_id = "9f8a5c90-cf1a-4ca3-9dea-c6a94174ae69"
    patient_data = {
       "name":"John",
       "surname": "Doe",
       "dni": "987654",
    }
    print(patient_data)
    created_patient = controller.create_patient(hospital_id,patient_data)
    assert created_patient.name == "John"
    assert created_patient.surname == "Doe"
    assert created_patient.dni == "987654"
    global score; score += 1.5 # Increase score


def test_update_patient():

    patient_data = {
       "id":"3a268172-6c5c-4d9b-8964-8b9a1e531af5",
       "name":"John",
       "surname": "Doe",
       "dni": "987654",
    }
    updated_patient=controller.update_patient(patient_data["id"],patient_data)
    assert updated_patient.id == patient_data["id"]
    assert updated_patient.name == patient_data["name"]
    assert updated_patient.surname == patient_data["surname"]
    assert updated_patient.dni == patient_data["dni"]
    global score; score += 1.5 # Increase score

def test_delete_patient():
    patient_id = "3a268172-6c5c-4d9b-8964-8b9a1e531af5"
    patient = controller.read_patient(patient_id)
    controller.delete_patient(patient_id)   
    assert patient is not None
    global score; score += 0.5 # Increase score

def test_assign_doctor():
    patient_id = "3a268172-6c5c-4d9b-8964-8b9a1e531af5"
    doctor = {
      "id": "014bd297-0a3d-4a17-b207-cff187690045",
      "name": "Dr Pedro",
      "surname": "Garcia",
      "speciality": "Medico de cabecera"
    }
    patient=controller.assign_doctor(patient_id,doctor["id"])
    assert patient.doctors[0].id== doctor["id"]
    assert patient.doctors[0].name== doctor["name"]
    assert patient.doctors[0].surname== doctor["surname"]
    assert patient.doctors[0].speciality== doctor["speciality"]
    global score; score += 2 # Increase score

def test_show_patient_doctors():
    patient_id = "3a268172-6c5c-4d9b-8964-8b9a1e531af5"
    doctors = controller.show_patient_doctors(patient_id)
    ("Test suite for show_patient_doctors function")
    assert len(doctors) == 2
    assert doctors[0].name == "Dr Pedro"
    assert doctors[1].name == "Dra Patricia"
    global score; score += 1 # Increase score

def test_show_score(capsys):
    with capsys.disabled():
        print('\n\nLa nota orientativa obtenida en la práctica es:')
        print('\n\n-----------------')
        print('| Score: {} /9.5|'.format(score))
        print('-----------------\n')