#application.py app for CP_Web_interface 
# -*- coding: utf-8 -*-
# Copyright 2017, CrowdPixi, LLC
# Created by Gene O'Donnell
import os
from datetime import timedelta, date, datetime, time
from decimal import *
import pytz
import cgi
import urllib
import argparse
import logging
import sys
import ctypes
import csv
import collections
import unicodedata
import numpy as np
import cv2

from urllib import FancyURLopener
from flask import Flask, render_template, request, flash, redirect, url_for, session
from flask_mail import Mail, Message
from forms import DirectorForm, DirectorConfirmForm, LoginForm, EventForm, SlideForm, SlideShowForm, AdminForm, SettingsForm, PwForm, EditForm
import pdb
from werkzeug.utils import secure_filename
from flask_wtf.csrf import CSRFProtect
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature

os.environ["PARSE_API_ROOT"]="https://parseapi.back4app.com/"

from parse_rest.datatypes import Function, Object, GeoPoint, File
from parse_rest.user import User
from parse_rest.connection import SessionToken, register
from parse_rest.query import QueryResourceDoesNotExist, QueryError, QueryManager
from parse_rest.connection import ParseBatcher
from parse_rest.core import ResourceRequestBadRequest, ParseError

APPLICATION_ID = 'fAO93g4jPRaQPKRke5ZPDSHxAILbUkRX3hEN2pel'
REST_API_KEY = 'jDi9SHsbh568wAa9eNNPwSy1XN94tqsU7kFeR8lC'
MASTER_KEY = 'p4v3wEGAA5ici7qH998dBmJv01uQxjEktcp56lEJ'

register(APPLICATION_ID, REST_API_KEY, master_key=MASTER_KEY)

UPLOAD_FOLDER='uploads'    
ALLOWED_IMAGE_EXTENSIONS = set(['jpg','png'])
ALLOWED_VIDEO_EXTENSIONS = set(['mp4'])

application = Flask(__name__)

app = application

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 32 * 1024 *1024

app.config['MAIL_SERVER'] = "mail.crowdpixie.com"
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = "sales@crowdpixie.com"
app.config['MAIL_PASSWORD'] = "!CPSimpact2047"



mail = Mail(app)

csrf = CSRFProtect()
csrf.init_app(app)

class MyOpener(FancyURLopener):
    version = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2227.1 Safari/537.36'

urllib._urlopener = MyOpener

class Director(User):
    pass 

class UploadedVideo(Object):
    pass

class StoredImage(Object):
    pass



app.secret_key = 'l\xe2\xdb\x87\xcc\xfc\xc5O\xe7v\x12\xac\xff%\xe6\xa4k\xd2\x12S\xe4/\xfa\xda'

s = URLSafeTimedSerializer(app.secret_key)


@app.route('/', methods = ['GET','POST'])
def main():
    form = LoginForm()
    if 'username' in session:
        form = EditForm()
        user = User.Query.get(username=session['username'])
        try:
            test = user.storedStatus
        except AttributeError:
            test = {'videoStatus': 'noVideo','imageStatus': 'noImage', 'videoId': 'None', 'imageId': 'None'}
        if request.method == 'GET':
            if test['videoStatus'] == 'videoSaved':
                uploadedVideo = UploadedVideo.Query.get(objectId=test['videoId'])
            else:
                uploadedVideo = createDefaultUploadedVideo()
            if test['imageStatus'] == 'imageSaved':
                storedImage = StoredImage.Query.get(objectId=test['imageId'])
            else:
                storedImage = createDefaultStoredImage()
        return render_template('landing.html', video=uploadedVideo, image = storedImage, form=form) 
    else:
        return render_template('login.html', form=form)        


@app.route('/landing/<pk>', methods = ['GET', 'POST'])
def landing(pk):
    form = LoginForm()
    if 'username' in session:
        form = EditForm()
        user = User.Query.get(username=session['username'])
        try:
            test = user.storedStatus
        except AttributeError:
            test = {'videoStatus': 'noVideo','imageStatus': 'noImage', 'videoId': 'None', 'imageId': 'None'}
        if request.method == 'GET':
            if not pk == 'NonewithNone':
                keys = pk.split("with")
                if keys[1] == 'Video':
                    test['videoStatus'] = 'videoSaved'
                    test['videoId'] = keys[0]
                if keys[1] == 'Image':
                    test['imageStatus'] = 'imageSaved'
                    test['imageId'] = keys[0]
            if test['videoStatus'] == 'videoSaved':
                uploadedVideo = UploadedVideo.Query.get(objectId=test['videoId'])
            else:
                uploadedVideo = createDefaultUploadedVideo()
            if test['imageStatus'] == 'imageSaved':
                storedImage = StoredImage.Query.get(objectId=test['imageId'])
            else:
                storedImage = createDefaultStoredImage()
        if request.method == 'POST':
            if form.validate():
                user = User.login(session['username'], session['password'])
                if form.saveVideo.data:
                    test = saveVideo(form.data, test)
                if form.saveImage.data:
                    test = saveImage(form.data, test)
                if form.go.data:
                    test = advanceToTime(form.data, test)
                    framePreview = StoredImage.Query.get(objectId=test['frameImage'])
                if form.storeFrame.data:
                    test = createImage(form.data, test)
                if form.execute.data:
                    test = processImage(form.data, test)
                if test['videoStatus'] == 'videoSaved':
                    uploadedVideo = UploadedVideo.Query.get(objectId=test['videoId'])
                else:
                    uploadedVideo = createDefaultUploadedVideo()
                if test['imageStatus'] == 'imageSaved':
                    storedImage = StoredImage.Query.get(objectId=test['imageId'])
                else:
                    storedImage = createDefaultStoredImage()
                user.storedStatus = test
                user.save()
            else:
                uploadedVideo = createDefaultUploadedVideo()
                storedImage = createDefaultStoredImage()
        if test['frameVideo'] and test['videoId']:
            if test['frameVideo'] == test['videoId']:
                framePreview = StoredImage.Query.get(objectId=test['frameImage'])
        else:
            framePreview = None
        return render_template('landing.html', video=uploadedVideo, image = storedImage, form=form, framePreview=framePreview) 
    else:
        return render_template('login.html', form=form)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    form = DirectorForm()
    director = Director()
    if request.method == 'POST'and form.validate():
        email = form.email.data
        confirmToken = s.dumps(email, salt='email-salt')
        link = url_for('confirm_email', token=confirmToken, _external=True) 
        mail.connect()
        confmail = Message("DerbyHacksDemo Registration",
                        sender=("CrowdPixie","sales@crowdpixie.com"), 
                        recipients=[email])
        confmail.body=u'please confirm your registration with DerbyHacksDemo {}'.format(link)
        confmail.html =render_template('confirmationEmail.html', link=link, name=form.email.data)
        mail.send(confmail)
        director = Director.signup(email=form.email.data, username=form.email.data, password=form.password.data)
        director.save()
        directorID = director.objectId
        return redirect(url_for('directorConfirm', pk=directorID))
    else:
        return render_template('directorCreate.html', form=form, object=director)

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-salt', max_age=86400)
        users = User.Query.all().filter(email=email).limit(1)
        if users:
            user = users[0]
            user.emailConfirmed = True
            form = LoginForm()
            return render_template('login.html', form=form) 
        else:
            return render_template('badToken.html')
    except SignatureExpired:
        return render_template('expiredToken.html')
    except BadSignature:
        return render_template('badToken.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate():
        try:
            user = User.login(form.username.data, form.password.data)
            currentDirector = user
            session['username'] = user.username
            session['password'] = form.password.data
            uploadedVideo = createDefaultUploadedVideo()
            storedImage = createDefaultStoredImage() 
            form = EditForm()
            return render_template('landing.html', video=uploadedVideo, image=storedImage, form=form)
        except ParseError:
            return render_template('login.html', form=form) 
    else:
        return render_template('login.html', form=form)

@app.route('/director/<pk>', methods = ['GET', 'POST'])
def directorDetail(pk):
    form = DirectorDetail()
    directors = Director.Query.filter(objectId=pk)
    if request.method == 'POST'and form.validate():
        director = Director(email=form.email.data)
        director.save()
        pk = director.objectId
    if request.method == 'GET' and directors.count() > 0:    
        director = directors[0]
    return render_template('directorCreate.html', form=form, object=director)

@app.route('/deleteVideo/<pk>', methods = ['GET', 'POST'])
def deleteVideo(pk):
    form = LoginForm()
    if 'username' in session:
        videoToRemove = UploadedVideo.Query.get(objectId=pk)
        videoToRemove.delete()
        user = User.Query.get(username=session['username'])
        username = session['username']
        myVideos = UploadedVideo.Query.all().filter(author=username).order_by("-updatedAt").limit(50) 
        return render_template('videoList.html', videoList = myVideos)
    else:
        return render_template('login.html', form=form)

@app.route('/deleteImage/<pk>', methods = ['GET', 'POST'])
def deleteImage(pk):
    form = LoginForm()
    if 'username' in session:
        imageToRemove = StoredImage.Query.get(objectId=pk)
        imageToRemove.delete()
        user = User.Query.get(username=session['username'])
        username = session['username']
        myImages = StoredImage.Query.all().filter(author=username).order_by("-updatedAt").limit(50) 
        return render_template('imageList.html', imageList = myImages)
    else:
        return render_template('login.html', form=form)

@app.route('/director/confirm/<pk>', methods = ['GET', 'POST'])
def directorConfirm(pk):
    form = DirectorConfirmForm()
    directors = Director.Query.filter(objectId=pk)
    currentDirector = directors[0]
    return render_template('directorConfirm.html', form=form, object=currentDirector)

@app.route('/admin/<pk>', methods = ['GET', 'POST'])
def admin(pk):
    form = LoginForm()
    if 'username' in session:
        form = AdminForm()
        user = User.Query.get(username=session['username'])
        director = user
        directorList = User.Query.all().filter(sponsor=director.verifiedName).order_by("-updatedAt").limit(1000)
        if pk == 'None':
            currentDirector = directorList[0]
        else:
            currentDirector = User.Query.get(objectId=pk)
        form.userData.email.data = str(currentDirector.email)
        if request.method == 'POST' and form.validate():
            if form.update.data:
                currentDirector.sessionToken = SessionToken(currentDirector)
                currentDirector.email = request.form.userData.email.data
                currentDirector.save()
        return render_template('admin.html', form=form, directorList=directorList)
    else:
        return render_template('login.html', form=form)
    
@app.route('/settings', methods = ['GET', 'POST'])
def settings():
    form = LoginForm()
    if 'username' in session:
        form = SettingsForm()
        user = User.Query.get(username=session['username'])
        director = user
        currentDirector = user
        form.email.data = str(currentDirector.email)
        if request.method == 'POST' and form.validate():
            currentDirector.sessionToken = SessionToken(currentDirector)
            if form.pwChange.data:
                form = PwForm()
                return render_template('pwChange.html', form=form, director=currentDirector)
        return render_template('accountInfo.html', form=form, director=currentDirector)
    else:
        return render_template('login.html', form=form)

@app.route('/pwChange', methods = ['GET', 'POST'])
def pwChange():
    form = LoginForm()
    if 'username' in session:
        form = PwForm()
        user = User.Query.get(username=session['username'])
        currentDirector = user
        if request.method == 'POST': 
            if form.cancel.data: 
                form = SettingsForm()
                form.email.data = str(currentDirector.email)
                return render_template('accountInfo.html', form=form, director=currentDirector)
            else:
                if form.update.data and form.validate():
                    priorPassword = request.form['oldPassword']
                    try:
                        currentDirector = User.login(session['username'], priorPassword)
                        currentDirector.sessionToken = SessionToken(currentDirector)
                        if currentDirector.is_authenticated():
                            form.oldPassword.errors = [u'Password change successful!']
                            currentDirector.password = request.form['password']
                            currentDirector.save()
                    except ParseError:
                        form.oldPassword.errors = [u'Incorrect old password!']
        return render_template('pwChange.html', form=form, director=currentDirector)
    else:
        return render_template('login.html', form=form)

@app.route('/images', methods = ['GET'])
def images():
    form = LoginForm()
    if 'username' in session:
        user = User.Query.get(username=session['username'])
        currentDirector = user
        username = session['username']
        myImages = StoredImage.Query.all().filter(author=username).order_by("-updatedAt").limit(50) 
        return render_template('imageList.html', imageList = myImages)
    else:
        return render_template('login.html', form=form)

@app.route('/videos', methods = ['GET'])
def videos():
    form = LoginForm()
    if 'username' in session:
        user = User.Query.get(username=session['username'])
        username = session['username']
        myVideos = UploadedVideo.Query.all().filter(author=username).order_by("-updatedAt").limit(50) 
        return render_template('videoList.html', videoList = myVideos)
    else:
        return render_template('login.html', form=form)
    


@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    form = LoginForm()
    session.pop('username', None)
    return render_template('login.html', form=form) 

def allowed_video_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_VIDEO_EXTENSIONS

def allowed_image_filename(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_IMAGE_EXTENSIONS

def advanceToTime(form, test):
    homepath = os.path.abspath('.')
    uploadedVideo = UploadedVideo.Query.get(objectId=test['videoId'])
    capture = url_to_videoCapture(uploadedVideo.videoFileName.url)
    targetTime = form['timeTarget']
    frameCount = capture.get(cv2.CAP_PROP_FRAME_COUNT)
    frameRate = capture.get(cv2.CAP_PROP_FPS)
    videoDuration = frameCount/frameRate
    if targetTime > videoDuration:
        targetFrame = frameCount - 1
    else:
        targetFrame = int(float(targetTime) * frameRate)
    capture.set(cv2.CAP_PROP_POS_FRAMES, targetFrame)
    image = capture.read()
    if image[0]:
        frameImage = image[1]
    else:
        frameImage = cv2.imread(homepath + '/static/errorImage.jpg')
    fileName = 'frame' + str(targetFrame) + uploadedVideo.videoName
    fileName = fileName[0:len(fileName)- 3] + 'jpg'
    tmppath = homepath + '/temp/' + fileName
    cv2.imwrite(tmppath, frameImage)
    imageFile = open(tmppath, "r")
    image_data = imageFile.read()
    imageFile.close()
    capture.release()
    frame = createStoredImage(fileName, image_data)
    frame.save()
    test['frameImage'] = frame.objectId
    test['frameVideo'] = test['videoId']
    return test


def saveVideo(form, test):
    filename = form['chooseVideo'].filename
    if not filename == '':
        validFile = allowed_video_filename(filename)
        if validFile:
            video_data = form['chooseVideo'].read()
            uploadedVideo = createUploadedVideo(filename, video_data)
            uploadedVideo.save()
            test['videoStatus'] = 'videoSaved'
            test['videoId'] = uploadedVideo.objectId
        else:
            test['validVideoFilename'] = 'invalid fileName'
    else:
        test['validVideoFileName'] = 'blank'
    return test

def saveImage(form, test):
    filename = form['chooseImage'].filename
    if not filename == '':
        validFile = allowed_image_filename(filename)
        if validFile:
            image_data = form['chooseImage'].read()
            storedImage = createStoredImage(filename, image_data)
            storedImage.save()
            test['imageStatus'] = 'imageSaved'
            test['imageId'] = storedImage.objectId
        else:
            test['validImageFilename'] = 'invalid fileName'
    else:
        test['validImageFileName'] = 'blank'
    return test    

def createStoredImage(filename, image_data):
    homepath = os.path.abspath('.')
    nameSplit = filename.split('/')
    nameOnly = nameSplit[len(nameSplit)-1]
    tmppath = homepath + '/temp/' + nameOnly
    tempFile = open(tmppath, "w")
    tempFile.write(image_data)
    tempFile.close()
    imageFile = open(tmppath, "r")
    imageData = imageFile.read()
    imageFile.close()
    imageCapture = cv2.imread(tmppath)
    imageWidth = imageCapture.shape[1]
    imageHeight = imageCapture.shape[0]
    preview = cv2.resize(imageCapture, (128,72),interpolation = cv2.INTER_AREA)
    nameOnly = nameOnly[0:len(nameOnly)-4]
    thumbName = nameOnly + "ImageThumb.jpg"
    tmpThumbPath = homepath + '/temp/' + thumbName
    cv2.imwrite(tmpThumbPath, preview)
    previewFile = open(tmpThumbPath, 'r')
    previewData = previewFile.read()
    newThumbName = thumbName
    newThumbFile = File(newThumbName, previewData, 'image/jpg')
    newThumbFile.save()
    newImageName = nameOnly + "Image.jpg"
    newImageFile = File(newImageName, imageData, 'image/jpg')
    newImageFile.save()
    user = User.Query.get(username=session['username'])
    defaultImage = StoredImage(imageName=newImageName, author=user.username, imageFileName = newImageFile, previewFileName= newThumbFile, height = imageHeight, width = imageWidth)
    return defaultImage

def createUploadedVideo(filename, video_data):
    homepath = os.path.abspath('.')
    nameSplit = filename.split('/')
    nameOnly = nameSplit[len(nameSplit)-1]
    tmppath = homepath + '/temp/' + nameOnly
    tempFile = open(tmppath, "w")
    tempFile.write(video_data)
    tempFile.close()
    videoFile = open(tmppath, "r")
    videoData = videoFile.read()
    videoFile.close()
    videoCapture = cv2.VideoCapture(tmppath)
    frameCount = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    frameRate = videoCapture.get(cv2.CAP_PROP_FPS)
    if not frameRate == 0:
        duration = frameCount/frameRate
    else:
        frameRate = 30
        duration = frameCount/frameRate
    videoWidth = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    videoHeight = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    preview = videoCapture.read(0)
    if preview[0]:
        preview = cv2.resize(preview[1], (128,72),interpolation = cv2.INTER_AREA)
    else:
        errorFileName = homepath + 'temp/noPreview.jpg'
        preview = cv2.imread(errorFileName)
    videoPreviewName = nameOnly + "Preview.jpg"
    tmpPreviewPath = homepath + '/temp/' + videoPreviewName
    cv2.imwrite(tmpPreviewPath, preview)
    previewFile = open(tmpPreviewPath, 'r')
    previewData = previewFile.read()
    newImageName = nameOnly + "Preview.jpg"
    newImageFile = File(newImageName, previewData, 'image/jpg')
    newImageFile.save()
    newVideoName = nameOnly + "Video.mp4"
    newVideoFile = File(newVideoName, videoData, 'video/mp4')
    newVideoFile.save()
    user = User.Query.get(username=session['username'])
    defaultVideo = UploadedVideo(videoName=nameOnly, author=user.username, videoFileName = newVideoFile, previewFileName= newImageFile, duration = duration, height = videoHeight, width = videoWidth)
    videoCapture.release()
    return defaultVideo

def createDefaultUploadedVideo():
    homepath = os.path.abspath('.')
    tmppath = homepath + '/temp/defaultVideo.mp4'
    videoFile = open(tmppath, "r")
    videoData = videoFile.read()
    videoFile.close()
    videoCapture = cv2.VideoCapture(tmppath)
    frameCount = videoCapture.get(cv2.CAP_PROP_FRAME_COUNT)
    frameRate = videoCapture.get(cv2.CAP_PROP_FPS)
    if not frameRate == 0:
        duration = frameCount/frameRate
    else:
        frameRate = 30
        duration = frameCount/frameRate
    videoWidth = videoCapture.get(cv2.CAP_PROP_FRAME_WIDTH)
    videoHeight = videoCapture.get(cv2.CAP_PROP_FRAME_HEIGHT)
    preview = videoCapture.read(0)
    if preview[0]:
        preview = cv2.resize(preview[1], (128,72),interpolation = cv2.INTER_AREA)
    else:
        errorFileName = homepath + 'temp/noPreview.jpg'
        preview = cv2.imread(errorFileName)
    videoPreviewName = "defaultPreview.jpg"
    tmpPreviewPath = homepath + '/temp/defaultPreview.jpg'
    cv2.imwrite(tmpPreviewPath, preview)
    previewFile = open(tmpPreviewPath, 'r')
    previewData = previewFile.read()
    newImageName = "defaultPreview.jpg"
    newImageFile = File(newImageName, previewData, 'image/jpg')
    newImageFile.save()
    newVideoName = "defaultVideo.mp4"
    newVideoFile = File(newVideoName, videoData, 'video/mp4')
    newVideoFile.save()
    user = User.Query.get(username=session['username'])
    defaultVideo = UploadedVideo(videoName="defaultVideo", author=user.username, videoFileName = newVideoFile, previewFileName= newImageFile, duration = duration, height = videoHeight, width = videoWidth)
    videoCapture.release()
    return defaultVideo

def createDefaultStoredImage():
    homepath = os.path.abspath('.')
    tmppath = homepath + '/temp/defaultImage.jpg'
    imageFile = open(tmppath, "r")
    imageData = imageFile.read()
    imageFile.close()
    imageCapture = cv2.imread(tmppath)
    imageWidth = imageCapture.shape[1]
    imageHeight = imageCapture.shape[0]
    preview = cv2.resize(imageCapture, (128,72),interpolation = cv2.INTER_AREA)
    imageName = "defaultImageThumb.jpg"
    tmpThumbPath = homepath + '/temp/defaultImageThumb.jpg'
    cv2.imwrite(tmpThumbPath, preview)
    previewFile = open(tmpThumbPath, 'r')
    previewData = previewFile.read()
    newThumbName = "defaultImageThumb.jpg"
    newThumbFile = File(newThumbName, previewData, 'image/jpg')
    newThumbFile.save()
    newImageName = "defaultImage.jpg"
    newImageFile = File(newImageName, imageData, 'image/jpg')
    newImageFile.save()
    user = User.Query.get(username=session['username'])
    defaultImage = StoredImage(imageName="defaultImage", author=user.username, imageFileName = newImageFile, previewFileName= newThumbFile, height = imageHeight, width = imageWidth)
    return defaultImage

def createPreviewImage(form):
    rows = int(form['audienceRows'])
    columns = int(form['audienceSeatsPerRow'])
    try:
        slideToPreview = form['selectedSlideShows']
        typeCheck = isinstance(slideToPreview, basestring)
    except KeyError:
        typeCheck = False
    if not rows == 0 and not columns == 0 and typeCheck:
        success = True
    else:
        success = False
    return success

def url_to_image(url):
    myopener = MyOpener()
    resp = myopener.open(url)
    image = np.asarray(bytearray(resp.read()), dtype="uint8")
    image = cv2.imdecode(image, cv2.IMREAD_COLOR)
    return image

def url_to_videoCapture(url):
    myopener = MyOpener()
    resp = myopener.open(url)
    data = resp.read()
    homepath = os.path.abspath('.')
    testPath = homepath + '/temp/testFile.mp4'
    testFile = open(testPath, "w")
    testFile.write(data)
    testFile.close()
    capture = cv2.VideoCapture(testPath)
    return capture


if __name__ == '__main__':
   app.run(debug = True)
