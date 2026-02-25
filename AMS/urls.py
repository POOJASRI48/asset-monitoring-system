"""
URL configuration for assestmanagementsystem project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.index,name='index'),
    path('register/',views.register,name='register'),
    path('login/',views.login,name='login'),
    path('logout/',views.logout,name='logout'),
    path('login/addemp/',views.addemp,name='addemp'),
    path('login/comcat/',views.comcat,name='comcat'),
    path('login/comedit/',views.comedit,name='comedit'),
    path('login/lapcat/',views.lapcat,name='lapcat'),
    path('login/lapedit/',views.lapedit,name='lapedit'),
    path('login/otheracc/',views.otheracc,name='otheracc'),
    path('login/otheraccedit/',views.otheraccedit,name='otheraccedit'),
    path('login/viewemployee/',views.viewemployee,name='viewemployee'),
    path('login/viewemployee/deleteemp/<int:id>/',views.deleteemp,name='deleteemp'),
    path('login/viewemployee/deletecom/<int:id>/',views.deletecom,name='deletecom'),
    path('login/viewemployee/deletelap/<int:id>/',views.deletelap,name='deletelap'),
    path('login/viewemployee/deleteother/<int:id>/',views.deleteother,name='deleteother'),
    path('login/addassests/',views.addassests,name='addassests'),
    path('login/viewass/',views.viewass,name='viewass'),
    path('login/viewass/addass/<int:id>/',views.addass,name='addass'),
    path('login/viewass/assass/viewreturn/viewfulldetails/<int:id>/',views.viewfulldetails,name='viewfulldetails'),
    path('login/viewass/returnempother/<int:id>/',views.returnempother,name='returnempother'),
    path('login/addotherass/',views.addotherass,name='addotherass'),
    path('login/viewass/returnprocess/<int:id>/',views.returnprocess,name='returnprocess'),
    path('login/updateprofile/',views.updateprofile,name='updateprofile'),
    path('login/updateprofile/actionupdate/<int:id>/',views.actionupdate,name='actionupdate'),
    path('login/todolist/',views.todolis,name='todolist'),
    path('login/todolist/delete/<int:id>/',views.tododel,name='tododel'),
     path('hi/', views.dashboard1, name='dashboard1'),

    # New module URLs
    # path('anomaly-detection/', views.anomaly_detection_view, name='anomaly_detection'),
    # path('depreciation/', views.depreciation_view, name='depreciation'),
    # path('reporting/', views.report_view, name='reporting'),

    #Updated urls
      path('dashboard/', views.dashboard1, name='dashboard'),
   path("depreciation/", views.depreciation, name="depreciation"),
    path("reporting/", views.reporting, name="reporting"),
    path("anomaly_detection/", views.anomaly_detection, name="anomaly_detection"),
]
