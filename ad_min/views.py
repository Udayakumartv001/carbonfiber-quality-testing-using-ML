from django.contrib import messages
from django.shortcuts import render,redirect
from ad_min.models import carbon,fibre
from django.core.mail import send_mail

# Create your views here.

# homepage.......

def home(request):
    return render(request,'homepage/homepage.html')

# # admin login & logout

def adminlogin(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        if email == "admin@gmail.com" and password == "admin":
            messages.info(request,"Admin Login Successful")
            return redirect("/adminhome/")
        else:
            messages.error(request,"wrong credentials")
            return render(request, 'ad_min/admin_login.html')

    else:
        return render(request, 'ad_min/admin_login.html')


def adminlogout(request):
    messages.info(request, 'Admin Logout Successful')
    return redirect('/')

# admin home...............

def adminhome(request):
    return render(request, 'ad_min/admin_home.html')

# admin requirements

def requirements(request):
    if request.method == 'POST':
        fibre_type = request.POST.get('fibre_type')
        quantity_of_fibre = request.POST.get('quantity_of_fibre')
        application = request.POST.get('application')
        color_of_fibre = request.POST.get('color_of_fibre')
        
        
        p=random.randint(1000,9999)
        
        project_id=f"Project:{p}"

        fibre(fibre_type=fibre_type,
                     quantity_of_fibre=quantity_of_fibre, 
                     application=application,
                     color_of_fibre=color_of_fibre,
                     project_id=project_id).save()
        
        messages.info(request, f"{project_id} :: Requirements Uploaded successfully.")
        
        return redirect('/adminhome/')  # Redirect to chief home after successful submission
    
    return render(request, 'ad_min/requirements.html')





# #  approve & reject..........

import random
def approve(request,id):
    data=carbon.objects.get(id=id)
    password=random.randint(1000,9999)
    print(password)
    data.password=password
    data.emp_id=f"SG:{password}"
    data.save()

    send_mail(
        '{0}:Username and Password'.format(data.department),
        'Hello {0},\n Your {1} profile has been Approved.\n Your Username is "{2}" and Password is "{3}".\n Make sure you use this Username and Password while your logging in to the portal of {1}.\n Thank You '.format(
            data.name,data.department, data.email,data.password),
        'anvi.aadiv@gmail.com',[data.email],  # the mail which is from user registration.
        fail_silently=False,
    )

    data.approve=True
    data.reject=False
    data.save()
    messages.info(request,f"{data.emp_id} : {data.department} Approval Successful,Kindly check the registered email for the login credentials.")
    return redirect("/adminhome/")



def reject(request,id):
    data = carbon.objects.get(id=id)
    data.approve=False
    data.reject=True
    data.save()

    subject = 'Client Rejection'
    plain_message = f"Hi {data.name},\nYour registration was rejected due to some reasons.try this later!"
    send_mail(subject, plain_message,'anvi.aadiv@gmail.com',[data.email], fail_silently=False)

    # data.delete()
    messages.info(request, "Rejection Mail Sent to Client")
    return redirect("/adminhome/")


# approve & reject..........

def formapprove(request):
    data = carbon.objects.filter(department='FORMULATION')
    return render(request, 'ad_min/form_approve.html',{'data': data})

def carapprove(request):
    data = carbon.objects.filter(department='CARBONIZATION')
    return render(request, 'ad_min/car_approve.html',{'data': data})

def actapprove(request):
    data = carbon.objects.filter(department='ACTIVATION')
    return render(request, 'ad_min/act_approve.html',{'data': data})

def evalapprove(request):
    data = carbon.objects.filter(department='EVALUATION')
    return render(request, 'ad_min/eval_approve.html',{'data': data})


# manage reports..........

def formmanage(request):
    data = fibre.objects.all()
    return render(request, 'ad_min/form_manage.html',{'data': data})

def carmanage(request):
    data = fibre.objects.all()
    return render(request, 'ad_min/car_manage.html',{'data': data})

def actmanage(request):
    data = fibre.objects.all()
    return render(request, 'ad_min/act_manage.html',{'data': data})

def evalmanage(request):
    data = fibre.objects.all()
    return render(request, 'ad_min/eval_manage.html',{'data': data})



# MANAGE STATUS

def managestatus(request):
    data = fibre.objects.all()
    return render(request, "ad_min/manage_status.html", {'data': data})

# FINAL REPORT

from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle
from django.http import HttpResponse
from django.core.files.base import ContentFile
from django.shortcuts import redirect
from django.contrib import messages


def final_report(request, project_id):
    data = fibre.objects.get(project_id=project_id)

    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)

    # Add page number function
    def add_page_number(c):
        c.setFont("Helvetica", 9)
        c.setFillColor(colors.grey)
        page_num_text = f"Page {c.getPageNumber()}"
        c.drawRightString(570, 20, page_num_text)

    def draw_title_and_project_id(c):
        # Draw background bar (taller so it covers 2 lines)
        c.setFillColor(colors.HexColor("#004d40"))  # deep teal
        c.rect(0, 790, 595, 50, fill=True, stroke=False)

        # Title split into 2 lines manually
        c.setFont("Helvetica-Bold", 13)
        c.setFillColor(colors.white)
        line1 = "ADVANCED PRECURSOR PREPARATION AND CARBONIZATION"
        line2 = "FOR PERFORMANCE-OPTIMIZED FIBERS"

        # Centered text
        c.drawCentredString(c._pagesize[0] / 2, 815, line1)
        c.drawCentredString(c._pagesize[0] / 2, 800, line2)

        # Project ID
        c.setFillColor(colors.black)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, 770, f"PROJECT ID: {data.project_id}")

        # Thin line
        c.setStrokeColor(colors.grey)
        c.setLineWidth(0.5)
        c.line(50, 765, 550, 765)

    def draw_section(c, title, section_data, start_y):
        # Section title with colored background
        c.setFillColor(colors.HexColor("#455A64"))  # blue-grey
        c.rect(45, start_y - 5, 510, 20, fill=True, stroke=False)
        c.setFillColor(colors.white)
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, start_y, title)
        start_y -= 30

        # Table with styled header and alternate row colors
        table_data = [["Parameter", "Value"]] + [[item[0], item[1]] for item in section_data]
        table = Table(table_data, colWidths=[250, 250])
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#90CAF9")),  # sky blue header
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.black),
            ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, -1), 10),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 6),
            ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor("#E3F2FD")]),
            ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
        ]))
        table.wrapOn(c, 500, 500)
        table.drawOn(c, 50, start_y - len(table_data) * 20)

        return start_y - len(table_data) * 20 - 40

    # Draw Title + Project ID ONLY on page 1
    draw_title_and_project_id(c)

    sections = [
        ("FORMULATION", [
            ["PAN POWDER (kg)", f"{data.pan_powder}"],
            ["DMF SOLVENT (kg)", f"{data.dmf_solvent}"],
            ["ADDITIVES (kg)", f"{data.additives}"],
        ]),
        ("CARBONIZATION", [
            ["HEATING TIME (hours)", f"{data.heating_time}"],
            ["ENERGY USE (kWh)", f"{data.energy_use}"],
            ["ARGON GAS (m³)", f"{data.argon_gas}"],
        ]),
        ("ACTIVATION", [
            ["OXIDATION (kg)", f"{data.oxidation}"],
            ["SIZING (kg)", f"{data.sizing}"],
            ["WATER (liters)", f"{data.water}"],
            ["DRYING (hrs)", f"{data.drying}"],
        ]),
        ("EVALUATION", [
            ["STRENGTH (%)", f"{data.strength}"],
            ["FLEXIBILITY (%)", f"{data.flexibilty}"],
            ["DIAMETER ACCURACY (%)", f"{data.diameter_accuracy}"],
            ["FINAL SCORE (%)", f"{data.final}"],
        ])
    ]

    y_position = 740
    for section_title, section_data in sections:
        y_position = draw_section(c, section_title, section_data, y_position)
        if y_position < 150:
            add_page_number(c)
            c.showPage()         # only when needed for next content
            y_position = 740

    # ✅ Final page number only, no extra showPage
    add_page_number(c)
    c.save()


    pdf_data = buffer.getvalue()
    buffer.close()

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="MARINEROOT_REPORT_{data.project_id}.pdf"'
    response.write(pdf_data)

    data.f_report.save(f"MARINEROOT_REPORT_{data.project_id}.pdf", ContentFile(pdf_data))
    data.rep = False
    data.report = True
    data.save()

    messages.success(request, f"{data.project_id}, Report Generated successfully")
    return redirect('/managestatus/')




