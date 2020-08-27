from wordcloud import WordCloud
import matplotlib.pyplot as plt
import numpy as np

text = 'contripy ' * 20


x, y = np.ogrid[:1000, :1000]
mask = (x - 500) ** 2 + (y - 500) ** 2 > 400 ** 2
mask = 255 * mask.astype(int)

wordcloud = WordCloud(background_color='white', repeat=True, mask=mask).generate(text)

plt.imshow(wordcloud, interpolation='bilinear')
plt.axis('off')
plt.savefig('contripy_logo.png')
