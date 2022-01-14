palavras = "empatia, embuste, cônjuge, exceção, efêmero, prolixo, caráter, idílico, verbete, análogo, genuíno, estória, sublime, pêsames, sucinto, inferir, apático, audácia, astúcia, acepção, família, recesso, pródigo, redimir, estável, estigma, cinismo, refutar, cultura, exortar, icônico, virtude, mórbido, cordial, trivial, escória, soberba, síntese, emergir, imputar, aspecto, mitigar, anátema, luxúria, deboche, candura, almejar, excerto, alegria, ademais, sucesso, frívolo, litígio, através, oriundo, contudo, austero, sensato, estrupo, fomento, alcunha, excesso, ambíguo, salutar, quimera, caralho, conciso, ambição, parcial, imersão, orgulho, modesto, coragem, exilado, relação, isenção, notório, exótico, ninfeta, padecer, colosso, demanda, erudito, auferir, ansioso, déspota, estirpe, colapso, difusão, intenso, inércia, volátil, emotivo, vigente, límpido, saudade, profano, piedade, hesitar, ousadia"

word = "Manel"
numeroDeArquivos = 20
conjuntoDePalavras = 1

frequencia = [2*i for i in range(numeroDeArquivos)]

for i in range(numeroDeArquivos):
    with open("Arquivos/arq"+str(i)+".txt", "w") as arquivo:
        for j in range(conjuntoDePalavras):
            arquivo.write(palavras)
        for k in range(frequencia[i]):
            arquivo.write(" "+ word + " ")
















