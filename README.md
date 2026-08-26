# InkDump 🐙

Outil Python léger pour extraire et filtrer l'historique de commandes d'une session **Bash** active en inspectant directement `/proc/<PID>/mem`.

Pratique pour l'investigation (DFIR), l'audit de sessions ou simplement récupérer des commandes tapées dans un terminal qui n'ont pas encore été écrites dans le `.bash_history`.

---

## Pourquoi InkDump ?

Sur une inspection mémoire brute (via `strings` ou un dump mémoire classique), la sortie est noyée sous des milliers de variables d'environnement, de fonctions internes et surtout de tampons `bash_completion` (`systemd`, `git`, `nvm`...).

**InkDump** nettoie ce bruit en :
* Ciblant uniquement les plages mémoires utilisateur (`[heap]` et segments `rw-p`).
* Découpant la mémoire au format d'octets nuls (`\x00`) utilisé par Readline.
* Filtrant les faux positifs via une regex axée sur les commandes système courantes.

---

## Prérequis

* **OS :** Linux (nécessite l'interface `/proc`)
* **Python :** 3.6+
* **Privilèges :** Droits `root` (`sudo`) obligatoires pour lire le `/proc/<PID>/mem` d'un autre processus.

---

## Installation & Utilisation

```bash
# 1. Récupérer le projet
git clone https://github.com/CyberPoulpe/InkDump.git
cd InkDump
chmod +x inkdump.py

# 2. Relever le PID du terminal cible (ex: pts/1)
w
ps -t pts/1 -o pid,ppid,user,args --forest 

# 3. Lancer l'extraction
sudo ./inkdump.py <PID>
