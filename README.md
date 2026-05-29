#  Projet IA – Jeu du Taquin 3×3

Mini-projet réalisé dans le cadre du module **Fondements de l’Intelligence Artificielle** (ISI 2025-2026).  
L’objectif est d’analyser et comparer différents algorithmes de recherche pour résoudre le jeu du taquin 3×3.

---

##  Présentation du problème
- Le taquin 3×3 consiste à remettre en ordre 8 tuiles numérotées sur une grille 3×3.
- L’espace d’états atteignables : **181 440**.
- Exemple de configuration initiale → état final en **23 mouvements optimaux**.

---

##  Algorithmes implémentés
- **DFS (Depth-First Search)** : non optimal, faible mémoire.
- **BFS (Breadth-First Search)** : optimal, mais coûteux en mémoire.
- **DLS (Depth-Limited Search)** : DFS borné à L niveaux, non optimal.
- **A\*** : recherche heuristique avec fonction `f(n) = g(n) + h(n)`  
  - g(n) = coût réel (nombre de mouvements)  
  - h(n) = heuristique (nombre de pièces mal placées)

---

##  Résultats expérimentaux
| Algorithme | Nœuds générés | Nœuds visités | Temps (s) | Mémoire (KB) | Solution | Optimal |
|------------|---------------|---------------|-----------|--------------|----------|---------|
| DFS        | ~181 440      | ~181 440      | ~2.0      | ~18 000      | Non opt. | ✗ |
| BFS        | 136 178       | 114 947       | 1.38      | 24 295       | 23 mvts  | ✓ |
| DLS (L=30) | 242 574       | 241 886       | 2.30      | 5 676        | 29 mvts  | ✗ |
| A*         | 19 339        | 12 872        | 0.26      | 4 018        | 23 mvts  | ✓ |

---

##  Conclusion
- **A\*** est le plus performant : optimal, rapide et peu coûteux en mémoire.  
- Classement final : **A\* > BFS > DFS > DLS**.  
- L’heuristique admissible (pièces mal placées) guide efficacement la recherche.

---

##  Auteur
- **Rayen Bouyahia** – L2CS01  
Institut Supérieur d’Informatique, Université de Tunis El Manar
