# Connect All

## Backend

To run the backend

```shell
cd /backend
pipenv shell --three    #only the first time
python3 manage.py run
```

Open the respective link to view the rest API and test it.

### Sign Language to Text and more...

Sign language gives voice to the mute and is the sound for the deaf. Using deep neural networks, we convert sign language to text, aiding those unable to comprehend sign language. 
![Sign Language Example](https://raw.githubusercontent.com/hackabit19/Apes_together_strong/master/backend/app/main/utils/toSignTranslator/ISL_Gifs/shall%20we%20go%20together%20tommorow.gif)

### Instant Message 4 all

Real time lag-free chat is made possible by hacks at socket level.To aid the specially-abled, speech-to-text and text-to-speech is also used on the fly. Technology stack used for this is socket.io, google cloud speech API.

### Book Narration

The workflow for a seamless narration of books begins by obtaining text using combination of pdf-parsing and OCR. The narration audios generated for each page is stitched together. The technology stack consists of Azure services for OCR and Audio. Apache Tika and PyPDF2 is used for parsing pdfs.

### Note Taking

The workflow starts with image - preprocessing and identification of skewedness and inversion of text. The text is extracted along with exact position and font size. The text is then intelligently parsed for clubbing various parts of the note under a heading / sub-heading or bullets and numbering. It then appropriately narrates the various sections of the note. The technology stack consists of Azure Vision service, OpenCV and Azure Speech service.

## Frontend

```
```
