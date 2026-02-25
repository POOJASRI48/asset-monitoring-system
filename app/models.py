from django.db import models



# Create your models here.
class Register(models.Model):
    user=models.CharField(max_length=50)
    email=models.EmailField()
    mobno=models.IntegerField()
    postion=models.CharField(max_length=50)
    staffid=models.CharField(max_length=50)
    pasw=models.CharField(max_length=50)

    def __str__(self):
        return self.user

class Employee(models.Model):
    empname=models.CharField(max_length=50)
    empemail=models.CharField(max_length=50)
    empdob=models.DateField()
    empmbno=models.IntegerField()
    empage=models.IntegerField()
    empid=models.CharField(max_length=50)
    emppos=models.CharField(max_length=50)
    empjndt=models.DateField()
    empexp=models.CharField(max_length=10)

    def __str__(self):
        return self.empname

class Com(models.Model):
    comname=models.CharField(max_length=50)
    os=models.CharField(max_length=50)
    hdd=models.CharField(max_length=50)
    ram=models.CharField(max_length=50)
    cpnm=models.CharField(max_length=50)
    cpsn=models.CharField(max_length=50)
    monname=models.CharField(max_length=50)
    mnsn=models.CharField(max_length=50)
    prcl=models.CharField(max_length=50)
    grcname=models.CharField(max_length=50)
    gcs=models.CharField(max_length=50)
    kyname=models.CharField(max_length=50)
    msname=models.CharField(max_length=50)

    def __str__(self):
        return self.comname


class Lap(models.Model):
    lapname=models.CharField(max_length=50)
    los=models.CharField(max_length=50)
    lhdd=models.CharField(max_length=50)
    lram=models.CharField(max_length=50)
    lcm=models.CharField(max_length=50)
    lsn=models.CharField(max_length=50)
    prcl=models.CharField(max_length=50)
    grcname=models.CharField(max_length=50)
    gcs=models.CharField(max_length=50)
    canv=models.CharField(max_length=50)

    def __str__(self):
        return self.lapname

class Otheracc(models.Model):
    keyboard=models.CharField(max_length=50)
    mouse=models.CharField(max_length=50)
    other=models.CharField(max_length=100)

class Assest(models.Model):
    empls=models.CharField(max_length=50)
    systy=models.CharField(max_length=50)
    gdt=models.DateField()
    rdt=models.DateField()
    usage_hours = models.IntegerField(default=0)  # NEW FIELD
    # ↓↓↓ new fields for depreciation ↓↓↓
    purchase_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    salvage_value  = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    useful_life_years = models.PositiveIntegerField(default=3)

    accumulated_depreciation = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    net_book_value = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    last_depreciation_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.empls} - {self.systy}"

class Returncom(models.Model):
    empname=models.CharField(max_length=50)
    comname = models.CharField(max_length=50)
    os = models.CharField(max_length=50)
    hdd = models.CharField(max_length=50)
    ram = models.CharField(max_length=50)
    cpnm = models.CharField(max_length=50)
    cpsn = models.CharField(max_length=50)
    monname = models.CharField(max_length=50)
    mnsn = models.CharField(max_length=50)
    prcl = models.CharField(max_length=50)
    grcname = models.CharField(max_length=50)
    gcs = models.CharField(max_length=50)
    kyname = models.CharField(max_length=50)
    msname = models.CharField(max_length=50)

class returnlap(models.Model):
    empname = models.CharField(max_length=50)
    lapname = models.CharField(max_length=50)
    los = models.CharField(max_length=50)
    lhdd = models.CharField(max_length=50)
    lram = models.CharField(max_length=50)
    lcm = models.CharField(max_length=50)
    lsn = models.CharField(max_length=50)
    prcl = models.CharField(max_length=50)
    grcname = models.CharField(max_length=50)
    gcs = models.CharField(max_length=50)
    canv = models.CharField(max_length=50)

class retOtheracc(models.Model):
    empname = models.CharField(max_length=50)
    keyboard=models.CharField(max_length=50)
    mouse=models.CharField(max_length=50)
    other=models.CharField(max_length=100)

class reass(models.Model):
    empls=models.CharField(max_length=50)
    otls=models.CharField(max_length=50)
    gdt=models.DateField()
    rdt=models.DateField()

class chart(models.Model):
    assest=models.IntegerField(null=True)
    com=models.IntegerField(null=True)
    retcom=models.IntegerField(null=True)
    lap=models.IntegerField(null=True)
    retlap=models.IntegerField(null=True)
    other=models.IntegerField(null=True)
    retother=models.IntegerField(null=True)

class todolist(models.Model):
    todo=models.TextField()
