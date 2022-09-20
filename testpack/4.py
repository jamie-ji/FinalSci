import json
import shutil

class todoc():

    def __init__(self,filepath,outpath):
        self.pdfpath=filepath
        self.outpath=outpath

    def doc(self):
        # Provide your username and license code
        LicenseCode = 'BE71CC77-E9F1-4261-8DF5-2ABC5C9567D3'
        UserName = 'JAMIE'

        try:
            import requests
        except ImportError:
            print("You need the requests library to be installed in order to use this sample.")
            print("Run 'pip install requests' to fix it.")

            exit()
        # Convert first 5 pages of multipage document into doc and txt
        RequestUrl = 'http://www.ocrwebservice.com/restservices/processDocument?language=english&pagerange=allpages&outputformat=docx';

        #Full path to uploaded document
        # FilePath = r"D:\discourse_code\code\resource\pdf_dome\YOLOX.pdf"

        outputformat='docx'

        with open(self.pdfpath, 'rb') as image_file:
            image_data = image_file.read()
            
        r = requests.post(RequestUrl,data=image_data, auth=(UserName, LicenseCode),)



        if r.status_code == 401:
            #Please provide valid username and license code
            print("Unauthorized request")
            exit()

        # Decode Output response
        jobj = json.loads(r.content)

        ocrError = str(jobj["ErrorMessage"])

        if ocrError != '':
                #Error occurs during recognition
                print ("Recognition Error: " + ocrError)
                exit()


        # Task description
        print("Task Description:" + str(jobj["TaskDescription"]))

        # Available pages 
        print("Available Pages:" + str(jobj["AvailablePages"]))

        # Processed pages 
        print("Processed Pages:" + str(jobj["ProcessedPages"]))


        #Download output file (if outputformat was specified)
        file_response = requests.get(jobj["OutputFileUrl"], stream=True)
        
        with open(self.outpath, 'wb') as output_file:
                shutil.copyfileobj(file_response.raw, output_file)



