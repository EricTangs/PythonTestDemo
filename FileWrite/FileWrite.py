file=open(r"F:\TestDemo\Python\PythonDemo\ZBPy\1.txt","wb")
myStr="""
397218641@qq.com,金玲玉,翠竹园西村,134,1501,,15856932310,21.80
573412569@qq.com,金玲玉,深圳大学 海棠阁601,144,7,,13428968478,56.50
数量2
"""
file.write(myStr.encode("utf-8"))
file.close()