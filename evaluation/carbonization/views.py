from django.shortcuts import render,redirect
from django.contrib import messages
from ad_min.models import carbon,fibre
from django.core.mail import send_mail

# Create your views here.

#HOME

def car_home(request):
    return render(request,"carbonization/car_home.html")

# carbonization register and login:


def car_register(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        department = request.POST.get('department')
        print(f"Name: {name}, Email: {email}, Phone: {phone}, Department: {department}")
        carbon(name=name,email=email,phone=phone,department=department).save()
        messages.success(request, f'carbonization Registration Successful, Kindly get the approval from admin for login credentials.')
        return redirect('/')
    return render(request,'carbonization/reg_log.html')



def car_login(request):
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
                    messages.info(request, f"{project_id} :: carbonization Login Successful")
                    return redirect("/car_home/")
                else:
                    messages.info(request, "No fibre data found.") 
                    return redirect("/car_home/")
            else:
                messages.info(request, "Wrong Credentials")
                return render(request, 'carbonization/reg_log.html')
        except carbon.DoesNotExist:
            # Handle case where the user with the provided credentials does not exist
            messages.info(request, "Wrong Credentials")
            return render(request, 'carbonization/reg_log.html')

    return render(request, 'carbonization/reg_log.html')





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
def form_final_report(request):
    data = fibre.objects.all()
    cyber = Cybernetics()

    if data.exists() and data[0].car_decryption_key:
        try:
            key_bytes = normalize_key(data[0].car_decryption_key)
        except ValueError as e:
            messages.error(request, f"Stored key invalid: {e}")
            key_bytes = get_random_bytes(16)
    else:
        key_bytes = get_random_bytes(16)

    encoded_key = base64.b64encode(key_bytes).decode('utf-8')

    for item in data:
        e_pan_powder = encrypt_data(str(item.pan_powder) if item.pan_powder else '0', key_bytes)
        e_dmf_solvent = encrypt_data(str(item.dmf_solvent) if item.dmf_solvent else '0', key_bytes)
        e_additives = encrypt_data(str(item.additives) if item.additives else '0', key_bytes)

        cyber.log_operation('pan_powder', e_pan_powder)
        cyber.log_operation('dmf_solvent', e_dmf_solvent)
        cyber.log_operation('additives', e_additives)

        item.encrypted_pan_powder = e_pan_powder
        item.encrypted_dmf_solvent = e_dmf_solvent
        item.encrypted_additives = e_additives
        item.car_decryption_key = encoded_key
        item.save()

    return render(request, 'carbonization/form_final_report.html', {'data': data})

# Generate/send key
def getkey_car(request, project_id):
    data = fibre.objects.get(project_id=project_id)

    if data.car_decryption_key:
        encoded_key = data.car_decryption_key
    else:
        key_bytes = get_random_bytes(16)
        encoded_key = base64.b64encode(key_bytes).decode('utf-8')
        data.car_decryption_key = encoded_key
    data.car_get_key = True
    data.save()

    send_mail(
        f'Carbonization: Decryption key',
        f'Hi,\nYour Decryption key for Decrypting "{data.project_id}" Record is:\n\n{encoded_key}\n\nPlease use the provided key to decrypt the records.\n\nThank You',
        'anvi.aadiv@gmail.com',
        ['udayakumartv4@gmail.com'],
        fail_silently=False,
    )

    messages.info(request, f"Decryption Key sent to {data.project_id} Successfully.")
    return redirect('/form_final_report/')

# Decrypt view
def decrypt_data_car(request, project_id):
    d = fibre.objects.get(project_id=project_id)
    try:
            
            d.car_decrypt = True
            d.save()
            messages.info(request, f'{d.project_id}: Decryption Successful')
    except Exception as e:
            messages.error(request, f'Decryption error: {e}')

    return redirect('/form_final_report/')






# car_scanning

def car_scan(request):
    data = fibre.objects.all()
    return render(request,"carbonization/car_scan.html",{'data': data})


def car_calculation(request, project_id):
    fibre_object = fibre.objects.get(project_id=project_id)

    # Get the fiber type and quantity
    fibre_type = fibre_object.fibre_type
    quantity_kg = float(fibre_object.quantity_of_fibre)  # Ensure numeric

    # Carbonization parameters (Temp, Duration per kg, Energy rate, Argon rate)
    params = {
        "PAN-based Carbon Fiber": {"temp": 1500, "duration": 2, "energy": 3.5, "argon": 0.8},
        "Pitch-based Carbon Fiber": {"temp": 1400, "duration": 2.5, "energy": 3.8, "argon": 0.9},
        "Rayon-based Carbon Fiber": {"temp": 1200, "duration": 3, "energy": 4.0, "argon": 1.0},
    }

    # Get parameters for selected fiber type
    if fibre_type in params:
        temp = params[fibre_type]["temp"]
        duration_per_kg = params[fibre_type]["duration"]
        energy_rate = params[fibre_type]["energy"]
        argon_rate = params[fibre_type]["argon"]

        # Calculate
        heating_time = quantity_kg * duration_per_kg
        energy_use = heating_time * energy_rate
        argon_gas = heating_time * argon_rate

        # Save results
        fibre_object.heating_time = round(heating_time, 2)
        fibre_object.energy_use = round(energy_use, 2)
        fibre_object.argon_gas = round(argon_gas, 2)
        fibre_object.status = "Carbonization Done"
        fibre_object.car_scanned = True
        fibre_object.save()

        messages.info(request, f"{project_id} :: Carbonization Processed Successfully")
    else:
        messages.error(request, "Invalid fiber type selected.")

    return redirect("/car_scan/")





# car file

def car_file(request):
    data=fibre.objects.filter(car_scanned=True)
    return render(request,"carbonization/car_file.html",{'data':data})

# Logout

def car_logout(request):
    messages.info(request, 'carbonization Logout successful')
    return redirect('/')