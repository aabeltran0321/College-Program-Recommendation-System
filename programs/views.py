from django.shortcuts import render
from .create_db import create_database
import random
import pandas as pd
import joblib
import json
from django.contrib import messages
from django.core.files.storage import FileSystemStorage

# Image finder/loader from "programs/static/media" and saving it for fast loading
def handle_uploaded_file(f,filename):
    
    with open('./programs/static/media/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

class MyViews:
    # Initializing all variable needed for later use of the system.
    def __init__(self) -> None:
        self.nickname = ""
        self.gwa = 0.0
        self.db1 = create_database("./programs/database.db")
        self.dictConv={
            "gen_info": "General Information",
            "science": "Science",
            "verbal_reasoning": "Verbal Reasoning",
            "abstract_reasoning": "Abstract Reasoning",
            "numerical_reasoning": "Numerical Reasoning",
        }

        self.answer_keys={
            "gen_info": [],
            "science": [],
            "verbal_reasoning": [],
            "abstract_reasoning": [],
            "numerical_reasoning": [],
        }
        

        self.total_score={
            "gen_info": 0.0,
            "science": 0.0,
            "verbal_reasoning": 0.0,
            "abstract_reasoning": 0.0,
            "numerical_reasoning": 0.0,
        }

        # Loading the courses
        self.dept_course =pd.read_csv('./programs/Department_Courses.tsv', sep='\t')

        # Loading the Actual trained model and mapping the ordered label for corresponding value.
        self.model = joblib.load("./programs/regression.pkl")
        f = open("./programs/labelmap.json")
        self.labelmap = json.load(f)

        f.close()
        self. nickname = ""
        self.GWA = 0.0


    # Block of code where the prediction occured
    def predict_courses(self,GWA,GI,SCI,NR,VR,AR):
        if GWA>0 and GI>0 and SCI>0 and NR>0 and AR>0:
            Y_pred_rf_proba = list(self.model.predict_proba([[GWA,GI,SCI,NR,VR,AR]])[0])
            Y_pred_rf_proba = self.sort_index(Y_pred_rf_proba)

            return_data = []
            print(Y_pred_rf_proba[:3])
            for x in Y_pred_rf_proba[:3]:
                str1 = self.labelmap[str(x+1)].replace("BS", "Bachelor of Science")
                str1 = str1.title()
                return_data.append(str1)
            

            return  return_data
        return ["","",""]

    def sort_index(self,lst, rev=True):
        index = range(len(lst))
        s = sorted(index, reverse=rev, key=lambda i: lst[i])
        return s

    def home(self,request):
        return render(request, 'programs/edithome.html')
    def admin_login(self,request):
        return render(request, 'programs/admin.html')
    def admin_home(self,request):
        if request.method == "POST":
            try:
                if request.POST['username'] == "admin" and request.POST['password'] == "admin123":
                    return render(request, 'programs/admin_home.html')
                else:
                    messages.success(request, 'Invalid Credentials!')
                    return render(request, 'programs/admin.html')
            except:
                category = self.dictConv[request.POST["subjects"]]
                question = request.POST["question"]
                choice_a = request.POST["choice_a"]
                choice_b = request.POST["choice_b"]
                choice_c = request.POST["choice_c"]
                choice_d = request.POST["choice_d"]
                correctanswer = request.POST["correct_answer"]
                pathtoimage = request.FILES["filename"]

                
                fss = FileSystemStorage()
                file = fss.save(pathtoimage.name, pathtoimage)
                file_url = fss.url(file)
                print(file_url)

                self.db1.insertQuestion(category,question,choice_a,choice_b,choice_c,choice_d,correctanswer,str(pathtoimage))
                pass
            return render(request, 'programs/admin_home.html')
        return render(request, 'programs/admin.html')

    # The actual block of code that calculate and request the prediction courses.
    def results(self,request):
        if request.method == "POST":
            self.check_answer_sheet(request,self.answer_keys["abstract_reasoning"],"abstract_reasoning")
            print(self.total_score)
            GI = self.total_score["gen_info"]
            SCI = self.total_score["science"]
            NR = self.total_score["numerical_reasoning"]
            VR = self.total_score["verbal_reasoning"]
            AR = self.total_score["abstract_reasoning"]

            self.results = self.predict_courses(float(self.GWA),GI,SCI,NR,VR,AR)

            #print(self.results)
            dict2 = {
            "choice_1": self.results[0],
            "choice_2": self.results[1],
            "choice_3": self.results[2],
            "score_1": GI,
            "score_2": SCI,
            "score_3": NR,
            "score_4": VR,
            "score_5": AR,
            }


            if len(self.results[0])>0:
                nickname = request.POST['submits']
                while (nickname!=self.nickname):
                    pass
                return render(request, 'programs/editedresult.html' , dict2)

        return render(request, 'programs/redirecting.html')

    # Homepage Rendering Request
    def intro(self,request):
        if request.method == "POST":
            self. nickname = request.POST['nickname']
            self.GWA = float(request.POST['gwa'])
            print(self.GWA)

            dict1 = {
                "nickname": self.nickname,
                }
            return render(request, 'programs/editedintro.html', dict1)
        return render(request, 'programs/redirecting.html')


    # General Information Page
    def gen_info(self,request):
        if request.method == "POST":
            return render(request, 'programs/editedgeninfo.html', self.load_questionnaire("gen_info")) 
        return render(request, 'programs/redirecting.html')


    # Science Page
    def science(self,request):
        if request.method == "POST":
            self.check_answer_sheet(request,self.answer_keys["gen_info"],"gen_info")
            
            return render(request, 'programs/editedscience.html' , self.load_questionnaire("science"))
        return render(request, 'programs/redirecting.html')


    # Numerical Reasoning Page
    def numerical_reasoning(self,request):
        
        if request.method == "POST":
            self.check_answer_sheet(request,self.answer_keys["science"],"science")
            
            return render(request, 'programs/editednumerical.html' , self.load_questionnaire("numerical_reasoning"))
        return render(request, 'programs/redirecting.html')


    # Verbal Reasoning Page
    def verbal_reasoning(self,request):
        
        if request.method == "POST":
            self.check_answer_sheet(request,self.answer_keys["numerical_reasoning"],"numerical_reasoning")
            
            return render(request, 'programs/editedverbal.html' , self.load_questionnaire("verbal_reasoning"))
        return render(request, 'programs/redirecting.html')


    # Abstract Reasoning Page
    def abstract_reasoning(self,request):
        
        if request.method == "POST":
            self.check_answer_sheet(request,self.answer_keys["verbal_reasoning"],"verbal_reasoning")
            
            return render(request, 'programs/editedabstract.html' , self.load_questionnaire("abstract_reasoning"))
        return render(request, 'programs/redirecting.html')


    # Autoload Questionnaire
    def load_questionnaire(self,subject=""):

        # Initializing the subjects questions
        data = list(self.db1.getQuestionsByCat(self.dictConv[subject]))
        if not("abstract" in subject):
            random.shuffle(data)
        dict1 = {
            subject+"_question_1" : "No Question Added in Database",
            subject+"_choices_1a" : "NO Choice A",
            subject+"_choices_1b" : "NO Choice B",
            subject+"_choices_1c" : "NO Choice C",
            subject+"_choices_1d" : "NO Choice D",
        }

        dict2 = {}
        # Only first 40 questionnaire
        for i in range(40):
            try:
                choices = list(data[i][2:6])
                if not("abstract" in subject):
                    random.shuffle(choices)
                    
                    if isinstance(data[i][7],str):
                        dict2[subject+"_pic_"+str(i+1)] = data[i][7]
                    else:
                        dict2[subject+"_pic_"+str(i+1)] = "empty.png"
                else:
                    dict2[subject+"_pic_"+str(i+1)] = "abstract %s.png" %(i+1)
                dict2[subject+"_question_"+str(i+1)] = data[i][1]
                dict2[subject+"_choices_"+str(i+1) +"a"] = choices[0]
                dict2[subject+"_choices_"+str(i+1) +"b"] = choices[1]
                dict2[subject+"_choices_"+str(i+1) +"c"] = choices[2]
                dict2[subject+"_choices_"+str(i+1) +"d"] = choices[3]
                

                self.answer_keys[subject].append(data[i][6])

            except:
                dict2[subject+"_question_"+str(i+1)] = dict1[subject+"_question_1"]
                dict2[subject+"_choices_"+str(i+1) +"a"] = dict1[subject+"_choices_1a"]
                dict2[subject+"_choices_"+str(i+1) +"b"] = dict1[subject+"_choices_1b"]
                dict2[subject+"_choices_"+str(i+1) +"c"] = dict1[subject+"_choices_1c"]
                dict2[subject+"_choices_"+str(i+1) +"d"] = dict1[subject+"_choices_1d"]
                self.answer_keys[subject].append("")

        dict2["nickname_1"] = self.nickname
        return dict2


    # Check answer sheet function
    def check_answer_sheet(self,request,answersheet,subject):
        lst = []
        #print(request.POST)
        for a in range(40):
            try:
                lst.append(answersheet[a]==request.POST[subject+'_choices_'+str(a+1)])
                # print(subject+'_choices_'+str(a+1))
                print(lst)
            except:
                lst.append(False)
        if not("abstract" in subject):
            self.total_score[subject] = float(sum(lst)/40)*100.0
        else:
            self.total_score[subject] = float(sum(lst)/20)*100.0
        print(self.total_score[subject])