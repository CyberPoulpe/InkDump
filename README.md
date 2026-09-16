# 🐙 InkDump
**Extracteur de mémoire Bash pour l'investigation DFIR et l'audit de sessions.**
Outil Python léger permettant d'extraire et de filtrer l'historique de commandes d'une session Bash active directement depuis /proc/<PID>/mem.

![License](https://img.shields.io/github/license/CyberPoulpe/InkDump?style=flat-square)
![Language](https://img.shields.io/github/languages/top/CyberPoulpe/InkDump?style=flat-square)
![Stars](https://img.shields.io/github/stars/CyberPoulpe/InkDump?style=flat-square)

## 🎯 Aperçu & Objectif
**InkDump** est conçu pour les intervenants DFIR, les auditeurs de sécurité et les administrateurs système ayant besoin de récupérer l'historique d'exécution volatile d'une session Bash en cours, avant même qu'il ne soit écrit dans le fichier '.bash_history'.

✨ Pourquoi InkDump ?
Lors d'une inspection mémoire brute (via strings ou un dump mémoire classique), la sortie est noyée sous des milliers de variables d'environnement, de fonctions internes et de tampons bash_completion (systemd, git, nvm...).

InkDump nettoie ce bruit grâce à :

🎯 Ciblage mémoire précis : Analyse uniquement les plages mémoires utilisateur ([heap] et segments rw-p).

🧩 Parsing Readline : Découpage de la mémoire selon le format d'octets nuls (\x00) utilisé par Readline.

🧹 Filtrage intelligent : Élimination des faux positifs via un filtrage orienté sur les commandes système courantes.

🚀 Pipeline d'exécution
Plaintext
[1/3] Inspection du processus (/proc/<PID>/maps)
      └── Identification des segments mémoires heap et rw-p actifs

[2/3] Extraction binaire (/proc/<PID>/mem)
      └── Lecture ciblée et découpage par délimiteur Readline (\x00)

[3/3] Filtrage & Restitution
      └── Nettoyage du bruit et affichage chronologique de l'historique
🚀 Installation & Prérequis
Prérequis
OS : Linux (nécessite l'interface /proc)

Python : 3.6 ou supérieur

Privilèges : Accès root (sudo) requis pour lire la mémoire d'un processus tiers

Installation
Cloner le dépôt : git clone [https://github.com/CyberPoulpe/InkDump.git](https://github.com/CyberPoulpe/InkDump.git)

Se déplacer dans le dossier : cd InkDump

Rendre le script exécutable : chmod +x inkdump.py

💡 Utilisation & Exemples
1. Identifier le PID de la session cible
Visualiser les sessions ouvertes (ex. pts/1) :

ps -t pts/1 -o pid,ppid,user,args --forest

2. Lancer l'extraction mémoire
sudo ./inkdump.py <PID>

🐛 Résolution de problèmes
Erreur Permission denied :

La lecture de /proc/<PID>/mem exige des privilèges d'administrateur. Relancer le script avec sudo.

Blocage ptrace / Yama Security :

Sur certaines distributions avec Yama ptrace activé, ajuster temporairement le paramètre du noyau si nécessaire :

sudo sysctl -w kernel.yama.ptrace_scope=0

🛡️ Sécurité & Avertissement
L'utilisation d'InkDump doit s'effectuer exclusivement dans le cadre d'investigations numériques légales, d'audits de sécurité autorisés ou de réponses à incidents. L'utilisateur assume l'entière responsabilité des analyses mémoire réalisées.

🤝 Contribution & Contact
Les contributions, signalements de bugs ou suggestions d'améliorations sont les bienvenus !

Auteur : CyberPoulpe

GitHub : @CyberPoulpe
