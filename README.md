# wuhan_corona_virus
up to date spyder of tencent news and BI panel (interactive pyecharts)
Note: please refer to the zip file if you have issues with pyecharts. read the instructions to fix the bug
Geo function fails on fuzzy matching on v1.6 pyecharts (full of bugs). many .py files were copied from old version to fix the bug
see my blog for the demo: https://www.geoseis.cn or https://geoseis.cn/CoV_en.html
tips:
1. Geo function has special requirement for data input. list(zip([list1], [list2])) will help
2. see my blog on how to insert a picture (e.g. wechat QR code ) to html in pyecharts https://www.geoseis.cn/2020/03/05/pyecharts%e5%a6%82%e4%bd%95%e6%b7%bb%e5%8a%a0%e8%87%aa%e5%ae%9a%e4%b9%89%e5%9b%be%e7%89%87/
3. you still need UA, headers for tencent news website. otherwise it'll fail. proxies are note necessary but helpful
4. if you don't know how to automate the script on vpn and upload to your website, read my blog:
https://www.geoseis.cn/2020/03/04/python-%e8%84%9a%e6%9c%ac%e8%87%aa%e5%90%af%e5%8a%a8%e5%8f%8a%e5%ae%9a%e6%97%b6%e4%bb%bb%e5%8a%a1/

Note: the framework of the script was from many blogs. you can google by some of the keywords in the script. main framework is from:
https://blog.csdn.net/qq_43613793/article/details/104268536
the scripts in this blog won't work any more because of update in tencent news. also i did many updates in this script. 

this blog also helps:
https://blog.csdn.net/AIRBOX520/article/details/104221945

5. if you see any countries missing from the Geo map, it's because of country names in the excel not matching the pyecharts Geo map. simply update it in the spreadsheet.

6. for Japan, japan mainland and cruiser ship numbers were added.

