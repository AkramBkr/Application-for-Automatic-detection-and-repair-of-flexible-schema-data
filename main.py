from PyQt5 import QtCore , QtGui , QtWidgets 
from PyQt5.QtWidgets import QMessageBox
from PyQt5.QtGui import *
import sys
from pymongo import MongoClient
import json 
import tkinter as tk
from tkinter import filedialog
import json
from bson import ObjectId

def serialize_document(doc):
    if "_id" in doc:
        doc["_id"] = str(doc["_id"])
    return doc



def docdoubleee():
    
    check, total_documents, first_half ,collection = getDB()
    if check:
        unique_docs = []
        deleted_count = 0
        count = 0
        duplicates = {}

        
        for doc in first_half:
            
            unique_doc = {}
            for key, value in doc.items():
                if key == "_id":
                    continue
                if value not in unique_doc.values():
                    unique_doc[key] = value

            
            if unique_doc in unique_docs:
                
                collection.delete_one({"_id": doc["_id"]})
                deleted_count += 1
                
                duplicates[doc["_id"]] = unique_doc
            else:
                
                unique_docs.append(unique_doc)
            count += 1

        
        count_string = f"Nombre de documents en double trouvés : {deleted_count}"
        listview1.addItem(count_string)

        if deleted_count > 0:
            
            window3 = QtWidgets.QWidget()
            window3.resize(580, 510)
            window3.move(450, 120)

            lbl00 = QtWidgets.QLabel(window3)
            pixmap = QPixmap('C:\\Users\\WinTen\\Desktop\\background\\server-room-purple-uhd-4k-wallpaper.jpg').scaled(
                580, 510)
            lbl00.setPixmap(pixmap)

            listview2 = QtWidgets.QListWidget(parent=window3)
            listview2.resize(380, 420)
            listview2.move(170, 50)

            lbl01 = QtWidgets.QLabel('<b>Documents en double :</b>', window3)
            lbl01.resize(150, 21)
            lbl01.move(20, 20)
            lbl01.setStyleSheet("color: white;")

            for doc_id, duplicate_doc in duplicates.items():
                duplicate_string = f"{doc_id}: {duplicate_doc}"
                listview2.addItem(duplicate_string)

            window3.show()
            sys.exit(app.exec_())





def docdouble():
    check,total_documents ,first_half = getDB()
    if(check):
        unique_docs = []
        deleted_count = 0
        count = 0
        
        for doc in first_half :
            
            unique_doc = {}
            for key, value in doc.items():
                if key == "_id":
                    continue
                if value not in unique_doc.values():
                    unique_doc[key] = value

            
            if unique_doc in unique_docs:
              
                db.cct.delete_one({"_id": doc["_id"]})
                deleted_count += 1
            else:
              
                unique_docs.append(unique_doc)
            count +=1
        progressbar1.setValue(int ((deleted_count * 100)/count))
        print(f"Supprimé {deleted_count} documents en double.")

def countDuplicates():
    db_name = combo2.currentText()
    coll_name = combo3.currentText()

    if db_name and coll_name:
        db = client[db_name]
        collection = db[coll_name]

        unique_docs = []
        duplicates_count = 0

        for doc in collection.find():
            unique_doc = {}
            for key, value in doc.items():
                if key == "_id":
                    continue
                if value not in unique_doc.values():
                    unique_doc[key] = value

            if unique_doc in unique_docs:
                duplicates_count += 1
            else:
                unique_docs.append(unique_doc)

        return duplicates_count

    return 0




def removeDuplicates():
    db_name = combo2.currentText()
    coll_name = combo3.currentText()

    if db_name and coll_name:
        db = client[db_name]
        collection = db[coll_name]

        unique_docs = []
        deleted_count = 0

        for doc in collection.find():
            unique_doc = {}
            for key, value in doc.items():
                if key == "_id":
                    continue
                if value not in unique_doc.values():
                    unique_doc[key] = value

            if unique_doc in unique_docs:
                # Supprimer le document en double
                collection.delete_one({"_id": doc["_id"]})
                deleted_count += 1
            else:
                unique_docs.append(unique_doc)

        if deleted_count > 0:
            
            reply = QMessageBox.question(window2, "Confirmation", "Les documents redondants ont été supprimés. Voulez-vous afficher la nouvelle collection ?",
                                         QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
               
                new_collection = collection.find()

               
                listview1.clear()
                for doc in new_collection:
                    serialized_doc = serialize_document(doc)
                    doc_string = json.dumps(serialized_doc, indent=4)
                    listview1.addItem(doc_string)
        else:
            
            QMessageBox.information(window2, "Information", "Il n'y a pas de documents redondants.", QMessageBox.Ok)

    


def docdouble2(first_half):    
    unique_docs = []
    deleted_count = 0
    count = 0
    
    for doc in first_half :
        
        unique_doc = {}
        for key, value in doc.items():
            if key == "_id":
                continue
            if value not in unique_doc.values():
                unique_doc[key] = value

        
        if unique_doc in unique_docs:
            deleted_count += 1
        else:
         
            unique_docs.append(unique_doc)
        count +=1
    if count > 0 :
     progressbar1.setValue(int ((deleted_count * 100)/count))
     
    else : progressbar1.setValue (0)


def normalize_document(doc):
    
    def replace_empty_strings(obj):
        if isinstance(obj, str) and obj == "":
            return "Null",1, 1
        elif isinstance(obj, dict):
            test = {}
            count = 0
            count_all = 0
            for k, v in obj.items():
                x, y,z = replace_empty_strings(v)
                test[k] = x
                count += y
                count_all +=z 
            return test, count, count_all
        elif isinstance(obj, list):
            test = []
            count = 0
            count_all = 0
            for item in obj:
                x, y,z = replace_empty_strings(item)
                test.append(x)
                count += y
                count_all +=z 
            return test, count, count_all
        else:
            return obj, 0, 1
    func,count, count_all = replace_empty_strings(doc)
    return json.loads(json.dumps(func, default=str)), count, count_all

def normalize_document2(doc):
    
    def replace_empty_strings2(obj):
        if isinstance(obj, str) and obj == "":
            return "Null",1, 1
        elif isinstance(obj, dict):
            test = {}
            count = 0
            count_all = 0
            for k, v in obj.items():
                x, y,z = replace_empty_strings2(v)
                if(x!="Null"):
                    test[k] = x
                count += y
                count_all +=z 
            return test, count, count_all
        elif isinstance(obj, list):
            test = []
            count = 0
            count_all = 0
            for item in obj:
                x, y,z = replace_empty_strings2(item)
                if(x!="Null"):
                    test.append(x)  
                count += y
                count_all +=z 
            return test, count, count_all
        else:
            return obj, 0, 1
    func,count, count_all = replace_empty_strings2(doc)
    return json.loads(json.dumps(func, default=str)), count, count_all

def normalize_document3(doc):
    
    def replace_empty_strings(obj):
        if isinstance(obj, str) and obj == "":
            return "",1, 1
        elif isinstance(obj, dict):
            test = {}
            count = 0
            count_all = 0
            for k, v in obj.items():
                x, y,z = replace_empty_strings(v)
                test[k] = x
                count += y
                count_all +=z 
            return test, count, count_all
        elif isinstance(obj, list):
            test = []
            count = 0
            count_all = 0
            for item in obj:
                x, y,z = replace_empty_strings(item)
                test.append(x)
                count += y
                count_all +=z 
            return test, count, count_all
        else:
            return obj, 0, 1
    func,count, count_all = replace_empty_strings(doc)
    return json.loads(json.dumps(func, default=str)), count, count_all




def open_file():
    
    file_path = filedialog.askopenfilename(filetypes=[("Fichier JSON", "*.json")])
    
    
    if file_path:
        
        with open(file_path, "r") as f:
            data = json.load(f)
            
            
            print(data)

def import_json():
    # Open a file dialog to select a JSON file
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if not file_path:
        return

    # Open the selected file and load the JSON data
    with open(file_path, 'r') as file:
        json_data = json.load(file)

    # Choose the database and collection to add the JSON data to
    db_name = 'my_database'
    collection_name = 'my_collection'
    db = client[db_name]
    collection = db[collection_name]

    # Insert the JSON data into the collection
    result = collection.insert_many(json_data)
    print(f"Imported {len(result.inserted_ids)} documents into '{db_name}.{collection_name}'")


def show_databases():
    global db_var  
    
    client = MongoClient("mongodb://localhost:27017/")

    
    databases = client.list_database_names()

    
    db_window = tk.Toplevel(root)
    db_window.title("Choisir une base de données")

    
    choose_db_label = tk.Label(db_window, text="Choisir votre base de données:")
    choose_db_label.pack()

    
    db_var = tk.StringVar(db_window)
    db_var.set(databases[0]) 
    db_dropdown = tk.OptionMenu(db_window, db_var, *databases)
    db_dropdown.pack()

 
def update_collections():
    db_name = combo2.currentText()
    if db_name:
        db = client[db_name]
        combo3.clear()
        combo3.addItem("...")
        for coll_name in db.list_collection_names():
            combo3.addItem(coll_name)


def getDB():
    db_name = combo2.currentText()
    if db_name:
        db = client[db_name]
        combo3.clear()
    
        for coll_name in db.list_collection_names():
            combo3.addItem(coll_name)

        coll_name = combo3.currentText()
        if coll_name:
            
            collection = db[coll_name]
            total_documents = collection.count_documents({})

            
            half_documents = total_documents // 1
            first_half = collection.find().limit(half_documents)
            return True, total_documents,first_half
    return False
    

def calculate_average_missing_values():
    check,total_documents ,first_half = getDB()
    if(check):
        total_missing_values = {}
        for document in first_half:
            for field in document:
                if field not in total_missing_values:
                    total_missing_values[field] = 0
                if document[field] is None or document[field] == "":
                    total_missing_values[field] += 1

        average_missing_values = {}
        for field in total_missing_values:
            average_missing_values[field] = round((total_missing_values[field] / total_documents) * 100, 2)

        
        total_average = sum(average_missing_values.values()) / len(average_missing_values)
        progressbar2 = QtWidgets.QProgressBar(window)
        progressbar2.resize(81,23)
        progressbar2.move(240,390)
        progressbar2.setValue(int(total_average))
        progressbar2.show()

def affbdd():
    db_name = combo2.currentText()
    coll_name = combo3.currentText()

    if db_name and coll_name:
        db = client[db_name]
        collection = db[coll_name]

        countAllNull = 0
        countAll = 0
        x = 0
        data = []  

        for document in collection.find():
            normalized_doc, countNull, count = normalize_document3(document)
            countAll += count
            countAllNull += countNull
            data.append(json.dumps(normalized_doc, indent=4))  
            x += 1
            

        countAllString = f'Le nombre de toutes les lignes est : {countAll}'
        countAllNullString = f'Le nombre de toutes les valeurs manquantes est : {countAllNull}'

        
        listview1.clear()  
        listview1.addItem(countAllString) 
        listview1.addItem(countAllNullString) 
        listview1.addItems(data)  


def test():
    check,total_documents ,first_half  = getDB()
    if(check):
        countAllNull = 0
        countAll = 0
        x=0
        data = []  
        unique_docs = []
        deleted_count = 0
        count = 0
        duplicates = {}

        for document in first_half:
            normalized_doc, countNull,count = normalize_document3(document)
            countAll += count
            countAllNull += countNull
            
            data.append(json.dumps(normalized_doc, indent=4))  
            x+= 1
            if(x== 100):
                break
        
        
        for doc in first_half:
            
            unique_doc = {}
            for key, value in doc.items():
                if key == "_id":
                    continue
                if value not in unique_doc.values():
                    unique_doc[key] = value

            
            if unique_doc in unique_docs:
                
                deleted_count += 1
                
                duplicates[doc["_id"]] = unique_doc
            else:
                
                unique_docs.append(unique_doc)
            count += 1

        
        cc = countDuplicates()
        count_string = f"Nombre de documents en double trouvés : {cc}"
        listview1.addItem(count_string)

        countAllString = f'Le nombre de tous ligne est :  {countAll}'
        
        countAllNullString = f'le nombre de tous les valeures manquantes est :  {countAllNull}'
        if countAll > 0:
         countAllNullPercentageString = f'Le pourcentage du valeures manquante est :  {int((countAllNull * 100) / countAll)} %'
        else :
            countAllNullPercentageString = f'Le pourcentage du valeures manquante est :  {int((countAllNull * 100) / 1)} %'

        listview1.addItem(countAllString)  
        listview1.addItem(countAllNullString) 
        listview1.addItem(countAllNullPercentageString) 



        progressbar3 = QtWidgets.QProgressBar(window2)
        progressbar3.resize(81,23)
        progressbar3.move(240,500)
        if countAll > 0:
         progressbar3.setValue(int(((cc * 100) / countAll)))
        else :
            progressbar3.setValue(int(((cc * 100) / 1)))


        progressbar3.show()
        docdouble2(first_half)
        
        progressbar2 = QtWidgets.QProgressBar(window2)
        progressbar2.resize(81,23)
        progressbar2.move(240,540)
        if countAll > 0:
         countAllNullPercentageString = f'Le pourcentage du valeures manquante est :  {int((countAllNull * 100) / countAll)} %'
        else:
         countAllNullPercentageString = f'Le pourcentage du valeures manquante est :  {int((countAllNull * 100) / 1)} %'

        # ...

        if countAll > 0:
         progressbar2.setValue(int(((countAllNull * 100) / countAll)))
        else:
         progressbar2.setValue(0)


        progressbar2.show()
        window2.show()
        window.hide()
    

        

    

def test3():
    check,total_documents ,first_half = getDB()
    if(check):
        countAllNull = 0
        countAll = 0
        x=0
        for document in first_half:
            normalized_doc, countNull,count = normalize_document(document)
            countAll += count
            countAllNull += countNull
            normalized_doc_string1 = json.dumps(normalized_doc, indent=4)
            #print(normalized_doc_string)
            listview1.addItem(normalized_doc_string1)
            x+= 1
            
            

       
       

def test2():
    check,total_documents ,first_half = getDB()
    if(check):
        countAllNull = 0
        countAll = 0
        x=0
        for document in first_half:
            normalized_doc, countNull,count = normalize_document2(document)
            countAll += count
            countAllNull += countNull
            normalized_doc_string = json.dumps(normalized_doc, indent=4)

            listview1.addItem(normalized_doc_string)
            if(x== 100):
                break

       
app=QtWidgets.QApplication(sys.argv)
window = QtWidgets.QWidget ()
window.resize(780,500)
window.move(320,70)
window.setWindowTitle('RQDB Plus ')
window.setWindowIcon(QtGui.QIcon('C:\\Users\\WinTen\\Desktop\\background\\x4.png'))


window2 = QtWidgets.QWidget ()
window2.setWindowTitle('RQDB Plus ')
window2.resize(600,610)
window2.move(450,50)
window2.setWindowIcon(QtGui.QIcon('C:\\Users\\WinTen\\Desktop\\background\\x4.png'))


lbl00 = QtWidgets.QLabel(window2)
pixmap = QPixmap('C:\\Users\\WinTen\\Desktop\\background\\a11.jpg').scaled(800,610)
lbl00.setPixmap(pixmap)

listview1 = QtWidgets.QListWidget(parent=window2)
listview1.resize(380,360)
listview1.move(170,50)

lbl01=QtWidgets.QLabel('<b> Resultat d affichage :  <\b> : ',window2)
lbl01.resize(120,21)
lbl01.move(20,130)
lbl01.setStyleSheet("color: white;") 

lbl0 = QtWidgets.QLabel(window)
pixmap = QPixmap('C:\\Users\\WinTen\\Desktop\\background\\a11.jpg').scaled(780,500)
lbl0.setPixmap(pixmap)



lbl1=QtWidgets.QLabel('<b> Choisir un fichie JSON <\b> : ',window)
lbl1.resize(150,21)
lbl1.move(20,150)
lbl1.setStyleSheet("color: white;") 



btn2 = QtWidgets.QPushButton(' Importer  ',window)
btn2.resize(85,27)
btn2.move(210,150)
btn2.clicked.connect(import_json)
btn2.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 10px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn2 {
    color: black;
    font-weight: bold;
}
""")
btn2.setObjectName("btn2")


lbl2=QtWidgets.QLabel('<b> Connecté MongoDB <\b> : ',window)
lbl2.resize(131,21)
lbl2.move(20,200)
lbl2.setStyleSheet("color: white;") # Définir la couleur du texte en blanc



client = MongoClient("mongodb://localhost:27017/")

db_names = client.list_database_names()


combo_style = """
    QComboBox {
        border: 2px solid gray;
        border-radius: 10px;
        padding: 1px 18px 1px 3px;
        min-width: 6em;
    }
    QComboBox:editable {
        background-color: black;
        color: black;
    }
    QComboBox:!editable, QComboBox::drop-down:editable {
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                          stop:0 #E1E1E1, stop:0.4 #DDDDDD,
                                          stop:0.5 #D8D8D8, stop:1.0 #D3D3D3);
    }
    QComboBox:!editable:on, QComboBox::drop-down:editable:on {
        background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                                    stop:0 #D3D3D3, stop:0.4 #D8D8D8,
                                    stop:0.5 #DDDDDD, stop:1.0 #E1E1E1);
    }
    QComboBox::drop-down {
        subcontrol-origin: padding;
        subcontrol-position: top right;
        width: 20px;
        border-left-width: 1px;
        border-left-color: darkgray;
        border-left-style: solid;
        border-top-right-radius: 10px;
        border-bottom-right-radius: 10px;
    }
    QComboBox::down-arrow {
        image: url(down_arrow.png);
        width: 12px;
        height: 12px;
    }
    QComboBox::down-arrow:on {
        top: 1px;
        left: 1px;
    }
"""


combo2 = QtWidgets.QComboBox(window)
combo2.resize(181,22)
combo2.move(160,200)
combo2.addItem(" Veuillez choisir une DB ")
combo2.setStyleSheet(combo_style)
for db_name in db_names:
    combo2.addItem(db_name)




lbl3=QtWidgets.QLabel('<b> Choisir votre collection <\b> : ',window)
lbl3.resize(131,21)
lbl3.move(360,200)
lbl3.setStyleSheet("color: white;") 


app.setStyle("Fusion")


combo3 = QtWidgets.QComboBox(window)
combo3.resize(181,22)
combo3.move(520,200)
combo3.setStyleSheet(combo_style)
combo3.addItem("Veuillez choisir une collection")
combo2.currentTextChanged.connect(update_collections)




lbl4=QtWidgets.QLabel('<b> Comance le controle  <\b> : ',window)
lbl4.resize(211,21)
lbl4.move(20,280)
lbl4.setStyleSheet("color: white;") 

btn4 = QtWidgets.QPushButton(' Start  ',window)
btn4.resize(100,27)
btn4.move(180,280)
btn4.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 10px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn4 {
    color: black;
    font-weight: bold;
}
""")
btn4.setObjectName("btn4")
btn4.clicked.connect(test)

lbl5=QtWidgets.QLabel('<b> Le taux des documentsredandant <\b> : ',window2)
lbl5.resize(191,21)
lbl5.move(10,500)
lbl5.setStyleSheet("color: white;") 

btn5 = QtWidgets.QPushButton(' Supprimer les doc en double  ',window2)
btn5.resize(211,27)
btn5.move(350,500)
btn5.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 10px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn5 {
    color: black;
    font-weight: bold;
}
""")
btn5.setObjectName("btn5")
btn5.clicked.connect(removeDuplicates)






lbl6=QtWidgets.QLabel('<b> Le taux des valeures manquantes <\b> : ',window2)
lbl6.resize(191,21)
lbl6.move(10,540)
lbl6.setStyleSheet("color: white;") # Définir la couleur du texte en blanc

btn6 = QtWidgets.QPushButton(' Supprimer les valeures manquantes  ',window2)
btn6.resize(220,27)
btn6.move(350,540)
btn6.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 10px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn6 {
    color: black;
    font-weight: bold;
}
""")

progressbar1= QtWidgets.QProgressBar(window2)
progressbar1.resize(81,23)
progressbar1.move(240,500)

btn6.setObjectName("btn6")
btn6.clicked.connect(test2)

btn7 = QtWidgets.QPushButton(' Null par-defaut  ',window2)
btn7.resize(101,27)
btn7.move(350,570)
btn7.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 10px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn7 {
    color: black;
    font-weight: bold;
}
""")
btn7.setObjectName("btn7")
btn7.clicked.connect(test3)




btn8 = QtWidgets.QPushButton(' Afficher votre BDD  ',window2)
btn8.resize(151,41)
btn8.move(400,430)
btn8.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 20px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn8 {
    color: black;
    font-weight: bold;
}
""")
btn8.setObjectName("btn8")
btn8.clicked.connect(affbdd)

btn9 = QtWidgets.QPushButton('Vider le tableau',window2)
btn9.resize(151,41)
btn9.move(250,430)
btn9.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 20px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn9 {
    color: black;
    font-weight: bold;
}
""")
btn9.setObjectName("btn9")
btn9.clicked.connect(listview1.clear)

btn10 = QtWidgets.QPushButton('Retour',window2)
btn10.resize(110,25)
btn10.move(490,10)
btn10.setStyleSheet("""
QPushButton {
    border: 2px solid #4d4d4d;
    border-radius: 20px;
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #fff, stop: 1 #888);
    padding: 5px;
    color: white;
}
QPushButton:hover {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #f2f2f2, stop: 1 #666);
}
QPushButton:pressed {
    background-color: qradialgradient(cx: 0.3, cy: -0.4,
                                      fx: 0.3, fy: -0.4,
                                      radius: 1.35,
                                      stop: 0 #ddd, stop: 1 #555);
}
QPushButton#btn10 {
    color: black;
    font-weight: bold;
}
""")
btn10.setObjectName("btn10")
btn10.clicked.connect(window.show)
btn10.clicked.connect(window2.hide)



window.show()
#window2.show()
app.exec_()

