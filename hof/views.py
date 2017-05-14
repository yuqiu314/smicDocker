#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import xlrd
from django.shortcuts import get_object_or_404, get_list_or_404, render
from django import forms
from django.contrib.admin.views.decorators import staff_member_required 
from django.http import HttpResponseRedirect  
from django.conf import settings
from .models import VisitCount, Employee
from .models import Choice, Poll, Vote, VotedEmp, Article

def grade(score, max, grades):
    return (grades*score+max-1)/max

class DataInput(forms.Form):
    file = forms.FileField()

    def save(self):
        input_excel = self.cleaned_data["file"]
        logs = []
        
        try:
            data = xlrd.open_workbook(file_contents=input_excel.read())
            table = data.sheet_by_name(u'S1名单')
            score_table = data.sheet_by_name(u'最新数据')
        except:
            logs.append(u'无法找到“S1名单”或者“最新数据”页面，请检查上传文件！')
            return logs
            
        dict = {}
        logs.append(u'开始录入S1名单数据，共%d条...' % (table.nrows-1))
        for rownum in range(1, table.nrows):
            row = table.row_values(rownum)
            if not row:
               logs.append(u'第%d条数据为空！' % rownum)
            else:
                emp = Employee()
                emp.id              = row[1].upper()
                emp.chinesename     = row[2]
                emp.preferredname   = row[3]
                emp.division        = row[4]
                emp.depart          = row[5]
                emp.section         = row[6]
                emp.hc              = row[7]
                emp.bcnt            = 0
                emp.bscore          = 0
                emp.brank           = 0
                emp.bgrade          = 0
                emp.ccnt            = 0
                emp.cscore          = 0
                emp.crank           = 0
                emp.cgrade          = 0
                emp.icnt            = 0
                emp.iscore          = 0
                emp.irank           = 0
                emp.igrade          = 0
                emp.qcnt            = 0
                emp.qscore          = 0
                emp.qrank           = 0
                emp.qgrade          = 0
                emp.cocnt           = 0
                emp.coscore         = 0
                emp.corank          = 0
                emp.cograde         = 0
                emp.totalcnt        = 0
                emp.totalscore      = 0
                emp.totalrank       = 0
                emp.totalgrade      = 0
                emp.showcnt         = 0
                emp.showscore       = 0
                emp.showrank        = 0
                emp.showgrade       = 0
                if not emp.id:
                    logs.append(u'第%d条数据异常：ID不能为空！' % rownum)
                elif u'离职' in emp.chinesename:
                    logs.append(u'第%d条数据：%s已经离职，不予记录。' % (rownum, emp.chinesename))
                elif u'转职' in emp.chinesename:
                    logs.append(u'第%d条数据：%s已经转职，不予记录。' % (rownum, emp.chinesename))
                elif u'不计' in emp.chinesename:
                    logs.append(u'第%d条数据：%s已经注明，不予记录。' % (rownum, emp.chinesename))
                elif dict.get(emp.id):
                    logs.append(u'第%d条数据：ID重复，不予记录。' % rownum)
                else:
                    dict[emp.id] = emp
        logs.append(u'员工名单录入完毕。')
        logs.append(u'开始统计获奖得分，共%d条...' % (score_table.nrows-1))
        for rownum in range(1, score_table.nrows):
            row = score_table.row_values(rownum)
            if not dict.get(row[1]):
                logs.append(u'第%d条数据：ID对应员工记录不存在，不予记录。' % rownum)
            elif row[6]==u'Behavior':
                dict.get(row[1]).bcnt += 1
                dict.get(row[1]).bscore += row[9]
                dict.get(row[1]).totalcnt += 1
                dict.get(row[1]).totalscore += row[9]
            elif row[6]==u'Capacity':
                dict.get(row[1]).ccnt += 1
                dict.get(row[1]).cscore += row[9]
                dict.get(row[1]).totalcnt += 1
                dict.get(row[1]).totalscore += row[9]
            elif row[6]==u'Innovation':
                dict.get(row[1]).icnt += 1
                dict.get(row[1]).iscore += row[9]
                dict.get(row[1]).totalcnt += 1
                dict.get(row[1]).totalscore += row[9]
            elif row[6]==u'Quality':
                dict.get(row[1]).qcnt += 1
                dict.get(row[1]).qscore += row[9]
                dict.get(row[1]).totalcnt += 1
                dict.get(row[1]).totalscore += row[9]
            elif row[6]==u'Cost':
                dict.get(row[1]).cocnt += 1
                dict.get(row[1]).coscore += row[9]
                dict.get(row[1]).totalcnt += 1
                dict.get(row[1]).totalscore += row[9]
        logs.append(u'得分统计完毕。')        
        
        logs.append(u'开始计算排名...')
        l = dict.values()
        #b
        l.sort(key=lambda x:x.bscore, reverse=True)
        bmax = l[0].bscore
        l[0].brank = 1
        dupcount = 0
        prev = l[0]
        for e in l[1:]:
            if e.bscore == prev.bscore:
                e.brank = prev.brank
                dupcount += 1
            else:
                e.brank = prev.brank + dupcount + 1
                dupcount = 0
                prev = e
        #c
        l.sort(key=lambda x:x.cscore, reverse=True)
        cmax = l[0].cscore
        l[0].crank = 1
        dupcount = 0
        prev = l[0]
        for e in l[1:]:
            if e.cscore == prev.cscore:
                e.crank = prev.crank
                dupcount += 1
            else:
                e.crank = prev.crank + dupcount + 1
                dupcount = 0
                prev = e
        #i
        l.sort(key=lambda x:x.iscore, reverse=True)
        imax = l[0].iscore        
        l[0].irank = 1
        dupcount = 0
        prev = l[0]
        for e in l[1:]:
            if e.iscore == prev.iscore:
                e.irank = prev.irank
                dupcount += 1
            else:
                e.irank = prev.irank + dupcount + 1
                dupcount = 0
                prev = e
        #q
        l.sort(key=lambda x:x.qscore, reverse=True)
        qmax = l[0].qscore        
        l[0].qrank = 1
        dupcount = 0
        prev = l[0]
        for e in l[1:]:
            if e.qscore == prev.qscore:
                e.qrank = prev.qrank
                dupcount += 1
            else:
                e.qrank = prev.qrank + dupcount + 1
                dupcount = 0
                prev = e
        #co
        l.sort(key=lambda x:x.coscore, reverse=True)    
        comax = l[0].coscore
        l[0].corank = 1
        dupcount = 0
        prev = l[0]
        for e in l[1:]:
            if e.coscore == prev.coscore:
                e.corank = prev.corank
                dupcount += 1
            else:
                e.corank = prev.corank + dupcount + 1
                dupcount = 0
                prev = e
        #total
        l.sort(key=lambda x:x.totalscore, reverse=True)    
        totalmax = l[0].totalscore
        l[0].totalrank = 1
        dupcount = 0
        prev = l[0]
        for e in l[1:]:
            if e.totalscore == prev.totalscore:
                e.totalrank = prev.totalrank
                dupcount += 1
            else:
                e.totalrank = prev.totalrank + dupcount + 1
                dupcount = 0
                prev = e
        
        for e in l:
            e.bgrade = grade(e.bscore, bmax, 5)
            e.cgrade = grade(e.cscore, cmax, 5)
            e.igrade = grade(e.iscore, imax, 5)
            e.qgrade = grade(e.qscore, qmax, 5)
            e.cograde = grade(e.coscore, comax, 5)
            e.totalgrade = grade(e.totalscore, totalmax, 15)
            
        logs.append(u'排名计算完毕。')
        #首先清空Employee表，然后将新的数据写入
        Employee.objects.all().delete()
        Employee.objects.bulk_create(l)
        logs.append(u'一共录入了%d名员工的数据。' % Employee.objects.all().count())
        
        return logs
        
# Create your views here.
def index(request):
    visit_count = VisitCount.objects.get()
    visit_count.cnt = visit_count.cnt + 1
    visit_count.save()
    context = {
        'visit_count': visit_count.cnt,
        'e_list': Employee.objects.filter(hc='Non-MA/TA').order_by('-totalscore')[0:10]}
    return render(request, 'hof/index.html', context)
    
@staff_member_required
def admin_update_data(request):
    if request.method == "POST":
        form = DataInput(request.POST, request.FILES)
        if form.is_valid():
            logs = form.save()
            context = {"form": form, "success": True, "logs": logs}
            return render(request, "hof/admin_update_data.html", context)
    else:
        form = DataInput()        
        context = {"form": form}
        return render(request, "hof/admin_update_data.html", context)
        
def top5(request):
    context = {
        'b_list': Employee.objects.order_by('-bscore')[0:5],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_list': Employee.objects.order_by('-cscore')[0:5],
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_list': Employee.objects.order_by('-iscore')[0:5],
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_list': Employee.objects.order_by('-qscore')[0:5],
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_list': Employee.objects.order_by('-coscore')[0:5],
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,}
    return render(request, 'hof/top5/index.html', context)
        
def top5b(request):
    context = { 
        'emp_list': Employee.objects.order_by('-bscore')[0:5],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'type': 'Behavior',
        'atype': 'b',
        'color': '#2980b9',
        'show_max': Employee.objects.order_by('-bscore')[0].bscore,}
    for e in context['emp_list']:
        e.showcnt = e.bcnt
        e.showscore = e.bscore
        e.showrank = e.brank
        e.showgrade = e.bgrade
    return render(request, 'hof/top5b/index.html', context)

def top5c(request):
    context = {
        'emp_list': Employee.objects.order_by('-cscore')[0:5],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'type': 'Capacity',
        'atype': 'c',
        'color': '#8e44ad',
        'show_max': Employee.objects.order_by('-cscore')[0].cscore,}
    for e in context['emp_list']:
        e.showcnt = e.ccnt
        e.showscore = e.cscore
        e.showrank = e.crank
        e.showgrade = e.cgrade
    return render(request, 'hof/top5b/index.html', context)
    
def top5i(request):
    context = { 
        'emp_list': Employee.objects.order_by('-iscore')[0:5],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'type': 'Innovation',
        'atype': 'i',
        'color': '#27ae60',
        'show_max': Employee.objects.order_by('-iscore')[0].iscore,}
    for e in context['emp_list']:
        e.showcnt = e.icnt
        e.showscore = e.iscore
        e.showrank = e.irank
        e.showgrade = e.igrade
    return render(request, 'hof/top5b/index.html', context)
    
def top5q(request):
    context = { 
        'emp_list': Employee.objects.order_by('-qscore')[0:5],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'type': 'Quality',
        'atype': 'q',
        'color': '#2c3e50',
        'show_max': Employee.objects.order_by('-qscore')[0].qscore,}
    for e in context['emp_list']:
        e.showcnt = e.qcnt
        e.showscore = e.qscore
        e.showrank = e.qrank
        e.showgrade = e.qgrade
    return render(request, 'hof/top5b/index.html', context)
    
def top5co(request):
    context = { 
        'emp_list': Employee.objects.order_by('-coscore')[0:5],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'type': 'Cost',
        'atype': 'co',
        'color': '#16a085',
        'show_max': Employee.objects.order_by('-coscore')[0].coscore,}
    for e in context['emp_list']:
        e.showcnt = e.cocnt
        e.showscore = e.coscore
        e.showrank = e.corank
        e.showgrade = e.cograde
    return render(request, 'hof/top5b/index.html', context)
    
def top10(request):
    context = {
        'e_list': Employee.objects.filter(hc='Non-MA/TA').order_by('-totalscore')[0:10],
        'm_list': Employee.objects.filter(hc='MA/TA', division='MFG').order_by('-totalscore')[0:10],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'total_e_max': Employee.objects.filter(hc='Non-MA/TA').order_by('-totalscore')[0].totalscore,
        'total_m_max': Employee.objects.filter(hc='MA/TA', division='MFG').order_by('-totalscore')[0].totalscore,}
    return render(request, 'hof/top10/index.html', context)
    
def top10e(request):
    context = {
        'emp_list': Employee.objects.filter(hc='Non-MA/TA').order_by('-totalscore')[0:10],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'show_max': Employee.objects.filter(hc='Non-MA/TA').order_by('-totalscore')[0].totalscore,
        'type': u'工程师组',
        'color': '#d35400',}
    return render(request, 'hof/top10e/index.html', context)
    
def top10m(request):
    context = {
        'emp_list': Employee.objects.filter(hc='MA/TA', division='MFG').order_by('-totalscore')[0:10],
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,
        'show_max': Employee.objects.filter(hc='MA/TA', division='MFG').order_by('-totalscore')[0].totalscore,
        'type': u'制造部MA-TA组',
        'color': '#d35400',}
    return render(request, 'hof/top10e/index.html', context)
    
def me(request):
    '''
    这里我用了最简单的cookie方式来
    以下三行代码的意思如下：
    如果不存在登陆的用户smic_eid这个cookie，则跳转至某个登陆页面
    在完成登陆以后再跳转回这个'xx:8000/me/'地址即可
    如果用其他逻辑实现也可以，有任何疑问都可以联系我。
    注销的逻辑会在登陆逻辑明确以后补完。
    '''
    #cookie = request.COOKIES.get('login_user', '')
    cookie = request.GET.get('u')
    if  not cookie or not Employee.objects.filter(id = cookie.upper()):
        context2 = {'not_found':cookie}
        return render(request, 'hof/me/index2.html', context2)
    context = { 
        'emp_list': Employee.objects.filter(id = cookie.upper()),
        'b_max': Employee.objects.order_by('-bscore')[0].bscore,
        'c_max': Employee.objects.order_by('-cscore')[0].cscore,
        'i_max': Employee.objects.order_by('-iscore')[0].iscore,
        'q_max': Employee.objects.order_by('-qscore')[0].qscore,
        'co_max': Employee.objects.order_by('-coscore')[0].coscore,}
    return render(request, 'hof/me/index.html', context)
    
def rules(request):
    context = {}
    return render(request, 'hof/rules/index.html', context)
    
def news(request, param='1'):
    try:
        curPage = int(param)
    except:
        curPage = 1
    totalPages = (Article.objects.count()+9)/10
    if curPage < 1 or curPage > totalPages:
        curPage = 1
    startnum = (curPage-1)*10
    endnum = min(curPage*10, Article.objects.count())
    articles = Article.objects.order_by('-pub_date')[startnum:endnum+1]
    for art in articles:
        cf = str(art.content_file)
        ext = cf.split('.')[-1]
        if ext == 'pdf':
            art.content_type = 'graph'
        elif ext == 'mp4':
            art.content_type = 'video'
        else:
            art.content_type = 'remove'
            
    pagemin = 1
    pagemax = totalPages
    pagecur = curPage
    pagestart = max(pagecur-2, pagemin)
    pageend = min(pagecur+2, pagemax)
    pagenum = range(pagestart, pageend+1)
    prevnum = max(pagecur-1, pagemin)
    nextnum = min(pagecur+1, pagemax)
    context = {'articles': articles,
                'pagenum': pagenum,
                'pagecur': pagecur,
                'prevnum': prevnum,
                'nextnum': nextnum}
    return render(request, 'hof/news/index.html', context)
    
def polls(request):
    #cookie = request.COOKIES.get('login_user', '')
    cookie = request.GET.get('u')
    
    #chicken egg
    egg = request.GET.get('ChickenEgg') 
    if egg:
        context = {'polls': Poll.objects.all(),
            'egg':egg,}
        return render(request, 'hof/polls/egg.html', context)
        
    voted = False
    if  (not cookie) or (not Employee.objects.filter(id = cookie.upper())):
        voted = True
        cookie = 'none'
    elif VotedEmp.objects.filter(id = cookie):
        voted = True
    context = {'polls': Poll.objects.all(),
                'voted': voted,
                'user':cookie,}
    return render(request, 'hof/polls/index.html', context)
    
def vote(request):
    #cookie = request.COOKIES.get('login_user', '')
    cookie = request.GET.get('u')
    #chicken egg
    egg = request.GET.get('ChickenEgg') 
    if egg:
        egg_num = int(egg)
    elif  (not cookie) or (not Employee.objects.filter(id = cookie.upper())):
        return HttpResponseRedirect("/polls/")
    polls = get_list_or_404(Poll)
    choices = []
    comments = []
    try:
        for i, poll in enumerate(polls):
            choices.append(poll.choice_set.get(pk=request.POST['choice'+str(i+1)]))
            comments.append(request.POST.get('comment'+str(i+1), ''))
    except:
        return HttpResponseRedirect("/polls/")
    else:
        for choice, comment in zip(choices, comments):
            #chicken egg
            if egg:
                insert_list = []
                for i in range(egg_num):
                    insert_list.append(Vote(choice=choice, comment=comment,))
                Vote.objects.bulk_create(insert_list)
            else:
                Vote.objects.create(
                    choice=choice,
                    comment=comment,
                )
        if not egg:
            VotedEmp.objects.create(
                id = cookie
            )
        return HttpResponseRedirect("/polls/")
    
def article(request, param):
    try:
        article = Article.objects.get(pk=param)
    except:
        return HttpResponseRedirect("/news/")
    else:
        cf = str(article.content_file)
        ext = cf.split('.')[-1]
        if ext == 'pdf':
            filename = os.path.join(settings.MEDIA_ROOT, cf)
            to = filename.replace(".pdf", "")
            i = 0
            images = []
            while True:
                fullpath = '{}[{}].jpg'.format(to, i)
                if not os.path.exists(fullpath):
                    break
                else:
                    images.append('{}[{}].jpg'.format(cf.replace(".pdf", ""), i))
                    i += 1
            context = {'article': article,
                        'images': images,}
            return render(request, 'hof/news/' + ext + '.html', context)
        elif ext == 'mp4':
            context = {'article': article}
            return render(request, 'hof/news/' + ext + '.html', context)
        else:
            return HttpResponseRedirect("/news/")
            
def login(request):
    return render(request, 'hof/login/index.html')