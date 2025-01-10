---
marp: true
theme: default
class: lead
paginate: true
math: mathjax
---

# Mínimos Quadrados
## Decomposição QR

---

## Conteúdo

1. Introdução ao Problema de Mínimos Quadrados Discreto
2. Método dos Mínimos Quadrados
3. Decomposição QR
4. Processo de Gram-Schmidt
5. Processo de Gram-Schmidt Modificado
6. Refletores de Householder
7. Householder QR

---

## Introdução ao Problema de Mínimos Quadrados Discreto

Dado um conjunto de pontos de dados discretos $\{(t_i, y_i)\}_{i=1}^m$, o objetivo do **problema de mínimos quadrados discreto** é encontrar um polinômio $p(t)$ de grau $d$ que aproxime esses dados minimizando o erro residual.

![bg right:40% fit](images/Least-Square-Method-Graph.png)

--- 

### Formulação Matemática

O polinômio $p(t)$ pode ser expresso como:

$$
p(t) = a_0 + a_1 t + a_2 t^2 + \cdots + a_d t^d
$$

Os resíduos para cada ponto de dados são:

$$
r_i = y_i - p(t_i), \quad \text{para } i = 1, 2, \ldots, m
$$

O objetivo é minimizar a soma dos quadrados dos resíduos:

$$
\min_{a_0, a_1, \ldots, a_d} \sum_{i=1}^m (y_i - p(t_i))^2
$$

![bg left:40% fit](images/linear_fit.svg)

---

### Representação Matricial

Podemos reescrever o problema em termos matriciais como:

$$
\mathbf{V} \mathbf{a} \approx \mathbf{y}
$$

onde $\mathbf{a}$ é o vetor de coeficientes do polinômio $p(t)$ e $\mathbf{V}$ é a matriz de Vandermonde.

Assim, temos:

$$
\underbrace{\begin{bmatrix}
1 & t_1 & t_1^2 & \cdots & t_1^d \\
1 & t_2 & t_2^2 & \cdots & t_2^d \\
\vdots & \vdots & \vdots & \ddots & \vdots \\
1 & t_m & t_m^2 & \cdots & t_m^d \\
\end{bmatrix}}_{\text{Matriz de Vandermonde}} \begin{bmatrix}
a_0 \\
a_1 \\
\vdots \\
a_d
\end{bmatrix} \approx \begin{bmatrix}
y_1 \\
y_2 \\
\vdots \\
y_m
\end{bmatrix}
$$

---
# 2. Método dos Mínimos Quadrados

Dado um sistema sobredeterminado $A \mathbf{x} \approx \mathbf{b}$:

- $A \in \mathbb{R}^{m \times n}, m \gg n$ (mais equações do que incógnitas)
- Queremos minimizar o erro residual:
  
  $$
  \min_{\mathbf{x} \in \mathbb{R}^n} \| A \mathbf{x} - \mathbf{b} \|_2^2
  $$

A solução é dada pelas **equações normais** [1]:

$$
A^\top A \mathbf{x} = A^\top \mathbf{b},
$$

que é um sistema linear de $n$ equações e $n$ incógnitas.

<div style="font-size: 25px; color: gray; font-style: italic;">
[1]: Pode se demonstrar que a solução das equações normais é o ponto de mínimo global do problema de mínimos quadrados.
</div>

---

# 3. Decomposição QR

## Definição

A **decomposição QR** de uma matriz $A \in \mathbb{R}^{m \times n}$ ($m \geq n$) é a fatoração de $A$ em:

$$
A = QR
$$

onde:

- $Q \in \mathbb{R}^{m \times m}$ é uma matriz ortogonal ($Q^\top Q = I$)
- $R \in \mathbb{R}^{m \times n}$ é uma matriz triangular superior

---

## Aplicação aos Mínimos Quadrados

Substituindo $A = QR$ na equação das mínimas quadrados:

$$QR \mathbf{x} \approx \mathbf{b}$$

Multiplicando ambos os lados por $Q^\top$:

$$Q^\top QR \mathbf{x} = R \mathbf{x} = Q^\top \mathbf{b}$$

Como $R$ é triangular superior, basta aplicarmos a substituição regressiva para encontrar a solução:

$$
\mathbf{x} = R^{-1} Q^\top \mathbf{b}
$$

---

# 4. Processo de Gram-Schmidt

<div style="display: flex; justify-content: space-between;">
<div style="width: 70%;">


Seja $\{ \mathbf{a}_1, \mathbf{a}_2, \ldots, \mathbf{a}_n \} \in \mathbb{R}^m$ um conjunto LI.


1. **Primeiro vetor ortonormal:** $\mathbf{q}_1 = \frac{\mathbf{a}_1}{\| \mathbf{a}_1 \|_2}$

2. **Segundo vetor ortonormal:**

   $$
   \mathbf{q}_2 = \frac{\mathbf{a}_2 - \operatorname{proj}_{\mathbf{q}_1}(\mathbf{a}_2)}{\| \mathbf{a}_2 - \operatorname{proj}_{\mathbf{q}_1}(\mathbf{a}_2) \|_2}
   $$

3. **Generalização para o $k$-ésimo vetor:**

   $$
   \mathbf{q}_k = \frac{\mathbf{a}_k - \sum_{j=1}^{k-1} (\mathbf{q}_j^\top \mathbf{a}_k) \mathbf{q}_j}{\| \mathbf{a}_k - \sum_{j=1}^{k-1} (\mathbf{q}_j^\top \mathbf{a}_k) \mathbf{q}_j \|_2}
   $$
</div>
<div style="width: 50%;">

A projeção de $\mathbf{v}$ sobre $\mathbf{u}$ é dada por:

$$
\operatorname{proj}_{\mathbf{u}}(\mathbf{v}) = \frac{\mathbf{u}^\top \mathbf{v}}{\mathbf{u}^\top \mathbf{u}} \mathbf{u}
$$

<img src="images/Gram–Schmidt_process.png" style="float: right; width: 400px; margin-left: 20%; margin-top: 50%; transform: translateY(-90%);">

</div>
</div>

---

# 5. Processo de Gram-Schmidt Modificado
<div style="display: flex; justify-content: space-between;">
<div style="width: 50%;">

**Diferença principal:**

- No **Gram-Schmidt clássico**, projetamos e subtraímos simultaneamente.
- No **modificado**, projetamos e subtraímos **incrementalmente**, garantindo maior ortogonalidade.


</div>
<div style="width: 50%;">

**Algoritmo: GS modificado**

Para cada vetor $\mathbf{a}_k \in \mathbb{R}^m$:

1. Inicialize $\mathbf{r}_k = \mathbf{a}_k$.
2. Para cada vetor ortonormal anterior $\mathbf{q}_j$:
   
   $$
   r_{jk} = \mathbf{q}_j^\top \mathbf{a}_k, \quad \mathbf{r}_k = \mathbf{r}_k - r_{jk} \mathbf{q}_j
   $$

3. Normalize:
   
   $$
   \mathbf{q}_k = \frac{\mathbf{r}_k}{\| \mathbf{r}_k \|_2}
   $$

</div>
</div>

---

# 6. Refletores de Householder

## Definição

Um refletor de Householder é uma matriz ortogonal $H \in \mathbb{R}^{m \times m}$ que reflete um vetor $\mathbf{x} \in \mathbb{R}^m$ em relação a um hiperplano ortogonal a um vetor $\mathbf{v} \in \mathbb{R}^m$:

$$H = I - 2 \frac{\mathbf{v} \mathbf{v}^\top}{\mathbf{v}^\top \mathbf{v}}$$

**Propriedades:**

- $H^\top H = I$ (ortogonalidade)
- $H = H^\top$ (simetria)

![bg right:30% fit](images/Householder.png)

---

# 7. Householder QR

As reflexões de Householder podem ser aplicadas na decomposição $QR$.

O processo envolve a construção iterativa de matrizes de Householder para introduzir zeros abaixo da diagonal principal, transformando $A$ em $R$.

O produto dessas matrizes de Householder forma a matriz ortogonal $Q$.

$$
\underbrace{H_n H_{n-1} \cdots H_1}_{\text{Matrizes de Householder}} A = R
$$

---

### Ideia Central

Suponha que desejamos refletir um vetor $\mathbf{x} \in \mathbb{R}^n$ de modo que ele se alinhe com um múltiplo do primeiro vetor base padrão $\mathbf{e}_1 = [1, 0, 0, \ldots, 0]^T$.

<div style="display: flex; justify-content: space-between; border: 1px solid red; border-radius: 10px; padding: 10px;">
<div style="width: 48%;">

1. **Calcule a norma de $\mathbf{x}$**:

   $$ \|\mathbf{x}\| = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2} $$

2. **Determine o escalar $\alpha$**:

   $$ \alpha = -\operatorname{sign}(x_1) \cdot \|\mathbf{x}\| $$

</div>
<div style="width: 48%;">

3. **Construa o vetor $\mathbf{v}$**:

   $$ \mathbf{v} = \mathbf{x} - \alpha \mathbf{e}_1 $$

4. **Normalize $\mathbf{v}$**:

   $$ \mathbf{v} = \frac{\mathbf{v}}{\|\mathbf{v}\|} $$

</div>
</div>

- A matriz de Householder resultante é $H = I - 2\mathbf{v}\mathbf{v}^T.$

- $H\mathbf{x}$ é um vetor com zeros em todos as componentes, exceto a primeira.

---

### Ideia Central (continuação)

Para aplicar sucessivamente as reflexões de Householder e reduzir a matriz $A$ a uma forma triangular superior, seguimos o seguinte procedimento:

1. Inicialmente, aplicamos a primeira reflexão de Householder $H_1$ à matriz completa $A$, zerando os elementos abaixo do primeiro elemento da primeira coluna. A matriz $H_1$ é da mesma dimensão de $A$.

$$H_1 A = \begin{bmatrix} * & * & * \\ 0 & * & * \\ 0 & * & * \end{bmatrix}$$

---

### Ideia Central (continuação)

2. Depois, excluímos a primeira linha e a primeira coluna de $A$ e construímos a matriz de Householder $H_2$ para zerar os elementos abaixo do primeiro elemento dessa submatriz. Aplicamos 

$$
\underbrace{\begin{bmatrix} 1 & 0 & 0  \\ 0 & * & * \\ 0 & * & * \end{bmatrix}}_{H_2} H_1 A = \begin{bmatrix} * & * & * \\ 0 & * & * \\ 0 & 0 & * \end{bmatrix}
$$

3. Esse processo é repetido sucessivamente para submatrizes menores, até que todos os elementos abaixo da diagonal principal de $A$ sejam zerados.

---

# Exercício:

1. Aplique a decomposição QR utilizando o refletor de Householder à matriz:

$$
A = \begin{bmatrix} 4 & 1 & 2 \\ 2 & 3 & 1 \\ 1 & 2 & 3 \end{bmatrix}
$$

2. Construa uma matriz de Hilbert $6 \times 6$;
2.1. Aplique a decomposição QR utilizando (a) o processo de Gram-Schmidt clássico, (b) o processo de Gram-Schmidt modificado e (c) o refletor de Householder;
2.2. Compare a precisão da decomposição QR utilizando os três métodos.

---
<!-- backgroundColor: orange -->

# PERGUNTAS?