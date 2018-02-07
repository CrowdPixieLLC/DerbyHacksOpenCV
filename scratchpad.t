            try:
                form.showName.data = currentSlideShow.showName[0]
            except AttributeError:
                form.showName.data = ''
                currentSlideShow.showName = ''
            try:
                form.slideType.data = str(currentSlideShow.slideType)
            except AttributeError:
                form.slideType.data = u'1'
                currentSlideShow.slideType = 1
            try:
                form.slideCount.data = len(currentSlideShow.pan)
                currentSlideShow.slideCount = [len(currentSlideShow.pan)]
            except AttributeError:
                form.slideCount.data = 1
                currentSlideShow.slideCount = [1]
            try:
                slideIndex = currentSlideShow.slideIndex[0]
            except AttributeError:
                slideIndexArray = [0]
                slideIndex = slideIndexArray[0]
                currentSlideShow.slideIndex = slideIndexArray
            if slideIndex < 0:
                slideIndex = 0
            form.slideIndex.data = slideIndex + 1
            try:
                test = str(currentSlideShow.durationInSeconds[slideIndex])
                form.durationInSeconds.data = Decimal(test)
            except AttributeError:
                test = 0.02
                form.durationInSeconds.object_data = str(test)
                form.durationInSeconds.data = Decimal(str(test))
                currentSlideShow.durationInSeconds = [test]
            try:
                form.pan.data = str(currentSlideShow.pan[slideIndex])
            except AttributeError:
                form.pan.data = u'0'
                currentSlideShow.pan = [0] 
            try:
                form.panSpeed.raw_data = str(currentSlideShow.panSpeed[slideIndex])
            except AttributeError:
                form.panSpeed.raw_data = u'0'
                currentSlideShow.panSpeed = [0]                
            try:
                form.scroll.data = str(currentSlideShow.scroll[slideIndex])
            except AttributeError:
                form.scroll.data = u'0'
                currentSlideShow.scroll = [0]
            try:
                form.scrollSpeed.raw_data = str(currentSlideShow.scrollSpeed[slideIndex])
            except AttributeError:
                form.scrollSpeed.raw_data = u'0'
                currentSlideShow.scrollSpeed = [0]
            try:
                form.repetition.raw_data = str(currentSlideShow.repetition[slideIndex])
            except AttributeError:
                form.repetition.raw_data = u'2'
                currentSlideShow.repetition = [2]
            try:
                form.foregroundColors.data = hex(currentSlideShow.foregroundColors[slideIndex] - int('ff000000',16))[2:]
            except AttributeError:
                form.foregroundColors.data = 'ffffff'
                currentSlideShow.foregroundColors = ['ffffff']                
            try:
                form.backgroundColors.data = hex(currentSlideShow.backgroundColors[slideIndex]- int('ff000000',16))[2:]
            except AttributeError:
                form.backgroundColors.data = '000000'
                currentSlideShow.backgroundColors = ['000000']    
            try:
                form.slideText.data = currentSlideShow.slideText[slideIndex]
            except AttributeError:
                form.slideText.data = ''
                currentSlideShow.slideText = ['']                
            try:
                test = currentSlideShow.textInPixies[slideIndex]
                if test:
                    form.textInPixies.data = 'True'
                else:
                    form.textInPixies.data = 'False'
            except AttributeError:
                form.textInPixies.data = 'False'
                currentSlideShow.textInPixies = ['False']
            try: 
                slideImages = currentSlideShow.imageIdList
            except AttributeError:
                if currentSlideShow.slideType == 0:
                    slideImages = []
                    for index, value in currentSlideShow.pan:
                        slideImages.append(["static/blank.jpg",u'',index])
                else:
                    slideImages = []
                    if type(currentSlideShow.objectId) is str:
                        slideImageGroup = SlideImage.Query.all().limit(30).filter(source=currentSlideShow.objectId).order_by("index")
                        if not len(slideImageGroup) == 0:
                            for imageUrl in slideImageGroup:
                                testUrl = imageUrl.fileName.url
                                if testUrl.find(".jpg") == -1 or testUrl.find("back4app") == -1:
                                    imageFile = "static/photos.jpg"
                                else:
                                    imageFile = testUrl
                                slideImages.append([imageFile, imageUrl.objectId, imageUrl.index])
                currentSlideShow.imageIdList = slideImages 

Post

                    currentSlideShow.showName[0] = request.form['showName']
                    currentSlideShow.slideIndex[0] = int(request.form['slideIndex']) - 1
                    slideIndex = currentSlideShow.slideIndex[0]
                    currentSlideShow.slideCount[0] = int(request.form['slideCount'])
                    currentSlideShow.slideType = int(request.form['slideType'])
                    currentSlideShow.durationInSeconds[slideIndex] = float(request.form['durationInSeconds'])
                    currentSlideShow.pan[slideIndex] = int(request.form['pan']) 
                    currentSlideShow.panSpeed[slideIndex] = int(request.form['panSpeed'])
                    currentSlideShow.scroll[slideIndex] = int(request.form['scroll'])
                    currentSlideShow.scrollSpeed[slideIndex] = int(request.form['scrollSpeed'])
                    currentSlideShow.repetition[slideIndex] = int(request.form['repetition'])
                    currentSlideShow.foregroundColors[slideIndex] = int(request.form['foregroundColors'],16) + int('ff000000',16)
                    currentSlideShow.backgroundColors[slideIndex] = int(request.form['backgroundColors'],16) + int('ff000000',16)
                    currentSlideShow.slideText[slideIndex] = request.form['slideText']
                    textInPixiesValue = request.form['textInPixies']
                    if textInPixiesValue == 'True':
                        currentSlideShow.textInPixies[slideIndex] = True
                    else:
                        currentSlideShow.textInPixies[slideIndex] = False
                    try: 
                        slideImages = currentSlideShow.imageIdList
                    except AttributeError:
                        if currentSlideShow.slideType == 0:
                            slideImages = []
                            for index, value in currentSlide.pan:
                                slideImages.append(["static/blank.jpg",u'',index])
                        else:
                            slideImages = []
                            slideImageGroup = SlideImage.Query.all().limit(30).filter(source=currentSlideShow.objectId).order_by("index")
                            if not len(slideImageGroup) == 0:
                                for imageUrl in slideImageGroup:
                                    testUrl = imageUrl.fileName.url
                                    if testUrl.find(".jpg") == -1 or testUrl.find("back4app") == -1:
                                        imageFile = "static/photos.jpg"
                                    else:
                                        imageFile = testUrl
                                    slideImages.append([imageFile, imageUrl.objectId, imageUrl.index])
                    currentSlideShow.imageIdList = slideImages


Add slide
                    currentSlideShow.slideCount[0] = currentSlideShow.slideCount[0] + 1
                    slideIndex = currentSlideShow.slideIndex[0]
                    currentSlideShow.durationInSeconds.insert(slideIndex,float(request.form['durationInSeconds']))
                    currentSlideShow.pan.insert(slideIndex,int(request.form['pan'])) 
                    currentSlideShow.panSpeed.insert(slideIndex, int(request.form['panSpeed']))
                    currentSlideShow.scroll.insert(slideIndex, int(request.form['scroll']))
                    currentSlideShow.scrollSpeed.insert(slideIndex, int(request.form['scrollSpeed']))
                    currentSlideShow.repetition.insert(slideIndex, int(request.form['repetition']))
                    currentSlideShow.foregroundColors.insert(slideIndex, int(request.form['foregroundColors'],16) + int('ff000000',16))
                    currentSlideShow.backgroundColors.insert(slideIndex, int(request.form['backgroundColors'],16) + int('ff000000',16))
                    currentSlideShow.slideText.insert(slideIndex, request.form['slideText'])
                    currentSlideShow.textInPixies.insert(slideIndex, currentSlideShow.textInPixies[slideIndex])
                    currentSlideShow.slideIndex[0] = currentSlideShow.slideIndex[0] + 1
                    try:
                        imageLocation = currentSlideShow.imageIdList[slideIndex]
                    except AttributeError:
                        imageLocation = ["static/blank.jpg",u'',slideIndex]
                    myopener = MyOpener()
                    fh = myopener.open(imageLocation[0])
                    rawData = fh.read()
                    extensionStart = imageLocation[0].find(currentSlideShow.showName[0]) + len(currentSlideShow.showName[0]) + len(str(currentSlideShow.slideIndex[0]))
                    extensionEnd = len(imageLocation[0])
                    newImageName = currentSlideShow.showName[0] + str(slideIndex) + imageLocation[0][extensionStart:extensionEnd]
                    if extensionStart == -1:
                        newImageName = currentSlideShow.showName[0] + str(slideIndex) + ".jpg"
                    newImageFile = File(newImageName, rawData, 'image/' + imageLocation[0][extensionStart:extensionEnd])
                    newImageFile.save()
                    newSlideImage = SlideImage(source=currentSlideShow.objectId,index=slideIndex,fileName=newImageFile)
                    newSlideImage.save()
                    currentSlideShow.imageIdList.insert(slideIndex,[newSlideImage.fileName.url,newSlideImage.objectId,slideIndex])
                    for index in range(len(currentSlideShow.imageIdList)):
                        currentSlideShow.imageIdList[index][2] = index
                        slideImage = SlideImage.Query.get(objectId=currentSlideShow.imageIdList[index][1])
                        slideImage.index = index
                        slideImage.save()

place data in form

                form.showName.data = str(currentSlideShow.showName[0])
                form.slideIndex.raw_data = [currentSlideShow.slideIndex[0] + 1]
                form.slideIndex.data = str(currentSlideShow.slideIndex[0] + 1)
                form.slideCount.raw_data = [len(currentSlideShow.pan)]
                form.slideCount.data = str(len(currentSlideShow.pan))
                form.slideType.data = str(currentSlideShow.slideType)
                test = unicode(currentSlideShow.durationInSeconds[slideIndex])
                form.durationInSeconds.data = Decimal(test)
                form.durationInSeconds.raw_data = [test]    
                form.pan.raw_data = str(currentSlideShow.pan[slideIndex])
                form.panSpeed.data = currentSlideShow.panSpeed[slideIndex]
                form.panSpeed.raw_data = [str(currentSlideShow.panSpeed[slideIndex])]
                form.scroll.raw_data = str(currentSlideShow.scroll[slideIndex])
                form.scrollSpeed.data = currentSlideShow.scrollSpeed[slideIndex]
                form.scrollSpeed.raw_data = [str(currentSlideShow.scrollSpeed[slideIndex])]
                form.repetition.data = currentSlideShow.repetition[slideIndex]
                form.repetition.raw_data = [str(currentSlideShow.repetition[slideIndex])]
                form.foregroundColors.data = hex(currentSlideShow.foregroundColors[slideIndex] - int('ff000000',16))[2:]
                form.backgroundColors.data = hex(currentSlideShow.backgroundColors[slideIndex]- int('ff000000',16))[2:]
                form.slideText.data = currentSlideShow.slideText[slideIndex]
                form.textInPixies.data = str(currentSlideShow.textInPixies[slideIndex])
