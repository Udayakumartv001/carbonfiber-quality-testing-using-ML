# Create your models here.
from django.db import models

 

class carbon(models.Model):

    # all modules register and login

    name = models.CharField(max_length=100, null=True)
    email = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=100, null=True)
    department= models.CharField(max_length=100, null=True)


    #user_id and mail password generation

    emp_id= models.CharField(max_length=100, null=True)
    password=models.PositiveBigIntegerField(null=True)



    # admin approve and reject

    approve = models.BooleanField(default=False)
    reject = models.BooleanField(default=False)

    # login and logout

    login = models.BooleanField(default=False)
    logout = models.BooleanField(default=False)




class fibre(models.Model):

    # project_id........................................................

    project_id = models.CharField(max_length=100, null=True)

    # admin requirements and datas before ecryption.......................

    fibre_type = models.CharField(max_length=100, null=True)
    quantity_of_fibre = models.CharField(max_length=100, null=True)
    application = models.CharField(max_length=100, null=True)
    color_of_fibre = models.CharField(max_length=100, null=True)
    

    # Module 1 - formulation

    # admin requirements and datas after ecryption

    encrypted_fibre_type= models.CharField(max_length=200, null=True)
    encrypted_quantity_of_fibre = models.CharField(max_length=200, null=True)
    encrypted_application = models.CharField(max_length=200, null=True)
    encrypted_color_of_fibre = models.CharField(max_length=200, null=True)


    # encryption key

    form_decryption_key = models.CharField(max_length=200,null=True)

    # # get key and decrypt  

    form_get_key = models.BooleanField(default=False,null=True)
    form_decrypt = models.BooleanField(default=False,null=True)

    # admin requirements and datas after decryption

    decrypted_fibre_type= models.CharField(max_length=200, null=True)
    decrypted_quantity_of_fibre = models.CharField(max_length=200, null=True)
    decrypted_application = models.CharField(max_length=200, null=True)
    decrypted_color_of_fibre = models.CharField(max_length=200, null=True)


    # formulation - Scanning

    pan_powder = models.CharField(max_length=100,null=True)
    dmf_solvent = models.CharField(max_length=100, null=True)
    additives = models.CharField(max_length=100,null=True)


    # Module 2 - carbonization ........................

    encrypted_pan_powder = models.CharField(max_length=256, null=True)
    encrypted_dmf_solvent = models.CharField(max_length=256, null=True)
    encrypted_additives = models.CharField(max_length=256, null=True)

    
  
    # encryption key

    car_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    car_get_key = models.BooleanField(default=False, null=True)
    car_decrypt = models.BooleanField(default=False, null=True)

    # decryption 

    decrypted_pan_powder = models.CharField(max_length=100, null=True)
    decrypted_dmf_solvent = models.CharField(max_length=100, null=True)
    decrypted_additives = models.CharField(max_length=100, null=True)


    # carbonization - Scanning

    heating_time = models.FloatField(null=True)
    energy_use = models.FloatField(null=True)   # <-- changed
    argon_gas = models.FloatField(null=True)    # <-- changed




    # Module - 3 - activation

    encrypted_heating_time = models.TextField(null=True)
    encrypted_energy_use = models.TextField(null=True)
    encrypted_argon_gas = models.TextField(null=True)



    # encryption key

    act_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    act_get_key = models.BooleanField(default=False, null=True)
    act_decrypt = models.BooleanField(default=False, null=True)

    # decryption

    decrypted_heating_time = models.CharField(max_length=100, null=True)
    decrypted_energy_use = models.CharField(max_length=100, null=True)
    decrypted_argon_gas = models.CharField(max_length=100, null=True)



    # activation- Scanning

    oxidation = models.CharField(max_length=100, null=True)
    sizing = models.CharField(max_length=100, null=True)
    water = models.CharField(max_length=100, null=True)
    drying = models.CharField(max_length=100, null=True)
    
    



    # Module - 4 - evaluation

    

    encrypted_oxidation = models.TextField(null=True)
    encrypted_sizing = models.TextField(null=True)
    encrypted_water = models.TextField(null=True)
    encrypted_drying = models.TextField(null=True)


    # encryption key

    eval_decryption_key = models.CharField(max_length=64, null=True)

    # get key and decrypt

    eval_get_key = models.BooleanField(default=False, null=True)
    eval_decrypt = models.BooleanField(default=False, null=True)


    # decryption

    decrypted_oxidation = models.TextField(null=True)
    decrypted_sizing = models.TextField(null=True)
    decrypted_water = models.TextField(null=True)
    decrypted_drying = models.TextField(null=True)

    # evaluation - Scanning

    strength = models.FloatField(null=True, blank=True)
    flexibilty = models.FloatField(null=True, blank=True)
    diameter_accuracy = models.IntegerField(null=True, blank=True)
    final = models.FloatField(null=True, blank=True)


    # all modules scanned name

    form_scanned = models.BooleanField(default=False)
    car_scanned =  models.BooleanField(default=False)
    act_scanned = models.BooleanField(default=False)
    eval_scanned = models.BooleanField(default=False)
    
    

    # all modules status

    status = models.CharField(default="Pending", null=True , max_length=100)

    # # reports

    report = models.BooleanField(default=False)
    rep = models.BooleanField(default=False)

    f_report = models.FileField(null=True, upload_to="Final_Report/")