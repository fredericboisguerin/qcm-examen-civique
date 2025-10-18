# -*- coding: utf-8 -*-
import json, random, os, zipfile, textwrap, math, itertools, string, datetime

root = "/mnt/data/qcm_civique_fr"
os.makedirs(root, exist_ok=True)

random.seed(42)  # deterministic

# Helper to build a question dict
def q(question, options, correct_idx, difficulty="facile", indice=None, explication=None):
    d = {"question": question.strip(),
         "options": [o.strip() for o in options],
         "correct_option": int(correct_idx)}
    if difficulty == "difficile":
        # Only include hint/explanation for difficult
        if indice:
            d["indice"] = indice.strip()
        if explication:
            d["explication"] = explication.strip()
    return d

# Small utility to shuffle options and track correct index
def make_options(correct, distractors):
    opts = distractors + [correct]
    random.shuffle(opts)
    correct_idx = opts.index(correct)
    return opts, correct_idx

# Pools by theme/subtheme and difficulty
# We keep pools concise but with parameterization for variety.
first_names = ["Aïcha", "Marc", "Fatou", "Thomas", "Sofia", "Mehdi", "Claire", "Nadia", "Jean", "Lina"]
cities = ["Lyon", "Marseille", "Lille", "Bordeaux", "Toulouse", "Rennes", "Nantes", "Strasbourg", "Nice", "Paris"]
rivers = ["Seine", "Loire", "Garonne", "Rhin", "Rhône", "Meuse"]
mountains = ["Alpes", "Pyrénées", "Massif central", "Jura", "Vosges"]
eu_institutions = ["Parlement européen", "Conseil de l’Union européenne", "Commission européenne"]
departements_outre_mer = ["Guadeloupe", "Martinique", "Guyane", "La Réunion", "Mayotte"]

def gen_devise_symboles(difficulty):
    items = []
    # 1) Devise
    if difficulty == "facile":
        question = "Quelle est la devise de la République française ?"
        correct = "Liberté, Égalité, Fraternité"
        distractors = ["Ordre, Progrès, Travail", "Unité, Justice, Paix", "Patrie, Honneur, Valeur"]
        opts, idx = make_options(correct, distractors)
        items.append(q(question, opts, idx, difficulty))
    else:
        form = random.choice([
            ("Complétez la devise républicaine : Liberté, Égalité, _____.", "Fraternité",
             ["Neutralité", "Laïcité", "Solidarité"],
             "Indice : c’est une valeur civique, non pas un principe juridique comme la laïcité.",
             "La devise officielle est « Liberté, Égalité, Fraternité ». La laïcité n’en fait pas partie."),
            ("Laquelle des propositions n’est pas un symbole officiel de la République française mentionné par la Constitution ?",
             "Le coq gaulois",
             ["Le drapeau tricolore", "La Marseillaise (hymne)", "La devise « Liberté, Égalité, Fraternité »"],
             "Indice : pensez à la différence entre symboles constitutionnels et coutumiers.",
             "Le coq est un symbole coutumier, pas constitutionnel, à la différence du drapeau, de l’hymne et de la devise.")] )
        question, correct, distractors, ind, exp = form
        opts, idx = make_options(correct, distractors)
        items.append(q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None))

    # 2) Langue officielle
    if difficulty == "facile":
        question = "Quelle est la langue officielle de la République selon la Constitution ?"
        correct = "Le français"
        distractors = ["Le français et l’anglais", "Les langues régionales", "Aucune, la Constitution ne le précise pas"]
        opts, idx = make_options(correct, distractors)
        items.append(q(question, opts, idx, difficulty))
    else:
        question = "D’après l’article 2 de la Constitution, quelle affirmation est exacte concernant la langue ?"
        correct = "« Le français est la langue de la République »."
        distractors = ["Le français et l’anglais sont co-officiels.", "Chaque région fixe librement sa langue officielle.", "Aucune langue n’est mentionnée dans la Constitution."]
        opts, idx = make_options(correct, distractors)
        ind = "Indice : article 2 de la Constitution de 1958."
        exp = "L’article 2 dispose explicitement que le français est la langue de la République."
        items.append(q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None))

    # 3) Symboles
    question = "Quel est l’hymne national de la France ?"
    correct = "La Marseillaise"
    distractors = ["Le Chant des Partisans", "La Carmagnole", "Le Chant du Départ"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items[:3]

def gen_laicite(difficulty):
    items = []
    # 1) Principe
    if difficulty == "facile":
        question = "La laïcité garantit d’abord :"
        correct = "La liberté de conscience et l’égalité des citoyens quelles que soient leurs croyances."
        distractors = ["La priorité d’une religion sur les autres.", "L’interdiction de toute pratique religieuse.", "La religion d’État."]
        opts, idx = make_options(correct, distractors)
        items.append(q(question, opts, idx, difficulty))
    else:
        question = "Laquelle de ces affirmations décrit le mieux la neutralité de l’État au regard des religions ?"
        correct = "L’État ne favorise ni ne défavorise aucun culte et garantit leur libre exercice dans le respect de l’ordre public."
        distractors = ["L’État contrôle les doctrines religieuses.", "Les cultes sont autorisés seulement dans les édifices privés.", "L’État impose la laïcité aux associations privées sans exception."]
        opts, idx = make_options(correct, distractors)
        ind = "Indice : loi de séparation des Églises et de l’État de 1905."
        exp = "La neutralité implique l’absence de privilège ou de discrimination entre cultes ; la liberté de culte s’exerce dans le cadre de l’ordre public."
        items.append(q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None))

    # 2) Usagers/agents
    if difficulty == "facile":
        question = "À l’école publique, les élèves :"
        correct = "Doivent respecter les règles de la laïcité et ne pas perturber les enseignements."
        distractors = ["Peuvent refuser un cours pour motif religieux.", "Imposent leurs convictions à leurs camarades.", "Sont tenus de participer à un culte."]
        opts, idx = make_options(correct, distractors)
        items.append(q(question, opts, idx, difficulty))
    else:
        question = "Dans un service public, qui est juridiquement tenu à une stricte neutralité religieuse ?"
        correct = "Les agents publics dans l’exercice de leurs fonctions."
        distractors = ["Tous les usagers en toutes circonstances.", "Les élus uniquement lors des séances publiques.", "Personne : la neutralité est purement symbolique."]
        opts, idx = make_options(correct, distractors)
        ind = "Indice : distinguer usagers et agents."
        exp = "Les agents publics ont une obligation de neutralité ; les usagers disposent de la liberté de manifester leurs convictions, sous réserve de l’ordre public et du non-prosélytisme."
        items.append(q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None))

    return items[:2]

def gen_principes_mises_sit(difficulty):
    items = []
    # 6 scenarios
    for _ in range(6):
        p = random.choice(first_names)
        situation = random.choice([
            f"{p} souhaite afficher une banderole d’opinion sur son balcon.",
            f"{p} refuse de serrer la main d’un élu pour des raisons religieuses.",
            f"{p} veut organiser une manifestation déclarée en centre-ville.",
            f"{p} porte un signe religieux ostensible lors d’une démarche en mairie.",
            f"{p} souhaite créer une association culturelle locale.",
            f"{p} critique publiquement une décision du gouvernement."
        ])
        if difficulty == "facile":
            question = f"{situation} Quel principe républicain protège d’abord son droit, dans le respect de la loi ?"
            correct = random.choice(["La liberté d’expression", "La liberté d’association", "La liberté de manifestation"])
            distractors = ["La censure préalable", "La supériorité d’une religion", "La suppression des libertés locales"]
        elif difficulty == "moyen":
            question = f"{situation} Quel cadre juridique s’applique en priorité ?"
            correct = random.choice(["Libertés publiques encadrées par l’ordre public", "Déclaration préalable et respect du parcours fixé", "Neutralité du service public"])
            distractors = ["Autorisation religieuse préalable", "Référendum local obligatoire", "Censure municipale discrétionnaire"]
        else:
            question = f"{situation} Quelle réponse juridiquement la plus exacte respecte les principes républicains ?"
            correct = "Exercer la liberté invoquée sous réserve de l’ordre public et sans prosélytisme abusif."
            distractors = ["Toute liberté prime sur l’ordre public.", "La religion autorise à déroger aux règles communes.", "Le maire peut interdire toute expression d’opinion."]
        opts, idx = make_options(correct, distractors)
        ind = "Indice : liberté oui, mais encadrée par l’ordre public."
        exp = "Les libertés (expression, réunion, association, culte) existent mais se concilient avec l’ordre public et le respect des règles communes."
        items.append(q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None))
    return items

def gen_democratie_vote(difficulty):
    items = []
    # 3 questions
    # 1) Séparation des pouvoirs
    if difficulty == "facile":
        question = "Quel pouvoir fait la loi en France ?"
        correct = "Le pouvoir législatif (Parlement)"
        distractors = ["Le pouvoir exécutif (Gouvernement)", "Le pouvoir judiciaire (Juges)", "Le Président seul"]
    elif difficulty == "moyen":
        question = "Quel énoncé caractérise l’État de droit ?"
        correct = "La loi s’applique à tous, autorités publiques comprises."
        distractors = ["La coutume prime toujours la loi.", "Le gouvernement peut ignorer la loi.", "La majorité n’est pas liée par la Constitution."]
    else:
        question = "Selon la DDHC, l’absence de séparation des pouvoirs conduit à :"
        correct = "L’impossibilité d’une Constitution (art. 16)."
        distractors = ["Une meilleure efficacité administrative.", "Une démocratie plus directe.", "La primauté des règlements sur la loi."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty,
                   "Indice : article 16 de la DDHC." if difficulty=="difficile" else None,
                   "L’article 16 DDHC fait de la séparation des pouvoirs une condition d’un régime constitutionnel." if difficulty=="difficile" else None))

    # 2) Droit de vote
    if difficulty == "facile":
        question = "Pour voter aux élections nationales en France, il faut notamment :"
        correct = "Être majeur et de nationalité française."
        distractors = ["Être résident depuis 10 ans.", "Avoir un diplôme.", "Disposer d’une carte professionnelle."]
    elif difficulty == "moyen":
        question = "La pluralité des partis politiques signifie que :"
        correct = "Plusieurs partis peuvent concourir librement aux élections."
        distractors = ["Un seul parti peut présenter des candidats.", "Les partis doivent être approuvés par un culte.", "Les partis sont interdits au niveau local."]
    else:
        question = "Quel cas entraîne la privation du droit de vote ?"
        correct = "Une condamnation pénale assortie d’une incapacité civile prononcée par le juge."
        distractors = ["Un simple désaccord politique.", "Une amende administrative.", "Un déménagement dans une autre commune."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty,
                   "Indice : conditions légales et sanctions pénales." if difficulty=="difficile" else None,
                   "Seule une décision judiciaire peut priver de droits civiques dans les conditions prévues par la loi." if difficulty=="difficile" else None))

    # 3) Type d'élections
    if difficulty == "facile":
        question = "Quelle élection permet d’élire le Président de la République ?"
        correct = "L’élection présidentielle au suffrage universel direct."
        distractors = ["Les élections législatives", "Les élections municipales", "Les élections européennes"]
    elif difficulty == "moyen":
        question = "À quoi servent les élections législatives ?"
        correct = "Élire les députés de l’Assemblée nationale."
        distractors = ["Élire les sénateurs", "Élire le Président", "Élire les conseillers régionaux"]
    else:
        question = "Quelle affirmation est exacte sur la durée des principaux mandats ?"
        correct = "Le mandat présidentiel est de 5 ans ; les députés sont élus pour 5 ans."
        distractors = ["Président 7 ans ; députés 6 ans", "Président 5 ans ; députés 6 ans", "Président 6 ans ; députés 5 ans"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_orga_republique(difficulty):
    items = []
    # 2 questions
    if difficulty == "facile":
        question = "Quelle institution appartient au pouvoir législatif ?"
        correct = "Le Sénat"
        distractors = ["Le Gouvernement", "Le Conseil d’État", "La Cour de cassation"]
    elif difficulty == "moyen":
        question = "Quel niveau gère principalement les collèges et lycées ?"
        correct = "Le département pour les collèges, la région pour les lycées."
        distractors = ["La commune pour les deux", "L’État pour les deux", "Le Sénat pour les lycées"]
    else:
        question = "Associez l’acteur à sa fonction :"
        correct = "Le maire exécute les décisions du conseil municipal et l’État lui délègue certaines missions."
        distractors = ["Le maire fait les lois nationales.", "Le maire nomme les ministres.", "Le maire contrôle la constitutionnalité des lois."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    if difficulty == "facile":
        question = "Quel couple appartient au pouvoir exécutif ?"
        correct = "Président de la République et Premier ministre"
        distractors = ["Président du Sénat et Députés", "Premier président de la Cour de cassation et Procureur", "Maire et Préfet de région"]
    elif difficulty == "moyen":
        question = "Quel énoncé est exact ?"
        correct = "Le Parlement comprend l’Assemblée nationale et le Sénat."
        distractors = ["Le Parlement comprend le Gouvernement.", "Le Parlement est composé des préfets.", "Le Parlement se confond avec le Conseil constitutionnel."]
    else:
        question = "Quel organe contrôle la conformité des lois à la Constitution ?"
        correct = "Le Conseil constitutionnel."
        distractors = ["Le Conseil d’État siégeant en contentieux constitutionnel.", "La Cour de cassation en premier ressort.", "Le Conseil des ministres."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_ue(difficulty):
    # 1 question
    if difficulty == "facile":
        question = "Quel est l’hymne européen ?"
        correct = "L’Ode à la joie"
        distractors = ["La Marseillaise", "God Save the King", "Bella Ciao"]
    elif difficulty == "moyen":
        question = "Quelle institution propose les textes et veille à l’application du droit de l’UE ?"
        correct = "La Commission européenne."
        distractors = ["Le Conseil de l’UE", "Le Parlement européen seul", "La Cour des comptes européenne"]
    else:
        question = "Un citoyen d’un État membre de l’UE résidant en France peut :"
        correct = "Voter aux élections municipales et européennes en France."
        distractors = ["Voter aux législatives françaises.", "Voter à la présidentielle française.", "Être juré d’assises automatiquement."]
    opts, idx = make_options(correct, distractors)
    ind = "Indice : citoyenneté européenne et droit de vote local/européen."
    exp = "Les citoyens de l’UE peuvent voter et être éligibles aux municipales et européennes dans leur État de résidence, pas aux scrutins nationaux."
    return [q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None)]

def gen_droits_fondamentaux(difficulty):
    items = []
    # 2 questions
    if difficulty == "facile":
        question = "Quelle liberté relève des droits fondamentaux ?"
        correct = "La liberté d’expression"
        distractors = ["L’obligation de culte", "La censure d’État généralisée", "La privation automatique de défense"]
    elif difficulty == "moyen":
        question = "Quel texte fondateur date de 1789 ?"
        correct = "La Déclaration des droits de l’homme et du citoyen"
        distractors = ["La Charte de l’environnement", "La Constitution de 1958", "Le Code civil"]
    else:
        question = "Quelle notion renvoie à l’intégrité de la personne ?"
        correct = "La dignité humaine, protégée par le bloc de constitutionnalité."
        distractors = ["L’intérêt général seulement financier.", "La primauté des coutumes privées.", "Le seul droit de propriété."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    if difficulty == "facile":
        question = "Quel droit social vise des conditions de vie dignes ?"
        correct = "La protection sociale et l’accès aux soins"
        distractors = ["L’obligation de travailler sans repos", "La suppression des syndicats", "La censure préalable"]
    elif difficulty == "moyen":
        question = "Quel ensemble de textes garantit les droits fondamentaux en France ?"
        correct = "Constitution, DDHC, Charte de l’environnement (bloc de constitutionnalité)."
        distractors = ["Uniquement des circulaires", "Des coutumes locales", "Des traités non publiés"]
    else:
        question = "Quelle phrase est exacte au regard de l’État de droit ?"
        correct = "Les libertés individuelles s’exercent dans le cadre de la loi, égale pour tous."
        distractors = ["La loi ne s’applique pas aux autorités.", "La liberté d’expression est absolue en toutes circonstances.", "Un maire peut légalement censurer toute critique."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_obligations_devoirs(difficulty):
    items = []
    # 3 questions
    if difficulty == "facile":
        question = "Quel est un devoir de toute personne résidant en France ?"
        correct = "Respecter la loi et payer ses impôts."
        distractors = ["Obéir aux consignes religieuses de la mairie.", "Travailler 60 h sans contrat.", "Voter à toutes les élections sous peine d’amende."]
    elif difficulty == "moyen":
        question = "Quel énoncé décrit l’ordre public ?"
        correct = "Sécurité, tranquillité, salubrité et dignité."
        distractors = ["Uniquement la sécurité routière", "Uniquement la morale privée", "Le contrôle des opinions"]
    else:
        question = "Quelle affirmation est conforme aux principes ?"
        correct = "Nul ne peut se soustraire aux règles communes par motif religieux."
        distractors = ["La foi permet de refuser l’impôt.", "Un club privé remplace la loi.", "Une coutume locale prime la loi nationale."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    # Rôle police/infractions
    if difficulty == "facile":
        question = "Qui assure notamment la sécurité publique ?"
        correct = "La police et la gendarmerie."
        distractors = ["Les associations religieuses", "Les partis politiques", "Les clubs sportifs"]
    elif difficulty == "moyen":
        question = "Qu’indique la typologie pénale ?"
        correct = "Contraventions, délits, crimes."
        distractors = ["Infractions, illégalités, fautes civiles", "Procès, appels, jugements", "Amendes, cautions, peines"]
    else:
        question = "Quelle est la conséquence d’un non-respect délibéré de la loi fiscale ?"
        correct = "Des sanctions pénales et/ou fiscales selon la gravité."
        distractors = ["Aucune si on s’excuse.", "Une simple médiation obligatoire.", "La perte automatique de nationalité."]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    # Participation citoyenne
    if difficulty == "facile":
        question = "Quelle action participe à la vie démocratique ?"
        correct = "Voter lors des élections."
        distractors = ["Refuser la loi locale", "Imposer sa religion à autrui", "Ignorer les règles sanitaires"]
    elif difficulty == "moyen":
        question = "Qu’est-ce qu’un juré d’assises ?"
        correct = "Un citoyen tiré au sort pour juger en cour d’assises."
        distractors = ["Un magistrat professionnel", "Un policier", "Un sénateur"]
    else:
        question = "Quel comportement illustre une attitude citoyenne ?"
        correct = "Respecter l’environnement et les règles communes au quotidien."
        distractors = ["Se soustraire aux règles par convenance", "Dégrader l’espace public", "Refuser toute solidarité"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_droits_mises_sit(difficulty):
    items = []
    for _ in range(6):
        p = random.choice(first_names)
        situation = random.choice([
            f"{p} veut filmer la police sur la voie publique sans gêner l’intervention.",
            f"{p} refuse une embauche en raison d’un prénom perçu comme étranger.",
            f"{p} est empêché d’entrer dans un restaurant à cause de son orientation.",
            f"{p} souhaite divorcer et se remarier.",
            f"{p} veut créer un syndicat dans son entreprise.",
            f"{p} est victime d’une agression raciste."
        ])
        if difficulty == "facile":
            question = f"{situation} Quel droit fondamental est principalement en jeu ?"
            correct = random.choice(["Liberté d’expression", "Égalité et non-discrimination", "Liberté d’association syndicale"])
            distractors = ["Interdiction de porter plainte", "Obligation religieuse", "Censure préalable"]
        elif difficulty == "moyen":
            question = f"{situation} Quelle démarche est la plus adaptée ?"
            correct = random.choice(["Saisir les autorités compétentes (police/justice, Défenseur des droits)", "Écrire à l’inspection du travail", "Déposer plainte"])
            distractors = ["Attendre sans agir", "S’adresser à un culte pour sanctionner", "Payer pour éviter la loi"]
        else:
            question = f"{situation} Quel énoncé est juridiquement le plus exact ?"
            correct = "La loi prohibe les discriminations et protège les libertés, sous contrôle du juge."
            distractors = ["La victime doit prouver son innocence.", "La discrimination est tolérée si discrète.", "Un règlement intérieur peut contredire la loi."]
        opts, idx = make_options(correct, distractors)
        ind = "Indice : droits fondamentaux + voies de recours."
        exp = "Les discriminations sont interdites ; des voies de droit existent (plainte, Défenseur des droits, prud’hommes selon le cas)."
        items.append(q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None))
    return items

def gen_hist_periodes(difficulty):
    items = []
    # 3 questions
    if difficulty == "facile":
        question = "En quelle année débute la Révolution française ?"
        correct = "1789"
        distractors = ["1776", "1792", "1815"]
    elif difficulty == "moyen":
        question = "Quel texte fondateur date de 1958 ?"
        correct = "La Constitution de la Ve République"
        distractors = ["Le Code civil", "La DDHC", "La Charte de l’environnement"]
    else:
        question = "Quel président a promulgué l’abolition de la peine de mort en 1981 ?"
        correct = "François Mitterrand"
        distractors = ["Charles de Gaulle", "Valéry Giscard d’Estaing", "Jacques Chirac"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    if difficulty == "facile":
        question = "Quel événement mondial a lieu de 1914 à 1918 ?"
        correct = "La Première Guerre mondiale"
        distractors = ["La Seconde Guerre mondiale", "La guerre de 1870", "La guerre froide"]
    elif difficulty == "moyen":
        question = "Quel appel célèbre date du 18 juin 1940 ?"
        correct = "L’appel du Général de Gaulle"
        distractors = ["Le discours de Verdun", "La charte de l’ONU", "Le traité de Rome"]
    else:
        question = "La Communauté économique européenne est créée en :"
        correct = "1957"
        distractors = ["1945", "1951", "1992"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    if difficulty == "facile":
        question = "Quel code juridique majeur est instauré sous Napoléon ?"
        correct = "Le Code civil"
        distractors = ["Le Code pénal médiéval", "La Common law", "Le Code napolitain"]
    elif difficulty == "moyen":
        question = "Quelle période installe l’école laïque, gratuite et obligatoire ?"
        correct = "La IIIe République (à partir des années 1880)"
        distractors = ["L’Empire", "La Restauration", "La Ve République"]
    else:
        question = "Quelle date correspond à l’instauration du suffrage universel direct pour l’élection présidentielle ?"
        correct = "1962"
        distractors = ["1958", "1968", "1974"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_geo(difficulty):
    items = []
    # 3 questions
    if difficulty == "facile":
        question = "Quel fleuve traverse Paris ?"
        correct = "La Seine"
        distractors = ["La Loire", "La Garonne", "Le Rhône"]
    elif difficulty == "moyen":
        question = "Quel massif montagneux se situe à l’est de la France ?"
        correct = "Le Jura ou les Vosges"
        distractors = ["Le Massif central", "Les Alpes uniquement en Italie", "Les Carpates"]
    else:
        question = "Quels pays ont une frontière terrestre avec la France métropolitaine ?"
        correct = "Belgique, Luxembourg, Allemagne, Suisse, Italie, Monaco, Espagne, Andorre"
        distractors = ["Portugal, Pays-Bas, Autriche", "Norvège, Danemark, Suède", "Pologne, Tchéquie, Slovaquie"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty,
                   "Indice : regardez une carte d’Europe." if difficulty=="difficile" else None,
                   "La France a 8 voisins terrestres en Europe, dont deux micro-États : Monaco et Andorre." if difficulty=="difficile" else None))

    if difficulty == "facile":
        question = "Combien d’habitants environ compte la France en 2025 ?"
        correct = "Environ 68 millions"
        distractors = ["Environ 40 millions", "Environ 85 millions", "Environ 120 millions"]
    elif difficulty == "moyen":
        question = "Quelle affirmation est exacte sur la population ?"
        correct = "La majorité vit dans des aires urbaines."
        distractors = ["La majorité vit à la campagne isolée.", "La population diminue sous 50 M.", "Aucune grande métropole en France."]
    else:
        question = "Citez un Département et Région d’Outre-mer (DROM)."
        correct = random.choice(departements_outre_mer)
        distractors = ["La Polynésie française (collectivité)", "Saint-Pierre-et-Miquelon (collectivité)", "Nouvelle-Calédonie (collectivité sui generis)"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    if difficulty == "facile":
        question = "Quel océan borde la côte ouest de la France ?"
        correct = "L’océan Atlantique"
        distractors = ["L’océan Indien", "L’océan Arctique", "L’océan Pacifique"]
    elif difficulty == "moyen":
        question = "Quelle région concentre beaucoup d’activités économiques ?"
        correct = "Les grandes aires métropolitaines et leurs axes de transport."
        distractors = ["Uniquement les zones rurales isolées", "Exclusivement les littoraux", "Uniquement les zones de montagne"]
    else:
        question = "Quelle zone est une destination touristique majeure en France ?"
        correct = "Côte d’Azur, littoral atlantique, Alpes ou grandes villes"
        distractors = ["Déserts intérieurs inexistants", "Banquise permanente", "Zones interdites au public"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_patrimoine(difficulty):
    items = []
    # 2 questions
    if difficulty == "facile":
        question = "Quel monument est emblématique de Paris ?"
        correct = "La tour Eiffel"
        distractors = ["Le Colisée", "La Sagrada Família", "Le Parthénon"]
    elif difficulty == "moyen":
        question = "Quel écrivain est français ?"
        correct = "Victor Hugo"
        distractors = ["Miguel de Cervantès", "William Shakespeare", "Dante Alighieri"]
    else:
        question = "La Francophonie désigne notamment :"
        correct = "L’ensemble des pays et institutions partageant l’usage du français."
        distractors = ["Uniquement la France", "Tous les pays latins", "Les pays de l’UE"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))

    if difficulty == "facile":
        question = "Quelle fête nationale a lieu le 14 juillet ?"
        correct = "La fête nationale française"
        distractors = ["La fête de la musique", "La Toussaint", "Noël"]
    elif difficulty == "moyen":
        question = "Quel plat est typiquement associé à la gastronomie française ?"
        correct = "Le bœuf bourguignon"
        distractors = ["La paella", "La pizza", "Le sushi"]
    else:
        question = "Combien de francophones dans le monde (ordre de grandeur) ?"
        correct = "Environ 321 millions"
        distractors = ["Environ 50 millions", "Environ 1,2 milliard", "Environ 900 millions"]
    opts, idx = make_options(correct, distractors)
    items.append(q(question, opts, idx, difficulty))
    return items

def gen_sinstaller(difficulty):
    # 1 question
    if difficulty == "facile":
        question = "Quelle démarche du quotidien est recommandée dès l’installation ?"
        correct = "Souscrire une assurance responsabilité civile."
        distractors = ["Demander une dispense générale de loi", "Ignorer le changement d’adresse", "Ne pas déclarer ses revenus"]
    elif difficulty == "moyen":
        question = "Pour un locataire, quel document définit droits et obligations ?"
        correct = "Le bail de location (contrat) et l’état des lieux."
        distractors = ["Un accord oral sans écrit", "Une promesse verbale du voisin", "Un ticket de caisse"]
    else:
        question = "Le titre de séjour doit être :"
        correct = "Demandé et renouvelé selon la procédure et les délais légaux."
        distractors = ["Optionnel si l’on travaille", "Remplaçable par un permis de conduire", "Automatique après 3 mois sans formalité"]
    opts, idx = make_options(correct, distractors)
    ind = "Indice : démarches de séjour, logement et fiscalité."
    exp = "La régularité du séjour et les contrats écrits (bail) sécurisent droits et obligations."
    return [q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None)]

def gen_soins(difficulty):
    if difficulty == "facile":
        question = "Quel numéro d’urgence appelle-t-on en cas de détresse vitale ?"
        correct = "112 (numéro d’urgence européen)"
        distractors = ["114 uniquement", "119 uniquement", "118 218"]
    elif difficulty == "moyen":
        question = "Quel professionnel coordonne votre parcours de soins ?"
        correct = "Le médecin traitant déclaré"
        distractors = ["Le maire", "Le pharmacien par défaut", "Le préfet"]
    else:
        question = "La prise en charge des soins repose sur :"
        correct = "L’Assurance maladie et, le cas échéant, une mutuelle complémentaire."
        distractors = ["Des dons privés obligatoires", "La seule charité", "Une taxe municipale spéciale"]
    opts, idx = make_options(correct, distractors)
    ind = "Indice : assurance maladie obligatoire + complémentaire."
    exp = "Le système français combine Sécurité sociale (base) et complémentaires (mutuelles/assureurs)."
    return [q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None)]

def gen_travailler(difficulty):
    if difficulty == "facile":
        question = "Quelle est la durée légale hebdomadaire du travail en France (hors dérogations) ?"
        correct = "35 heures"
        distractors = ["25 heures", "40 heures obligatoires", "60 heures"]
    elif difficulty == "moyen":
        question = "Quel droit relève du droit du travail ?"
        correct = "Le droit syndical et l’accès à la formation"
        distractors = ["L’obligation d’adhérer à un parti", "Le secret médical de l’employeur", "La censure d’opinion"]
    else:
        question = "Pour créer son entreprise, on peut s’appuyer sur :"
        correct = "Les chambres consulaires et plateformes publiques (ex. guichet unique)."
        distractors = ["Une autorisation religieuse", "Un vote du voisinage", "Un simple SMS au maire"]
    opts, idx = make_options(correct, distractors)
    ind = "Indice : démarches et acteurs (emploi/entreprendre)."
    exp = "Pôle emploi/France Travail, Chambres de commerce/métiers, et guichet unique accompagnent les démarches."
    return [q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None)]

def gen_parentalite_education(difficulty):
    if difficulty == "facile":
        question = "L’instruction est :"
        correct = "Obligatoire pour les enfants d’une certaine tranche d’âge."
        distractors = ["Optionnelle selon la météo", "Réservée aux garçons", "Payante pour l’école primaire publique"]
    elif difficulty == "moyen":
        question = "Que recouvre l’autorité parentale ?"
        correct = "Obligations et responsabilités envers l’enfant mineur."
        distractors = ["Droit de punir sans limite", "Transfert automatique à l’école", "Dispense de soins"]
    else:
        question = "Dans l’école publique, contester un enseignement pour motif religieux :"
        correct = "N’est pas conforme aux principes de laïcité et au règlement."
        distractors = ["Est un droit absolu", "Est obligatoire", "Remplace le programme officiel"]
    opts, idx = make_options(correct, distractors)
    ind = "Indice : charte de la laïcité à l’école."
    exp = "La neutralité protège la liberté de conscience des élèves et le bon fonctionnement de l’école."
    return [q(question, opts, idx, difficulty, ind if difficulty=="difficile" else None, exp if difficulty=="difficile" else None)]

def build_exam(difficulty):
    # Compose exactly 40 questions with the requested breakdown
    exam = []
    # 1. Principes et valeurs (11)
    exam += gen_devise_symboles(difficulty)        # 3
    exam += gen_laicite(difficulty)                # 2
    exam += gen_principes_mises_sit(difficulty)    # 6
    # 2. Système institutionnel et politique (6)
    exam += gen_democratie_vote(difficulty)        # 3
    exam += gen_orga_republique(difficulty)        # 2
    exam += gen_ue(difficulty)                     # 1
    # 3. Droits et devoirs (11)
    exam += gen_droits_fondamentaux(difficulty)    # 2
    exam += gen_obligations_devoirs(difficulty)    # 3
    exam += gen_droits_mises_sit(difficulty)       # 6
    # 4. Histoire, géographie et culture (8)
    exam += gen_hist_periodes(difficulty)          # 3
    exam += gen_geo(difficulty)                    # 3
    exam += gen_patrimoine(difficulty)             # 2
    # 5. Vivre dans la société (4)
    exam += gen_sinstaller(difficulty)             # 1
    exam += gen_soins(difficulty)                  # 1
    exam += gen_travailler(difficulty)             # 1
    exam += gen_parentalite_education(difficulty)  # 1
    assert len(exam) == 40, len(exam)
    return exam

# Generate 120 files (40 per difficulty)
levels = (["facile"]*40) + (["moyen"]*40) + (["difficile"]*40)
for i, level in enumerate(levels, start=1):
    exam = build_exam(level)
    # File name with zero padding and level
    fname = f"QCM_{i:03d}_{level}.json"
    with open(os.path.join(root, fname), "w", encoding="utf-8") as f:
        json.dump(exam, f, ensure_ascii=False, indent=2)

# Zip everything
zip_path = "/mnt/data/QCM_civique_fr_120_fichiers.zip"
with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
    for fn in sorted(os.listdir(root)):
        zf.write(os.path.join(root, fn), arcname=fn)

zip_path
