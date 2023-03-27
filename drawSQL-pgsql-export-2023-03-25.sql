CREATE TABLE "analise"(
    "id" INTEGER NOT NULL,
    "elementoId" INTEGER NOT NULL,
    "arquivo" VARCHAR(255) NOT NULL,
    "numeroDoc" VARCHAR(255) NOT NULL,
    "PercentualComple" DOUBLE PRECISION NOT NULL,
    "PercentualConfor" DOUBLE PRECISION NOT NULL
);
ALTER TABLE
    "analise" ADD PRIMARY KEY("id");
CREATE TABLE "Elemento"(
    "id" INTEGER NOT NULL,
    "titulo" VARCHAR(255) NOT NULL
);
ALTER TABLE
    "Elemento" ADD PRIMARY KEY("id");
CREATE TABLE "NormaAnalise"(
    "id" INTEGER NOT NULL,
    "atributo" VARCHAR(255) NOT NULL,
    "valorMin" VARCHAR(255) NOT NULL,
    "valorMax" VARCHAR(255) NOT NULL,
    "operacaoId" INTEGER NOT NULL,
    "perfilID" INTEGER NOT NULL
);
ALTER TABLE
    "NormaAnalise" ADD PRIMARY KEY("id");
CREATE TABLE "ConjuntoNorma"(
    "id" INTEGER NOT NULL,
    "Nome" VARCHAR(255) NOT NULL,
    "elementoId" INTEGER NOT NULL
);
ALTER TABLE
    "ConjuntoNorma" ADD PRIMARY KEY("id");
CREATE TABLE "atributo"(
    "id" INTEGER NOT NULL,
    "nome" VARCHAR(255) NOT NULL,
    "valor" VARCHAR(255) NOT NULL,
    "status" VARCHAR(255) CHECK
        ("status" IN('')) NOT NULL,
        "analiseId" INTEGER NOT NULL
);
ALTER TABLE
    "atributo" ADD PRIMARY KEY("id");
CREATE TABLE "tipoOperacao"(
    "id" INTEGER NOT NULL,
    "tipoOperacao" INTEGER NOT NULL
);
ALTER TABLE
    "tipoOperacao" ADD PRIMARY KEY("id");
ALTER TABLE
    "analise" ADD CONSTRAINT "analise_elementoid_foreign" FOREIGN KEY("elementoId") REFERENCES "Elemento"("id");
ALTER TABLE
    "NormaAnalise" ADD CONSTRAINT "normaanalise_perfilid_foreign" FOREIGN KEY("perfilID") REFERENCES "ConjuntoNorma"("id");
ALTER TABLE
    "ConjuntoNorma" ADD CONSTRAINT "conjuntonorma_elementoid_foreign" FOREIGN KEY("elementoId") REFERENCES "Elemento"("id");
ALTER TABLE
    "NormaAnalise" ADD CONSTRAINT "normaanalise_operacaoid_foreign" FOREIGN KEY("operacaoId") REFERENCES "tipoOperacao"("id");
ALTER TABLE
    "atributo" ADD CONSTRAINT "atributo_analiseid_foreign" FOREIGN KEY("analiseId") REFERENCES "analise"("id");