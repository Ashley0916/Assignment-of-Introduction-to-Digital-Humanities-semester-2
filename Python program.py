# -*- coding: utf-8 -*-

## normally all imports I need to use are done at the beginning of the notebook.
import urllib.request
import re
import string
import operator
import matplotlib.pyplot as plt
from wordcloud import WordCloud, ImageColorGenerator

#Exclude common word functions.
def isCommon(ngram):
    commonWords = ["the", "be", "and", "of", "a", "in", "to", "have",
                   "it", "i", "that", "for", "you", "he", "with", "on", "do", "say",
                   "this", "they", "is", "an", "at", "but","we", "his", "from", "that",
                   "not", "by", "she", "or", "as", "what", "go", "their","can", "who",
                   "get", "if", "would", "her", "all", "my", "make", "about", "know",
                   "will","as", "up", "one", "time", "has", "been", "there", "year", "so",
                   "think", "when", "which", "them", "some", "me", "people", "take", "out",
                   "into", "just", "see", "him", "your", "come", "could", "now", "than",
                   "like", "other", "how", "then", "its", "our", "two", "more", "these",
                   "want", "way", "look", "first", "also", "new", "because", "day", "more",
                   "use", "no", "man", "find", "here", "thing", "give", "many", "well"]

    if ngram in commonWords:
        return True
    else:
        return False


def cleanText(input):
 input = re.sub('\n+', " ", input).lower()  #  Match line feeds with spaces replaced by spaces.
 print(type(input))
 input = re.sub('\[[0-9]*\]', "", input)  # Remove reference marks like [1].
 input = re.sub(' +', " ", input)  # Replace multiple consecutive spaces with a single space.
 input = bytes(input.encode('utf-8'))  #encode('utf-8') # Convert content to utf-8 format to eliminate escaped characters.
 # input = input.decode("ascii", "ignore")
 return input


def cleanInput(input):
 input = cleanText(input)
 cleanInput = []
 print(type(input))
 input = input.decode().split(' ')   # Return list separated by spaces.

 for item in input:
  item = item.strip(string.punctuation)  # Getting all punctuation marks by string.punctuation method.

  if len(item) > 1 or (item.lower() == 'a' or item.lower() == 'i'):  # Find words, including individual words such as i,a.
   cleanInput.append(item)
 return cleanInput


def getNgrams(input, n):
 input = cleanInput(input)

 output = {}  # Constructed dictionaries.
 for i in range(len(input) - n + 1):
  ngramTemp = " ".join(input[i:i + n])  # .encode('utf-8')

  if isCommon(ngramTemp.split()[0]) or isCommon(ngramTemp.split()[1]):
   pass
  else:
   if ngramTemp not in output:   # Word frequency statistics.
    output[ngramTemp] = 0  # Typical dictionary operations.
   output[ngramTemp] += 1
 return output

#Get the sentence the core word is in.
def getFirstSentenceContaining(ngram, content):
    #print(ngram)
    sentences = content.split(".")
    for sentence in sentences:
        if ngram in sentence:
            return sentence
    return ""

# Supplementary method: direct reading of the page.
# content = urllib.request.urlopen("http://pythonscraping.com/files/inaugurationSpeech.txt").read()
# print(content)
# Reading of local files, no network required.
content = open("How to build an information time machine.txt").read()
ngrams = getNgrams(content, 2)
sortedNGrams = sorted(ngrams.items(), key = operator.itemgetter(1), reverse=True) # reverse=True Descending order.
print (sortedNGrams)
for top3 in range(3):
    print ("###"+getFirstSentenceContaining(sortedNGrams[top3][0],content.lower())+"###")
# the font from github: https://github.com/adobe-fonts
font = r'simhei.ttf'
#coloring = np.array(Image.open("screenshot.png"))  # Defining the mask layer.
wc = WordCloud(background_color="white",
               collocations=False,
               font_path=font,
               width=1400,
               height=1400,
               margin=2,
               ).generate_from_frequencies(dict(sortedNGrams))
#image_colors = ImageColorGenerator(np.array(Image.open("screenshot.png")))
#plt.imshow(wc.recolor(color_func=image_colors))
plt.imshow(wc)
plt.axis("off")
plt.savefig("1.png")
plt.show()
wc.to_file('save.png')  # Save the word cloud.
plt.hist(list(filter(lambda y:y>1,map(lambda x:x[-1],sortedNGrams))),bins=20)  # Counting the number of categories under each word frequency, here the words that occur once are removed using filter.
plt.xlabel('words frequence')
plt.ylabel('times')
plt.savefig("2.png")
plt.show()