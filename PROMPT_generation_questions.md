A partir du fichier themes.json, génère 120 QCM (questions à choix multiples) pour un examen civique français. Chaque question doit avoir 4 options de réponse, dont une seule correcte. Les questions doivent couvrir les thématiques présentes dans le fichier themes.json avec une répartition comme telle :

1. Principes et valeurs de la République : 11 questions, dont :
   - Devise et symboles de la République : 3 questions ;
   - Laïcité : 2 questions ;
   - Mises en situation : 6 questions.
2. Système institutionnel et politique : 6 questions, dont :
   - Démocratie et droit de vote : 3 questions ;
   - Organisation de la République française : 2 questions ;
   - Institutions européennes : 1 question.
3. Droits et devoirs : 11 questions, dont :
   - Droits fondamentaux : 2 questions ;
   - Obligations et devoirs des personnes résidant en France : 3 questions ;
   - Mises en situation : 6 questions.
4. Histoire, géographie et culture : 8 questions, dont :
   - Principales périodes et personnages historiques : 3 questions ;
   - Territoires et géographie : 3 questions ;
   - Patrimoine français : 2 questions.
5. Vivre dans la société française : 4 questions dont :
   - S’installer et résider en France : 1 question ;
   - L’accès aux soins : 1 question ;
   - Travailler en France : 1 question ;
   - Autorité parentale et système éducatif : 1 question.

Je veux 120 fichiers différents en sortie (tu peux faire une archive ZIP), répartis selon 3 niveau de difficulté :
- Facile : 40 fichiers
- Moyen : 40 fichiers
- Difficile : 40 fichiers

Le niveau de difficulté doit influencer la complexité des questions posées et des options proposées. Par exemple, les questions de niveau facile devraient être plus directes et les options plus évidentes, tandis que les questions de niveau difficile pourraient inclure des détails plus subtils et des options plus proches les unes des autres, autrement dit des questions-pièges où la compréhension du français et la lecture attentive de la question est primordiale pour répondre correctement.

Concernant le format : pour chaque question questions au format JSON avec les champs suivants :
- "question" : au format texte ;
- "options" : liste des 4 options en format texte ;
- "correct_option" : index de l'option correcte dans la liste "options" ;
- "indice" : un indice pour aider à répondre à la question (optionnel, mais disponible pour les questions difficiles) ;
- "explication" : une explication de la réponse correcte (optionnel, mais disponible pour les questions difficiles).

