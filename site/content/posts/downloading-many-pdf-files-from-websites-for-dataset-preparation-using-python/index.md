---


title: web scraping many pdf files from websites for dataset preparation using python
date: '2022-05-24T00:00:00+00:00'
lastmod: '2022-05-24T00:00:00+00:00'
slug: downloading-many-pdf-files-from-websites-for-dataset-preparation-using-python
categories:
- python
tags:
- "download"
- "pdf"
- "web-scraping"
- "web-scrapper"
- "downloading"
draft: false
---
There are good websites which store a lot of pdf files that can be used for data. However, it can be quite difficult to automate the downloading process with a simple web scraping tool because the data download url that the user wants resides behind another webpage. I will use IMF website for example.

## Gathering bulletin’s item urls

`[https://www.imf.org/en/publications/reo](https://www.imf.org/en/publications/reo)` this url has a paginated bulletin which holds links to many pdf publications. Thankfully, this page is not a javascript rendered site and instead the html response is the final html that is shown in the web browser. If the page was javascript rendered (e.g. developed by React etc.), then the html response for this url wouldn’t contain the final html visualized by the web browser. In this case, we need to use a headless web browser driver to simulate a web browser but this is another topic.

One can check if the webpage is javascript rendered or not by simply viewing the ‘page sourcecode’ by right clicking the webpage. If the page sourcecode contains the final html that is rendered on screen, then you are good to go.

As of now, the bulletin has 17 pages and for each page there are multiple pagelinks which contains the actual pdf link.

Right click a page item and go to ‘inspect’ to see the exact html element that hold it.

```generic
<a href="/en/Publications/REO/SSA/Issues/2022/04/28/regional-economic-outlook-for-sub-saharan-africa-april-2022">        Regional Economic Outlook for Sub-Saharan Africa, April 2022
</a>
```

It is an element where the `href` attribute hold the url to the webpage that contains the pdf link. The first stage will be gathering all these page urls.

One can check the xpath of this element by right clicking it -> copy -> copy full xpath.

the xpath is like this:

```generic
/html/body/div\[3\]/main/article/div\[3\]/div\[2\]/h6/a
```

Check the next item’s xpath which is:

```generic
/html/body/div\[3\]/main/article/div\[3\]/div\[3\]/h6/a
```

we can see that the last `div`’s number is increased. Therefore we can figure out that we can gather all the elements holding the webpage urls as href using the following xpath

```generic
/html/body/div\[3\]/main/article/div\[3\]/div\[\*\]/h6/a
```

As for navigating the 17 pages, we try moving to page 2. The webpage url changes to `https://www.imf.org/en/publications/reo?page=2`. We can figure out that we can navigate pages by changing the value at the end of the url. (e.g. <https://www.imf.org/en/publications/reo?page=3>, <https://www.imf.org/en/publications/reo?page=4> )

We figured out how to navigate through bulletin pages, and how to extract the elements holding the items in each page. Let’s put this into python code, using `requests` and `lxml` package.

```generic
import requests
from lxml import etree

base\_url = "https://www.imf.org/en/publications/reo"

page\_count = 17

hrefs = \[\]
for pageno in tqdm(range(1, page\_count + 1)):

    page\_url = f"{base\_url}?page={pageno}"

    resp = requests.get(page\_url)

    root = etree.HTML(resp.text)

    a = root.xpath("/html/body/div\[3\]/main/article/div\[3\]/div\[\*\]/h6/a")

    # gather hrefs

    for b in a:
        try:

            h = b.attrib\["href"\]
            hrefs.append(h)
        except:
            continue
```

In the code, after gathering the elements, we also checked if it had `href` attribute and gathered the urls.

## Extract actual pdf download url from item webpages

Let’s inspect a few pdf link containing webpage urls that we gathered in the previous section.

Check this url: <https://www.imf.org/en/Publications/REO/SSA/Issues/2022/04/28/regional-economic-outlook-for-sub-saharan-africa-april-2022>

There is a `full report` button which downloads the pdf file. Inspecting this button, we get the following html element

```generic
<a href="/-/media/Files/Publications/REO/AFR/2022/April/English/text.ashx"><img src="/-/media/Images/IMF/Flagship/section-images/icon-pdf.ashx?la=en" alt="">Full REPORT</a>
```

The actual download pdf url is `"/-/media/Files/Publications/REO/AFR/2022/April/English/text.ashx`, which is relative path. The realpath would be `https://www.imf.org"/-/media/Files/Publications/REO/AFR/2022/April/English/text.ashx`

Try opening this url in a new tab, and you can see that it downloads the pdf. Or you can check if this url is valid from the terminal

```generic
$ wget "/-/media/Files/Publications/REO/AFR/2022/April/English/text.ashx
```

try this command in linux, change the extention to ‘pdf’ and you can see that it is a valid pdf file.

From this small experiment, we have confirmed that performing GET on `~~~.ashx` urls are enough to trigger downloading the pdfs.

On this example url, the xpath of this `full report` button is

```generic
/html/body/div\[3\]/article/div\[4\]/div/div\[2\]/ul/li\[1\]/a
```

Let’s check another url: <https://www.imf.org/en/Publications/REO/EU/Issues/2017/01/25/SAFEGUARDING-THE-RECOVERY-AS-THE-GLOBAL-LIQUIDITY-TIDE-RECEDES>

This webpage has a different layout as the first one, and not only if the pdf download url different, there are more than one pdf download urls.

this is the full text download button element

```generic
<a href="/~/media/Websites/IMF/imported-flagship-issues/external/pubs/ft/reo/2014/eur/eng/pdf/\_ereo0414pdf.ashx" class="colorlink">Download<br>Full Text </a>
```

and this is the spanish executive summary download url element:

```generic
<a href="/~/media/Websites/IMF/imported-flagship-issues/external/spanish/pubs/ft/reo/2014/eur/\_ereo0414exespdf.ashx" title="Español">Español</a>
```

and we see that images used in the webpage also have the `~~~.ashx` href. We need to exclude them.

After inspecting these two, I decided to go with the following strategy:

- gather all elements that have `href` attribute in webpage
- among the collected elements, check the `href` url value and if it contains “pdf” or “media/Files” string inside it, then consider these urls to be valid pdf download urls

With this strategy we can gather valid pdf download urls. Lets put this into python code:

```generic
import requests
from lxml import etree
from urllib.parse import urljoin

def find\_download\_urls\_from\_root(url, root):

    ret = root.xpath("//a\[contains(@href,'.ashx')\]")

    sub\_url\_set = set()

    for r in ret:
        href = r.attrib\["href"\]
        sub\_url\_set.add(href)

    output = \[\]
    for s in list(sub\_url\_set):
        full\_url = urljoin(url, s)

        add = False
        if "media/Files" in s:
            add = True
        elif "pdf" in s:
            add = True

        if add:
            output.append(full\_url)
    return output

# main
# \`urls\` variable hold the webpage urls gathered in previous section
for u in tqdm(urls):

    resp = requests.get(u)

    root = etree.HTML(resp.text)

    downloadable\_urls = find\_download\_urls\_from\_root(u, root)

    if not downloadable\_urls:
        no\_xpath\_found\_urls.append(u)
    else:
        download\_urls.extend(downloadable\_urls)
```

`urljoin` function from `urllib` package is very useful when converting relative url paths to absolute url paths.

### Download pdf and save as pdf

Now that we have gathered all the direct pdf download urls, all that remains is simply downloading them. The only consideration is how to save the http response as a pdf file. This is very simple.

```generic
import requests, os

def try\_download(url, index, savedir):

    r = requests.get(url)

    if r.status\_code != 200:
        return False

    filename = get\_filename(url)
    filename = f"{index:05d}\_{filename}"

    if len(filename) > 200:
        filename = filename\[:200\]

    savepath = os.path.join(savedir, f"{filename}.pdf")

    with open(savepath, "wb") as fd:
        fd.write(r.content)

    return True

# main  
# prepare dir to save. in this code, variable \`savedir\` hold this information.
# assume download\_urls variable hold the pdf download urls.

for i, u in enumerate(download\_urls):
    try\_download(u, i, savedir)
```

saving `response.content` as binary format and saving with filename having `.pdf` extension is enough to save pdf file.

---

I emphasize that this procedure is possible since all webpages accessed in this tutorial were not javascript rendered webpages and finalized static htmls were sent over http response.
