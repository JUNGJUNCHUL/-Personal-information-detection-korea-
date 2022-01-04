# 만든이 정준철!! 무료 공유 및 수정 배포는 가능하지만.. 원 출저만 밝혀주세요 ㅠㅠ
# 블로그 https://blog.naver.com/pouerccat
# python3에서 동작(windows,linux 둘다가능)
# lastfile 남은 상태 저장 lastfile2 돌린상태까지 저장
"""
옵션 1은 : 경로 지정하면 그냥 그경로를 다 검사하고 결과값을 aresult.txt에 저장!
옵션 2는 : 경로 지정하면 검사하지만 도중에 오래걸려서 취소후 다시 2로 검사하면 이어서 검사하는 기능!(result.txt에 저장됨)
검사 요소 : 주민번호, 핸드폰번호만
검사 파일 : 일반 텍스트 파일 + 엑셀 + PDF 까지! 한글이나 기타는 추가할 예정
윈도우 리눅스 둘다 테스트 하였으며 추가 사용자 편의하게 기능 보수개발할 예정 ! ㅎㅎ 지금은 끝
감사합니당.
검사는 하위의 디렉토리까지 다합니당~
사용법 : jcjung.py [디렉토리]

# xlrd must be a 1.2 version
"""

import os
import re
import time
import sys
import pandas
import openpyxl
from xlrd import open_workbook # xlrd must be a 1.2 version
import pdfplumber
import shutil

if len(sys.argv) > 3:
    print("[-] Usage: jcjungpi.py [PATH]")
    os._exit(0)

#sys.stdout = open('stdout.txt', 'a')
#sys.stdout.close()

start = time.time()  # 시작 시간 저장
dir=sys.argv[1]
pattern = '([0-9]{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[1,2][0-9]|3[0,1]))-?[1-4][0-9]{6}'
pattern2 = '010-?([0-9]{4})-?([0-9]{4})'

def search(dirname):
    aresult = open('aresult.txt', 'a')
    try:
        filenames = os.listdir(dirname)
        for filename in filenames:
            full_filename = os.path.join(dirname, filename)
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                ext = os.path.splitext(full_filename)[-1]
                if ext == '.xls' or ext == '.xlsx' or ext == '.xlsm' :
                    try:
                        book = open_workbook(full_filename)
                        jcount = 0
                        pcount = 0
                        saveexcel = []
                        for sheet in book.sheets():
                            for rowidx in range(sheet.nrows):
                                row = sheet.row(rowidx)
                                for colidx, cell in enumerate(row):
                                    if len(re.findall(pattern, str(cell.value))) > 0:
                                        jcount = jcount + 1
                                        saveexcel.append(str(cell.value))
                                    if len(re.findall(pattern2, str(cell.value))) > 0:
                                        pcount = pcount + 1
                                        saveexcel.append(str(cell.value))
                        if (jcount == 0 and pcount == 0):
                            pass
                        else:
                            aresult.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s 나온 결과 : %s \n" % (str(full_filename), jcount, pcount, saveexcel))
                    except:
                        pass
                elif ext=='.pdf':
                    try:
                        jsum=0
                        psum=0
                        pdfscan=[]
                        with pdfplumber.open(full_filename) as temp:
                            for i in temp.pages:
                                first_page = i
                                if (len(re.findall(pattern, i.extract_text()))==0 and len(re.findall(pattern2, i.extract_text()))==0):
                                    pass
                                else:
                                    jsum=jsum+len(re.findall(pattern, i.extract_text()))
                                    psum=psum+len(re.findall(pattern2, i.extract_text()))
                                    pdfscan.append(re.findall(pattern, i.extract_text()))
                                    pdfscan.append(re.findall(pattern2, i.extract_text()))
                            if (jsum==0 and psum==0):
                                pass
                            else:
                                aresult.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s 나온 결과 : %s \n" % (str(full_filename), jsum, psum, pdfscan))
                    except:
                        pass

                else:
                    try:
                        with open(full_filename, encoding='utf-8') as file:
                            data = file.read()
                            filelist = []
                            # print(str(filelists) + " 주민번호 갯수는 " + str(len(re.findall(pattern,data))) + " 휴대폰번호 갯수는 " + str(len(re.findall(pattern2, data)))) 메모리량사용커서 바꿈
                            if (len(re.findall(pattern, data)) == 0 and len(re.findall(pattern2, data)) == 0):
                                pass
                            else:
                                filelist.append(re.findall(pattern, data))
                                filelist.append(re.findall(pattern2, data))
                                aresult.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s \n" % (
                                    str(full_filename), str(len(re.findall(pattern, data))),
                                    str(len(re.findall(pattern2, data)))),filelist)
                    except:
                        pass

    except PermissionError:
        pass

def alllist(dirname2):
    f = open("lastfile.txt","a")
    try:
        filenames = os.listdir(dirname2)
        for filename in filenames:
            full_filename = os.path.join(dirname2, filename)
            if os.path.isdir(full_filename):
                alllist(full_filename)
            else:
                f.write(full_filename+"\n")
    except:
        pass

def pi(full_filename):
    result=open('result.txt', 'a')
    ext = os.path.splitext(full_filename)[-1]
    if  ext == '.xls' or ext == '.xlsx' or ext == '.xlsm':
        try:
            book = open_workbook(full_filename)
            saveexcel = []
            jcount = 0
            pcount = 0
            for sheet in book.sheets():
                for rowidx in range(sheet.nrows):
                    row = sheet.row(rowidx)
                    for colidx, cell in enumerate(row):
                        if len(re.findall(pattern, str(cell.value))) > 0:
                            jcount = jcount + 1
                            saveexcel.append(str(cell.value))
                        if len(re.findall(pattern2, str(cell.value))) > 0:
                            pcount = pcount + 1
                            saveexcel.append(str(cell.value))
            if (jcount == 0 and pcount == 0):
                pass
            else:
                #result.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s" % (str(full_filename), jcount, pcount))
                result.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s 나온 결과 : %s \n" % (str(full_filename), jcount, pcount ,saveexcel))
        except:
            pass
    elif ext == '.pdf':
        try:
            jsum = 0
            psum = 0
            pdfscan=[]
            with pdfplumber.open(full_filename) as temp:
                for i in temp.pages:
                    first_page = i
                    if (len(re.findall(pattern, i.extract_text())) == 0 and len(
                            re.findall(pattern2, i.extract_text())) == 0):
                        pass
                    else:
                        jsum = jsum + len(re.findall(pattern, i.extract_text()))
                        psum = psum + len(re.findall(pattern2, i.extract_text()))
                        pdfscan.append(re.findall(pattern, i.extract_text()))
                        pdfscan.append(re.findall(pattern2, i.extract_text()))
                if (jsum == 0 and psum == 0):
                    pass
                else:
                    result.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s 나온 결과 : %s \n" % (str(full_filename), jsum, psum, pdfscan))
        except:
            pass

    else:
        try:
            with open(full_filename, encoding='utf-8') as file:
                data = file.read()
                filelist = []
                # print(str(filelists) + " 주민번호 갯수는 " + str(len(re.findall(pattern,data))) + " 휴대폰번호 갯수는 " + str(len(re.findall(pattern2, data)))) 메모리량사용커서 바꿈
                if (len(re.findall(pattern, data)) == 0 and len(re.findall(pattern2, data)) == 0):
                    pass
                else:
                    filelist.append(re.findall(pattern, data))
                    filelist.append(re.findall(pattern2, data))
                    result.write("%s 주민번호 갯수는 %s  휴대폰번호 갯수는 %s \n" % (
                        str(full_filename), str(len(re.findall(pattern, data))),
                        str(len(re.findall(pattern2, data)))),filelist)
        except:
            pass

#search(dir)
def schedule():
    with open('lastfile.txt') as file:
        for i in file:
            files = i.replace("\n","")
            pi(files)
            with open("lastfile2.txt", "a") as file2:
                file2.write(i)

def makefile():
    f = open("lastfile.txt")
    f2 = open("lastfile2.txt")
    f3 =  open("lastfile3.txt", "a")
    lastfile = f.readlines()
    lastfile2 = f2.readlines()
    for i in range(len(lastfile2),len(lastfile)):
        f3.write(lastfile[i])
    shutil.copyfile("lastfile3.txt", "lastfile.txt")
    time.sleep(1)
    f.close()
    f2.close()
    f3.close()
    os.remove("lastfile2.txt")
    os.remove("lastfile3.txt")

if len(sys.argv) == 3:
    option=sys.argv[2]
else :
    print("option 1 is full searcrh with no stop")
    print("option 2 is schedule searcrh")  # must have same dir past
    option =input("please enter option : ")

if option == "2" :
    if os.path.exists('lastfile2.txt') :
        makefile()
        print("증분대상 리스트 생성 완료 ! 한번 더 실행해주세요.")
    elif os.path.exists('lastfile.txt') :
        schedule()
    else :
        alllist(dir)
        print("검색대상 리스트 생성 완료 ! 한번 더 실행해주세요.")
elif option =="1" :
    search(dir)
else:
    print("option 1 is full searcrh with no stop plz retry")
    print("option 2 is schedule searcrh plz retry")

print("총 소요 시간 : %s" %(str(time.time()-start)))
