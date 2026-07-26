from django.shortcuts import render,redirect
from django.contrib import messages
from ad_min.models import carbon,fibre
from django.core.mail import send_mail

# Create your views here.

#HOME

def act_home(request):
    return render(request,"activation/act_home.html")

# activation register and login:


def act_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        print(f"Name: {name}, Email: {email}, Phone: {phone}, Department: {department}")
        carbon(name=name,email=email,phone=phone,department=department).save()
        messages.success(request, f'activation Registration Successful, Kindly get the approval from admin for login credentials.')
        return redirect('/')
    return render(request,'activation/reg_log.html')



def act_login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            # Try to retrieve the user with the given email and password
            user = carbon.objects.get(email=email, password=password)

            if user:
                # Set the login field to True (1) upon successful login
                user.login = True
                user.save()

                fibre_data = fibre.objects.filter().first()  # Use first() to avoid MultipleObjectsReturned

                if fibre_data:  # Check if fibre_data exists
                    project_id = fibre_data.project_id
                    messages.info(request, f"{project_id} :: activation Login Successful")
                    return redirect("/act_home/")
                else:
                    messages.info(request, "No fibre data found.") 
                    return redirect("/act_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, 'activation/reg_log.html')
        except carbon.DoesNotExist:
            # Handle case where the user with the provided credentials does not exist
            messages.info(request, "Wrong Credentials")
            return render(request, 'activation/reg_log.html')

    return render(request, 'activation/reg_log.html')





import json
import datetime
import hashlib
from django.shortcuts import render, redirect
import base64
from django.core.mail import send_mail
from django.contrib import messages
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad

# Cybernetics class (kept for logs)
class Cybernetics:
    def __init__(self):
        self.logs = []

    def log_operation(self, label, encrypted_value):
        self.logs.append({
            'timestamp': str(datetime.datetime.now()),
            'label': label,
            'encrypted_value': encrypted_value
        })

    def get_feedback(self):
        return f"Total encrypted fields processed: {len(self.logs)}"

# Helper: ensure we end up with raw key bytes of length 16/24/32
def normalize_key(maybe_key):
    if maybe_key is None:
        raise ValueError("No key provided")

    if isinstance(maybe_key, str):
        current = maybe_key.encode('utf-8')
    else:
        current = maybe_key

    if len(current) in (16, 24, 32):
        return current

    for _ in range(3):
        try:
            decoded = base64.b64decode(current)
        except Exception:
            break
        if len(decoded) in (16, 24, 32):
            return decoded
        current = decoded

    raise ValueError(f"Could not normalize key to 16/24/32 bytes. Current length: {len(current)}")

# Encrypt data using AES
def encrypt_data(plain_text, key_bytes):
    key = normalize_key(key_bytes)
    cipher = AES.new(key, AES.MODE_CBC)
    ct_bytes = cipher.encrypt(pad(plain_text.encode('utf-8'), AES.block_size))
    return base64.b64encode(cipher.iv + ct_bytes).decode('utf-8')

# Decrypt data using AES
def decrypt_data(encrypted_b64, key_bytes):
    key = normalize_key(key_bytes)
    raw = base64.b64decode(encrypted_b64)
    iv = raw[:AES.block_size]
    ct = raw[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CBC, iv)
    pt = unpad(cipher.decrypt(ct), AES.block_size)
    return pt.decode('utf-8')

# Admin encryption endpoint
def car_final_report(request):
    data = fibre.objects.all()
    cyber = Cybernetics()

    if data.exists() and data[0].act_decryption_key:
        try:
            key_bytes = normalize_key(data[0].act_decryption_key)
        except ValueError as e:
            messages.error(request, f"Stored key invalid: {e}")
            key_bytes = get_random_bytes(16)
    else:
        key_bytes = get_random_bytes(16)

    encoded_key = base64.b64encode(key_bytes).decode('utf-8')

    for item in data:
        e_heating_time = encrypt_data(str(item.heating_time) if item.heating_time else '0', key_bytes)
        e_energy_use = encrypt_data(str(item.energy_use) if item.energy_use else '0', key_bytes)
        e_argon_gas = encrypt_data(str(item.argon_gas) if item.argon_gas else '0', key_bytes)

        cyber.log_operation('heating_time', e_heating_time)
        cyber.log_operation('energy_use', e_energy_use)
        cyber.log_operation('argon_gas', e_argon_gas)

        item.encrypted_heating_time = e_heating_time
        item.encrypted_energy_use = e_energy_use
        item.encrypted_argon_gas = e_argon_gas
        item.act_decryption_key = encoded_key
        item.save()

    return render(request, 'activation/car_final_report.html', {'data': data})

# Generate/send key
def getkey_act(request, project_id):
    data = fibre.objects.get(project_id=project_id)

    if data.car_decryption_key:
        encoded_key = data.act_decryption_key
    else:
        key_bytes = get_random_bytes(16)
        encoded_key = base64.b64encode(key_bytes).decode('utf-8')
        data.act_decryption_key = encoded_key
    data.act_get_key = True
    data.save()

    send_mail(
        f'activation: Decryption key',
        f'Hi,\nYour Decryption key for Decrypting "{data.project_id}" Record is:\n\n{encoded_key}\n\nPlease use the provided key to decrypt the records.\n\nThank You',
        'anvi.aadiv@gmail.com',
        ['udayakumartv4@gmail.com'],
        fail_silently=False,
    )

    messages.info(request, f"Decryption Key sent to {data.project_id} Successfully.")
    return redirect('/car_final_report/')

# Decrypt view
def decrypt_data_act(request, project_id):
    d = fibre.objects.get(project_id=project_id)
    try:
            
            d.act_decrypt = True
            d.save()
            messages.info(request, f'{d.project_id}: Decryption Successful')
    except Exception as e:
            messages.error(request, f'Decryption error: {e}')

    return redirect('/car_final_report/')






# act_scanning

def act_scan(request):
    data = fibre.objects.all()
    return render(request,"activation/act_scan.html",{'data': data})


def act_calculation(request, project_id):
    fibre_object = fibre.objects.get(project_id=project_id)

    # Get fiber type and quantity (Q in kg) from database
    fibre_type = fibre_object.fibre_type  # Make sure this field exists
    try:
        quantity_kg = float(fibre_object.quantity_of_fibre)  # Q in kg
    except (ValueError, TypeError):
        messages.error(request, "Invalid quantity of fibre")
        return redirect("/act_scan/")

    # Coefficients for calculations (kg/kg or liters/kg)
    coefficients = {
        "PAN-based Carbon Fiber": {"oxidation": 0.015, "sizing": 0.005, "water": 0.5, "drying": 1.5},
        "Pitch-based Carbon Fiber": {"oxidation": 0.020, "sizing": 0.006, "water": 0.6, "drying": 1.6},
        "Rayon-based Carbon Fiber": {"oxidation": 0.018, "sizing": 0.007, "water": 0.7, "drying": 1.8},
    }

    if fibre_type not in coefficients:
        messages.error(request, f"Unknown fibre type: {fibre_type}")
        return redirect("/act_scan/")

    # Perform Module 4 calculations
    oxidation = quantity_kg * coefficients[fibre_type]["oxidation"]
    sizing = quantity_kg * coefficients[fibre_type]["sizing"]
    water = quantity_kg * coefficients[fibre_type]["water"]
    drying = quantity_kg * coefficients[fibre_type]["drying"]

    # Save calculated values (rounded to 3 decimals)
    fibre_object.oxidation = str(round(oxidation, 3))
    fibre_object.sizing = str(round(sizing, 3))
    fibre_object.water = str(round(water, 3))
    fibre_object.drying = str(round(drying, 3))

    fibre_object.act_scanned = True
    fibre_object.status = "activation Done"
    fibre_object.save()

    messages.info(request, f"{project_id} :: activation Processed Successfully")
    return redirect("/act_scan/")






# act file

def act_file(request):
    data=fibre.objects.filter(act_scanned=True)
    return render(request,"activation/act_file.html",{'data':data})

# Logout

def act_logout(request):
    messages.info(request, 'Activation Logout successful')
    return redirect('/')