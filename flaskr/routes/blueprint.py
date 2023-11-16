from flask import Blueprint, request 
from controllers.patientController import *

blueprint = Blueprint('blueprint', __name__, template_folder='templates')

@blueprint.route('/', methods=['GET'])
def index():
    return redirect("/hospitals")

@blueprint.route('/home', methods=['GET'])
def show_home():
    return redirect("/hospitals")

@blueprint.route('/hospitals', methods=['GET'])
def route_hospitals():
	return render_template("index_hospitals.html",hospitals=show_hospitals())

@blueprint.route('/hospitals/filterByCity', methods=['GET','POST'])
def route_filterHospitalsByCity():
    city = request.form['city']
    return render_template("index_hospitals.html",hospitals=filterHospitalsByCity(city))

@blueprint.route('/hospitals/<hospital_id>/patients', methods=['GET'])
def route_list_hospital_patients(hospital_id):
    patients = list_hospital_patients(hospital_id)
    return render_template("index_patients.html",hospital=hospital_id, patients=patients)

@blueprint.route('/hospitals/<hospital_id>/show', methods=['GET','POST'])
def route_show_hospital(hospital_id):
	result = show_hospital(hospital_id)
	hospital_info=result[0]
	hospital_iri=result[1]
	return render_template("show_hospital.html",
                           iri=hospital_iri,
                           hospital_info=hospital_info)

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>', methods=['GET','POST'])
def route_read_patient(hospital_id,patient_id):
    patient = read_patient(patient_id)
    return render_template("show.html",hospital=hospital_id, patient= patient)

@blueprint.route('/hospitals/<hospital_id>/patients/new', methods=['GET','POST'])
def show_create(hospital_id):
    return render_template('new.html',hospital=hospital_id)

@blueprint.route('/hospitals/<hospital_id>/patients', methods=['GET','POST'])
def route_create_patient(hospital_id):
	body = {
		#"id":request.form["id"],
		"name":request.form["name"],
		"surname":request.form["surname"],
		"dni":request.form["dni"]

	}
	create_patient(hospital_id,body)
	return redirect('/hospitals/'+hospital_id+'/patients')

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>/edit', methods=['GET'])
def route_create_edited_patient(hospital_id,patient_id):
    patient = create_edited_patient(patient_id)
    return render_template("edit.html",hospital=hospital_id, patient= patient)

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>/updated', methods=['GET','POST'])
def route_update_patient(hospital_id,patient_id):
	body = {
		#"id":request.form["id"],
		"name":request.form["name"],
		"surname":request.form["surname"],
		"dni":request.form["dni"]

	}
	patient=update_patient(patient_id,body)
	return render_template("show.html",hospital=hospital_id, patient= patient)

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>/delete', methods=['GET','POST'])
def route_delete_patient(hospital_id,patient_id):
    delete_patient(patient_id)
    return redirect('/hospitals/'+hospital_id+'/patients?patientDeleted=true')

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>/assign_doctor/assigned', methods=['GET','POST','PUT'])
def route_assign_doctor(hospital_id,patient_id):
	doctor_id = request.form['doctor']
	patient=assign_doctor(patient_id,doctor_id)
	return render_template("show.html",hospital=hospital_id, patient= patient)

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>/assign_doctor', methods=['GET'])
def pass_doctor(hospital_id,patient_id):
    return render_template("assign_doctor.html",hospital=hospital_id, patient= patient_id)

@blueprint.route('/hospitals/<hospital_id>/patients/<patient_id>/show_doctors', methods=['GET','POST'])
def route_show_patient_doctors(hospital_id,patient_id):
    doctors = show_patient_doctors(patient_id)
    return render_template("show_doctors.html",doctors=doctors, patient= patient_id)
