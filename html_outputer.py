# coding:utf-8
import sqlite3

class HtmlOutputer(object):
    """HTML 输出器"""
    def __init__(self):
        self.datas = []

    def collect_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self, host="localhost", port=27017):
        '''保存数据，可以选择 mongodb、sqlite3、文件，这个方法使用sqlite3，
        迟点改为使用 mongodb，并增加一个判断，当 mongodb 服务未开启时使用下一个
        方法 output_html_file 保存数据到文件中'''
        conn = sqlite3.connect("baike.db")
        cursor = conn.cursor()
        try:
            cursor.execute("""CREATE TABLE baike 
                        (url VARCHAR PRIMARY KEY NOT NULL, 
                        title VARCHAR NOT NULL, 
                        summary TEXT NOT NULL, 
                        content TEXT);""")
        except sqlite3.OperationalError:
            pass

        for data in self.datas:
            try:
                # 必须使用问号格式化内容，否则会出现有语法错误，太坑
                cursor.execute("INSERT INTO baike {} VALUES (?,?,?,?)".format(tuple(data.keys())), tuple(data.values()))
            except sqlite3.IntegrityError:
                continue

        cursor.close()
        conn.commit()
        conn.close()

    def output_html_file(self):
        fout = open("output.html", 'w')

        fout.write("<html>")
        fout.write("<body>")
        fout.write("<table>")

        # ascii
        for data in self.datas:
            fout.write("<tr>")
            fout.write("<td>%s</td>" % data['url'])
            fout.write("<td>%s</td>" % data['title'].encode("utf-8"))
            fout.write("<td>%s</td>" % data['summary'].encode("utf-8"))
            fout.write("</tr>")

        fout.write("</table>")
        fout.write("</body>")
        fout.write("</html>")

        fout.close()
