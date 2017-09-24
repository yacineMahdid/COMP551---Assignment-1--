# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup
from langdetect import detect_langs
from scrapy.linkextractors import LinkExtractor
import json
import codecs

class YahooAnSpider(scrapy.Spider):
    name = 'yahoobot'
    real_base = 'https://fr.answers.yahoo.com'
    yahoo_base_url = 'https://fr.answers.yahoo.com/_module?name=YANewDiscoverTabModule&after=pc%s~p:%s&bpos=%s&cpos=%s'
    start_urls = [yahoo_base_url % (20,0,2,18)]
    download_delay = 1.5
    base_pc = 20;
    base_bpos = 2;
    base_cpos = 18;
    
    global utterance
    utterance = 0
    global english_sentence
    english_sentence = 0
    global conversation
    conversation = 0;
 
    def parse(self, response):
        data = json.loads(response.body_as_unicode())
        data = data['YANewDiscoverTabModule']
        options = data['options'];

        soup = BeautifulSoup(data['html'], "html.parser")
        whole_divs = soup.select("div.Bfc")
        
        next_link = soup.findAll("a",{'class':"Fz-14 Fw-b Clr-b Wow-bw title"})#('a', {'class': 'Fz-14 Fw-b Clr-b Wow-bw title'})['href']
        number_comments = soup.findAll("div",{'class':'Clr-888 Fz-12 Lh-18'})
        for index,link in enumerate(next_link):
            url = self.real_base + link['href']
            big_phrase = number_comments[index].text.strip().split()
            comment_number = big_phrase[0];
            if(int(comment_number) > 3):
                print(url)
                print(comment_number)
                yield response.follow(url, callback=self.thread_parse)
                
                
        
    
        print('*****')
        #print(next_link);
        print('xxxxx')
            
        if options['disableLoadMore'] is False:
            self.base_pc = self.base_pc + 20
            self.base_bpos = self.base_bpos + 1;
            self.base_cpos = self.base_cpos + 17;
            print('Next page')
            yield scrapy.Request(self.yahoo_base_url % (self.base_pc,0,self.base_bpos,self.base_cpos))
            
    def thread_parse(self,response):
        global utterance
        global english_sentence
        global conversation
        
        soup = BeautifulSoup(response.body, "html.parser")
        file = open('yahoocorpus.xml',"a",encoding='utf8')
        current_id = 1;
        question = soup.find("h1",{'class':"Fz-24 Fw-300 Mb-10"})
        file.write('<s>')
        file.write('<utt uid='+str(current_id)+'> '+question.text.strip()+'\n</utt>')
        current_id = current_id + 1;
        answers = soup.findAll('span',{'class':'ya-q-full-text'})
        for answer in answers:
            file.write('<utt uid='+str(current_id)+'> '+answer.text.strip()+'\n</utt>')
            current_id = current_id + 1;
            utterance = utterance + 1;
            
        file.write('</s>\n')
        conversation = conversation + 1;
        file.close()
        
        print('Number of utterance = %d' %(utterance))
        print('Number of english sentence = %d' %(english_sentence))
        print('Number of conversation = %d' %(conversation))