xx = """<input type="radio" id="%s" name="%s" value="{{ %s }}">
<label for="%s">{{ %s }}</label><br>"""

yy= '<img src="/static/media/{{abstract_reasoning_pic_%s}}" alt="" width="60" height="300" style="position: absolute; left: 0;">'
# 1,1,1a,1,1a
topic1 = "abstract_reasoning_question_"
topic2 = "abstract_reasoning_choices_"

for i in range(20):
    print( yy % (i+1,))
    print("<br><br><br><br><br><br><br><br><br><br>")
    #print('<label for="fname">%s. {{ %s }}</label><br><br>' % (i+1,topic1 + str(i+1)))
    for alpha in range(4):
        print(xx % (topic2+str(i+1),topic2+str(i+1),topic2+str(i+1)+chr(97+alpha),topic2+str(i+1),topic2+str(i+1)+chr(97+alpha)))
    print(chr(13)+chr(13)+"<br><br>"+chr(13)+chr(13))