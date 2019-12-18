# Bing advanced options
### Crash course

#### Bing advanced options and what they mean

The following is a list of bing advanced options that can be passed

To the BingUrl class

See [Bing Advanced options](http://help.bing.microsoft.com/#apex/18/en-US/10001/-1)

> * `contains`: Find results with filetypes specified
>> Eg to find pdfs type <code> arrival to earth transformers contains:pdf</code>
> * `ext`:Returns web pages with filename extension specified 
>> Eg to find reports created in DOCX format type <code>subject ext:docx</code>
> * `filetype`: Returns web pages with the filenames specified
>> Eg to find reports created in PDF type <code>filetype:pdf</code>
> * `inanchor` `inbody` `intitle`: Return pages that contain specified term in metadata 
>> Eg to  find web pages containing wiki in the title type <code>intitle:wiki</code>
> * `ip`: Find sites hosted by a specific IP address
>> Eg type <code>ip:127.0.0.1</code>
> * `language` or `ln` : Returns webpages for a specific country or region
>> Eg add <code>language:en</code> to fetch results in English
> *  `loc` or `location` : Return web pages for a specific country or region
>> See [Country, region and language codes](http://help.bing.microsoft.com/#apex/18/en-US/10004/-1)
> * `prefer`: Add emphasis to search terms
>>Eg to search for football with regards to organisations type <code>football prefer:organisation</code>
>* `site`:Return web pages belonging to a specified site 
>> Eg to find web stories about DDT type <code>DDT site:wikipedia.com</code>
> * `feed`: Find RSS or Atom feeds on a website
>> Feeds about Android type feed:Android
> * `hasfeed`: Find pages that contain RSS ot Atom feeds


```
  > Do not include a space after the colon in the keywords
  > Some features are not available in all countries/regions
```