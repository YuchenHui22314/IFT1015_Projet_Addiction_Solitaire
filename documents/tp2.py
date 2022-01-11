

#Noms :Yuchen Hui 20150470  Lingxin Zhou 20150704
#Date: 20/12/2020

#la fonction genererEtBrasser prend un nombre non-negatif en parametre et 
#retourne un tableau qui contient les nombre 0~nb sans ordre.
def genererEtBrasser(nb):
    tabCarte=[]
    for i in range(nb):
        tabCarte.append(i)
    for i in range(len(tabCarte)-1,1,-1):
        j=math.floor((i+1)*random())
        temp=tabCarte[i]
        tabCarte[i]=tabCarte[j]
        tabCarte[j]=temp
    return tabCarte

#la fonction img prend en parametre un nombre entre 0 et 51 qui presente une
#carte parmi les 52 cartes utilisees dans le jeu Addition solitaire.
#Elle retourne une balise <img> dont l'attribut src fait reference a l'image
#correspondante.
def img(index):
    couleurs=["C","D","H","S"]
    valeurs=["A","2","3","4","5","6","7","8","9","10",
             "J","Q","K"]
    valeur=valeurs[index//4]   
    couleur=couleurs[index%4]
    if valeur != "A":
        return '<img src="cards/'+valeur+couleur+'.svg">'
    else:
        return ''
    
#La fonction td prend en parametres deux element.identifiant est pour 
#l'attribut id et contenu est egal a innerHTML.
def td(identifiant,contenu):
    
    return ('<td id="case'+str(identifiant)+\
'" onclick="clic('+str(identifiant)+')">'+contenu+'</td>')

#code provenant de demonstration   
def grouper(lst, taille):  # taille = taille maximale des groupes
    groupes = []
    accum = []
    for elem in lst:
        accum.append(elem)
        if len(accum) == taille:
            groupes.append(accum)
            accum = []
    if len(accum) > 0:
        groupes.append(accum)
    return groupes

#fonctions provenant de demonstration.
def tr(contenu): return '<tr>' + contenu + '</tr>'
def table(contenu): return '<table>' + contenu + '</table>'
def trJoin(lst): return tr(''.join(lst))
def tableJoin(lst): return table(''.join(lst))

def listeToTableau(liste,taille):
    liste=list(map(img,liste))   #etape1:transformation en "<img...>"
    
    for i in range(len(liste)):   #etape2:enfermer avec <td id..></td>
        liste[i]=td(i,liste[i])
        
    return tableJoin(list(map(trJoin,grouper(liste,taille))))

#une procedure pour changer le style«background color» vers lime.(green) 
def changerBgColorVert(index):
    case = document.querySelector("#case"+str(index))
    case.setAttribute("style", "background-color: lime")

    
    
#la fonction genererPaquetStruct prend en parametre un tableau des nombres et
#retourne un tableau des enregistrements en transformant chaque nombre en un
#enregistrement d'une maniere unique afin que chaque enregistrement contienne
#des informations sur la couleur, la valeur, la colonne ou il existe, etat de
#vide,et la plus important:la case vers laquelle sera transferee la carte 
#representee par le nombre apres le clic

def genererPaquetStruct(paquet):
    paquetStruct=[]
    couleurs=["C","D","H","S"]
    valeurs=["1","2","3","4","5","6","7","8","9","10",
             "11","12","13"]
    for index in range(len(paquet)):
        colonne=index%13
        couleur=couleurs[paquet[index]%4]
        valeur=valeurs[paquet[index]//4]
        if valeur == "1"  :
            
            vide=True
        else:
            vide=False
        paquetStruct.append(struct(index=index,
                                   colonne=colonne,
                                   couleur=couleur,
                                   valeur=valeur,
                                   positionDesti=None,
                                   vide=vide))
    return paquetStruct



#la procedure avantClic cherche les cases vides et determine le changement 
#a faire apres un clic.
def avantClic():
    global paquet
    global paquetStruct
    global TrousPremiereColonne
    global win
    global lose
    global foisBrasser
    TrousPremiereColonne=[]
    #chercher les cases vides
    
    for caseVide in paquetStruct:
        if caseVide.vide == True:
            
            if caseVide.colonne != 0:   #case vide a la premiere colonne?
                #pas une case vide a la premiere colonne:
                indexPrecedent=caseVide.index-1
                casePrecedente=paquetStruct[indexPrecedent]
                
                if casePrecedente.vide == False:
                    valeur=int(casePrecedente.valeur)
                    couleur=casePrecedente.couleur
                    for carte in paquetStruct:
                        cValeur=int(carte.valeur)
                        if cValeur==valeur+1 and carte.couleur==couleur:

         #la position de destination de cette carte apres un clic.                   
                            carte.positionDesti=caseVide.index
                            changerBgColorVert(carte.index)
            else: #les cases vides a la premiere colonne:
                
                TrousPremiereColonne.append(caseVide.index)
            if len(TrousPremiereColonne)!=0:
                   
                    #simulation de comportement des cartes de valeur 2:
                    for carte in paquetStruct: 
                        if carte.valeur == "2":
                            changerBgColorVert(carte.index)  
                            if carte.colonne == 0: # 2 de colonne=0
                                for indexTrou in TrousPremiereColonne:
                                    if indexTrou < carte.index:
                                        carte.positionDesti=indexTrou
                                    if indexTrou > carte.index:
                                        carte.positionDesti=indexTrou
                                        break
                            else:             #2 de colonne !=0 
                                changerBgColorVert(carte.index)
                                carte.positionDesti=TrousPremiereColonne[0]
                                
    
   
    #jugement de win/lose:
    ligneComplete=0           #variable auxiliaire utile pour le jugement
    
    for carte in paquetStruct:
        if carte.positionDesti!=None:
            break  
            
    else:#win or lose???       
        
        message = document.querySelector("#message")
        message.innerHTML =('<div id="message">Vous devez \
<button onclick="brasser();">Brasser les cartes</button>')
        for index in [0,13,26,39]:
            if paquet[index]//4!=1:
                break   
            else:
                for i in range(1,12):
                    if paquet[index]+4*i!=paquet[index+i]:
                        break
                else:
                    ligneComplete+=1
                if ligneComplete==4:    
                    win=True
        if foisBrasser==0:
            lose=True
            
    #l'affichage de win et lose:
    if lose==True:
        message = document.querySelector("#message")
        message.innerHTML="Vous n'avez pas réussi à placer toutes les cartes.\
.. Essayez à nouveau!"
    if win==True:
        message = document.querySelector("#message")
        message.innerHTML="Vous avez réussi à placer toutes les cartes! Merci!"

        
                
#la procedure clic prend en parametre un nombre entre 0 et 51 qui indique 
#la case cliquee par le souri.Elle s'occupe l'execution de  comportement 
#du jeu apres un clic.

def clic(index):
    global paquet
    global paquetStruct
    global TrousPremiereColonne
    global foisBrasser
    
    carteDepart=paquetStruct[index]
    indexDesti=carteDepart.positionDesti
    if indexDesti != None:
        carteDesti=paquetStruct[indexDesti]
        indexDepart=carteDepart.index
        
        #echangement de carteDepart et carteDesti dans le tableau«paquet»:
        
        temp=paquet[indexDepart]
        paquet[indexDepart]=paquet[indexDesti]
        paquet[indexDesti]=temp
        
        #echangement de carteDepart et carteDesti dans le tableau
        #«paquetStruct»:
        temp=carteDepart.couleur
        carteDepart.couleur=carteDesti.couleur
        carteDesti.couleur=temp
        temp=carteDepart.valeur
        carteDepart.valeur= carteDesti.valeur
        carteDesti.valeur=temp
        temp=carteDepart.vide
        carteDepart.vide= carteDesti.vide
        carteDesti.vide=temp
        
        #initialisation des positionDesti s
        for carte in paquetStruct:
            carte.positionDesti=None
        
        
        #nouvel affichage apres ce clic
        
        div = document.querySelector("#jeu")
        div.innerHTML =listeToTableau(paquet,13)
        
        #Retrouver les cases vides apres clic
        avantClic()

#la procedure brasser va brasser les cartes une fois le joueur clique sur le
#bouton "brasser" en bas et elle va changer le nombre de fois restant pour
#effectuer un brassage.
def brasser():
    global win
    global lose
    global paquet
    global paquetStruct
    global foisBrasser
    
    foisBrasser-=1  
    indexDejaVu=[]
    for index in [0,13,26,39]:
        if paquet[index]//4==1:
            indexDejaVu.append(index)
            for i in range(1,12):
                if paquet[index]+4*i==paquet[index+i]:
                    indexDejaVu.append(index+i)
                else:
                    break
                    
    valeursDejaVu=[]
    for index in indexDejaVu:
        valeursDejaVu.append(paquet[index])
    
    for index in range(len(paquet)):
        if index not in indexDejaVu:
            while True:
                valeurNouvelle=math.floor(random()*52)
                if valeurNouvelle not in valeursDejaVu:
                    paquet[index]=valeurNouvelle
                    indexDejaVu.append(index)
                    valeursDejaVu.append(valeurNouvelle)
                    break
                   
    paquetStruct=genererPaquetStruct(paquet)
    # nouvel affichage
    div = document.querySelector("#jeu")
    div.innerHTML =listeToTableau(paquet,13)
    
    #nouvel affichage en bas
    message = document.querySelector("#message")
    if foisBrasser!=0:
        message.innerHTML =('<div id="message">Vous pouvez encore\
<button onclick="brasser();">Brasser les cartes</button> '+str(foisBrasser)\
+' fois</div>')
    else:
        message.innerHTML="Vous ne pouvez plus brasser les cartes"
        
    avantClic()
    
                 
def init():
    global lose
    global paquet
    global paquetStruct
    global TrousPremiereColonne
    global foisBrasser
    global win
    
    #l'initialisation des variables importantes.
    lose=False
    win=False
    foisBrasser=3
    #les styles et les balises 
    main = document.querySelector("#main")
    main.innerHTML = """
      <style>
        #jeu table { float: none; }
        #jeu table td { border: 0; padding: 1px 2px; height: auto; }
        #jeu table td img { height: auto; }
      </style>
      <div id="jeu">
        
      </div>
      <br>
      <div id="message">
      Vous pouvez encore 
      <button onclick="brasser();">Brasser les cartes</button> 3 fois
      </div>
      <br>
      <button onclick="init();">Nouvelle partie</button>
      """
    
    paquet=genererEtBrasser(52)
    div = document.querySelector("#jeu")
    div.innerHTML =listeToTableau(paquet,13)
    
    paquetStruct=genererPaquetStruct(paquet)
    
    avantClic()

# Commence!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!       
init()
