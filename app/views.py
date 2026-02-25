from django.shortcuts import render, redirect, get_object_or_404
from django.forms.models import model_to_dict

from .models import *
import hashlib
import sweetify


# # Create your views here.
# def index(request):
#     l = Employee.objects.all()
#     p = len(l)
#     com = Com.objects.all()
#     cl = len(com)
#     lap = Lap.objects.all()
#     lp = len(lap)
#     ass=Assest.objects.all()
#     asss=len(ass)
#     po = reass.objects.all()
#     poo = len(po)
#     fass = asss + poo
#     asl = []
#     coml = []
#     retcoml = []
#     lapl=[]
#     retlapl=[]
#     otherl=[]
#     retotherl=[]
#     mo = chart.objects.all().filter()
#     for i in mo:
#         if i.assest != None:
#             asl.append(i.assest)
#         else:
#             asl.append(0)
#         if i.com != None:
#             coml.append(i.com)
#         else:
#             coml.append(0)
#         if i.retcom != None:
#             retcoml.append(i.retcom)
#         else:
#             retcoml.append(0)
#         if i.lap != None:
#             lapl.append(i.lap)
#         else:
#             lapl.append(0)
#         if i.retlap != None:
#             retlapl.append(i.retlap)
#         else:
#             retlapl.append(0)
#         if i.other != None:
#             otherl.append(i.other)
#         else:
#             otherl.append(0)
#         if i.retother != None:
#             retotherl.append(i.retother)
#         else:
#             retotherl.append(0)
#     to=todolist.objects.all()
#     if 'email' in request.session:
#         a = Register.objects.get(email=request.session['email'])
#         u = a.user
#         pos = a.postion
#         return render(request, 'index.html', {'user': u, 'emp': p, 'pos': pos, 'com': cl, 'lap': lp,'ass':fass,'asl':asl,'coml': coml,'retcoml': retcoml,'lapl': lapl, 'retlapl': retlapl,'otherl': otherl, 'retotherl': retotherl,'todo':to})
#     else:
#         return render(request, 'index.html', {'user': None, 'emp': p, 'pos': None, 'com': cl, 'lap': lp,'ass':asss, 'asl':asl,'coml': coml,'retcoml': retcoml,'lapl': lapl, 'retlapl': retlapl,'otherl': otherl, 'retotherl': retotherl})


from django.db.models import Avg  

def index(request):
    # Counts for dashboard
    p = Employee.objects.count()
    cl = Com.objects.count()
    lp = Lap.objects.count()
    asss = Assest.objects.count()
    poo = reass.objects.count()
    fass = asss + poo
    print(fass)

    # Lists for chart display
    asl, coml, retcoml, lapl, retlapl, otherl, retotherl = [], [], [], [], [], [], []

    # Anomaly detection list
    anomalies = []
    print(anomalies)

    # Get all chart data
    mo = chart.objects.all()

    if mo.exists():
        # Calculate averages for anomaly detection
        avg_values = mo.aggregate(
            avg_assest=Avg('assest'),
            avg_com=Avg('com'),
            avg_retcom=Avg('retcom'),
            avg_lap=Avg('lap'),
            avg_retlap=Avg('retlap'),
            avg_other=Avg('other'),
            avg_retother=Avg('retother')
        )

        for record in mo:
            # Append for chart display
            asl.append(record.assest or 0)
            coml.append(record.com or 0)
            retcoml.append(record.retcom or 0)
            lapl.append(record.lap or 0)
            retlapl.append(record.retlap or 0)
            otherl.append(record.other or 0)
            retotherl.append(record.retother or 0)

            # Threshold check: > 50% higher than average
            if record.assest and avg_values['avg_assest'] and record.assest > avg_values['avg_assest'] * 1.5:
                anomalies.append(f"High asset assignments detected ({record.assest})")
            if record.com and avg_values['avg_com'] and record.com > avg_values['avg_com'] * 1.5:
                anomalies.append(f"High computer assignments detected ({record.com})")
            if record.lap and avg_values['avg_lap'] and record.lap > avg_values['avg_lap'] * 1.5:
                anomalies.append(f"High laptop assignments detected ({record.lap})")
            if record.retcom and avg_values['avg_retcom'] and record.retcom > avg_values['avg_retcom'] * 1.5:
                anomalies.append(f"High computer returns detected ({record.retcom})")
            if record.retlap and avg_values['avg_retlap'] and record.retlap > avg_values['avg_retlap'] * 1.5:
                anomalies.append(f"High laptop returns detected ({record.retlap})")
            if record.other and avg_values['avg_other'] and record.other > avg_values['avg_other'] * 1.5:
                anomalies.append(f"High other accessories assignments detected ({record.other})")
            if record.retother and avg_values['avg_retother'] and record.retother > avg_values['avg_retother'] * 1.5:
                anomalies.append(f"High other accessories returns detected ({record.retother})")

    # Todo list
    to = todolist.objects.all()

    context = {
        'emp': p, 'com': cl, 'lap': lp, 'ass': fass,
        'asl': asl, 'coml': coml, 'retcoml': retcoml,
        'lapl': lapl, 'retlapl': retlapl,
        'otherl': otherl, 'retotherl': retotherl,
        'todo': to, 'anomalies': anomalies
    }

    # Session check
    if 'email' in request.session:
        a = Register.objects.get(email=request.session['email'])
        context['user'] = a.user
        context['pos'] = a.postion
    else:
        context['user'] = None
        context['pos'] = None

    return render(request, 'index.html', context)


#__________________________________________________
# views.py

# from django.http import JsonResponse, HttpResponse
# from .models import Assest
# from .helo import detect_anomalies, calculate_depreciation, generate_report

# # Dashboard view
# # def dashboard1(request):
# #     assets = Assest.objects.all()
# #     anomalies = detect_anomalies(assets)
# #     context = {
# #         'assets': assets,
# #         'anomalies': anomalies
# #     }
# #     return render(request, 'hi.html', context)
# from collections import defaultdict
# from django.db.models import Avg

# def dashboard1(request):
#     emp_count = Employee.objects.count()
#     com_count = Com.objects.count()
#     lap_count = Lap.objects.count()
#     reass_count = reass.objects.count()
#     assets_count = Assest.objects.count() + reass_count

#     asl, coml, retcoml, lapl, retlapl, otherl, retotherl = [], [], [], [], [], [], []
#     anomalies = defaultdict(list)
#     all_anomalies = []

#     mo = chart.objects.all()
#     if mo.exists():
#         avg_values = mo.aggregate(
#             avg_assest=Avg('assest'),
#             avg_com=Avg('com'),
#             avg_retcom=Avg('retcom'),
#             avg_lap=Avg('lap'),
#             avg_retlap=Avg('retlap'),
#             avg_other=Avg('other'),
#             avg_retother=Avg('retother')
#         )

#         def get_severity(value, avg):
#             if not avg or not value:
#                 return None, None, None, 0
#             ratio = value / avg
#             percent = int((ratio - 1) * 100)
#             if ratio > 2:
#                 return "🔴 Critical", percent, "red", 3
#             elif ratio > 1.5:
#                 return "🟠 High", percent, "orange", 2
#             elif ratio > 1.2:
#                 return "🟡 Moderate", percent, "gold", 1
#             return None, None, None, 0

#         checks = [
#             ("Asset", "assest", "assignments"),
#             ("Computer", "com", "assignments"),
#             ("Computer", "retcom", "returns"),
#             ("Laptop", "lap", "assignments"),
#             ("Laptop", "retlap", "returns"),
#             ("Other Accessories", "other", "assignments"),
#             ("Other Accessories", "retother", "returns"),
#         ]

#         id_counter = 1
#         for record in mo:
#             for category, field, label in checks:
#                 value = getattr(record, field, 0)
#                 avg = avg_values[f"avg_{field}"]
#                 sev, percent, color, rank = get_severity(value, avg)
#                 if sev:
#                     anomaly = {
#                         "id": f"anomaly-{id_counter}",
#                         "category": category,
#                         "severity": sev,
#                         "label": label.capitalize(),
#                         "value": value,
#                         "avg": round(avg, 1) if avg else 0,
#                         "percent": percent,
#                         "color": color,
#                         "rank": rank
#                     }
#                     id_counter += 1
#                     anomalies[category].append(anomaly)
#                     all_anomalies.append(anomaly)

#     top_anomalies = sorted(all_anomalies, key=lambda x: (x["rank"], x["percent"]), reverse=True)[:3]

#     # Fill chart lists
#     for record in mo:
#         asl.append(record.assest or 0)
#         coml.append(record.com or 0)
#         retcoml.append(record.retcom or 0)
#         lapl.append(record.lap or 0)
#         retlapl.append(record.retlap or 0)
#         otherl.append(record.other or 0)
#         retotherl.append(record.retother or 0)

#     to = todolist.objects.all()

#     if 'email' in request.session:
#         reg = Register.objects.get(email=request.session['email'])
#         user = reg.user
#         pos = reg.postion
#     else:
#         user = None
#         pos = None

#     context = {
#         'emp': emp_count,
#         'com': com_count,
#         'lap': lap_count,
#         'ass': assets_count,
#         'asl': asl, 'coml': coml, 'retcoml': retcoml,
#         'lapl': lapl, 'retlapl': retlapl,
#         'otherl': otherl, 'retotherl': retotherl,
#         'todo': to,
#         'anomalies': dict(anomalies),
#         'top_anomalies': top_anomalies,
#         'user': user,
#         'pos': pos,
#     }
#     return render(request, 'hi.html', context)

# # Anomaly Detection View
# def anomaly_detection_view(request):
#     assets = Assest.objects.all()
#     anomalies = detect_anomalies(assets)
#     return JsonResponse({'anomalies': anomalies})

# # Depreciation Calculation View
# def depreciation_view(request):
#     assets = Assest.objects.all()
#     for asset in assets:
#         asset.depreciation_value = calculate_depreciation(asset)
#         asset.save()
#     return JsonResponse({'status': 'Depreciation updated for all assets'})

# # Reporting View
# def report_view(request):
#     report_file = generate_report()
#     with open(report_file, 'rb') as f:
#         response = HttpResponse(f.read(), content_type='application/pdf')
#         response['Content-Disposition'] = f'attachment; filename="asset_report.pdf"'
#         return response




# #________________________________________________________
from collections import defaultdict
from django.db.models import Avg
from django.shortcuts import render

def dashboard1(request):
    emp_count = Employee.objects.count()
    com_count = Com.objects.count()
    lap_count = Lap.objects.count()
    reass_count = reass.objects.count()
    assets_count = Assest.objects.count() + reass_count

    asl, coml, retcoml, lapl, retlapl, otherl, retotherl = [], [], [], [], [], [], []
    anomalies = defaultdict(list)
    all_anomalies = []

    mo = chart.objects.all()
    if mo.exists():
        avg_values = mo.aggregate(
            avg_assest=Avg('assest'),
            avg_com=Avg('com'),
            avg_retcom=Avg('retcom'),
            avg_lap=Avg('lap'),
            avg_retlap=Avg('retlap'),
            avg_other=Avg('other'),
            avg_retother=Avg('retother')
        )

        # Keep severity calculation consistent
        def get_severity(value, avg):
            if avg is None or avg == 0 or value is None:
                return None, None, None, 0, 0

            display_avg = round(avg, 1)
            if display_avg == 0:
                return None, None, None, 0, 0

            ratio = value / display_avg
            percent = int((ratio - 1) * 100)

            if ratio > 2:
                return "🔴 Critical", percent, "red", 3, display_avg
            elif ratio > 1.5:
                return "🟠 High", percent, "orange", 2, display_avg
            elif ratio > 1.2:
                return "🟡 Moderate", percent, "gold", 1, display_avg
            return None, None, None, 0, display_avg
        # def get_severity(value, avg):
        #     if avg is None or avg == 0 or value is None:
        #         return None, None, None, 0, avg

        #     display_avg = round(avg, 2)

        #     # 🚫 If average is very small, ignore anomaly (to avoid fake critical alerts)
        #     if display_avg < 5:
        #         return None, None, None, 0, display_avg

        #     ratio = value / display_avg
        #     percent = int((ratio - 1) * 100)

        #     if ratio > 2:
        #         return "🔴 Critical", percent, "red", 3, display_avg
        #     elif ratio > 1.5:
        #         return "🟠 High", percent, "orange", 2, display_avg
        #     elif ratio > 1.2:
        #         return "🟡 Moderate", percent, "gold", 1, display_avg

        #     return None, None, None, 0, display_avg


        checks = [
            ("Asset", "assest", "assignments"),
            ("Computer", "com", "assignments"),
            ("Computer", "retcom", "returns"),
            ("Laptop", "lap", "assignments"),
            ("Laptop", "retlap", "returns"),
            ("Other Accessories", "other", "assignments"),
            ("Other Accessories", "retother", "returns"),
        ]

        id_counter = 1
        unique_anomalies = {}  # prevent duplicates

        for record in mo:
            for category, field, label in checks:
                value = getattr(record, field, 0)
                avg = avg_values[f"avg_{field}"]
                sev, percent, color, rank, display_avg = get_severity(value, avg)

                if sev:
                    key = (category, label)  # unique key
                    anomaly = {
                        "id": f"anomaly-{id_counter}",
                        "category": category,
                        "severity": sev,
                        "label": label.capitalize(),
                        "value": value,
                        "avg": display_avg,
                        "percent": percent,
                        "color": color,
                        "rank": rank
                    }
                    id_counter += 1

                    # keep only the highest severity per (category, label)
                    if key not in unique_anomalies or percent > unique_anomalies[key]["percent"]:
                        unique_anomalies[key] = anomaly

        # final anomaly lists
        all_anomalies = list(unique_anomalies.values())
        for anomaly in all_anomalies:
            anomalies[anomaly["category"]].append(anomaly)

    # 🔹 Top 3 anomalies
    top_anomalies = sorted(all_anomalies, key=lambda x: (x["rank"], x["percent"]), reverse=True)[:3]

    # Fill chart lists
    for record in mo:
        asl.append(record.assest or 0)
        coml.append(record.com or 0)
        retcoml.append(record.retcom or 0)
        lapl.append(record.lap or 0)
        retlapl.append(record.retlap or 0)
        otherl.append(record.other or 0)
        retotherl.append(record.retother or 0)

    to = todolist.objects.all()

    if 'email' in request.session:
        reg = Register.objects.get(email=request.session['email'])
        user = reg.user
        pos = reg.postion
    else:
        user = None
        pos = None

    context = {
        'emp': emp_count,
        'com': com_count,
        'lap': lap_count,
        'ass': assets_count,
        'asl': asl, 'coml': coml, 'retcoml': retcoml,
        'lapl': lapl, 'retlapl': retlapl,
        'otherl': otherl, 'retotherl': retotherl,
        'todo': to,
        'anomalies': dict(anomalies),
        'top_anomalies': top_anomalies,
        'user': user,
        'pos': pos,
    }
    return render(request, 'hi.html', context)


def register(request):
    if request.method == "POST":
        user = request.POST.get('user')
        email = request.POST.get('email')
        mobno = request.POST.get('mobno')
        postion = request.POST.get('postion')
        staffid = request.POST.get('staffid')
        pasw = request.POST.get('pasw')
        spasw = hashlib.md5(pasw.encode()).hexdigest()
        a = Register.objects.filter(email=email)
        b = []
        for i in a:
            em = i.email
            b.append(em)
        if a is not None and email not in b:
            reg = Register(user=user, email=email, mobno=mobno, postion=postion, staffid=staffid, pasw=spasw)
            reg.save()
            sweetify.success(request, title="Success", text="Register Successfull", timer=2000)
            return redirect('index')
        else:
            sweetify.error(request, title="Error", text="User Has Already Exists", timer=2000)
    return render(request, 'signup.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pasw = request.POST.get('pasw')
        spasw = hashlib.md5(pasw.encode()).hexdigest()
        try:
            a = Register.objects.get(email=email)
            if a.pasw == spasw:
                request.session['email'] = email
                sweetify.success(request, title='Success', text='Login Successfully', timer=2000)
                return redirect('index')
            else:
                sweetify.error(request, title='Error', text='Email and Password Does not match', timer=2000)
        except:
            sweetify.error(request, 'User Account Does Not Exists')
    return render(request, 'signin.html')


def logout(request):
    if 'email' in request.session:
        del request.session['email']
        return redirect('index')


def addemp(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        if request.method == 'POST':
            empname = request.POST.get('empname')
            empemail = request.POST.get('empemail')
            empdob = request.POST.get('empdob')
            empmbno = request.POST.get('empmbno')
            empage = request.POST.get('empage')
            empid = request.POST.get('empid')
            emppos = request.POST.get('emppos')
            empjndt = request.POST.get('empjndt')
            empexp = request.POST.get('empexp')
            emp = Employee(empname=empname, empemail=empemail, empdob=empdob, empmbno=empmbno, empage=empage,
                           empid=empid, emppos=emppos, empjndt=empjndt, empexp=empexp)
            emp.save()
            sweetify.success(request, title='success', text='Employee Details Register Successfully', timer=2000)
            return redirect('index')
        return render(request, 'addemp.html', {'user': u, 'pos': pos})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def comcat(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        com = Com.objects.all().filter()
        return render(request, 'comcat.html', {'user': u, 'pos': pos, 'com': com})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def comedit(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        if request.method == "POST":
            comname = request.POST.get('comname')
            os = request.POST.get('os')
            hdd = request.POST.get('hdd')
            ram = request.POST.get('ram')
            cpnm = request.POST.get('cpnm')
            cpsn = request.POST.get('cpsn')
            monname = request.POST.get('monname')
            mnsn = request.POST.get('mnsn')
            prcl = request.POST.get('prcl')
            grcname = request.POST.get('grcname')
            gcs = request.POST.get('gcs')
            kyname = request.POST.get('kyname')
            msname = request.POST.get('msname')
            c=Com.objects.all()
            o=[]
            for i in c:
                o.append(i.comname)
            print(o)
            recom=Returncom.objects.all()
            r=[]
            for j in recom:
                r.append(j.comname)
            if comname not in o:
                if comname not in r:
                    com = Com(comname=comname, os=os, hdd=hdd, ram=ram, cpnm=cpnm, cpsn=cpsn, monname=monname,
                              mnsn=mnsn,
                              prcl=prcl, grcname=grcname, gcs=gcs, kyname=kyname, msname=msname)
                    com.save()
                    asee = Assest.objects.all()
                    asse = len(asee)
                    po = reass.objects.all()
                    poo = len(po)
                    fass = asse + poo
                    cooo = Com.objects.all()
                    coe = len(cooo)
                    recm = Returncom.objects.all()
                    reco = len(recm)
                    lppp = Lap.objects.all()
                    cl = len(lppp)
                    relapp = returnlap.objects.all()
                    relaap = len(relapp)
                    cooo = Otheracc.objects.all()
                    cob = len(cooo)
                    recmmm = retOtheracc.objects.all()
                    recom = len(recmmm)
                    m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                    m.save()
                    sweetify.success(request, title='success', text=f'{comname} Details Register Successfully',
                                     timer=2000)
                    return redirect('comcat')
                else:
                    sweetify.error(request, title='Error', text=f'That {comname} Name has already got on employee', timer=2000)
                    return redirect('comcat')
            else:
                sweetify.error(request, title='Error', text=f'That { comname } Name has already exists', timer=2000)
                return redirect('comcat')
        return render(request, 'comedit.html', {'user': u, 'pos': pos})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def lapcat(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        lap = Lap.objects.all().filter()
        return render(request, 'lapcat.html', {'user': u, 'pos': pos, 'lap': lap})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def lapedit(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        if request.method == "POST":
            lapname = request.POST.get('lapname')
            los = request.POST.get('los')
            lhdd = request.POST.get('lhdd')
            lram = request.POST.get('lram')
            lcm = request.POST.get('lcm')
            lsn = request.POST.get('lsn')
            prcl = request.POST.get('prcl')
            grcname = request.POST.get('grcname')
            gcs = request.POST.get('gcs')
            canv = None
            canvs = request.POST.get('canv')
            canvss = request.POST.get('canvs')
            if bool(canvs) is False and bool(canvss) is True:
                canv = 'No'
            else:
                canv = canvs
            c = Lap.objects.all()
            o = []
            for i in c:
                o.append(i.lapname)
            rl=[]
            rlp=returnlap.objects.all()
            for j in rlp:
                rl.append(j.lapname)
            if lapname not in o:
                if lapname not in rl:
                    lap = Lap(lapname=lapname, los=los, lhdd=lhdd, lram=lram, lcm=lcm, lsn=lsn, prcl=prcl,
                              grcname=grcname,
                              gcs=gcs, canv=canv)
                    lap.save()
                    asee = Assest.objects.all()
                    asse = len(asee)
                    po = reass.objects.all()
                    poo = len(po)
                    fass = asse + poo
                    cooo = Com.objects.all()
                    coe = len(cooo)
                    recm = Returncom.objects.all()
                    reco = len(recm)
                    lppp = Lap.objects.all()
                    cl = len(lppp)
                    relapp = returnlap.objects.all()
                    relaap = len(relapp)
                    cooo = Otheracc.objects.all()
                    cob = len(cooo)
                    recmmm = retOtheracc.objects.all()
                    recom = len(recmmm)
                    m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                    m.save()
                    print('s')
                    sweetify.success(request, title='success', text=f'{lapname} Details Register Successfully',
                                     timer=2000)
                    return redirect('lapcat')
                else:
                    sweetify.error(request, title='Error', text=f'That {lapname} Name has already got on employee', timer=2000)
                    return redirect('lapcat')
            else:
                sweetify.error(request, title='Error', text=f'That { lapname } Name has already exists', timer=2000)
                return redirect('lapcat')
        return render(request, 'lapedit.html', {'user': u, 'pos': pos})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def otheracc(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        oth = Otheracc.objects.all().filter()
        return render(request, 'othcat.html', {'user': u, 'pos': pos, 'oth': oth})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def otheraccedit(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        if request.method == "POST":
            keyboard = request.POST.get('keyboard')
            mouse = request.POST.get('mouse')
            other = request.POST.get('other')
            ok=Otheracc.objects.all().filter(keyboard=keyboard)
            p=[]
            for i in ok:
                p.append(i.keyboard)
            ork=[]
            ortk=retOtheracc.objects.all().filter(keyboard=keyboard)
            for i in ortk:
                ork.append(i.keyboard)
            m=[]
            om=Otheracc.objects.all().filter(mouse=mouse)
            for i in om:
                m.append(i.mouse)
            orm = []
            ortm = retOtheracc.objects.all().filter(mouse=mouse)
            for i in ortm:
                orm.append(i.mouse)
            o=[]
            oo=Otheracc.objects.all().filter(other=other)
            for i in oo:
                o.append(i.other)
            oro = []
            orto = retOtheracc.objects.all().filter(other=other)
            for i in orto:
                oro.append(i.other)
            if keyboard:
                if keyboard not in p:
                    if keyboard not in ork:
                        oth = Otheracc(keyboard=keyboard)
                        oth.save()
                        asee = Assest.objects.all()
                        asse = len(asee)
                        po = reass.objects.all()
                        poo = len(po)
                        fass = asse + poo
                        cooo = Com.objects.all()
                        coe = len(cooo)
                        recm = Returncom.objects.all()
                        reco = len(recm)
                        lppp = Lap.objects.all()
                        cl = len(lppp)
                        relapp = returnlap.objects.all()
                        relaap = len(relapp)
                        cooo = Otheracc.objects.all()
                        cob = len(cooo)
                        recmmm = retOtheracc.objects.all()
                        recom = len(recmmm)
                        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                        m.save()
                        sweetify.success(request, title='success', text='Other Accessories Register Successfully',
                                         timer=2000)
                        return redirect('otheracc')
                    else:
                        sweetify.error(request, title='error',
                                       text=f'That {keyboard} has already got on employee please Given Other name')
                        return redirect('otheracc')
                else:
                    sweetify.error(request, title='error', text=f'That {keyboard} has already exists please Given Other name')
                    return redirect('otheracc')
            elif mouse:
                if mouse not in m:
                    if mouse not in orm:
                        oth = Otheracc(mouse=mouse)
                        oth.save()
                        asee = Assest.objects.all()
                        asse = len(asee)
                        po = reass.objects.all()
                        poo = len(po)
                        fass = asse + poo
                        cooo = Com.objects.all()
                        coe = len(cooo)
                        recm = Returncom.objects.all()
                        reco = len(recm)
                        lppp = Lap.objects.all()
                        cl = len(lppp)
                        relapp = returnlap.objects.all()
                        relaap = len(relapp)
                        cooo = Otheracc.objects.all()
                        cob = len(cooo)
                        recmmm = retOtheracc.objects.all()
                        recom = len(recmmm)
                        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                        m.save()
                        sweetify.success(request, title='success', text='Other Accessories Register Successfully',
                                         timer=2000)
                        return redirect('otheracc')
                    else:
                        sweetify.error(request, title='error',
                                       text=f'That {mouse} has already got on employee please Given Other name')
                        return redirect('otheracc')

                else:
                    sweetify.error(request, title='error', text=f'That {mouse} has already exists please Given Other name')
                    return redirect('otheracc')
            elif other:
                if other not in o:
                    if other not in oro:
                        oth = Otheracc(other=other)
                        oth.save()
                        asee = Assest.objects.all()
                        asse = len(asee)
                        po = reass.objects.all()
                        poo = len(po)
                        fass = asse + poo
                        cooo = Com.objects.all()
                        coe = len(cooo)
                        recm = Returncom.objects.all()
                        reco = len(recm)
                        lppp = Lap.objects.all()
                        cl = len(lppp)
                        relapp = returnlap.objects.all()
                        relaap = len(relapp)
                        cooo = Otheracc.objects.all()
                        cob = len(cooo)
                        recmmm = retOtheracc.objects.all()
                        recom = len(recmmm)
                        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                        m.save()
                        sweetify.success(request, title='success', text=f'{other} Register Successfully',
                                         timer=2000)
                        return redirect('otheracc')
                    else:
                        sweetify.error(request, title='error',
                                       text=f'That {other} has already got on employee please Given Other name')
                        return redirect('otheracc')
                else:
                    sweetify.error(request, title='error', text=f'That {other} has already exists please Given Other name')
                    return redirect('otheracc')
            return redirect('otheracc')
        return render(request, 'otheraccedit.html', {'user': u, 'pos': pos})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def viewemployee(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        emp = Employee.objects.all().filter()
        return render(request, 'viewemployee.html', {'user': u, 'pos': pos, 'e': emp})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})

def addotherass(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        emp = Employee.objects.all().filter()
        oth = Otheracc.objects.all().filter()
        if request.method == 'POST':
            empls = request.POST.get('empls')
            otls = request.POST.get('otls')
            gdt = request.POST.get('gdt')
            rdt = request.POST.get('rdt')
            if gdt != rdt:
                fgdt = gdt[8:]
                frdt = rdt[8:]
                if fgdt < frdt:
                    if otls != 'None':
                        for i in oth:
                            if otls == i.keyboard:
                                oi = Otheracc.objects.get(keyboard=otls)
                                oi.delete()
                                ok=retOtheracc(empname=empls,keyboard=otls)
                                ok.save()
                                break

                            if otls == i.mouse:
                                omm = Otheracc.objects.get(mouse=otls)
                                omm.delete()
                                om = retOtheracc(empname=empls, mouse=otls)
                                om.save()
                                break

                            if otls == i.other:
                                ooo = Otheracc.objects.get(other=otls)
                                ooo.delete()
                                oo = retOtheracc(empname=empls, other=otls)
                                oo.save()
                                break
                        aast=reass(empls=empls,otls=otls,gdt=gdt,rdt=rdt)
                        aast.save()
                        asee = Assest.objects.all()
                        asse = len(asee)
                        po = reass.objects.all()
                        poo = len(po)
                        fass = asse + poo
                        cooo = Com.objects.all()
                        coe = len(cooo)
                        recm = Returncom.objects.all()
                        reco = len(recm)
                        lppp = Lap.objects.all()
                        cl = len(lppp)
                        relapp = returnlap.objects.all()
                        relaap = len(relapp)
                        cooo = Otheracc.objects.all()
                        cob = len(cooo)
                        recmmm = retOtheracc.objects.all()
                        recom = len(recmmm)
                        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                        m.save()
                        sweetify.success(request, title='success', text='add Other accessories Successfully', timer=2000)
                        return redirect('index')
                else:
                    sweetify.error(request, title='error', text=f'Return Date should be after the given date ({gdt}>{rdt})',timer=3000)
            else:
                sweetify.error(request, title='error', text=f'Given Date and Return Data Has Same ({gdt}=={rdt})', timer=3000)
        return render(request, 'addass.html', {'user': u, 'pos': pos,'oth':oth,'emp':emp})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})

def addassests(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        emp = Employee.objects.all().filter()
        lap = Lap.objects.all().filter()
        com = Com.objects.all().filter()
        oth = Otheracc.objects.all().filter()
        if request.method == 'POST':
            empls = request.POST.get('empls')
            cmpls = request.POST.get('cmpls')
            lpls = request.POST.get('lpls')
            gdt = request.POST.get('gdt')
            rdt = request.POST.get('rdt')
            systy = None
            if gdt != rdt:
                fgdt=gdt[8:]
                frdt=rdt[8:]
                if fgdt < frdt:
                    recom = Returncom.objects.all().filter(empname=empls)
                    relap=returnlap.objects.all().filter(empname=empls)
                    rec=[]
                    rlp=[]
                    for i in recom:
                        rec.append(i.empname)
                    for i in relap:
                        rlp.append(i.empname)
                    if cmpls != 'None':
                        if empls in rec or empls in rlp:
                            sweetify.error(request,title='error',text=f'{empls} already got the Computer or laptop',timer=3000)
                            return redirect('/')
                        else:
                            systy=cmpls
                            cm=Com.objects.all().filter(comname=cmpls)
                            for i in cm:
                                dt=Returncom(empname=empls,comname=i.comname,os=i.os, hdd=i.hdd, ram=i.ram, cpnm=i.cpnm, cpsn=i.cpsn,
                                           monname=i.monname, mnsn=i.mnsn, prcl=i.prcl, grcname=i.grcname, gcs=i.gcs,
                                           kyname=i.kyname, msname=i.msname)
                                dt.save()
                                cmm=Com.objects.get(comname=cmpls)
                                cmm.delete()
                    if lpls != 'None':
                        if empls in rlp or empls in rec:
                            sweetify.error(request,title='error',text=f'{empls} already got the Computer or laptop',timer=3000)
                            return redirect('/')
                        else:
                            systy=lpls
                            lps=Lap.objects.all().filter(lapname=lpls)
                            for i in lps:
                                dl=returnlap(empname=empls,lapname=i.lapname, los=i.los, lhdd=i.lhdd, lram=i.lram, lcm=i.lcm, lsn=i.lsn,
                                           prcl=i.prcl, grcname=i.grcname, gcs=i.gcs, canv=i.canv)
                                dl.save()
                                lpp=Lap.objects.get(lapname=lpls)
                                lpp.delete()
                    aast=Assest(empls=empls,systy=systy,gdt=gdt,rdt=rdt)
                    aast.save()
                    asee = Assest.objects.all()
                    asse = len(asee)
                    po = reass.objects.all()
                    poo = len(po)
                    fass = asse + poo
                    cooo = Com.objects.all()
                    coe = len(cooo)
                    recm = Returncom.objects.all()
                    reco = len(recm)
                    lppp = Lap.objects.all()
                    cl = len(lppp)
                    relapp = returnlap.objects.all()
                    relaap = len(relapp)
                    cooo = Otheracc.objects.all()
                    cob = len(cooo)
                    recmmm = retOtheracc.objects.all()
                    recom = len(recmmm)
                    m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                    m.save()
                    sweetify.success(request, title='success', text='Assest Register Successfully', timer=2000)
                    return redirect('viewass')
                else:
                    sweetify.error(request, title='error', text=f'Return Date should be after the given date ({gdt}>{rdt})',timer=3000)
            else:
                sweetify.error(request, title='error', text=f'Given Date and Return Date Has Same ({gdt}=={rdt})', timer=3000)

        return render(request, 'addassests.html',
                      {'user': u, 'pos': pos, 'emp': emp, 'com': com, 'lap': lap, 'oth': oth})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})


def viewass(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        ass = Assest.objects.all().filter()
        accem = reass.objects.all().filter()
        return render(request, 'viewass.html', {'user': u, 'pos': pos, 'ass': ass,'oass':accem})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})
def addass(request,id):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        oth = Otheracc.objects.all().filter()
        p=Assest.objects.get(id=id)
        if request.method == 'POST':
            empls = request.POST.get('empls')
            otls = request.POST.get('otls')
            gdt = request.POST.get('gdt')
            rdt = request.POST.get('rdt')
            if gdt != rdt:
                fgdt = gdt[8:]
                frdt = rdt[8:]
                if fgdt < frdt:
                    if otls != 'None':
                        for i in oth:
                            if otls == i.keyboard:
                                oi = Otheracc.objects.get(keyboard=otls)
                                oi.delete()
                                ok=retOtheracc(empname=empls,keyboard=otls)
                                ok.save()
                                break

                            if otls == i.mouse:
                                omm = Otheracc.objects.get(mouse=otls)
                                omm.delete()
                                om = retOtheracc(empname=empls, mouse=otls)
                                om.save()
                                break

                            if otls == i.other:
                                ooo = Otheracc.objects.get(other=otls)
                                ooo.delete()
                                oo = retOtheracc(empname=empls, other=otls)
                                oo.save()
                                break
                        aast=reass(empls=empls,otls=otls,gdt=gdt,rdt=rdt)
                        aast.save()
                        asee = Assest.objects.all()
                        asse = len(asee)
                        po = reass.objects.all()
                        poo = len(po)
                        fass = asse + poo
                        cooo = Com.objects.all()
                        coe = len(cooo)
                        recm = Returncom.objects.all()
                        reco = len(recm)
                        lppp = Lap.objects.all()
                        cl = len(lppp)
                        relapp = returnlap.objects.all()
                        relaap = len(relapp)
                        cooo = Otheracc.objects.all()
                        cob = len(cooo)
                        recmmm = retOtheracc.objects.all()
                        recom = len(recmmm)
                        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
                        m.save()
                        sweetify.success(request, title='success', text='add extra accessories Successfully', timer=2000)
                        return redirect('index')
                else:
                    sweetify.error(request, title='error', text=f'Return Date should be after the given date ({gdt}>{rdt})',timer=3000)
            else:
                sweetify.error(request, title='error', text=f'Given Date and Return Data Has Same ({gdt}=={rdt})', timer=3000)
        return render(request, 'addass.html', {'user': u, 'pos': pos,'oth':oth,'em':p.empls})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})




def viewfulldetails(request,id):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        ass=Assest.objects.get(id=id)
        c=Returncom.objects.all().filter(empname=ass.empls)
        cl=returnlap.objects.all().filter(empname=ass.empls)
        return render(request, 'viewfullcom.html', {'user': u, 'pos': pos,'com':c,'lap':cl})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})




def returnempother(request,id):
    print(id)
    c=reass.objects.get(id=id)
    # print(c)
    # print(c.empls,c.otls)
    reto=retOtheracc.objects.filter(empname=c.empls)
    # print(reto)
    for i in reto:
        if i.keyboard == c.otls:
            k = Otheracc(keyboard=i.keyboard)
            k.save()
            reoter = retOtheracc.objects.get(keyboard=i.keyboard)
            reoter.delete()
            c.delete()
            sweetify.success(request, title='Return', text=f'{i.keyboard} Accessories has Return Successfully')
        elif i.mouse == c.otls:
            m = Otheracc(mouse=i.mouse)
            m.save()
            reoter = retOtheracc.objects.get(mouse=i.mouse)
            reoter.delete()
            c.delete()
            sweetify.success(request, title='Return', text=f'{i.mouse} Accessories has Return Successfully')
        elif i.other == c.otls:
            o = Otheracc(other=i.other)
            o.save()
            reoter = retOtheracc.objects.get(other=i.other)
            reoter.delete()
            c.delete()
            sweetify.success(request, title='Return', text=f'{i.other} Accessories has Return Successfully')
    asee = Assest.objects.all()
    asse = len(asee)
    po = reass.objects.all()
    poo = len(po)
    fass = asse + poo
    cooo = Com.objects.all()
    coe = len(cooo)
    recm = Returncom.objects.all()
    reco = len(recm)
    lppp = Lap.objects.all()
    cl = len(lppp)
    relapp = returnlap.objects.all()
    relaap = len(relapp)
    cooo = Otheracc.objects.all()
    cob = len(cooo)
    recmmm = retOtheracc.objects.all()
    recom = len(recmmm)
    m = chart(assest=fass,com=coe,retcom=reco,lap=cl,retlap=relaap,other=cob, retother=recom)
    m.save()
    return redirect('index')

def returnprocess(request,id):
    c=Assest.objects.get(id=id)
    com=Returncom.objects.all().filter(comname=c.systy)
    lap = returnlap.objects.all().filter(lapname=c.systy)
    if com:
        for i in com:
            f = Com(comname=i.comname, os=i.os, hdd=i.hdd, ram=i.ram, cpnm=i.cpnm, cpsn=i.cpsn, monname=i.monname,
                    mnsn=i.mnsn,
                    prcl=i.prcl, grcname=i.grcname, gcs=i.gcs, kyname=i.kyname, msname=i.msname)
            f.save()
            sweetify.success(request, title='Return', text=f'{i.comname} Computer has Return Successfully')
        d = Returncom.objects.get(empname=c.empls)
        d.delete()
        c.delete()
        asee = Assest.objects.all()
        asse = len(asee)
        po = reass.objects.all()
        poo = len(po)
        fass = asse + poo
        cooo = Com.objects.all()
        coe = len(cooo)
        recm = Returncom.objects.all()
        reco = len(recm)
        lppp = Lap.objects.all()
        cl = len(lppp)
        relapp = returnlap.objects.all()
        relaap = len(relapp)
        cooo = Otheracc.objects.all()
        cob = len(cooo)
        recmmm = retOtheracc.objects.all()
        recom = len(recmmm)
        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
        m.save()
        return redirect('index')
    elif lap:
        for i in lap:
            l = Lap(lapname=i.lapname, los=i.los, lhdd=i.lhdd, lram=i.lram, lcm=i.lcm, lsn=i.lsn, prcl=i.prcl,
                    grcname=i.grcname,
                    gcs=i.gcs, canv=i.canv)
            l.save()
            sweetify.success(request, title='Return', text=f'{i.lapname} laptop has Return Successfully')
        d = returnlap.objects.get(empname=c.empls)
        d.delete()
        c.delete()
        asee = Assest.objects.all()
        asse = len(asee)
        po = reass.objects.all()
        poo = len(po)
        fass = asse + poo
        cooo = Com.objects.all()
        coe = len(cooo)
        recm = Returncom.objects.all()
        reco = len(recm)
        lppp = Lap.objects.all()
        cl = len(lppp)
        relapp = returnlap.objects.all()
        relaap = len(relapp)
        cooo = Otheracc.objects.all()
        cob = len(cooo)
        recmmm = retOtheracc.objects.all()
        recom = len(recmmm)
        m = chart(assest=fass, com=coe, retcom=reco, lap=cl, retlap=relaap, other=cob, retother=recom)
        m.save()
        return redirect('index')

def deleteemp(request,id):
    r=Employee.objects.get(id=id)
    r.delete()
    sweetify.success(request, title='Delete', text=f'Deleted Successfully')
    return redirect('index')

def deletecom(request,id):
    c=Com.objects.get(id=id)
    c.delete()
    sweetify.success(request, title='Delete', text=f'Deleted Successfully')
    return redirect('index')
def deletelap(request,id):
    l=Lap.objects.get(id=id)
    l.delete()
    sweetify.success(request, title='Delete', text=f'Deleted Successfully')
    return redirect('index')
def deleteother(request,id):
    o=Otheracc.objects.get(id=id)
    o.delete()
    sweetify.success(request, title='Delete', text=f'Deleted Successfully')
    return redirect('index')

def updateprofile(request):
    try:
        a = Register.objects.get(email=request.session['email'])
        u = a.user
        pos = a.postion
        b=Register.objects.all().filter(email=request.session['email'])
        return render(request, 'updateprof.html', {'user': u, 'pos': pos,'pro':b})
    except:
        return render(request, 'signrequestpage.html', {'user': None, 'pos': None})

def actionupdate(request,id):
    if request.method == "POST":
        user = request.POST.get('user')
        mobno = request.POST.get('mobno')
        postion = request.POST.get('postion')
        staffid = request.POST.get('staffid')
        a=Register.objects.get(id=id)
        a.user=user
        a.mobno=mobno
        a.postion=postion
        a.staffid=staffid
        a.save()
        sweetify.success(request, title='Update', text=f'Updated Successfully')
    return redirect('index')

def todolis(request):
    if 'email' in request.session:
        if request.method == 'POST':
            task = request.POST.get('task')
            print(task)
            tl=[]
            to=todolist.objects.all()
            for i in to:
                tl.append(i.todo)
            if task not in tl:
                t = todolist(todo=task)
                t.save()
                sweetify.success(request, title='Todo', text=f'Todolist addedd Successfully')
                return redirect('index')
            else:
                sweetify.error(request, title='Todo Error', text=f'Todolist Already Exists')
                return redirect('index')
    else:
        sweetify.error(request,title='Sign request',text='Please Login The Page')
        return redirect('index')

def tododel(request,id):
    t=todolist.objects.get(id=id)
    t.delete()
    sweetify.success(request, title='Delete', text=f'Deleted Successfully')
    return redirect('index')
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Assest
import datetime
import io
from reportlab.pdfgen import canvas


from django.utils.timezone import now
from datetime import date




# app/helo.py
from datetime import date
from decimal import Decimal, ROUND_HALF_UP

def calc_depreciation(asset, as_of=None):
    """
    Straight-line depreciation.
    annual = (cost - salvage) / life
    accumulated = min(annual * years_used, cost - salvage)
    NBV = cost - accumulated
    """
    as_of = as_of or date.today()

    # years in service (fractional)
    days = max(0, (as_of - asset.gdt).days)
    years_used = days / 365.0

    cost = (asset.purchase_value or Decimal("0")).quantize(Decimal("0.01"))
    salvage = (asset.salvage_value or Decimal("0")).quantize(Decimal("0.01"))
    life = asset.useful_life_years or 1

    depreciable_base = max(Decimal("0.00"), cost - salvage)
    annual = (depreciable_base / Decimal(life)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    accumulated = (annual * Decimal(years_used)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
    if accumulated > depreciable_base:
        accumulated = depreciable_base

    nbv = (cost - accumulated).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    return {
        "years_used": round(years_used, 2),
        "annual_depreciation": annual,
        "accumulated_depreciation": accumulated,
        "net_book_value": nbv,
    }
# app/views.py
from datetime import date
from decimal import Decimal
from django.shortcuts import render
from .models import Assest
# from .helo import calc_depreciation

# Optional sensible defaults if fields aren’t filled
DEFAULT_COST = {
    "Computer": Decimal("35000"),
    "Laptop":   Decimal("55000"),
    "Other":    Decimal("5000"),
}
DEFAULT_LIFE = {"Computer": 3, "Laptop": 3, "Other": 5}

def depreciation(request):
    today = date.today()
    rows = []

    assets = Assest.objects.all().order_by("systy", "empls")
    for a in assets:
        # Fallbacks if not set
        if not a.purchase_value or a.purchase_value == 0:
            a.purchase_value = DEFAULT_COST.get(a.systy, DEFAULT_COST["Other"])
        if not a.useful_life_years or a.useful_life_years <= 0:
            a.useful_life_years = DEFAULT_LIFE.get(a.systy, DEFAULT_LIFE["Other"])
        if a.salvage_value is None:
            a.salvage_value = Decimal("0")

        calc = calc_depreciation(a, as_of=today)

        # Persist summary to the asset
        a.accumulated_depreciation = calc["accumulated_depreciation"]
        a.net_book_value = calc["net_book_value"]
        a.last_depreciation_date = today
        a.save(update_fields=[
            "purchase_value", "salvage_value", "useful_life_years",
            "accumulated_depreciation", "net_book_value", "last_depreciation_date"
        ])

        rows.append({
            "employee": a.empls,
            "type": a.systy,
            "purchase_date": a.gdt,
            "cost": a.purchase_value,
            "salvage": a.salvage_value,
            "life": a.useful_life_years,
            "years_used": calc["years_used"],
            "annual": calc["annual_depreciation"],
            "accumulated": calc["accumulated_depreciation"],
            "nbv": calc["net_book_value"],
        })

    totals = {
        "cost": sum((r["cost"] for r in rows), Decimal("0")),
        "accumulated": sum((r["accumulated"] for r in rows), Decimal("0")),
        "nbv": sum((r["nbv"] for r in rows), Decimal("0")),
    }

    return render(request, "depreciation_report.html", {
        "rows": rows,
        "totals": totals,
        "as_of": today,
    })






























# def depreciation(request):
#     today = date.today()
#     assets = Assest.objects.all()

#     for asset in assets:
#         # Treat gdt as purchase/acquisition date
#         purchase_date = asset.gdt  

#         # Years in service
#         years_used = max(1, (today - purchase_date).days // 365)

#         # Mock depreciation: decrease usage_hours by 10% per year
#         asset.usage_hours = int(asset.usage_hours * (0.9 ** years_used))
#         asset.save()

#     return HttpResponse("✅ Depreciation successfully updated for all assets!")

# ---------- Download Audit Report (PDF) ----------
def reporting(request):
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    p.setFont("Helvetica", 14)
    p.drawString(100, 800, "Audit Report - Assets Summary")

    y = 750
    for a in Assest.objects.all():
        p.drawString(100, y, f"Employee: {a.empls}, System: {a.systy}, Usage Hours: {a.usage_hours}")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="audit_report.pdf"'
    return response

# ---------- Refresh Anomaly Check ----------
def anomaly_detection(request):
    flagged_assets = []
    for a in Assest.objects.all():
        if a.usage_hours > 1000:  # example anomaly rule
            flagged_assets.append(a)

    if flagged_assets:
        return render(request, "anomalies.html", {"flagged_assets": flagged_assets})
    else:
        return HttpResponse("✅ No anomalies detected.")
