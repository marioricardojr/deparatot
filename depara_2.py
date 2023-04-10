import psycopg
import ngram
import re


def consulta(tabela, coluna, atributo, id):
    try:
        conn = psycopg.connect(
            dbname="ptoiymlf",
            user="ptoiymlf",
            password="f7wT7R3HS3CvPkV9ez350Dvw0HY7651U",
            port="5432",
            host="babar.db.elephantsql.com")

        cur = conn.cursor()
        # se a coluna não for nula retorna apenas o valor da tabela e coluna selecionado
        if coluna != "NULL":
            query = (('select id, "{}" from "{}" where "{}" = {}').format(coluna, tabela, atributo, id))
        # se a coluna for NULL
        if coluna == "NULL":
            # e o atributo não for nulo, retorna a linha do id selecionado
            if atributo != "NULL":
                query = (('select * from "{}" where "{}" = {}').format(tabela, atributo, id))
            # e o atributo for nulo, retorna toda a tabela
            if atributo == "NULL":
                query = (('select * from "{}"').format(tabela))




    except (Exception, psycopg.Error) as error:
        print("Error in update operation", error)

    finally:
        if conn:
            cur.execute(query)
            resultado = cur.fetchall()
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")
    return resultado


def update(tabela, coluna, valor, id):
    try:
        conn = psycopg.connect(
            dbname="ptoiymlf",
            user="ptoiymlf",
            password="f7wT7R3HS3CvPkV9ez350Dvw0HY7651U",
            port="5432",
            host="babar.db.elephantsql.com")
        cur = conn.cursor()
        query = (('UPDATE "{}" SET "{}" = {} WHERE id={} ').format(tabela, coluna, valor, id))
        cur.execute(query)
    except (Exception, psycopg.Error) as error:
        print("Error in update operation", error)
    finally:
        if conn:
            conn.commit()
            cur.close()
            conn.close()
            print("PostgreSQL connection is closed")


def estrutura_dados(id):
    atributos_ok = 0
    # Primeiro passo recuperar elemento
    recupera_elemento = consulta("Elemento", "titulo", "id", id)
    elemento_id = recupera_elemento[0][0]
    elemento = recupera_elemento[0][1]

    if (elemento != "NULL"):
        atributos_ok = +1
        # print(atributos_ok)

    # Recupera conjunto de normas aplicaveis a esse elemento >>AQUI TEM QUE REVER ESSE CONCEITO PARA CASO TIVER MAIS DE UMA NORMA<<
    recupera_conjnormas = consulta("ConjuntoNorma", "Nome", "elementoId", elemento_id)
    # print(len(recupera_conjnormas))
    id_norma = recupera_conjnormas[0][0]
    nome_norma = recupera_conjnormas[0][1]

    if (nome_norma != "NULL"):
        atributos_ok = atributos_ok + 1
        # print(atributos_ok)
    # Recupera atributos da norma
    recupera_norma = consulta("NormaAnalise", "NULL", "perfilID", id_norma)
    norma = []

    norma_temp = []
    tam_norma = len(recupera_norma)
    # Tratamento dos dados recuperados
    for i in range(0, 1):
        for k in range(0, tam_norma):
            norma_temp.clear()
            # atributo
            norma_temp.append(str(recupera_norma[k][1]))
            # valormin
            norma_temp.append(float(recupera_norma[k][2]))
            # valormax
            norma_temp.append(float(recupera_norma[k][3]))
            #tipo operaçao
            norma_temp.append(int(recupera_norma[k][4]))
            norma.append(list(norma_temp))




    # Recupera tipo analise do certificado
    recupera_tipo_analise = consulta("analise", "NULL", "id", elemento_id)
    # print(recupera_tipo_analise)
    analise_id = recupera_tipo_analise[0][0]
    tipo_analise = recupera_tipo_analise[0][1]

    for p in range(2, len(recupera_tipo_analise[0])):
        if (recupera_tipo_analise[0][p] != "NULL"):
            atributos_ok = atributos_ok + 1

    # Recupera valores para cada atributo do certificado
    recupera_atributos_analise = consulta("atributo", "NULL", "analiseId", analise_id)
    # Tratamento dos dados recuperados
    atributos = []
    atributos_temp = []
    tam_atributos = len(recupera_atributos_analise)
    for m in range(0, 1):
        for n in range(0, tam_atributos):
            atributos_temp.clear()
            # atributo
            if (recupera_atributos_analise[n][1] != "NULL"):
                atributos_ok = atributos_ok + 1
                # print(atributos_ok)
            atributos_temp.append(str(recupera_atributos_analise[n][1]))
            # valor
            if (recupera_atributos_analise[n][2] != "NULL"):
                atributos_ok = atributos_ok + 1
                # print(atributos_ok)
            atributos_temp.append(float(recupera_atributos_analise[n][2]))
            atributos.append(list(atributos_temp))

        total_atributos = 6 + len(recupera_atributos_analise) * 2
        # 6 são os atributos que sempre serão buscados e os das normas são multiplicados por 2 por ser atributo e valor

        #calcula o percentual da completude
        comp= (atributos_ok/total_atributos )*100
    #atualiza o valor no banco
    update("analise", "PercentualComple", comp, analise_id)


    return norma, atributos, analise_id


def verifica_conformidade(norma,analise,n):
    atributos_ok=0
    for p in range(0, len(analise)):
        for q in range(0, len(norma)):
            total_atributos = len(analise)

            norma[q][0] = re.sub(r"\s+", "", norma[q][0], flags=re.UNICODE)
            analise[p][0] = re.sub(r"\s+", "", analise[p][0], flags=re.UNICODE)

            if n==1:

                if (((analise[p][0]).lower()).replace(" ", ""))==(((norma[q][0]).lower()).replace(" ", "")):

                    if norma[p][3] == 1:
                        if (analise[p][1] >= norma[q][1]):
                            atributos_ok = atributos_ok+1


                    if norma[p][3] == 2:
                        if (analise[p][1] <= norma[q][2]):
                            atributos_ok = atributos_ok+1


                    if norma[p][3] == 3:
                        if ((analise[p][1] >= norma[q][1])and(analise[p][1] <= norma[q][2])):
                            atributos_ok = atributos_ok+1


            if n<1:
                result_compara = ngram.NGram.compare(((analise[p][0]).lower()).replace(" ", ""),
                                                     ((norma[q][0]).lower()).replace(" ", ""), N=1)
                # result_compara = (jellyfish.jaro_distance(str(norma[q][0]), analise[p][0]))
                #print("a comparação entre",analise[p][0],"e",norma[q][0],"eh",result_compara,"\n")
            # Se o valor encontrado pelo ngrama é maior que o minimo aceitavel definido
                if result_compara >=n:
                    #print("compara",analise[p][0],"e",norma[q][0])
                    # faz as operaçoes, nesse caso só está implementado operação menor igual  #1, maior igual #2, intervalo #3
                    if norma[p][3] == 1:
                        if (analise[p][1] >= norma[q][1]):
                            atributos_ok = atributos_ok+1


                    if norma[p][3] == 2:
                        if (analise[p][1] <= norma[q][2]):
                            atributos_ok = atributos_ok+1


                    if norma[p][3] == 3:
                        if ((analise[p][1] >= norma[q][1])and(analise[p][1] <= norma[q][2])):
                            atributos_ok = atributos_ok+1



        percentual = (atributos_ok / total_atributos) * 100


    return percentual


#aqui é o valor que o outro serviço tem que passar ao chamar esse, esse é o id do documento que vai ser analisado
id_api=1

#faz a estruturação dos dados e calcula completude
norma_analisada,doc_analisado,analiseid = estrutura_dados(id_api)

#calcula conformidade

n=1
resultado_conformidade = verifica_conformidade(norma_analisada,doc_analisado,n)

#atualiza o valor da conformidade no banco
update("analise","PercentualConfor",resultado_conformidade,analiseid)






