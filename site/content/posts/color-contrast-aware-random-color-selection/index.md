---
title: color contrast aware random color selection
date: '2020-05-29T00:00:00+00:00'
lastmod: '2020-05-29T00:00:00+00:00'
slug: color-contrast-aware-random-color-selection
categories: []
tags:
- color-contrast-ratio
draft: false
---
When generating synthetic image data, finding and using a pair of colors that are at least human readable is often useful. One crude way to do it is to find two colors in RGB space with minimum distance, but I find this method to be too crude and often it doesn’t give human readable contrast colors even with quite a bit of a high distance threshold.

I wondered if there were more scientific ways that define color contrast and some systematic approach to handle human readable color contrast. I don’t know why I did not bother to google this earlier but I found the concept of “color contrast ratio” which numerically measures contrast between colors. And as I have expected from my butt-headed dive in with random RGB space color picking, each RGB components have different contributions to color contrast which is why my crude method did not seem to give me consistent color pairs that are contrast sufficient.

Here for what contrast ratio is: <https://medium.muz.li/the-science-of-color-contrast-an-expert-designers-guide-33e84c41d156>

calculation formula for color constrast ratio: <https://www.w3.org/TR/WCAG20/#relativeluminancedef>

python module for calculating contrast ratio: <https://pypi.org/project/wcag-contrast-ratio/>

here is my code snippet for randomly picking pair of colors that have minimum contrast ratio:

```python
def pick\_random\_color():
    r = random.randint(0, 255)
    g = random.randint(0, 255)
    b = random.randint(0, 255)

    return (r,g,b)

def normalize\_255\_scaled\_color(color):
    r = color\[0\]/255
    g = color\[1\] / 255
    b = color\[2\] / 255

    return (r,g,b)

def pick\_random\_color\_with\_min\_constrast\_ratio(min\_contrast\_ratio, maxloop=1000):

    assert min\_contrast\_ratio <=21 and min\_contrast\_ratio > 0, "invalid min contrast ratio={}".format(min\_contrast\_ratio)

    loop\_count = 0

    while loop\_count < maxloop:
        color1 = pick\_random\_color()
        color2 = pick\_random\_color()

        norm\_color1 = normalize\_255\_scaled\_color(color1)
        norm\_color2 = normalize\_255\_scaled\_color(color2)

        print(norm\_color1, norm\_color2)

        cr = contrast.rgb(norm\_color1, norm\_color2)
        print(cr)

        if cr >= min\_contrast\_ratio:

            return color1, color2

        loop\_count +=1

    return None

```

with this snippet, it can easily find pair of colors with minimum contrast ratio of 4.5. However, when this threshold is incrased to 10, it does make many more attempts to find a pair. Keep this in mind.
