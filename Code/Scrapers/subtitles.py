import scrapy
import zipfile
import os
import shutil
import datetime
import shutil

class QuotesSpider(scrapy.Spider):
    name = "subtitles"
    start_urls = [
        'https://www.sous-titres.eu/films.html',
        'https://www.sous-titres.eu/series.html'
    ]
    zipFileDownloadLocation = '/home/2013/mbouch95/cp551/p1/tutorial/tutorial/zipFiles'
    unzippedFileContents = '/home/2013/mbouch95/cp551/p1/tutorial/tutorial/unzippedContents'
    conversationsLocation = '/home/2013/mbouch95/cp551/p1/tutorial/tutorial/conversations'
    conversationFileName = 'series.xml'
    isClean = False
    hasCreatedFile = False

    
   
    def parse(self, response):  
        if not self.isClean:
            os.makedirs(self.zipFileDownloadLocation)
            os.makedirs(self.unzippedFileContents)
            os.makedirs(self.conversationsLocation)
            os.mknod(self.conversationsLocation + '/' + self.conversationFileName)
            self.isClean = True      

        for page in response.css('#indexItems a::attr(href)'):
            next_page = response.urljoin(page.extract())
            yield scrapy.Request(next_page, callback=self.chooseZipFile)   

    def chooseZipFile(self, response):
        for download_link in response.css('a.subList'):
            images = download_link.css('img::attr(title)').extract();

            #we want only french results
            if 'en' not in images and 'fr' in images:
                extracted_link = download_link.css('a::attr(href)').extract_first()

                #download link
                zipFileUrl = response.urljoin(extracted_link)
                yield scrapy.Request(zipFileUrl, callback=self.storeZipFile)


    def storeZipFile(self, response):
        path = self.zipFileDownloadLocation + '/' + response.url.split("/")[-1]
        with open(path, "wb") as f:
            f.write(response.body)

        self.extractZipContents(path)
    

    def extractZipContents(self, zipPath):
        with zipfile.ZipFile(zipPath) as zip_file:
            tmp_dir = self.unzippedFileContents + '/' + zipPath.split("/")[-1];
            os.makedirs(tmp_dir)
            for member in zip_file.namelist():
                filename = os.path.basename(member)
                
                # skip directories
                if not filename:
                    continue

                # copy file (taken from zipfile's extract)
                source = zip_file.open(member)
                srtFileName = os.path.join(tmp_dir, filename)
                target = file(srtFileName, "wb")
                with source, target:
                    shutil.copyfileobj(source, target)

                #remove the zip file
                os.remove(zipPath)
                
                #parse the srt file
                self.parseSRTfile(os.path.join(tmp_dir, srtFileName))
    
    def parseSRTfile(self, srtFilePath):
        srt_file = open(srtFilePath)

        cur=[]

        #if not hasCreatedFile:
        dialoguePath = self.conversationsLocation + '/' + self.conversationFileName

        with open(dialoguePath, "ab") as f:
            #f.write('<dialog>\n')
            f.write('\t<s>\n')

            i = 0;
            for line in srt_file:
                if line in ['\n', '\r\n']:

                    #remove subtitle id
                    cur.pop(0)

                    #remove time stamps
                    cur.pop(0)

                    #join text into 1 string and remove special characters
                    text = "".join(cur)
                    text = text.replace('<i>', '')
                    text = text.replace('</i>', '')
                    text = text.replace('-', '')
                    text = text.rstrip()
                    
                    #write to file
                    f.write("\t\t<utt uid=\"%d\"> %s </utt>\n" % (i, text))
                    i = i + 1

                    #reset the temporary storage for a subtitle
                    cur = []
                else:
                    #remove the new line characters
                    cur.append(line.rstrip())

            #write footer for file
            f.write('\t</s>\n')
            #f.write('</dialog>\n')
        
        #close srt file and delete it
        srt_file.close()
        os.remove(srtFilePath)