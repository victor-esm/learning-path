import string
from PIL import Image
import numpy as np
from matplotlib import pyplot as plt
from wordcloud import WordCloud, STOPWORDS

with open('trump_inaugural_address_jan_20_2025.txt', 'r') as file:
    trump_full_text = file.read()
with open('biden_inaugural_address_jan_20_2021.txt', 'r') as file:
    biden_full_text = file.read()

# Cleaning process:
trump_cleaned_text = trump_full_text.lower()
biden_cleaned_text = biden_full_text.lower()

for char in string.punctuation:
            trump_cleaned_text = trump_cleaned_text.replace(char, ' ')
            biden_cleaned_text = biden_cleaned_text.replace(char, ' ')

trump_words_list = trump_cleaned_text.split()
biden_words_list = biden_cleaned_text.split()

trump_single_word_string = ' '.join(trump_words_list)
biden_single_word_string = ' '.join(biden_words_list)

# Start of word cloud
stopwords=set(STOPWORDS)
stopwords.add('applause')
stopwords.add('thank')
stopwords.add('will')
stopwords.add('day')
stopwords.add('today')
stopwords.add('president')
stopwords.add('ll')
stopwords.add('ve')
stopwords.add('s')
stopwords.add('us')

# Create the masks
trump_mask_img = Image.open("trump.png").convert("L")  # grayscale
trump_mask = np.array(trump_mask_img)
trump_mask = np.where(trump_mask > 10, 255, 0).astype(np.uint8)

biden_mask_img = Image.open("biden.png").convert("L")
biden_mask = np.array(biden_mask_img)
biden_mask = np.where(biden_mask > 10, 255, 0).astype(np.uint8)

# Code to assess quality of the mask
# fig = plt.figure(figsize=(14, 18))
# plt.imshow(trump_mask, cmap=plt.cm.gray, interpolation='bilinear')
# plt.axis('off')
# plt.show()

trump_speech_wc = WordCloud(stopwords=stopwords, background_color='white', max_words=2000, mask=trump_mask)
trump_speech_wc.generate(trump_single_word_string)

biden_speech_wc = WordCloud(stopwords=stopwords, background_color='white', max_words=2000, mask=biden_mask)
biden_speech_wc.generate(biden_single_word_string)

fig = plt.figure(figsize=(40,20))
ax1=fig.add_subplot(1, 2, 1)
plt.imshow(trump_speech_wc, interpolation='bilinear')
plt.axis('off')

ax2=fig.add_subplot(1, 2, 2)
plt.imshow(biden_speech_wc, interpolation='bilinear')
plt.axis('off')
plt.show()
