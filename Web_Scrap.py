import statistics
import re
import pyodbc
import undetected_chromedriver as uc
import streamlit as st
import pandas as pd
import io
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from io import BytesIO
from datetime import date
import requests
import base64


arabic_names = {
    "قسم بنى سويف الجديده" : "قسم مدينه بنى سويف الجديده",
    "قسم شرطه التجمع الخامس" : "قسم اول القاهره الجديده",
    "قسم الفيوم"  : "قسم اول الفيوم" ,
    "مركز شبرا خيت" : "مركز شبراخيت",
    "قسم اول مدينه كفر الشيخ" : "قسم اول كفر الشيخ",
    "الساحل الشمالى":"قسم الساحل الشمالى",
    "قسم اول الاسماعيليه":"قسم اول",
    "قسم ثان الاسماعيليه": "قسم ثان",
    "قسم القنطره شرق" : "مركز القنطره شرق",
    "مركز نصر" : "مركز نصر النوبه",
    "مركز ابو طشت": "مركز ابو تشت",
    "مركزههيا" :"مركز ههيا",
    "مركزمنيا القمح": "مركز منيا القمح",
    "قسم ثان الجنوب" :"قسم الجنوب",
    "مركز سمالوط غرب" : "مركز سمالوط",
    "مركز السادات" : "مركز ومدينه السادات",
    "مركز شبين الكوم" : "قسم شبين الكوم",
    "قسم اول شرم الشيخ" : "قسم شرم الشيخ",
    "مركز جهينه الغربيه" : "مركز جهينه",
    "مركز سوهاج الجديده" : "مدينه سوهاج الجديده",


    "Alexandria": "محافظه الاسكندريه",
    "Attarin": "قسم العطارين",
    "Borg al-Arab": "قسم برج العرب",
    "New Borg al-Arab": "مدينه برج العرب الجديده",
    "Dekheila": "قسم الدخيله",
    "Gomrok": "قسم الجمرك",
    "Karmous": "قسم كرموز",
    "Labban": "قسم اللبان",
    "Manshiyya": "قسم المنشيه",
    "Mina El Basal": "قسم مينا البصل",
    "Moharam Bik": "قسم محرم بك",
    "Montazah": "قسم اول المنتزه",
    "Raml Station ": "قسم اول الرمل",
    "Sidi Gaber": "قسم سيدى جابر",

    "Beni Suef": "محافظه بني سويف",
    "Al Feshn": "مركز الفشن",
    "Al Wasty": "مركز الواسطى",
    "Beba": "مركز ببا",
    "Beni Suef City": "مركز بنى سويف",
    "Ehnasia": "مركز اهناسيا",
    "Nasser": "مركز ناصر",
    "New Beni Suef": "قسم مدينه بنى سويف الجديده",
    "Samasta": "مركز سمسطا",

    "Cairo": "محافظه القاهره",
    "15 May City": "قسم 15 مايو",
    "Ain Shams": "قسم عين شمس",
    "Al Amiriyyah": "قسم الاميريه",
    "Bab al-Shereia": "قسم باب الشعريه",
    "Badr City": "قسم بدر",
    "Basateen": "قسم البساتين",
    "Boulaq Abo El Ela": "قسم بولاق",
    "Dar al-Salaam": "قسم دار السلام",
    "Darb al-Ahmar": "قسم الدرب الاحمر",
    "Gamaleya": "قسم الجماليه",
    "Hadayek al-Kobba": "قسم حدائق القبه",
    "Helwan": "قسم حلوان",
    "Ma'sara": "قسم المعصره",
    "Maadi": "قسم المعادى",
    "Marg": "قسم المرج",
    "Masr al-Kadema": "قسم مصر القديمه",
    "Matareya": "قسم المطريه",
    "Mokattam": "قسم المقطم",
    "Nasr City ": "قسم اول مدينه نصر",
    "New Cairo ": "قسم اول القاهره الجديده",
    "Qasr al-Nil": "قسم قصر النيل",
    "Rod al-Farag": "قسم روض الفرج",
    "Salam City ": "قسم اول السلام",
    "Sayeda Zeinab": "قسم السيده زينب",
    "Sharabeya": "قسم الشرابيه",
    "Shorouk City": "قسم الشروق",
    "Shubra": "قسم شبرا",
    "Tebeen": "قسم التبين",
    "Tura": "قسم طره",
    "Waili": "قسم الوايلى",
    "Zamalek": "قسم الزمالك",
    "Zawya al-Hamra": "قسم الزاويه الحمراء",
    "New Valley": "محافظه الوادي الجديد",
    "Balat": "مركز بلاط",
    "Dakhla": "مركز الداخله",
    "Farafra": "مركز الفرافره",
    "Kharga": "قسم الخارجه",
    "Paris": "مركز باريس",

    "Luxor": "محافظه الاقصر",
    "Armant": "مركز ارمنت",
    "Isna": "مركز اسنا",
    "Luxor City": "قسم الاقصر",
    "Luxor Center": "مركز الاقصر",
    "Qurna": "مركز القرنه",
    "Gharbia": "محافظه الغربيه",
    "Basyoun": "مركز بسيون",
    "Kafr al-Zayat": "مركز كفر الزيات",
    "Mahalla al-Kobra": "قسم اول المحله الكبرى",
    "Mahalla al-Kobra Center": "مركز المحله الكبرى",
    "Qutour": "مركز قطور",
    "Samanoud": "مركز سمنود",
    "Santa": "مركز السنطه",

    "Fayoum": "محافظه الفيوم",
    "Atssa": "مركز اطسا",
    "Fayoum City": "قسم اول الفيوم",
    "Fayoum Center": "مركز الفيوم",
    "Ibshway": "مركز ابشواى",
    "New Fayoum": "مدينه الفيوم الجديده",
    "Sinnuras": "مركز سنورس",
    "Tamiya": "مركز طاميه",
    "Yusuf al-Sadiq": "مركز يوسف الصديق",

    "Beheira": "محافظه البحيره",
    "Abou Homs": "مركز ابو حمص",
    "Abuu al-Matamer": "مركز ابو المطامير",
    "Al Nubariyah": "قسم غرب النوباريه",
    "Damanhour": "قسم دمنهور",
    "Damanhour Center": "مركز دمنهور",
    "Delengat": "مركز الدلنجات",
    "Edko": "مركز ادكو",
    "Etay al-Barud": "مركز ايتاى البارود",
    "Hosh Essa": "مركز حوش عيسى",
    "Kafr al-Dawwar": "قسم كفر الدوار",
    "Kafr al-Dawwar Center": "مركز كفر الدوار",
    "Kom Hamadah": "مركز كوم حماده",
    "Mahmoudiyah": "مركز المحموديه",
    "Markaz Badr": "مركز بدر",
    "Rahmaniya": "مركز الرحمانيه",
    "Rashid": "مركز رشيد",
    "Shubrakhit": "مركز شبراخيت",
    "Wadi al-Natrun": "مركز وادى النطرون",
    "Kafr al-Sheikh": "محافظه كفر الشيخ",
    "Bella": "قسم بيلا",
    "Bella Center": "مركز بيلا",
    "Brolos": "مركز البرلس",
    "Desouk": "مركز دسوق",
    "Fouh": "مركز فوه",
    "Hamoul": "مركز الحامول",
    "Kafr al-Sheikh City ": "قسم اول كفر الشيخ",
    "Kafr al-Sheikh Center": "مركز كفر الشيخ",
    "Motobas": "مركز مطوبس",
    "Qaleen": "مركز قلين",
    "Riyadh": "مركز الرياض",
    "Sidi Salem": "مركز سيدى سالم",

    "Matruh": "محافظه مطروح",
    "Alamein": "قسم العلمين",
    "Barany": "قسم سيدى برانى",
    "Dabaa": "قسم الضبعه",
    "Hammam": "قسم الحمام",
    "Marsa Matrouh": "قسم مرسي مطروح",
    "Nagela": "قسم النجيله",
    "North Coast": "قسم الساحل الشمالى",
    "Salloum": "قسم السلوم",
    "Siwa": "قسم سيوه",

    "Ismailia": "محافظه الاسماعيليه",
    "Abu Swear": "مركز ابوصوير",
    "Fayed": "مركز فايد",
    "Ismailia City 1": "قسم اول",
    "Ismailia City 2": "قسم ثان",
    "Kantara East": "مركز القنطره شرق",
    "Kantara West": "مركز القنطره غرب",
    "Qassaseen": "مركز القصاصين الجديده",
    "Tal al-Kebeer": "مركز التل الكبير",

    "Giza": "محافظه الجيزه",
    "6th of October ": "قسم اول 6 اكتوبر",
    "6th of October 2": "قسم ثان 6 اكتوير",
    "6th of October 3": "قسم ثالث 6 اكتوبر",
    "6th of October 4": "قسم رابع 6 اكتوبر",
    "Agouza": "قسم العجوزه",
    "Badrasheen": "مركز البدرشين",
    "Boulaq Dakrour": "قسم بولاق الدكرور",
    "Dokki": "قسم الدقى",
    "El Ayyat": "مركز العياط",
    "Giza District": "قسم الجيزه",
    "Hawamdeya": "قسم الحوامديه",
    "Imbaba": "قسم امبابه",
    "Kerdasa": "مركز كرداسه",
    "Oseem": "مركز اوسيم",
    "Saf": "مركز الصف",
    "Sheikh Zayed": "قسم الشيخ زايد",
    "Warraq": "قسم الوراق",

    "Asyut": "محافظه اسيوط",
    "Qusiya": "مركز القوصيه",
    "Sahel Selim": "مركز ساحل سليم",
    "Sedfa": "مركز صدفا",

    "Aswan": "محافظه اسوان",
    "Abou Simbel": "مركز ابو سمبل",
    "Daraw": "مركز دراو",
    "Edfu": "مركز ادفو",
    "Kom Ombo": "مركز كوم امبو",
    "Nasr al-Noba": "مركز نصر النوبه",

    "Damietta": "محافظه دمياط",
    "Fareskour": "مركز فارسكور",
    "Kafr al-Bateekh": "مركز كفر البطيخ",
    "Kafr Saad": "مركز كفر سعد",
    "New Damietta": "قسم مدينه دمياط الجديدة",
    "Ras al-Bar": "قسم راس البر",
    "Saro": "قسم السرو",
    "Zarqa": "مركز الزرقا",

    "Qalyubia": "محافظه القليوبيه",
    "Banha": "مركز بنها",
    "Kafr Shukr": "مركز كفر شكر",
    "Khanka": "قسم الخانكه",
    "Khosous": "قسم الخصوص",
    "Qaha": "قسم قها",
    "Qalyub": "قسم قليوب",
    "Qanater al-Khairia": "مركز القناطر الخيريه",
    "Shebin al-Qanater": "مركز شبين القناطر",
    "Shubra al-Khaimah": "قسم اول شبرا الخيمه",
    "Tookh": "مركز طوخ",

    "Qena": "محافظه قنا",
    "Abu Tisht": "مركز ابو تشت",
    "Dishna": "مركز دشنا",
    "Farshout": "مركز فرشوط",
    "Nag Hammadi": "مركز نجع حمادى",
    "Nakada": "مركز نقاده",
    "Quos": "مركز قوص",
    "Wakf": "مركز الوقف",

    "Sharqia": "محافظه الشرقيه",
    "10th of Ramadan": "العاشر من رمضان",
    "Abu Hammad": "مركز ابو حماد",
    "Abu Kabir": "مركز ابو كبير",
    "Alqnayat": "مدينة القنايات",
    "Awlad Saqr": "مركز اولاد صقر",
    "Bilbeis": "مركز بلبيس",
    "Deyerb Negm": "مركز ديرب نجم",
    "Faqous": "مركز فاقوس",
    "Hihya": "مركز ههيا",
    "Husseiniya": "مركز الحسينيه",
    "Ibrahemyah": "مركز الابراهيمية",
    "Kafr Saqr": "مركز كفر صقر",
    "Mashtool al-Souk": "مركز مشتول السوق",
    "Minya al-Qamh": "مركز منيا القمح",
    "Qareen": "مدينة القرين",
    "Zagazig": "مركز الزقازيق",

    "Port Said": "محافظه بورسعيد",
    "Arab District": "قسم العرب",
    "Dawahy District": "قسم الضواحى",
    "Ganoub District": "قسم الجنوب",
    "Manakh District": "قسم المناخ",
    "Port Fouad": "قسم بورفؤاد",
    "Sharq District": "قسم الشرق",
    "Zohour District": "قسم الزهور",

    "Minya": "محافظه المنيا",
    "Abu Qurqas": "مركز ابو قرقاص",
    "Adwa": "مركز العدوه",
    "Beni Mazar": "مركز بنى مزار",
    "Deir Mawas": "مركز دير مواس",
    "Maghagha": "مركز مغاغه",
    "Malawi": "قسم ملوى",
    "Matay": "مركز مطاى",
    "New Minya": "قسم المنيا الجديده",
    "Samalut": "مركز سمالوط",

    "Monufia": "محافظه المنوفيه",
    "Ashmon": "مركز اشمون",
    "Bagour": "مركز الباجور",
    "Berket al-Sabaa": "مركز بركه السبع",
    "Menouf": "قسم مدينه منوف",
    "Quesna": "مركز قويسنا",
    "Sadat": "مركز ومدينه السادات",
    "Sers al-Lyan": "قسم سرس الليان",
    "Shebin al-Koum": "قسم شبين الكوم",
    "Shohadaa": "مركز الشهداء",
    "Tala": "مركز تلا",

    "Suez": "محافظه السويس",
    "Arbaeen": "قسم الاربعين",
    "Attaka": "قسم عتاقه",
    "Faisal District": "قسم فيصل",
    "Ganayen": "قسم الجناين",
    "Suez District": "قسم السويس",

    "South Sinai": "محافظه جنوب سيناء",
    "Abu Rudeis": "قسم ابورديس",
    "Abu Zenimah": "قسم ابوزنيمه",
    "Dahab": "قسم دهب",
    "Nuweiba": "قسم نويبع",
    "Ras Sedr": "قسم راس سدر",
    "Sharm al-Sheikh": "قسم شرم الشيخ",
    "St. Catherine": "قسم سانت كاترين",
    "Taba": "قسم طابا",
    "Tor Sinai": "قسم الطور",

    "Sohag": "محافظه سوهاج",
    "Akhmim": "مركز اخميم",
    "Alasirat": "مركز العسيرات",
    "Baliana": "مركز البلينا",
    "Girga": "مركز جرجا",
    "Maragha": "مركز المراغه",
    "Markaz Dar El Salam": "مركز دار السلام",
    "Markaz Juhaynah": "مركز جهينه",
    "Markaz Sohag": "مركز سوهاج",
    "Monsha'a": "مركز المنشاه",
    "New Sohag": "مدينه سوهاج الجديده",
    "Sakaltah": "مركز ساقلته",
    "Tahta": "مركز طهطا",
    "Tama": "مركز طما",


"Properties": "عقارات",
    "Lands": "أراضي",
    "monufia": "محافظه المنوفيه",
    "menouf": "مركز منوف",
    "shebin-al-koum": "مركز شبين الكوم",
    "berket-al-sabaa": "مركز بركه السبع",
    "faqous": "مركز فاقوس",
    "bilbeis": "مركز بلبيس",
    "Buildings and Lands": "أراضي",
    "Commercial Properties": "عقارات",
    "Residential Properties": "عقارات",
    "Residential Apartments": "عقارات",
    "Nasr City": "قسم مدينه نصر ",
    "Residential": "عقارات",
    "Commercial": "عقارات",
}

filter_mapping = {
    "apartments-duplex-for-sale": {
        "وحدة سكنية": "type_eq_1",
        "غرفة": "type_eq_1"
    },
    "commercial-for-sale": {
        "وحدة إدارية": "type_eq_6",
        "مبني اداري": "type_eq_2",
        "محل تجاري": "type_eq_5",
        "جراج": "type_eq_5",
        "مول تجاري": "type_eq_2",
        "مول تجاري وجراج": "type_eq_2",
        "مخبز": "type_eq_5",
        "وحدة طبية": "type_eq_11",
        "مبنى خدمي": "type_eq_2",
        "فندق": "type_eq_2",
        "فندق عائم": "type_eq_2",
        "مطعم": "type_eq_7",
        "مطعم عائم": "type_eq_7",
        "قاعة مناسبات": "type_eq_7",
        "جبانات": "type_eq_7"
    },
    "buildings-lands-other": {
        "مبني سكني": "type_eq_1",
        "مبني": "type_eq_1"
    }
}

ASSET_SUB_TYPE_MAPPING = {
    "apartments-duplex-for-sale": ["غرفة", "وحدة سكنية"],
    "commercial-for-sale": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "buildings-lands-other": ["مبني سكني", "مبني"]
}

# ------------------ SMSARKO MAPPINGS ------------------
smsarko_property_types = {
      "شقق": "apartments-for-sale",
    "فيلات": "villas-for-",
    "عقارات تجارية": "commercial-for-sale",
    "مصايف" :"vacation-for-sale" ,
    "اراضي" : "lands-for-sale",
    "اخري" : "other-for-sale"
}
#  https://www.smsarko.com/search/apartments-for-sale/alexandria-port-police-department

filter_mapping_smsarko = {
    "apartments-for-sale": {
        "وحدة سكنية": "type_eq_1",
        "غرفة": "type_eq_1"
    },
    "commercial-for-sale": {
        "وحدة إدارية": "type_eq_6",
        "مبني اداري": "type_eq_2",
        "محل تجاري": "type_eq_5",
        "جراج": "type_eq_5",
        "مول تجاري": "type_eq_2",
        "مول تجاري وجراج": "type_eq_2",
        "مخبز": "type_eq_5",
        "وحدة طبية": "type_eq_11",
        "مبنى خدمي": "type_eq_2",
        "فندق": "type_eq_2",
        "فندق عائم": "type_eq_2",
        "مطعم": "type_eq_7",
        "مطعم عائم": "type_eq_7",
        "قاعة مناسبات": "type_eq_7",
        "جبانات": "type_eq_7",
    },
    "lands-for-sale": {
        "مبني سكني": "type_eq_1",
        "مبني": "type_eq_1"
    }
}

#لسااااااااا
smsarko_asset_sub_mapping = {
    "apartments-for-sale": ["غرفة", "وحدة سكنية"],
    "commercial-for-sale": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "lands-for-sale": ["مبني سكني", "مبني"]
}

smsarko_governorates = {
            "محافظه اسوان": "aswan",
    "محافظه اسيوط": "assiot",
    "محافظه الاسكندريه": "alexandria",
    "محافظه الاقصر": "luxor",
    "محافظه الاسماعيليه": "ismalia",
    "البحر الأحمر": "red-sea", # 
    "محافظه البحيره": "el-behera",
    "محافظه الجيزه": "giza",
    "الدقهلية": "el-daqahlia",
    "محافظه السويس": "suez",
    "محافظه الشرقيه": "el-sharkia",
    "محافظه الغربيه": "el-gharbia",
    "محافظه الفيوم": "el-faioum",
    "محافظه القاهره": "cairo",
    "محافظه القليوبيه": "el-qaliobia",
    "محافظه المنوفيه": "el-monofia",
    "محافظه المنيا": "el-menia",
    "محافظه الوادي الجديد": "el-wadi-el-gidid",
    "محافظه بني سويف": "beni-suef",
    "محافظه بورسعيد": "port-said",
    "محافظه جنوب سيناء": "south-sinai",
    "محافظه دمياط": "domiat",
    "محافظه سوهاج": "sohag",
    "شمال سيناء": "north-sinai", # 
    "محافظه قنا": "qena",
    "محافظه كفر الشيخ": "kafr-el-shikh",
    "محافظه مطروح": "matroh"
        }

smsarko_location_dict = {
    "Alexandria": "محافظه الاسكندريه",
    "Attarin": "قسم العطارين",
    "Borg al-Arab": "قسم برج العرب",
    "New Borg al-Arab": "مدينه برج العرب الجديده",
    "Dekheila": "قسم الدخيله",
    "Gomrok": "قسم الجمرك",
    "Karmous": "قسم كرموز",
    "Labban": "قسم اللبان",
    "Manshiyya": "قسم المنشيه",
    "Mina El Basal": "قسم مينا البصل",
    "Moharam Bik": "قسم محرم بك",
    "Montazah": "قسم اول المنتزه",
    "Raml Station ": "قسم اول الرمل",
    "Sidi Gaber": "قسم سيدى جابر",

    "Beni Suef": "محافظه بني سويف",
    "Al Feshn": "مركز الفشن",
    "Al Wasty": "مركز الواسطى",
    "Beba": "مركز ببا",
    "Beni Suef City": "مركز بنى سويف",
    "Ehnasia": "مركز اهناسيا",
    "Nasser": "مركز ناصر",
    "New Beni Suef": "قسم مدينه بنى سويف الجديده",
    "Samasta": "مركز سمسطا",

    "Cairo": "محافظه القاهره",
    "15 May City": "قسم 15 مايو",
    "Ain Shams": "قسم عين شمس",
    "Al Amiriyyah": "قسم الاميريه",
    "Bab al-Shereia": "قسم باب الشعريه",
    "Badr City": "قسم بدر",
    "Basateen": "قسم البساتين",
    "Boulaq Abo El Ela": "قسم بولاق",
    "Dar al-Salaam": "قسم دار السلام",
    "Darb al-Ahmar": "قسم الدرب الاحمر",
    "Gamaleya": "قسم الجماليه",
    "Hadayek al-Kobba": "قسم حدائق القبه",
    "Helwan": "قسم حلوان",
    "Ma'sara": "قسم المعصره",
    "Maadi": "قسم المعادى",
    "Marg": "قسم المرج",
    "Masr al-Kadema": "قسم مصر القديمه",
    "Matareya": "قسم المطريه",
    "Mokattam": "قسم المقطم",
    "Nasr City 1": "قسم اول مدينه نصر",
    "Nasr City 2": "قسم ثان مدينه نصر",
    "New Cairo 1": "قسم اول القاهره الجديده",
    "New Cairo 2": "قسم ثان القاهره الجديده",
    "New Cairo 3": "قسم ثالث القاهره الجديده",
    "Qasr al-Nil": "قسم قصر النيل",
    "Rod al-Farag": "قسم روض الفرج",
    "Salam City 1": "قسم اول السلام",
    "Salam City 2": "قسم ثان السلام",
    "Sayeda Zeinab": "قسم السيده زينب",
    "Sharabeya": "قسم الشرابيه",
    "Shorouk City": "قسم الشروق",
    "Shubra": "قسم شبرا",
    "Tebeen": "قسم التبين",
    "Tura": "قسم طره",
    "Waili": "قسم الوايلى",
    "Zamalek": "قسم الزمالك",
    "Zawya al-Hamra": "قسم الزاويه الحمراء",
    "New Valley": "محافظه الوادي الجديد",
    "Balat": "مركز بلاط",
    "Dakhla": "مركز الداخله",
    "Farafra": "مركز الفرافره",
    "Kharga": "قسم الخارجه",
    "Paris": "مركز باريس",

    "Luxor": "محافظه الاقصر",
    "Armant": "مركز ارمنت",
    "Isna": "مركز اسنا",
    "Luxor City": "قسم الاقصر",
    "Luxor Center": "مركز الاقصر",
    "Qurna": "مركز القرنه",
    "Gharbia": "محافظه الغربيه",
    "Basyoun": "مركز بسيون",
    "Kafr al-Zayat": "مركز كفر الزيات",
    "Mahalla al-Kobra": "قسم اول المحله الكبرى",
    "Mahalla al-Kobra 2": "قسم ثان المحله الكبرى",
    "Mahalla al-Kobra 3": "قسم ثالث المحله الكبرى",
    "Mahalla al-Kobra Center": "مركز المحله الكبرى",
    "Qutour": "مركز قطور",
    "Samanoud": "مركز سمنود",
    "Santa": "مركز السنطه",

    "Fayoum": "محافظه الفيوم",
    "Atssa": "مركز اطسا",
    "Fayoum City": "قسم اول الفيوم",
    "Fayoum Center": "مركز الفيوم",
    "Ibshway": "مركز ابشواى",
    "New Fayoum": "مدينه الفيوم الجديده",
    "Sinnuras": "مركز سنورس",
    "Tamiya": "مركز طاميه",
    "Yusuf al-Sadiq": "مركز يوسف الصديق",

    "Beheira": "محافظه البحيره",
    "Abou Homs": "مركز ابو حمص",
    "Abuu al-Matamer": "مركز ابو المطامير",
    "Al Nubariyah": "قسم غرب النوباريه",
    "Damanhour": "قسم دمنهور",
    "Damanhour Center": "مركز دمنهور",
    "Delengat": "مركز الدلنجات",
    "Edko": "مركز ادكو",
    "Etay al-Barud": "مركز ايتاى البارود",
    "Hosh Essa": "مركز حوش عيسى",
    "Kafr al-Dawwar": "قسم كفر الدوار",
    "Kafr al-Dawwar Center": "مركز كفر الدوار",
    "Kom Hamadah": "مركز كوم حماده",
    "Mahmoudiyah": "مركز المحموديه",
    "Markaz Badr": "مركز بدر",
    "Rahmaniya": "مركز الرحمانيه",
    "Rashid": "مركز رشيد",
    "Shubrakhit": "مركز شبراخيت",
    "Wadi al-Natrun": "مركز وادى النطرون",
    "Kafr al-Sheikh": "محافظه كفر الشيخ",
    "Bella": "قسم بيلا",
    "Bella Center": "مركز بيلا",
    "Brolos": "مركز البرلس",
    "Desouk": "مركز دسوق",
    "Fouh": "مركز فوه",
    "Hamoul": "مركز الحامول",
    "Kafr al-Sheikh City 1": "قسم اول كفر الشيخ",
    "Kafr al-Sheikh City 2": "قسم ثان كفر الشيخ",
    "Kafr al-Sheikh Center": "مركز كفر الشيخ",
    "Motobas": "مركز مطوبس",
    "Qaleen": "مركز قلين",
    "Riyadh": "مركز الرياض",
    "Sidi Salem": "مركز سيدى سالم",

    "Matruh": "محافظه مطروح",
    "Alamein": "قسم العلمين",
    "Barany": "قسم سيدى برانى",
    "Dabaa": "قسم الضبعه",
    "Hammam": "قسم الحمام",
    "Marsa Matrouh": "قسم مرسي مطروح",
    "Nagela": "قسم النجيله",
    "North Coast": "قسم الساحل الشمالى",
    "Salloum": "قسم السلوم",
    "Siwa": "قسم سيوه",

    "Ismailia": "محافظه الاسماعيليه",
    "Abu Swear": "مركز ابوصوير",
    "Fayed": "مركز فايد",
    "Ismailia City 1": "قسم اول",
    "Ismailia City 2": "قسم ثان",
    "Kantara East": "مركز القنطره شرق",
    "Kantara West": "مركز القنطره غرب",
    "Qassaseen": "مركز القصاصين الجديده",
    "Tal al-Kebeer": "مركز التل الكبير",

    "Giza": "محافظه الجيزه",
    "6th of October 1": "قسم اول 6 اكتوبر",
    "6th of October 2": "قسم ثان 6 اكتوير",
    "6th of October 3": "قسم ثالث 6 اكتوبر",
    "6th of October 4": "قسم رابع 6 اكتوبر",
    "Agouza": "قسم العجوزه",
    "Badrasheen": "مركز البدرشين",
    "Boulaq Dakrour": "قسم بولاق الدكرور",
    "Dokki": "قسم الدقى",
    "El Ayyat": "مركز العياط",
    "Giza District": "قسم الجيزه",
    "Hawamdeya": "قسم الحوامديه",
    "Imbaba": "قسم امبابه",
    "Kerdasa": "مركز كرداسه",
    "Oseem": "مركز اوسيم",
    "Saf": "مركز الصف",
    "Sheikh Zayed": "قسم الشيخ زايد",
    "Warraq": "قسم الوراق",

    "Asyut": "محافظه اسيوط",
    "Qusiya": "مركز القوصيه",
    "Sahel Selim": "مركز ساحل سليم",
    "Sedfa": "مركز صدفا",

    "Aswan": "محافظه اسوان",
    "Abou Simbel": "مركز ابو سمبل",
    "Daraw": "مركز دراو",
    "Edfu": "مركز ادفو",
    "Kom Ombo": "مركز كوم امبو",
    "Nasr al-Noba": "مركز نصر النوبه",

    "Damietta": "محافظه دمياط",
    "Fareskour": "مركز فارسكور",
    "Kafr al-Bateekh": "مركز كفر البطيخ",
    "Kafr Saad": "مركز كفر سعد",
    "New Damietta": "قسم مدينه دمياط الجديدة",
    "Ras al-Bar": "قسم راس البر",
    "Saro": "قسم السرو",
    "Zarqa": "مركز الزرقا",

    "Qalyubia": "محافظه القليوبيه",
    "Banha": "مركز بنها",
    "Kafr Shukr": "مركز كفر شكر",
    "Khanka": "قسم الخانكه",
    "Khosous": "قسم الخصوص",
    "Qaha": "قسم قها",
    "Qalyub": "قسم قليوب",
    "Qanater al-Khairia": "مركز القناطر الخيريه",
    "Shebin al-Qanater": "مركز شبين القناطر",
    "Shubra al-Khaimah": "قسم اول شبرا الخيمه",
    "Tookh": "مركز طوخ",

    "Qena": "محافظه قنا",
    "Abu Tisht": "مركز ابو تشت",
    "Dishna": "مركز دشنا",
    "Farshout": "مركز فرشوط",
    "Nag Hammadi": "مركز نجع حمادى",
    "Nakada": "مركز نقاده",
    "Quos": "مركز قوص",
    "Wakf": "مركز الوقف",

    "Sharqia": "محافظه الشرقيه",
    "10th of Ramadan": "العاشر من رمضان",
    "Abu Hammad": "مركز ابو حماد",
    "Abu Kabir": "مركز ابو كبير",
    "Alqnayat": "مدينة القنايات",
    "Awlad Saqr": "مركز اولاد صقر",
    "Bilbeis": "مركز بلبيس",
    "Deyerb Negm": "مركز ديرب نجم",
    "Faqous": "مركز فاقوس",
    "Hihya": "مركز ههيا",
    "Husseiniya": "مركز الحسينيه",
    "Ibrahemyah": "مركز الابراهيمية",
    "Kafr Saqr": "مركز كفر صقر",
    "Mashtool al-Souk": "مركز مشتول السوق",
    "Minya al-Qamh": "مركز منيا القمح",
    "Qareen": "مدينة القرين",
    "Zagazig": "مركز الزقازيق",

    "Port Said": "محافظه بورسعيد",
    "Arab District": "قسم العرب",
    "Dawahy District": "قسم الضواحى",
    "Ganoub District": "قسم الجنوب",
    "Manakh District": "قسم المناخ",
    "Port Fouad": "قسم بورفؤاد",
    "Sharq District": "قسم الشرق",
    "Zohour District": "قسم الزهور",

    "Minya": "محافظه المنيا",
    "Abu Qurqas": "مركز ابو قرقاص",
    "Adwa": "مركز العدوه",
    "Beni Mazar": "مركز بنى مزار",
    "Deir Mawas": "مركز دير مواس",
    "Maghagha": "مركز مغاغه",
    "Malawi": "قسم ملوى",
    "Matay": "مركز مطاى",
    "New Minya": "قسم المنيا الجديده",
    "Samalut": "مركز سمالوط",

    "Monufia": "محافظه المنوفيه",
    "Ashmon": "مركز اشمون",
    "Bagour": "مركز الباجور",
    "Berket al-Sabaa": "مركز بركه السبع",
    "Menouf": "قسم مدينه منوف",
    "Quesna": "مركز قويسنا",
    "Sadat": "مركز ومدينه السادات",
    "Sers al-Lyan": "قسم سرس الليان",
    "Shebin al-Koum": "قسم شبين الكوم",
    "Shohadaa": "مركز الشهداء",
    "Tala": "مركز تلا",

    "Suez": "محافظه السويس",
    "Arbaeen": "قسم الاربعين",
    "Attaka": "قسم عتاقه",
    "Faisal District": "قسم فيصل",
    "Ganayen": "قسم الجناين",
    "Suez District": "قسم السويس",

    "South Sinai": "محافظه جنوب سيناء",
    "Abu Rudeis": "قسم ابورديس",
    "Abu Zenimah": "قسم ابوزنيمه",
    "Dahab": "قسم دهب",
    "Nuweiba": "قسم نويبع",
    "Ras Sedr": "قسم راس سدر",
    "Sharm al-Sheikh": "قسم شرم الشيخ",
    "St. Catherine": "قسم سانت كاترين",
    "Taba": "قسم طابا",
    "Tor Sinai": "قسم الطور",

    "Sohag": "محافظه سوهاج",
    "Akhmim": "مركز اخميم",
    "Alasirat": "مركز العسيرات",
    "Baliana": "مركز البلينا",
    "Girga": "مركز جرجا",
    "Maragha": "مركز المراغه",
    "Markaz Dar El Salam": "مركز دار السلام",
    "Markaz Juhaynah": "مركز جهينه",
    "Markaz Sohag": "مركز سوهاج",
    "Monsha'a": "مركز المنشاه",
    "New Sohag": "مدينه سوهاج الجديده",
    "Sakaltah": "مركز ساقلته",
    "Tahta": "مركز طهطا",
    "Tama": "مركز طما",

    "Properties": "عقارات",
    "Lands": "أراضي",
    "monufia": "محافظه المنوفيه",
    "menouf": "مركز منوف",
    "shebin-al-koum": "مركز شبين الكوم",
    "berket-al-sabaa": "مركز بركه السبع",
    "faqous": "مركز فاقوس",
    "bilbeis": "مركز بلبيس",
    "Buildings and Lands": "أراضي",
    "Commercial Properties": "عقارات",
    "Residential Properties": "عقارات",
    "Residential Apartments": "عقارات",
    "Nasr City": "قسم مدينه نصر ",
    "Residential": "عقارات",
    "Commercial": "عقارات",
}

# ------------------ AQARMAP MAPPINGS ------------------
aqarmap_property_types = {
    "Commercial": "commercial",
    "Apartment": "apartment",
    "Land or Farm": "land-or-farm"
}

filter_mapping_smsarko = {
    "apartments-for-sale": {
        "وحدة سكنية": "type_eq_1",
        "غرفة": "type_eq_1"
    },
    "commercial-for-sale": {
        "وحدة إدارية": "type_eq_6",
        "مبني اداري": "type_eq_2",
        "محل تجاري": "type_eq_5",
        "جراج": "type_eq_5",
        "مول تجاري": "type_eq_2",
        "مول تجاري وجراج": "type_eq_2",
        "مخبز": "type_eq_5",
        "وحدة طبية": "type_eq_11",
        "مبنى خدمي": "type_eq_2",
        "فندق": "type_eq_2",
        "فندق عائم": "type_eq_2",
        "مطعم": "type_eq_7",
        "مطعم عائم": "type_eq_7",
        "قاعة مناسبات": "type_eq_7",
        "جبانات": "type_eq_7"
    },
    "lands-for-sale": {
        "مبني سكني": "type_eq_1",
        "مبني": "type_eq_1"
    }
}

aqarmap_ASSET_SUB_TYPE_MAPPING = {
    "apartments-for-sale": ["غرفة", "وحدة سكنية"],
    "commercial-for-sale": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "lands-for-sale": ["مبني سكني", "مبني"]
}

aqarmap_asset_sub_mapping = {
    "apartment": ["غرفة", "وحدة سكنية"],
    "commercial": ["وحدة إدارية", "مبني اداري", "محل تجاري", "جراج", "مول تجاري", "مول تجاري وجراج", "مخبز", "وحدة طبية", "مبنى خدمي", "فندق", "فندق عائم", "مطعم", "مطعم عائم", "قاعة مناسبات", "جبانات"],
    "land-or-farm": ["مبني سكني", "مبني"]
}

aqarmap_governorates = {
    "Alexandria": [
        "Attarin", "Borg al-Arab", "Dekheila", "Gomrok", "Karmous", "Labban", "Manshiyya",
        "Mina El Basal", "Moharam Bik", "Montazah", "Raml Station",
        "Sidi Gaber"
    ],
    "Beni Suef": [
        "Al Feshn", "Al Wasty", "Beba", "Beni Suef City", "Ehnasia", "Nasser", "New Beni Suef", "Samasta"
    ],
    "Cairo": [
        "15 May City", "Ain Shams", "Al Amiriyyah", "Bab al-Shereia", "Badr City", "Basateen",
        "Boulaq Abo El Ela",
        "Dar al-Salaam", "Darb al-Ahmar", "Gamaleya", "Hadayek al-Kobba", "Helwan", "Ma'sara", "Maadi", "Marg",
        "Masr al-Kadema", "Matareya", "Mokattam", "Nasr City", "New Cairo",
        "Qasr al-Nil", "Rod al-Farag", "Salam City ", "Sayeda Zeinab",
        "Sharabeya",
        "Shorouk City", "Shubra", "Tebeen", "Tura", "Waili", "Zamalek", "Zawya al-Hamra"
    ],
    "Gharbia": [
        "Basyoun", "Kafr al-Zayat", "Mahalla al-Kobra",
        "Mahalla al-Kobra Center", "Qutour", "Samanoud", "Santa"
    ],
    "el-fayoum": [
        "Atssa", "Fayoum City", "Fayoum Center",  "Ibshway", "New Fayoum", "Sinnuras", "Tamiya",
        "Yusuf al-Sadiq"
    ],
    "Beheira": [
        "Abou Homs", "Abuu al-Matamer", "Al Nubariyah", "Damanhour", "Damanhour Center", "Delengat", "Edko",
        "Etay al-Barud", "Hosh Essa", "Kafr al-Dawwar", "Kafr al-Dawwar Center", "Kom Hamadah", "Mahmoudiyah",
        "Markaz Badr", "Rahmaniya", "Rashid", "Shubrakhit", "Wadi al-Natrun"
    ],

    "New Valley": ["Balat", "Dakhla", "Farafra", "Kharga", "Paris"],
    "Luxor": ["Armant", "Isna", "Luxor City", "Luxor Center", "Qurna"],
    "Kafr al-Sheikh": ["Bella", "Bella Center", "Brolos", "Desouk", "Fouh", "Hamoul",
                       "Kafr al-Sheikh City", "Kafr al-Sheikh Center", "Motobas", "Qaleen", "Riyadh",
                       "Sidi Salem"],
    "marsa-matruh": ["Alamein", "Barany", "Dabaa", "Hammam", "Marsa Matrouh", "Nagela", "North Coast", "Salloum",
               "Siwa"],
    "Ismailia": ["Abu Swear", "Fayed", "Ismailia City", "Kantara East", "Kantara West",
                 "Qassaseen", "Tal al-Kebeer"],
    "Giza": ["6th of October", "Agouza",
             "Badrasheen",
             "Boulaq Dakrour", "Dokki", "El Ayyat", "Giza District", "Hawamdeya", "Imbaba", "Kerdasa", "Oseem",
             "Saf",
             "Sheikh Zayed", "Warraq"],

    "Asyut": ["Qusiya", "Sahel Selim", "Sedfa"],
    "Aswan": ["Abou Simbel", "Daraw", "Edfu", "Kom Ombo", "Nasr al-Noba"],
    "Damietta": ["Fareskour", "Kafr al-Bateekh", "Kafr Saad", "New Damietta", "Ras al-Bar", "Saro", "Zarqa"],

    "Qalyubia": ["Banha", "Kafr Shukr", "Khanka", "Khosous", "Qaha", "Qalyub", "Qanater al-Khairia",
                 "Shebin al-Qanater", "Shubra al-Khaimah", "Tookh"],
    "Qena": ["Abu Tisht", "Dishna", "Farshout", "Nag Hammadi", "Nakada", "Quos", "Wakf"],
    "Sharqia": ["10th of Ramadan", "Abu Hammad", "Abu Kabir", "Alqnayat", "Awlad Saqr", "Bilbeis",
                "Deyerb Negm",
                "Faqous", "Hihya", "Husseiniya", "Ibrahemyah", "Kafr Saqr", "Mashtool al-Souk", "Minya al-Qamh",
                "Qareen", "Zagazig"],
    "Suez": ["Arbaeen", "Attaka", "Faisal District", "Ganayen", "Suez District"],
    "South Sinai": ["Abu Rudeis", "Abu Zenimah", "Dahab", "Nuweiba", "Ras Sedr", "Sharm al-Sheikh",
                    "St. Catherine",
                    "Taba", "Tor Sinai"],
    "Sohag": ["Akhmim", "Alasirat", "Baliana", "Girga", "Maragha", "Markaz Dar El Salam", "Markaz Juhaynah",
              "Markaz Sohag", "Monsha'a", "New Sohag", "Sakaltah", "Tahta", "Tama"],
}

def setup_driver():
    chrome_path = r'C:\Users\edge-t\appdata\roaming\undetected_chromedriver\undetected_chromedriver.exe'

    if os.path.exists(chrome_path):
        try:
            os.remove(chrome_path)
        except Exception as e:
            print(f"Could not remove file at {chrome_path}: {e}")



    options = uc.ChromeOptions()
    options.add_argument('--headless=new')
    options.add_argument('--window-size=1920,1080')
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_argument('--start-maximized')
    options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                     'AppleWebKit/537.36 (KHTML, like Gecko) '
                     'Chrome/137.0.0.0 Safari/537.36')





    try:
        driver = uc.Chrome(options=options, version_main=137, use_subprocess=True)
    except FileExistsError as fee:
        print(f"FileExistsError encountered: {fee}. Trying to remove the file again.")
        if os.path.exists(chrome_path):
            try:
                os.remove(chrome_path)
            except Exception as e:
                print(f"Second attempt to remove {chrome_path} failed: {e}")
        driver = uc.Chrome(options=options, version_main=137, use_subprocess=True)

    return driver

def extract_number(text, min_val, max_val):
    cleaned = re.sub(r"[^\d.]", "", text)
    cleaned = cleaned.replace('²', '')
    if cleaned:
        try:
            number = float(cleaned)
            if min_val <= number <= max_val:
                return number
        except ValueError:
            return None
    return None

# ------------------ SCRAPING FUNCTIONS ------------------
def get_listing_elements(driver):
    candidate_xpaths = [
        "//div[contains(@class, '_357a9937')]",
        "//div[contains(@class, 'listing-item')]",
        "//div[contains(@class, '_948d9e0a')]",
        "//article[.//span[contains(text(), 'EGP')]]",
        "//div[contains(@class, 'sc-') and .//span[contains(text(), 'EGP')]]"
    ]
    for xpath in candidate_xpaths:
        elements = driver.find_elements(By.XPATH, xpath)
        if elements:
            valid_elements = [el for el in elements if "EGP" in el.text and any(unit in el.text for unit in ['m²', 'SQM', 'متر'])]
            if valid_elements:
                return valid_elements
    return []

def scrape_property_data(url, is_land=False, selected_sub_type=None, use_client_filter=False, url_type=None):
    driver = setup_driver()
    property_data = []
    try:
        driver.get(url)
        time.sleep(5)
        price_selectors = [
            ".//span[contains(@class, '_95eae7db')]",
            ".//span[contains(text(), 'EGP')]",
            ".//*[contains(@class, 'price')]"
        ]
        area_selectors = [
            ".//span[contains(text(), 'SQM')]",
            ".//span[contains(text(), 'm²')]",
            ".//span[contains(@class, '_3e1113f0')]"
        ]
        listings = get_listing_elements(driver)
        for listing in listings:
            price = None
            area = None
            for selector in price_selectors:
                try:
                    price_el = listing.find_element(By.XPATH, selector)
                    price = extract_number(price_el.text, 100000, 100000000)
                    if price:
                        break
                except Exception:
                    continue
            for selector in area_selectors:
                try:
                    area_el = listing.find_element(By.XPATH, selector)
                    area = extract_number(area_el.text, 20, 1000)
                    if area:
                        break
                except Exception:
                    continue
            if price:
                if not area and is_land:
                    area = 100.0
                    st.warning("Area not found; using default value for a Buildings and Lands listing.")
                if area:
                    property_data.append((price, area))
        return property_data
    finally:
        driver.quit()

def scrape_smsarko_data(url):
    driver = setup_driver()
    property_data = []
    try:
        driver.get(url)
        time.sleep(5)
        articles = driver.find_elements(By.TAG_NAME, "article")
        for article in articles:
            try:
                price_el = article.find_element(By.CSS_SELECTOR, "div.badge.text-bg-success.fs-6.fw-light")
                area_el = article.find_element(By.CSS_SELECTOR, "div.badge.text-bg-dark.fs-6.fw-light")
                price = extract_number(price_el.text, 100000, 100000000)
                area = extract_number(area_el.text, 20, 1000)
                if price and area:
                    property_data.append((price, area))
            except Exception:
                continue
        return property_data
    finally:
        driver.quit()

def scrape_aqarmap_data(url):
    driver = setup_driver() 
    property_data = []
    try:
        driver.get(url)

        wait = WebDriverWait(driver, 30)
        wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'listing-card')]")))

        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)

        cards = driver.find_elements(By.XPATH, "//div[contains(@class, 'listing-card')]")
        for index, card in enumerate(cards, start=1):
            try:
                details_links = card.find_elements(
                    By.XPATH, ".//a[contains(@class, 'p-2x') and starts-with(@href, '/en/listing/')]"
                )
                if not details_links:
                    continue
                details_link = details_links[0]

                price_elems = details_link.find_elements(
                    By.XPATH, ".//span[contains(@class, 'text-title_4')]"
                )
                if not price_elems:
                    print(f"Card {index}: No price element found in card details.")
                    continue
                price_elem = price_elems[0]
                price_text = price_elem.text.strip()
                price = extract_number(price_text, 100000, 1000000000)

                area_elems = details_link.find_elements(
                    By.XPATH, ".//p[contains(., 'm²')]"
                )
                if not area_elems:
                    print(f"Card {index}: No area element found in card details.")
                    continue
                area_elem = area_elems[0]
                area_text = area_elem.text.strip()
                area = extract_number(area_text, 20, 10000)

                if price is not None and area is not None:
                    property_data.append((price, area))
            except Exception as e:
                print(f"Card {index}: Error processing a card:", e)
                continue

        return property_data
    except Exception as general_e:
        print("General error during scraping:", general_e)
        return property_data
    finally:
        driver.quit()

# imp    (done)
def calculate_metrics(data):
    if not data:
        return None
    prices, areas = zip(*data)
    avg_price = statistics.mean(prices)
    avg_area = statistics.mean(areas)
    return {
        'avg_price': avg_price,
        'avg_area': avg_area,
        'avg_price_per_m2': avg_price / avg_area,
        'median_price': statistics.median(prices),
        'sample_size': len(data)
    }

# ------------------ REPORTS SAVEEE FUNCTIONS ------------------
def save_report_excel(property_type, governorate, city, metrics, selected_sub_type):
    default_sub_type = selected_sub_type if selected_sub_type and selected_sub_type.strip() != "" else "غير محدد"
    governorate_arabic = arabic_names.get(governorate, governorate)
    city_arabic = arabic_names.get(city, city)
    property_type_arabic = arabic_names.get(property_type, property_type)
    report_data = {
        'ASSET_TYPE_DESC': [property_type_arabic],
        'GOVERNORATE_NAME': [governorate_arabic],
        'SECTION_NAME': [city_arabic],
        'Price per m²': [metrics['avg_price_per_m2']],
        'Rent per m²': [metrics['avg_price_per_m2'] / (12 * 20)],
        'Date': [pd.Timestamp.now().strftime('%Y-%m-%d')],
        'ASSET_SUB_TYPE_DESC': [default_sub_type]
    }
    report_df = pd.DataFrame(report_data)
    base_path = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    file_path = os.path.join(base_path, "dubizzle_report.xlsx")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        report_df.to_excel(file_path, index=False)
    except Exception as e:
        st.error(f"Failed to save report: {e}")
        return None, None
    buffer = io.BytesIO()
    report_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer, report_df

def save_smsarko_report_excel(property_type, governorate, city, metrics, selected_sub_type):
    default_sub_type = selected_sub_type if selected_sub_type and selected_sub_type.strip() != "" else "غير محدد"
    governorate_arabic = arabic_names.get(governorate, governorate)
    city_arabic = smsarko_location_dict.get(city, city)
    property_type_arabic = arabic_names.get(property_type, property_type)
    report_data = {
        'ASSET_TYPE_DESC': [property_type_arabic],
        'GOVERNORATE_NAME': [governorate_arabic],
        'SECTION_NAME': [city_arabic],
        'Price per m²': [metrics['avg_price_per_m2']],
        'Rent per m²': [metrics['avg_price_per_m2'] / (12 * 20)],
        'Date': [pd.Timestamp.now().strftime('%Y-%m-%d')],
        'ASSET_SUB_TYPE_DESC': [default_sub_type]
    }
    report_df = pd.DataFrame(report_data)
    base_path = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    file_path = os.path.join(base_path, "smsarko_report.xlsx")
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        report_df.to_excel(file_path, index=False)
    except Exception as e:
        st.error(f"Failed to save SMSARKO report: {e}")
        return None, None
    buffer = io.BytesIO()
    report_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer, report_df

def save_aqarmap_report_excel(property_type, governorate, city, metrics, selected_sub_type):
    default_sub_type = selected_sub_type if selected_sub_type and selected_sub_type.strip() != "" else "غير محدد"
    property_type_arabic = convert_to_arabic(property_type)
    governorate_arabic = convert_to_arabic(governorate)
    city_arabic = convert_to_arabic(city)

    report_data = {
        'ASSET_TYPE_DESC': [property_type_arabic],
        'GOVERNORATE_NAME': [governorate_arabic],
        'SECTION_NAME': [city_arabic],
        'Price per m²': [metrics.get('avg_price_per_m2', 0)],
        'Rent per m²': [metrics.get('avg_price_per_m2', 0) / (12 * 20) if metrics.get('avg_price_per_m2', 0) else 0],
        'Date': [pd.Timestamp.now().strftime('%Y-%m-%d')],
        'ASSET_SUB_TYPE_DESC': [default_sub_type]
    }

    report_df = pd.DataFrame(report_data)
    base_path = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    file_path = os.path.join(base_path, "aqarmap_report.xlsx")

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
        report_df.to_excel(file_path, index=False)
    except Exception as e:
        st.error(f"Failed to save Aqarmap report: {e}")
        return None, None

    buffer = io.BytesIO()
    report_df.to_excel(buffer, index=False)
    buffer.seek(0)
    return buffer, report_df

# ------------------ DATABASE  ------------------ ✔️✔️✔️✔️✔️ DONEEEEEEE
def get_db_connection():
    conn_str = (
        'DRIVER={SQL Server};'
        'SERVER=omar-pc;'
        'DATABASE=EAMS_R2_01_copy;'
        'UID=sa;'
        'PWD=P@ssw0rd;'
        'TrustServerCertificate=yes;'
    )
    try:
        conn = pyodbc.connect(conn_str)
        return conn
    except pyodbc.Error as e:
        st.error(f"Failed to connect to SQL Server: {e}")
        return None

def fetch_all_matching_assets_by_keys(asset_type_desc, asset_sub_type_desc, governorate_name, section_name):
    conn = get_db_connection()
    if not conn:
        return None

    governorate_name_ar = arabic_names.get(governorate_name, governorate_name)
    section_name_ar = arabic_names.get(section_name, section_name)

    query = """
    SELECT a.asset_id, a.final_area_m2, a.ASSET_TYPE_DESC, 
           a.ASSET_SUB_TYPE_DESC, a.GOVERNORATE_NAME, a.SECTION_NAME
    FROM dbo.v_assets_aream2 a
    WHERE LOWER(LTRIM(RTRIM(a.ASSET_TYPE_DESC))) = LOWER(?)
      AND LOWER(LTRIM(RTRIM(a.ASSET_SUB_TYPE_DESC))) = LOWER(?)
      AND LOWER(LTRIM(RTRIM(a.GOVERNORATE_NAME))) = LOWER(?)
      AND LOWER(LTRIM(RTRIM(a.SECTION_NAME))) = LOWER(?)
    """
    try:
        cursor = conn.cursor()
        st.write("جاري البحث عن الأصول بالمفاتيح التالية:")
        st.write("نوع الأصل:", asset_type_desc)
        st.write("نوع الأصل الفرعي:", asset_sub_type_desc)
        st.write("المحافظة:", governorate_name_ar)
        st.write("القسم:", section_name_ar)

        cursor.execute(query, (asset_type_desc, asset_sub_type_desc, governorate_name_ar, section_name_ar))
        results = cursor.fetchall()

        st.write("تم العثور على", len(results), "أصل مطابق في العرض.")
        return results
    except Exception as e:
        st.error(f"حدث خطأ أثناء جلب الأصول بالمفاتيح: {e}")
        return None
    finally:
        conn.close()

def process_assets_batch(assets, price_per_m2, rent_per_m2):
    conn = get_db_connection()
    if not conn:
        return None
    current_date = pd.Timestamp.now().strftime('%Y-%m-%d')
    processed_count = {'updated': 0}
    try:
        cursor = conn.cursor()
        update_query = """
            UPDATE [EVAL].[ASSETS_EVALUATE]
            SET SITE_MONTHLY_VALUE_EGP = ?,
                SITE_MARKTING_VALUE_EGP = ?,
                SITE_EVAL_DATE = ?,
                DATE_MODIFIED = GETDATE()
            WHERE ASSET_ID = ?
        """
        batch_size = 50
        total_assets = len(assets)
        st_progress_container = st.empty()
        for i in range(0, total_assets, batch_size):
            batch = assets[i:i + batch_size]
            params = []
            for asset in batch:
                asset_id = asset[0]
                final_area_m2 = float(asset[1]) if asset[1] is not None else 100.0
                site_marketing_value = final_area_m2 * float(price_per_m2)
                site_monthly_value = final_area_m2 * float(rent_per_m2)
                params.append((site_monthly_value, site_marketing_value, current_date, asset_id))
                processed_count['updated'] += 1
            cursor.executemany(update_query, params)
            conn.commit()
            progress = (i + len(batch)) / total_assets
            st_progress_container.progress(progress)
            st_progress_container.write(f"Updated {i + len(batch)} of {total_assets} assets")
            time.sleep(0.05)
        st.success(f"Successfully updated {processed_count['updated']} assets")
        return processed_count
    except Exception as e:
        st.error(f"Database operation failed: {str(e)}")
        conn.rollback()
        return None
    finally:
        conn.close()

def convert_to_arabic(name, lowercase_lookup=False):

    key = name.lower() if lowercase_lookup else name
    return arabic_names.get(key, name)

@st.cache_data
def fetch_smsarko_cities(governorate_slug):
    base_url = "https://www.smsarko.com/api/v1/locations/level2/"
    full_url = base_url + governorate_slug
    response = requests.get(full_url)

    if response.status_code == 200:
        data = response.json()
        return {item["name_ar"]: item["slug"] for item in data}
    else:
        return {}

# -------------------------------------------------------

def get_base64_image(image_path):
    with open(image_path, "rb") as img_file:
        b64_str = base64.b64encode(img_file.read()).decode()
        return b64_str

def main():
    st.set_page_config(page_title="Property Market Analysis", layout="wide")
    
    img_base64 = get_base64_image("Logo.png")
    
    st.markdown(f"""
        <div style='display: flex; flex-direction: column; align-items: center; margin-top: -10px;'>
            <img src="data:image/png;base64,{img_base64}" width="200" style="margin-right: 20px; align-self: flex-start;" />
            <div>
                <h1 style="margin-bottom: 0;">🏡 Property Market Analysis</h1>
                <h4 style="margin-top: 0; margin-left: 70px;">Analyze property prices and land rates in Egypt</h4>
            </div>
        </div>
    """, unsafe_allow_html=True)

    source_options = ["Dubizzle", "Smsarko", "Aqarmap"]
    selected_source = st.radio("Select Data Source:", source_options)

   # ------------------ Dubizzle SECTION ------------------
    if selected_source == "Dubizzle":
        st.subheader("Dubizzle Scraping Settings")

        property_types = {
            "Residential Properties": "apartments-duplex-for-sale",
            "Commercial Properties": "commercial-for-sale",
            "Buildings and Lands": "buildings-lands-other"
        }
        governorates_list = {
            "Alexandria": [
                "Attarin", "Borg al-Arab", "Dekheila", "Gomrok", "Karmous", "Labban", "Manshiyya",
                "Mina El Basal", "Moharam Bik", "Montazah", "Raml Station",
                "Sidi Gaber"
            ],
            "Beni Suef": [
                "Al Feshn", "Al Wasty", "Beba", "Beni Suef City", "Ehnasia", "Nasser", "New Beni Suef", "Samasta"
            ],
            "Cairo": [
                "15 May City", "Ain Shams", "Al Amiriyyah", "Bab al-Shereia", "Badr City", "Basateen",
                "Boulaq Abo El Ela",
                "Dar al-Salaam", "Darb al-Ahmar", "Gamaleya", "Hadayek al-Kobba", "Helwan", "Ma'sara", "Maadi", "Marg",
                "Masr al-Kadema", "Matareya", "Mokattam", "Nasr City", "New Cairo",
                 "Qasr al-Nil", "Rod al-Farag", "Salam City", "Sayeda Zeinab",
                "Sharabeya",
                "Shorouk City", "Shubra", "Tebeen", "Tura", "Waili", "Zamalek", "Zawya al-Hamra"
            ],
            "Gharbia": [
                "Basyoun", "Kafr al-Zayat", "Mahalla al-Kobra",
                "Mahalla al-Kobra Center", "Qutour", "Samanoud", "Santa"
            ],
            "Fayoum": [
                "Atssa", "Fayoum City", "Fayoum Center", "Ibshway", "New Fayoum", "Sinnuras", "Tamiya",
                "Yusuf al-Sadiq"
            ],
            "Beheira": [
                "Abou Homs", "Abuu al-Matamer", "Al Nubariyah", "Damanhour", "Damanhour Center", "Delengat", "Edko",
                "Etay al-Barud", "Hosh Essa", "Kafr al-Dawwar", "Kafr al-Dawwar Center", "Kom Hamadah", "Mahmoudiyah",
                "Markaz Badr", "Rahmaniya", "Rashid", "Shubrakhit", "Wadi al-Natrun"
            ],

            "New Valley": ["Balat", "Dakhla", "Farafra", "Kharga", "Paris"],

            "Luxor": ["Armant", "Isna", "Luxor City", "Luxor Center", "Qurna"],

            "Kafr al-Sheikh": ["Bella", "Bella Center", "Brolos", "Desouk", "Fouh", "Hamoul", "Kafr al-Sheikh City",
                                "Kafr al-Sheikh Center", "Motobas", "Qaleen", "Riyadh",
                               "Sidi Salem"],
            "Matruh": ["Alamein", "Barany", "Dabaa", "Hammam", "Marsa Matrouh", "Nagela", "North Coast", "Salloum",
                       "Siwa"],
            "Ismailia": ["Abu Swear", "Fayed", "Ismailia City", "Kantara East", "Kantara West",
                         "Qassaseen", "Tal al-Kebeer"],
            "Giza": ["6th of October", "Agouza",
                     "Badrasheen",
                     "Boulaq Dakrour", "Dokki", "El Ayyat", "Giza District", "Hawamdeya", "Imbaba", "Kerdasa", "Oseem",
                     "Saf",
                     "Sheikh Zayed", "Warraq"],

            "Asyut": ["Qusiya", "Sahel Selim", "Sedfa"],
            "Aswan": ["Abou Simbel", "Daraw", "Edfu", "Kom Ombo", "Nasr al-Noba"],
            "Damietta": ["Fareskour", "Kafr al-Bateekh", "Kafr Saad", "New Damietta", "Ras al-Bar", "Saro", "Zarqa"],
            "Qalyubia": ["Banha", "Kafr Shukr", "Khanka", "Khosous", "Qaha", "Qalyub", "Qanater al-Khairia",
                         "Shebin al-Qanater", "Shubra al-Khaimah", "Tookh"],
            "Qena": ["Abu Tisht", "Dishna", "Farshout", "Nag Hammadi", "Nakada", "Quos", "Wakf"],
            "Sharqia": ["10th of Ramadan", "Abu Hammad", "Abu Kabir", "Alqnayat", "Awlad Saqr", "Bilbeis",
                        "Deyerb Negm",
                        "Faqous", "Hihya", "Husseiniya", "Ibrahemyah", "Kafr Saqr", "Mashtool al-Souk", "Minya al-Qamh",
                        "Qareen", "Zagazig"],
            "Suez": ["Arbaeen", "Attaka", "Faisal District", "Ganayen", "Suez District"],
            "South Sinai": ["Abu Rudeis", "Abu Zenimah", "Dahab", "Nuweiba", "Ras Sedr", "Sharm al-Sheikh",
                            "St. Catherine",
                            "Taba", "Tor Sinai"],
            "Sohag": ["Akhmim", "Alasirat", "Baliana", "Girga", "Maragha", "Markaz Dar El Salam", "Markaz Juhaynah",
                      "Markaz Sohag", "Monsha'a", "New Sohag", "Sakaltah", "Tahta", "Tama"],
        }

        property_type = st.selectbox("🏠 Select property type:", list(property_types.keys()), index=0)
        url_type = property_types[property_type]
        asset_sub_options = ASSET_SUB_TYPE_MAPPING.get(url_type, [])
        selected_sub_type = st.selectbox("🔎 Select asset sub-type filter:", asset_sub_options) if asset_sub_options else ""
        default_sub_type = selected_sub_type if selected_sub_type.strip() != "" else "غير محدد"
        selected_governorate = st.selectbox("🌍 Select a governorate:", list(governorates_list.keys()), index=0)
        selected_city = st.selectbox("🏙️ Select a city:", governorates_list[selected_governorate], index=0)
        city_slug = selected_city.lower().replace(" ", "-")
        base_url = f"https://www.dubizzle.com.eg/en/properties/{url_type}/{city_slug}/"
        url = base_url
        if default_sub_type != "غير محدد" and selected_sub_type in filter_mapping.get(url_type, {}):
            filter_code = filter_mapping[url_type][selected_sub_type]
            url = f"{base_url}?filter={filter_code}"
        # st.write("Using URL:", url)
        if st.button("📊 Analyze Market Prices (Dubizzle)"):
            with st.spinner("Scraping Dubizzle market data..."):
                data = scrape_property_data(url,
                                            is_land=(url_type == "buildings-lands-other"),
                                            selected_sub_type=selected_sub_type,
                                            use_client_filter=True,
                                            url_type=url_type)
                if not data:
                    st.error("❌ No listings found matching the filter! Check your search criteria or website structure.")
                    return
                metrics = calculate_metrics(data)
                if metrics:
                    st.subheader("Final Report Generation")
                    st.metric("Average Price", f"{metrics.get('avg_price', 0):,.0f} EGP")
                    st.metric("Average Area", f"{metrics.get('avg_area', 0):,.2f} m²")
                    df_prices = pd.DataFrame(data, columns=['Price', 'Area'])
                    st.subheader("Market Price Distribution")
                    st.line_chart(df_prices['Price'])
                    arabic_property_type = convert_to_arabic(property_type)
                    arabic_governorate = convert_to_arabic(selected_governorate)
                    arabic_city = convert_to_arabic(selected_city)

                    buffer, report_df = save_report_excel(
                        arabic_property_type,
                        arabic_governorate,
                        arabic_city,
                        metrics,
                        default_sub_type
                    )

                    if buffer is not None:
                        st.download_button(
                            label=f"📥 Download {property_type} Report",
                            data=buffer,
                            file_name="dubizzle_report.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                        st.write("### Current Dubizzle Data (Saved in dubizzle_report.xlsx)")
                        st.dataframe(report_df)
                        st.session_state["dubizzle_report_df"] = report_df
                        st.session_state["dubizzle_metrics"] = metrics
                        st.session_state["dubizzle_governorate"] = selected_governorate
                        st.session_state["dubizzle_city"] = selected_city
                        st.session_state["dubizzle_asset_sub"] = default_sub_type
        if "dubizzle_report_df" in st.session_state:
            if st.button("🔄 Update Asset Values (Dubizzle)"):
                with st.spinner("Updating Dubizzle assets in database..."):
                    metrics = st.session_state["dubizzle_metrics"]
                    selected_governorate = st.session_state["dubizzle_governorate"]
                    selected_city = st.session_state["dubizzle_city"]
                    excel_data = {
                        'asset_type_desc': convert_to_arabic(
                            'أراضي' if url_type == "buildings-lands-other" else 'عقارات'),
                        'asset_sub_type': default_sub_type,
                        'governorate_name': convert_to_arabic(selected_governorate),
                        'section_name': convert_to_arabic(selected_city, lowercase_lookup=True),
                        'price_per_m2': metrics.get('avg_price_per_m2', 0),
                        'rent_per_m2': metrics.get('avg_price_per_m2', 0) / (12 * 20)
                    }

                    matching_assets = fetch_all_matching_assets_by_keys(
                        excel_data['asset_type_desc'],
                        excel_data['asset_sub_type'],
                        excel_data['governorate_name'],
                        excel_data['section_name']
                    )
                    if matching_assets and len(matching_assets) > 0:
                        st.write(f"Found {len(matching_assets)} matching Dubizzle assets to update")
                        result = process_assets_batch(matching_assets,
                                                      excel_data['price_per_m2'],
                                                      excel_data['rent_per_m2'])
                        if result:
                            st.success(f"✅ Updated {result['updated']} Dubizzle assets in database")
                        else:
                            st.error("❌ Failed to update Dubizzle assets")
                    else:
                        st.warning("No Dubizzle assets found for the selected criteria.")

   # ------------------ SMSARKO SECTION ------------------
    if selected_source == "Smsarko":
        st.subheader("📊 SMSARKO Scraping Settings")

        smsarko_property = st.selectbox("🏠 Select SMSARKO property type:", list(smsarko_property_types.keys()))
        smsarko_property_value = smsarko_property_types[smsarko_property]

        smsarko_selected_governorate = st.selectbox("🌍 Select SMSARKO governorate:", list(smsarko_governorates.keys()))
        governorate_slug = smsarko_governorates[smsarko_selected_governorate]

        cities_list = fetch_smsarko_cities(governorate_slug)
        if cities_list:
            smsarko_selected_city = st.selectbox("🏙️ Select SMSARKO city:", list(cities_list.keys()))
            city_slug = cities_list[smsarko_selected_city]
        else:
            st.warning("❌ No cities available for the selected governorate.")
            return

        url = f"https://www.smsarko.com/search/{smsarko_property_value}/{city_slug}"
        # st.write("🔗 Using URL:", url)

        if st.button("📊 Analyze Market Prices (SMSARKO)"):
            with st.spinner("Scraping SMSARKO market data..."):
                data = scrape_smsarko_data(url)
                if not data:
                    st.error("❌ No SMSARKO listings found!")
                else:
                    metrics = calculate_metrics(data)
                    if metrics:
                        st.subheader("Final Report Generation")
                        st.metric("Average Price", f"{metrics.get('avg_price', 0):,.0f} EGP")
                        st.metric("Average Area", f"{metrics.get('avg_area', 0):,.2f} m²")
                        df_prices = pd.DataFrame(data, columns=['Price', 'Area'])

                        st.subheader("📈 SMSARKO Market Price Distribution")
                        st.line_chart(df_prices['Price'])

                        smsarko_default_sub = "غير محدد"

                        buffer, report_df = save_smsarko_report_excel(
                            smsarko_property,
                            smsarko_selected_governorate,
                            smsarko_selected_city,
                            metrics,
                            smsarko_default_sub
                        )

                        if buffer is not None:
                            st.download_button(
                                label=f"📥 Download SMSARKO {smsarko_property} Report",
                                data=buffer,
                                file_name="smsarko_report.xlsx",
                                mime="application/vnd.ms-excel"
                            )
                            st.write("### SMSARKO Report Data")
                            st.dataframe(report_df)

                            # Store in session_state
                            st.session_state["smsarko_report_df"] = report_df
                            st.session_state["smsarko_metrics"] = metrics
                            st.session_state["smsarko_governorate"] = smsarko_selected_governorate
                            st.session_state["smsarko_city"] = smsarko_selected_city
                            st.session_state["smsarko_asset_sub"] = smsarko_default_sub

        if "smsarko_report_df" in st.session_state:
            if st.button("🔄 Update Asset Values (SMSARKO)"):
                with st.spinner("Updating SMSARKO assets in database..."):
                    metrics = st.session_state["smsarko_metrics"]
                    selected_governorate = st.session_state["smsarko_governorate"]
                    selected_city = st.session_state["smsarko_city"]
                    asset_sub = st.session_state["smsarko_asset_sub"]

                    excel_data = {
                        'asset_type_desc': 'أراضي' if smsarko_property_value == "lands-for-sale" else 'عقارات',
                        'asset_sub_type': asset_sub,
                        'governorate_name': arabic_names.get(selected_governorate, selected_governorate),
                        'section_name': convert_to_arabic(selected_city, lowercase_lookup=True),
                        'price_per_m2': metrics.get('avg_price_per_m2', 0),
                        'rent_per_m2': metrics.get('avg_price_per_m2', 0) / (12 * 20)
                    }

                    matching_assets = fetch_all_matching_assets_by_keys(
                        excel_data['asset_type_desc'],
                        excel_data['asset_sub_type'],
                        excel_data['governorate_name'],
                        excel_data['section_name']
                    )

                    if matching_assets and len(matching_assets) > 0:
                        st.write(f"🔍 Found {len(matching_assets)} matching SMSARKO assets to update")
                        result = process_assets_batch(
                            matching_assets,
                            excel_data['price_per_m2'],
                            excel_data['rent_per_m2']
                        )
                        if result:
                            st.success(f"✅ Updated {result['updated']} SMSARKO assets in database")
                        else:
                            st.error("❌ Failed to update SMSARKO assets")
                    else:
                        st.warning("⚠️ No matching assets found for the selected criteria.")

        # ------------------ Aqarmap SECTION ------------------

   # ------------------ Aqarmap SECTION ------------------
    elif selected_source == "Aqarmap":
        st.subheader("Aqarmap Scraping Settings")

        aqarmap_property = st.selectbox("🏠 Select Aqarmap property type:", list(aqarmap_property_types.keys()))
        aqarmap_property_value = aqarmap_property_types[aqarmap_property]

        aqarmap_asset_sub_options = aqarmap_asset_sub_mapping.get(aqarmap_property_value, [])
        if aqarmap_asset_sub_options:
            aqarmap_selected_asset_sub = st.selectbox("🔎 Select Aqarmap asset sub-type filter:", aqarmap_asset_sub_options)
        else:
            aqarmap_selected_asset_sub = "غير محدد"
        aqarmap_default_sub = aqarmap_selected_asset_sub if aqarmap_selected_asset_sub.strip() != "" else "غير محدد"

        aqarmap_selected_governorate = st.selectbox("🌍 Select Aqarmap governorate:", list(aqarmap_governorates.keys()))

        aqarmap_selected_city = st.selectbox("🏙️ Select Aqarmap city:", aqarmap_governorates[aqarmap_selected_governorate])
        aqarmap_governorate_slug = aqarmap_selected_governorate.lower().replace(" ", "-")
        aqarmap_city_slug = aqarmap_selected_city.lower().replace(" ", "-")
        base_url = f"https://aqarmap.com.eg/en/for-sale/{aqarmap_property_value}/{aqarmap_governorate_slug}/{aqarmap_city_slug}/"


        # st.write("Using URL:", base_url)

        if st.button("📊 Analyze Market Prices (Aqarmap)"):
            with st.spinner("Scraping Aqarmap market data..."):
                data = scrape_aqarmap_data(base_url)
                if not data:
                    st.error("❌ No Aqarmap listings found!")
                    return
                metrics = calculate_metrics(data)
                if metrics:
                    st.subheader("Final Report Generation")
                    st.metric("Average Price", f"{metrics.get('avg_price', 0):,.0f} EGP")
                    st.metric("Average Area", f"{metrics.get('avg_area', 0):,.2f} m²")
                    df_prices = pd.DataFrame(data, columns=['Price', 'Area'])
                    st.subheader("Aqarmap Market Price Distribution")
                    st.line_chart(df_prices['Price'])
                    buffer, report_df = save_aqarmap_report_excel(
                        aqarmap_property,
                        aqarmap_selected_governorate,
                        aqarmap_selected_city,
                        metrics,
                        aqarmap_default_sub
                    )
                    if buffer is not None:
                        st.download_button(
                            label="📥 Download Aqarmap Report",
                            data=buffer,
                            file_name="aqarmap_report.xlsx",
                            mime="application/vnd.ms-excel"
                        )
                        st.write("### Current Aqarmap Data")
                        st.dataframe(report_df)
                        st.session_state["aqarmap_report_df"] = report_df
                        st.session_state["aqarmap_metrics"] = metrics
                        st.session_state["aqarmap_governorate"] = aqarmap_selected_governorate
                        st.session_state["aqarmap_city"] = aqarmap_selected_city
                        st.session_state["aqarmap_asset_sub"] = aqarmap_default_sub
                        st.session_state["aqarmap_property_value"] = aqarmap_property_value

        if "aqarmap_report_df" in st.session_state:
            if st.button("🔄 Update Asset Values (Aqarmap)"):
                with st.spinner("Updating Aqarmap assets in database..."):
                    metrics = st.session_state["aqarmap_metrics"]
                    selected_governorate = st.session_state["aqarmap_governorate"]
                    selected_city = st.session_state["aqarmap_city"]
                    aqarmap_property_value = st.session_state["aqarmap_property_value"]
                    aqarmap_asset_sub = st.session_state["aqarmap_asset_sub"]
                    asset_type_desc = 'أراضي' if aqarmap_property_value == "lands-for-sale" else 'عقارات'
                    matching_assets = fetch_all_matching_assets_by_keys(
                        asset_type_desc,
                        aqarmap_asset_sub,
                        arabic_names.get(selected_governorate, selected_governorate),
                        arabic_names.get(selected_city, selected_city)
                    )
                    if matching_assets and len(matching_assets) > 0:
                        st.write(f"Found {len(matching_assets)} matching Aqarmap assets to update")
                        result = process_assets_batch(matching_assets,
                                                      metrics.get('avg_price_per_m2', 0),
                                                      metrics.get('avg_price_per_m2', 0) / (12 * 20))
                        if result:
                            st.success(f"✅ Updated {result['updated']} Aqarmap assets in database")
                        else:
                            st.error("❌ Failed to update Aqarmap assets")
                    else:
                        st.warning("No Aqarmap assets found for the selected criteria.")


    # --- Create final report excel sheet ---


    BASE_PATH = r"C:\Users\edge-t\Desktop\Edge Pro\cama_web_scrappin\housing sf"
    st.markdown("---")
    if all(key in st.session_state for key in ["dubizzle_report_df", "smsarko_report_df", "aqarmap_report_df"]):
        if st.button("✨ Generate Final Report"):
            with st.spinner("Processing final report..."):
                dubizzle_df = st.session_state["dubizzle_report_df"]
                smsarko_df = st.session_state["smsarko_report_df"]
                aqarmap_df = st.session_state["aqarmap_report_df"]

                required_columns = [
                    'ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME',
                    'SECTION_NAME', 'Price per m²', 'Rent per m²', 'Date'
                ]
                dfs = {'Dubizzle': dubizzle_df, 'SMSARKO': smsarko_df, 'Aqarmap': aqarmap_df}

                for name, df in dfs.items():
                    missing = [col for col in required_columns if col not in df.columns]
                    if missing:
                        st.error(f"❌ {name} report is missing columns: {', '.join(missing)}")
                        return

                def get_groups(df):
                    return set(df[['ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME']].apply(tuple, axis=1))

                dubizzle_groups = get_groups(dubizzle_df)
                smsarko_groups = get_groups(smsarko_df)
                aqarmap_groups = get_groups(aqarmap_df)
                common_groups = dubizzle_groups & smsarko_groups & aqarmap_groups

                if not common_groups:
                    st.error("❌ No common entries found across all three reports!")
                    return
                combined_dfs = []
                for df in [dubizzle_df, smsarko_df, aqarmap_df]:
                    df['Group'] = df[['ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME']].apply(tuple,
                                                                                                           axis=1)
                    filtered = df[df['Group'].isin(common_groups)]
                    combined_dfs.append(filtered.drop(columns=['Group']))

                combined_df = pd.concat(combined_dfs, ignore_index=True)

                numeric_cols = ['Price per m²', 'Rent per m²']
                for col in numeric_cols:
                    combined_df[col] = pd.to_numeric(combined_df[col], errors='coerce')

                grouped = combined_df.groupby(
                    ['ASSET_SUB_TYPE_DESC', 'ASSET_TYPE_DESC', 'GOVERNORATE_NAME', 'SECTION_NAME']
                ).agg({
                    'Price per m²': 'mean',
                    'Rent per m²': 'mean'
                }).reset_index()

                grouped['Date'] = date.today().strftime('%Y-%m-%d')
                final_df = grouped[['ASSET_TYPE_DESC', 'GOVERNORATE_NAME', 'SECTION_NAME',
                                    'Price per m²', 'Rent per m²', 'Date', 'ASSET_SUB_TYPE_DESC']]

                buffer = BytesIO()
                with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='Final Report')
                buffer.seek(0)
                file_path = os.path.join(BASE_PATH, "final_report.xlsx")
                with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
                    final_df.to_excel(writer, index=False, sheet_name='Final Report')

                st.success("✅ Final report generated and saved successfully!")
                st.download_button(
                    label="📥 Download Final Report",
                    data=buffer,
                    file_name="final_report.xlsx",
                    mime="application/vnd.ms-excel"
                )
                st.write("### Final Report Preview")
                st.dataframe(final_df)
                st.session_state["final_df"] = final_df

    # --- Button to update final report data to database ---

    if "final_df" in st.session_state:
        if st.button("🔄 Update Final Report to Database"):
            with st.spinner("Updating Final Report assets in database..."):
                final_df = st.session_state["final_df"]
                total_updated = 0
                for idx, row in final_df.iterrows():
                    asset_type_desc = row['ASSET_TYPE_DESC']
                    asset_sub_type = row['ASSET_SUB_TYPE_DESC']
                    governorate_name = row['GOVERNORATE_NAME']
                    section_name = row['SECTION_NAME']
                    price_per_m2 = row['Price per m²']
                    rent_per_m2 = row['Rent per m²']

                    matching_assets = fetch_all_matching_assets_by_keys(
                        asset_type_desc,
                        asset_sub_type,
                        governorate_name,
                        section_name
                    )

                    if matching_assets and len(matching_assets) > 0:
                        st.write(
                            f"Found {len(matching_assets)} matching assets for {asset_type_desc} in {governorate_name} - {section_name}")
                        result = process_assets_batch(matching_assets, price_per_m2, rent_per_m2)
                        if result:
                            total_updated += result.get('updated', 0)

                if total_updated > 0:
                    st.success(f"✅ Updated {total_updated} assets from Final Report in the database")
                else:
                    st.warning("No matching assets found for Final Report update.")
 
if __name__ == "__main__":
    main()