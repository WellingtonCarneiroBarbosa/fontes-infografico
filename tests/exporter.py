import pandas as pd
import os, random

def excel_exporter(names, comments, codes):
    try:
        m = 0
        fname = "comments.csv"
        while os.path.exists(fname):
            m += 1
            fname = "comments" + "(" + str(m) + ")" + ".csv"
        temp = {}                    
        temp_names = []
        temp_comments = []
        temp_codes = []
        temp_names.extend(names)
        temp_comments.extend(comments)
        temp_codes.extend(codes)
        temp.update({'a - username': temp_names, 'b - comment': temp_comments, 'c - codes': temp_codes})
        df = pd.DataFrame(temp)
        df.to_csv(fname, index=False, encoding='utf-8')
    except Exception as e:
        print("\rErro no codigo do excel_exporter")
        print("\rComunique o desenvolvedor")
        print("\rCodigo do erro (mostre isso ao desenvolvedor) => ")
        print(e)


users = []
comments = []
print("gerando codigos....")
codes = random.sample(range(10000000, 99999999), 10000000)

print("gerando comentarios fakes...")
for i in range(10000000):
    print("\rgenerate " + str(i))
    users.append("blablabla blablabla")
    comments.append("blablabla blablabla")

print("salvando na planilha...")
excel_exporter(users, comments, codes)
print("finalizado com sucesso!!!!!!")