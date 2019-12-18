# ISearch

A command-line Search Engine

Search the world from the comfort of your command line

### Features of ISearch

- We got a lit command line interface built using urwid checkout that project [here](https://github.com/urwid/urwid)
- Ability to fetch next results of a search query(ability to fetch previous search results is in the implementation stage)
- Colors (Because we all love colors)
- Ability to choose which search engine to use( Right now limited to Bing, Google and DuckDuckGo) 
- Support for DuckDuckGo [!bangs](https://api.duckduckgo.com/bang)
- Download box for those times you need to download things quickly.
-  Output results in xml or JSON
 - Error Handling when there is no internet connection.
 
### Installation
Cloning the Repository
```
git clone https://github.com/steve-tyler/ISearch.git
```
ISearch requires external libraries to function well and Python 3

External libraries can be installed by 
```
pip3 install -r requirements.txt
```
or 
```
pip3 install  selenium bs4 lxml urwid requests
```

### Running 
In the ISearch directory run <code> ./isearch -h</code>  for available options 

##### Interactive mode
[![Isearch Interactive mode](https://i.ibb.co/DQgszRh/https-i-ytimg-com-vi-w-Bf-Rq-Eb-Vz0s-maxresdefault.jpg)](https://youtu.be/wBfRqEbVz0s "Isearch Interactive mode")

### Problems
Gnome terminal version 3.34.2 was rendering very weird interfaces

### Contribution
Feel free to report any issues encountered and also feature requests are welcome:fire:
#### Todo
- Add a previous button in the Interactive mode
- Add more search engines
### Donation
Donation for good work is highly appreciated
For those wishing to donate via Paypal that can be done from [here](https://www.paypal.com/cgi_bin/webscr?cmd=_pay-inv&viewtype=altview&id=INV2-5JYK-9F6Z-3W5F-FJSC)




