# Name:
# Date:
# Description:
#
#

import math, os, pickle, re

class Bayes_Classifier:
    dict_positive = dict();
    dict_negative = dict();

    def __init__(self):
        """This method initializes and trains the Naive Bayes Sentiment Classifier.  If a
        cache of a trained classifier has been stored, it loads this cache.  Otherwise,
        the system will proceed through training.  After running this method, the classifier
        is ready to classify input text."""

        #check if dicts already exist
        if os.path.isfile("dict_positive") and os.path.isfile("dict_negative"):
            self.dict_positive = self.load("dict_positive")
            self.dict_negative = self.load("dict_negative")
            #print "YO!"
        else:
            self.train()
            #print "finished training!"

    def train(self):
        """Trains the Naive Bayes Sentiment Classifier."""
        #get the list of training data
        fileList = []
        for f in os.walk("movies_reviews/"):
          fileList = f[2]
          break

        #build two dicts
        for filename in fileList:
          f = self.loadFile("movies_reviews/"+filename)
          tokens = self.tokenize(f)
          #moives-1-ID
          if filename[7] == '1': #negative reviews
              for token in tokens:
                  token = token.lower()
                  if token in self.dict_negative:
                      self.dict_negative[token] = self.dict_negative[token] + 1
                  else:
                      self.dict_negative[token] = 1
          if filename[7] == '5': #positive reviews
              for token in tokens:
                  token = token.lower()
                  if token in self.dict_positive:
                      self.dict_positive[token] = self.dict_positive[token] + 1
                  else:
                      self.dict_positive[token] = 1

        #save dicts
        self.save(self.dict_positive, "dict_positive")
        self.save(self.dict_negative, "dict_negative")




    def classify(self, sText):
        """Given a target string sText, this function returns the most likely document
        class to which the target string belongs (i.e., positive, negative or neutral).
        """

        #get the list of training data
        fileList = []
        for f in os.walk("movies_reviews/"):
          fileList = f[2]
          break

        #compute prior probability
        positive = 0
        negative = 0
        for filename in fileList:
            if filename[7] == '1': #negative reviews
                negative = negative + 1
            elif filename[7] == '5': #positive reviews
                positive = positive + 1
        prior_positive = positive / (positive+negative)
        prior_negative = negative / (positive+negative)

        #compute frequencies sum of both positive and negative dicts
        #add one to smooth
        freq_positive = 0
        freq_negative = 0
        for word, num in self.dict_positive.iteritems():
            freq_positive = freq_positive + (num+1)
        for word, num in self.dict_negative.iteritems():
            freq_negative = freq_negative + (num+1)
        freq_positive = float(freq_positive)
        freq_negative = float(freq_negative)

        #compute prob for the input text
        prob_positive = 0
        prob_negative = 0
        for token in self.tokenize(sText):
            token = token.lower()
            if token in self.dict_positive:
                prob_positive += math.log((self.dict_positive[token]/freq_positive))
            else:#add one smoothing
                prob_positive += math.log(1/freq_positive)

            if token in self.dict_negative:
                prob_negative += math.log((self.dict_negative[token]/freq_negative))
            else:#add one smoothing
                prob_negative += math.log(1/freq_negative)

        #if prob_positive and prob_negative difference < 0.1, the comment is neutral
        if abs(prob_positive - prob_negative) < 0.1:
            print prob_positive-prob_negative
            return "neutral"
        if prob_positive - prob_negative > 0:
            print prob_positive-prob_negative
            return "positive"
        elif prob_positive - prob_negative < 0:
            print prob_negative-prob_positive
            return "negative"






    def loadFile(self, sFilename):
        """Given a file name, return the contents of the file as a string."""

        f = open(sFilename, "r")
        sTxt = f.read()
        f.close()
        return sTxt

    def save(self, dObj, sFilename):
        """Given an object and a file name, write the object to the file using pickle."""

        f = open(sFilename, "w")
        p = pickle.Pickler(f)
        p.dump(dObj)
        f.close()

    def load(self, sFilename):
        """Given a file name, load and return the object stored in the file."""

        f = open(sFilename, "r")
        u = pickle.Unpickler(f)
        dObj = u.load()
        f.close()
        return dObj

    def tokenize(self, sText):
        """Given a string of text sText, returns a list of the individual tokens that
        occur in that string (in order)."""

        lTokens = []
        sToken = ""
        for c in sText:
         if re.match("[a-zA-Z0-9]", str(c)) != None or c == "\"" or c == "_" or c == "-":
            sToken += c
         else:
            if sToken != "":
               lTokens.append(sToken)
               sToken = ""
            if c.strip() != "":
               lTokens.append(str(c.strip()))

        if sToken != "":
         lTokens.append(sToken)

        return lTokens
