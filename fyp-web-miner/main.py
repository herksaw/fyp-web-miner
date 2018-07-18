from web.parser import Parser

from lxml import etree
from lxml import html
from lxml.html import tostring, html5parser

# import tensorflow as tf

url_list = ["https://www.york.ac.uk/teaching/cws/wws/webpage1.html",
            "https://www.lazada.com.my/catalog/?q=laptop&_keyori=ss&from=input&spm=a2o4k.home.search.go.75f824f6QLmzE4",
            "http://www.11street.my/totalsearch/TotalSearchAction/searchTotal.do?targetTab=T&isGnb=Y&prdType=&category=&cmd=&pageSize=60&lCtgrNo=0&mCtgrNo=0&sCtgrNo=0&ctgrType=&fromACK=&gnbTag=TO&schFrom=&tagetTabNm=T&aKwdTrcNo=&aUrl=&kwd=laptop&callId=7274c0ac642e390b8fc",
            "https://shopee.com.my/search/?keyword=laptop",
            "https://www.lelong.com.my/catalog/all/list?TheKeyword=laptop",
            "https://s.taobao.com/search?q=%E6%89%8B%E6%8F%90%E7%94%B5%E8%84%91&imgfile=&commend=all&ssid=s5-e&search_type=item&sourceId=tb.index&spm=a21bo.2017.201856-taobao-item.1&ie=utf8&initiative_id=tbindexz_20170306",
            "https://www.amazon.com/s/ref=nb_sb_noss?url=search-alias%3Daps&field-keywords=laptop",
            "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSDF15D356B046D53BC1256D550038A9E0?OpenDocument&wg=U1232&refDoc=CMS322921A477B31844C125707B0034EB15",
            "https://www.schukat.com/schukat/schukat_cms_en.nsf/index/CMSB5A38F73D94252D2C125707B00357507?OpenDocument"]

if __name__ == "__main__":
    curr_url = url_list[0]

    parser = Parser()

    # parser.start_parsing(curr_url)
    parser.start_mdr(curr_url)
