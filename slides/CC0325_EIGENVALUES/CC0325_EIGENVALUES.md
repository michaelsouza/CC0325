---
marp: true
title: "Métodos Numéricos para Autovalores"
theme: default
paginate: true
size: 16:9
backgroundColor: #fff
---

# Métodos Numéricos para Autovalores
### Curso de Graduação em Ciência de Dados

- Autovalores aparecem em PCA, SVD, Cadeias de Markov
- Veremos os principais algoritmos e teoremas
- Espere um humor rápido

---

## Teoremas

---

### Teorema Espectral
- Para matrizes reais simétricas (ou Hermitianas):
  - Autovalores são reais.
  - Autovetores podem ser escolhidos ortonormais.

**Relevância:**
Matrizes reais simétricas aparecem frequentemente (como matrizes de covariância em PCA). Saber que os autovalores são todos reais e os autovetores são ortonormais torna as coisas mais estáveis e fáceis de calcular.

---

### Teorema dos Círculos de Gershgorin
- Autovalores estão dentro dos discos de Gershgorin:
  $$
    D(a_{ii}, R_i) \quad \text{com} \quad R_i = \sum_{j\neq i} |a_{ij}|.
  $$
- Maneira rápida de estimar onde os autovalores podem estar.

**Significado:**
O teorema diz que cada autovalor está em pelo menos um dos discos centrados em cada entrada da diagonal com raio igual à soma dos valores absolutos na mesma linha.

**Relevância:**
É uma maneira rápida de limitar ou adivinhar onde os autovalores podem estar, para que você não entre em uma busca desenfreada por eles.

---

### Decomposição de Schur
- Toda matriz quadrada $A$ pode ser transformada unitariamente:
  $$
    A = Q U Q^*
  $$
  com $U$ triangular superior.
- Autovalores estão na diagonal de $U$.

**Significado:**
Qualquer matriz pode ser "quase" diagonalizada. Em vez de diagonal, você obtém uma forma triangular superior com os mesmos autovalores na diagonal.

**Relevância:**
É a base de muitos algoritmos de autovalores (como o método QR) que dependem da redução de uma matriz a algo mais simples, mas preservando os autovalores.

---

## Método da Potência
### O Básico
- **Processo**: Repetidamente faça $v_{k+1} = A v_k / \|A v_k\|$.
- **Resultado**: Converge para o autovetor com o maior autovalor em magnitude.
- **Advertência**: Se seu vetor inicial for ortogonal ao autovetor principal, azar o seu (embora seja raro).

### Quando Usar
- Matrizes enormes e esparsas.
- Precisa apenas do autovalor dominante.

---

## Algoritmo QR
### A Ideia
1. Fatore $A_k = Q_k R_k$.
2. Forme $A_{k+1} = R_k Q_k$.
3. Repita até que $A_k$ seja triangular superior (autovalores na diagonal).

### Por Que Importa
- Padrão ouro para matrizes densas.
- Detalhe de implementação: "Shifts" aceleram a convergência.

---

## Método de Jacobi (para simétricas)
### Esboço
- Rotacione pares de eixos para zerar as entradas fora da diagonal.
- Converge para uma matriz diagonal com autovalores na diagonal.

### Uso Real
- Fácil de entender para ensino.
- Não é o mais rápido para problemas de grande escala, mas conceitualmente simples.

---

## Iteração do Quociente de Rayleigh
### Passos Principais
- Atualize a estimativa do autovalor via $\rho(x) = \frac{x^T A x}{x^T x}$.
- Ajuste o shift em cada iteração.

### Desempenho
- Convergência cúbica perto de um autovalor real (rápido, mas cada iteração pode ser cara).
- Bom quando você precisa de alta precisão para um autopar.

---

## Método de Lanczos (para simétricas grandes)
### Destaques
- Constrói um subespaço de Krylov: $\mathcal{K}_m(A, v) = \{v, Av, A^2 v, \dots, A^{m-1} v\}$.
- Produz uma matriz tridiagonal cujos autovalores se aproximam dos de $A$.

### Caso de uso
- Eficiente para matrizes esparsas e grandes.
- Geralmente usado para obter apenas os $k$ autovalores principais.

---

## Método de Arnoldi (não simétricas)
### O que é?
- Generaliza Lanczos para matrizes não simétricas (ou não Hermitianas).
- Constrói uma matriz de Hessenberg superior que se aproxima dos autovalores (valores de Ritz).

### Caso de uso
- Problemas grandes, esparsos e não simétricos (como matrizes de adjacência de grafos direcionados).

---

## Conclusão
- Métodos da Potência / Rayleigh: abordagens iterativas "atire para o topo".
- QR: robusto para espectro completo, usado em bibliotecas padrão.
- Lanczos / Arnoldi: mantenha barato e aproxime para matrizes grandes.
- Teoria espectral: real simétrico é o melhor cenário. Não simétrico precisa de cautela extra.