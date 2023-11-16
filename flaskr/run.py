# encoding: utf-8

from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from models import Hospital, Patient, Doctor, sparql
from routes.blueprint import blueprint
from db import db, app
import json
import uuid
import os


def create_app():
    db.init_app(app)  # Initializing the database
    return app

app = create_app()  # Creating the app
app.register_blueprint(blueprint, url_prefix='/')


################### Espacio para seeders ############################

# método que comprueba si estamos conectados a la base de datos y si hay hospitales, si no los añade de seeders/seeders.json
def seeder(app):
    print('#### METODO SEEDER ####')
    with app.app_context():
        db_name = db.get_db().name
        if(db_name):
            print('#### Database exist with name: '+ db_name +' ####')
        else:
            print('#### Database not exist ####')


    all_hospitals = Hospital.objects.all()

    if (len(all_hospitals) <= 0):
        print('#### Collections are empty ####')
        print('#### Adding some entries... ####')
        with open(os.path.join(os.path.dirname(__file__), 'seeders/seeders.json'), 'r', encoding='utf-8') as f:
            print('#### seeders.json file opened... ---####')
            data = json.load(f)

        for hospital in data['hospitals']:
            new_hospital = Hospital(**hospital)
            new_hospital.save()

        doctors = {}
        for doctor in data['doctors']:
            new_doctor = Doctor(id=doctor['id'], name=doctor['name'], surname=doctor['surname'], speciality=doctor['speciality'])
            new_doctor.save()
            doctors[doctor['id']] = new_doctor

        for patient in data['patients']:
            new_patient = Patient(id=patient['id'], name=patient['name'], surname=patient['surname'], dni=patient['dni'])
            hospital = Hospital.objects.get(id=patient['hospital_id'])
            new_patient.hospital = hospital
            if (patient['id'] == '3a268172-6c5c-4d9b-8964-8b9a1e531af5'):
                new_patient.doctors.append(doctors['014bd297-0a3d-4a17-b207-cff187690045'])
                new_patient.doctors.append(doctors['9bb2e300-fa15-4063-a291-13f7199ddb52'])
            elif (patient['id'] == '088d58e2-7691-47b6-a322-eeffcadc9054'):
                new_patient.doctors.append(doctors['a0f54d52-5ccb-4e50-adca-5ea0064262fd'])
            elif (patient['id'] == '8ec8c43b-f7e1-43e4-b70f-6d5a9799a86a'):
                new_patient.doctors.append(doctors['1497d1be-577a-41ad-b129-45271e113cc0'])
            elif (patient['id'] == '923ec756-87b7-4743-808b-795a04b6dd21'):
                new_patient.doctors.append(doctors['9bb2e300-fa15-4063-a291-13f7199ddb52'])
            new_patient.save()
        print('#### Finished! ####')
    else:
        print('#### Database already seeded ####')

seeder(app)

if __name__ == '__main__':  # Running the app
    app.run(host='localhost', port=5002, debug=True)

