# Author:cedar-QQ:1773187610
# Date: 2019/06/17
# System: Window10/Visual Studio 2017/Python 3.6
import urllib.request
import re
import json
import jieba
import chardet
import os
from bs4 import BeautifulSoup  
from distutils.filelist import findall
from wordcloud import WordCloud



#获取某一个问题前五个答案
def getFirstAnswer(QuestionId):
    data = []
    response = urllib.request.urlopen('https://www.zhihu.com/question/' + QuestionId)
    contents = response.read()
    soup = BeautifulSoup(contents,"html.parser")
    #MaxAnswer = soup.find_all('div' ,class_ ='List-header')[0].find('span').get_text()
    for tag in soup.find_all('div',class_ = 'List-item'):
        data.append(tag.find('span',class_ = 'RichText ztext CopyrightRichText-richText').get_text())
    return data

#获取某一个问题答案数
def getMaxAnswerNum(QuestionId):
    response = urllib.request.urlopen('https://www.zhihu.com/question/' + QuestionId)
    contents = response.read()
    soup = BeautifulSoup(contents,"html.parser")
    MaxAnswer = soup.find_all('div' ,class_ ='List-header')[0].find('span').get_text()
    MaxAnswer = re.sub("\D", "", MaxAnswer)
    return MaxAnswer

#获取剩余全部的answer数据包
def getAllHtml(QuestionId):
    MAX = int(int(getMaxAnswerNum(QuestionId))/5)
    AllHtml = []
    for num in range(1,MAX):
        url = "https://www.zhihu.com/api/v4/questions/" + QuestionId + \
            "/answers?include=data%5B%2A%5D.is_normal%2Cadmin_closed_comment%2Creward_info%2C" + \
            "is_collapsed%2Cannotation_action%2Cannotation_detail%2Ccollapse_reason%2Cis_sticky%2C" + \
            "collapsed_by%2Csuggest_edit%2Ccomment_count%2Ccan_comment%2Ccontent%2Ceditable_content%2C" + \
            "voteup_count%2Creshipment_settings%2Ccomment_permission%2Ccreated_time%2Cupdated_time%2C" + \
            "review_info%2Crelevant_info%2Cquestion%2Cexcerpt%2Crelationship.is_authorized%2Cis_author%2Cvoting%2C" +\
            "is_thanked%2Cis_nothelp%2Cis_labeled%2Cis_recognized%2Cpaid_info%3Bdata%5B%2A%5D.mark_infos%5B%2A%5D.url%3Bdata%5B%2A%" + \
            "5D.author.follower_count%2Cbadge%5B%2A%5D.topics&limit=5&offset="+ str(num*5) + "&platform=desktop&sort_by=default"
        response = urllib.request.urlopen(url)
        html = response.read()
        AllHtml.append(html)
    return AllHtml


#获取json内的answer内容并处理
def DealData(htmls):
    data = []
    for html in htmls:
        hjson = json.loads(html)
        for flag in range(0,5):
            data.append(hjson['data'][flag]['content'])
    return data



#中文jieba分词
def chinese_jieba(txt):
    wordlist_jieba = jieba.cut(txt) # 将文本分割，返回列表
    txt_jieba = " ".join(wordlist_jieba) # 将列表拼接为以空格为间断的字符串
    return txt_jieba

stopwords = {'这些':0, '那些':0, '因为':0, '所以':0,'他们':0,'什么':0,'一个':0,'现在':0,'自己':0,'就是':0,'时候':0} # 噪声词

#生成词云
def CreateWordCloud(txt):
    txt = chinese_jieba(txt)
    wordcloud = WordCloud(font_path=r'‪C:\Windows\Fonts\FZYTK.TTF',
                          width = int (800), #输出的画布宽度，默认为400像素
                          height = int (500),#输出的画布高度，默认为200像素
                          background_color = 'black', # 背景色
                          max_words = 70, # 最大显示单词数
                          max_font_size = 100, # 频率最大单词字体大小
                          stopwords = stopwords # 过滤噪声词
                      ).generate(txt)
    image = wordcloud.to_image()
    image.show()


def saveAllData(question):
    txt = ""
    print("数据获取开始，请等待……")
    list = getFirstAnswer(question)
    list.extend(DealData(getAllHtml(question)))
    print("正在生成词云，请等待……")
    for str in list:
        str = re.sub("[A-Za-z0-9\!\%\[\]\,\。\<\>]", "", str)
        txt += str;
    return txt


questionId = "321744364"
CreateWordCloud(saveAllData(questionId))
