---
marp: true
theme: default
paginate: true
math: mathjax
---

# Sensibilidade de Sistemas Lineares
## Efeitos dos Erros de Arredondamento

---
<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Errar não é só humano</h2>
</div>

<div style="margin-top: 60px;">
<div style="display: flex; align-items: flex-start; gap: 20px;">
<img src="images/errrors_types.png" style="width: 60%;">
<div>

1. **Erro do Modelo** ($e_m$)  
  Ocorre ao simplificar a realidade física ($PP$) em um modelo matemático ($MP$). Está além do controle computacional.

</div>
</div>
</div>

<footer>
Quarteroni, Alfio, Fausto Saleri, and Paola Gervasio. Scientific computing with MATLAB and Octave. Vol. 3. Berlin: Springer, 2006.
</footer>

---
<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Errar não é só humano</h2>
</div>

<div style="margin-top: 60px;">
<div style="display: flex; align-items: flex-start; gap: 20px;">
<img src="images/errrors_types.png" style="width: 60%;">
<div>

2. **Erro Algorítmico** ($e_a$)  
  Erros introduzidos durante a resolução computacional do modelo matemático, principalmente devido a arredondamentos na representação numérica.

</div>
</div>
</div>

<footer>
Quarteroni, Alfio, Fausto Saleri, and Paola Gervasio. Scientific computing with MATLAB and Octave. Vol. 3. Berlin: Springer, 2006.
</footer>

---

<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Errar não é só humano</h2>
</div>

<div style="margin-top: 60px;">
<div style="display: flex; align-items: flex-start; gap: 20px;">
<img src="images/errrors_types.png" style="width: 60%;">
<div>

3. **Erro de Truncamento** ($e_t$)  
   Erros introduzidos ao aproximar sequências infinitas por operações finitas. Ocorre quando a solução numérica ($x_n$) difere da solução exata ($x$).

</div>
</div>
</div>

<footer>
Quarteroni, Alfio, Fausto Saleri, and Paola Gervasio. Scientific computing with MATLAB and Octave. Vol. 3. Berlin: Springer, 2006.
</footer>

---

<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Errar não é só humano</h2>
</div>

<div style="margin-top: 60px;">
<div style="display: flex; align-items: flex-start; gap: 20px;">
<img src="images/errrors_types.png" style="width: 60%;">
<div>

4. **Erro Computacional** ($e_c$)  
   O erro total que surge a partir da soma do erro algorítmico ($e_a$) e do erro de truncamento ($e_t$). 
   
   Este é o erro de interesse ao resolver problemas numéricos.

</div>
</div>
</div>

<footer>
Quarteroni, Alfio, Fausto Saleri, and Paola Gervasio. Scientific computing with MATLAB and Octave. Vol. 3. Berlin: Springer, 2006.
</footer>

---

<div style="display: flex; justify-content: space-between; gap: 20px;">
<div style="flex: 1; padding: 0px;">

## Precisão Numérica
A precisão numérica é afetada pela ***ordem das operações aritméticas*** (pelo algoritmo). 

Como ilustração, suponha uma máquina com dois algarismos significativos e que desejamos calcular

$$1 + \epsilon + \epsilon + \ldots + \epsilon,$$

onde $\epsilon=3.0 \times 10^{-2}$ e que tenhamos $n=11$ parcelas.

  </div>
  <div style="flex: 1; border: 1px solid black; padding: 20px; border-radius: 10px;">
    <h6>Algoritmo Ingênuo de Soma </h6>

```python
s = 0
for i in range(n):
  s += epsilon
```
   
<h6>Algoritmo de Soma de Kahan</h6>

```python
s = 0
c = 0
for i in range(n):
  # y : parcela + compensação
  y = epsilon - c
  # soma efetiva
  t = s + y       
  # c : erro de arredondamento
  c = (t - s) - y 
  s = t
```
  </div>
</div>

---

## Algoritmo de Soma de Kahan

<div style="font-size: 0.9em; display: flex; justify-content: center;">

$k$ | $y = \epsilon - c$ | $t = s + y$ | $c = (t - s) - y$ | $s = t$
|:-:|:-:|:-:|:-:|:-:|
1| $3.0 \times 10^{-2}$ | $1.0$ | $(1.0 - 0.0) - 3.0 \times 10^{-2} = -3.0 \times 10^{-2}$ | $1.0$ |
2| $6.0 \times 10^{-2}$ | $1.0$ | $(1.0 - 0.0) - 6.0 \times 10^{-2} = -3.0 \times 10^{-2}$ | $1.0$ |
3| $9.0 \times 10^{-2}$ | $1.0$ | $(1.0 - 0.0) - 9.0 \times 10^{-2} = -6.0 \times 10^{-2}$ | $1.0$ |
4| $1.2 \times 10^{-1}$ | $1.1$ | $(1.1 - 1.0) - 1.2 \times 10^{-2} = -2.0 \times 10^{-2}$ | $1.1$ |
5| $5.0 \times 10^{-2}$ | $1.1$ | $(1.1 - 1.1) - 5.0 \times 10^{-2} = -5.0 \times 10^{-2}$ | $1.1$ |
6| $8.0 \times 10^{-2}$ | $1.1$ | $(1.1 - 1.1) - 8.0 \times 10^{-2} = -8.0 \times 10^{-2}$ | $1.1$ |
7| $1.1 \times 10^{-1}$ | $1.2$ | $(1.2 - 1.1) - 1.1 \times 10^{-1} = -1.0 \times 10^{-2}$ | $1.2$ |

</div>

---

## Caso de estudo

Para a matriz $A$, calcule a solução dos sistemas lineares $Ax = b$ e $A\hat{x} = \hat{b}$ onde
$$A = \begin{bmatrix} 1000 & 999 \\ 999 & 998 \end{bmatrix}, \quad b = \begin{bmatrix} 1999 \\ 1998 \end{bmatrix} \quad \text{e} \quad \hat{b} = \begin{bmatrix} 1999 \\ 1998.001 \end{bmatrix}.$$

Escrevendo $\hat{x} = x + \delta x$ e $\hat{b} = b + \delta b$, compare as variações relativas $\Large{\frac{\delta x}{x}}$ e $\Large{\frac{\delta b}{b}}$.

---

## Norma de um vetor

**Uma norma** (ou **norma vetorial**) em $\mathbb{R}^n$ é uma função que atribui a cada $x \in \mathbb{R}^n$ um número real não-negativo $\|x\|$, tal que para todos $x, y \in \mathbb{R}^n$ e todos $\alpha \in \mathbb{R}$:

1. **Positividade**
$\|x\| \geq 0$ para todo $x$, e $\|x\| = 0$ se e somente se $x = 0$ 

2. **Homogeneidade absoluta**
$\|\alpha x\| = |\alpha| \|x\|$ 

3. **Desigualdade triangular**
$\|x + y\| \leq \|x\| + \|y\|$ 

---

## Exemplos

1. Norma euclidiana
$$||x||_2 = \sqrt{x_1^2 + x_2^2 + \cdots + x_n^2}$$

2. Norma de Manhattan (ou *norma do valor absoluto* ou *norma 1*)
$$||x||_1 = |x_1| + |x_2| + \cdots + |x_n|$$

3. Norma infinita
$$||x||_\infty = \max(|x_1|, |x_2|, \cdots, |x_n|)$$

4. Norma $p$
$$||x||_p = \left( \sum_{i=1}^n |x_i|^p \right)^{1/p}$$

---

## Norma de uma matriz

Para todos $A,B \in \mathbb{R}^{n \times n}$ e $\alpha \in \mathbb{R}$:

1. **Positividade**
$\|A\| \geq 0$ para todo $A$, e $\|A\| = 0$ se e somente se $A = 0$ 

2. **Homogeneidade absoluta**
$\|A\alpha\| = |\alpha| \|A\|$ 

3. **Desigualdade triangular**
$\|A + B\| \leq \|A\| + \|B\|$ 

<span style="color: blue;">

4. **Submultiplicatividade** 
$\|AB\| \leq \|A\| \|B\|$ 

</span>

---

## Exemplos

1. Norma de Frobenius
$$||A||_F = \sqrt{\sum_{i=1}^n \sum_{j=1}^n a_{ij}^2}$$

2. Norma de Schatten $p$
$$||A||_p = \left( \sum_{i=1}^n \sigma_i^p \right)^{1/p},$$
onde $\sigma_i$ são os valores singulares de $A$.

---

## Norma Matricial Induzida

Seja $A \in \mathbb{R}^{n \times n}$. A norma induzida por uma norma vetorial $\| \cdot \|$ é definida como
$$||A|| = \max_{x \neq 0} \frac{||Ax||}{||x||}.$$

*A norma induzida mede a amplificação máxima de um vetor $x$ por uma matriz $A$.*

---

## Teorema 2.1.26
A norma matricial induzida é uma norma matricial.

## Teorema 2.1.24

Uma norma vetorial e sua norma matricial induzida satisfazem a desigualdade 

$$||Ax|| \leq ||A||\,||x||$$

para todo $A \in \mathbb{R}^{n \times n}$ e $x \in \mathbb{R}^n$. 

Além disso, sempre existe um vetor $x$ tal que $||Ax|| = ||A||\,||x||.$

---

## Retornando ao caso de estudo

1. $Ax=b$ e $A(x+\delta x)=b + \delta b$ implica em $A\delta x = \delta b$, portanto $\delta x = A^{-1} \delta b$.

2. Uma vez que $||Az|| \leq ||A||\,||z||$ para todo $z \in \mathbb{R}^n$, temos
  2.1 $||\delta x|| \leq ||A^{-1}||\,||\delta b||.$
  2.2 $||b|| \leq ||A||\,||x|| \Longrightarrow ||x|| \geq \Large{\frac{||b||}{||A||}}.$

Portanto,

$$\frac{||\delta x||}{||x||} \leq ||A||\,||A^{-1}|| \frac{|| \delta b ||}{||b||}.$$

---

## Número de Condição

Seja $A$ uma matriz não singular. O número de condição de $A$ é definido como
$$\kappa(A) = ||A|| ||A^{-1}||.$$

1. *O número de condição mede a sensibilidade da solução de um sistema linear às variações dos dados.* 

2. *Em um sistema linear com número de condição alto, pequenas variações nos dados podem causar grandes variações na solução.*


**Retornando ao caso de estudo...**

Calcule o número de condição da matriz $A$ para a norma de Frobenius.

---

## Exemplo: Matrizes de Hilbert

Um dos exemplos mais famosos de matrizes mal condicionadas são as **matrizes de Hilbert**, definidas por $h_{ij} = 1 / (i + j - 1)$. 


Essas matrizes são simétricas, podem ser mostradas como positivas definidas e se tornam cada vez mais mal condicionadas à medida que $n$ aumenta. Por exemplo,  $\kappa_2(H_4) \approx 1.6 \times 10^4$ e $\kappa_2(H_8) \approx 1.5 \times 10^{10}$.

$$
H_4 = 
\begin{bmatrix}
1 & 1/2 & 1/3 & 1/4 \\
1/2 & 1/3 & 1/4 & 1/5 \\
1/3 & 1/4 & 1/5 & 1/6 \\
1/4 & 1/5 & 1/6 & 1/7
\end{bmatrix},
$$

---

<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Interpretação Geométrica do Condicionamento</h2>
</div>

### Definições
Ampliação máxima e mínima

$$maxmag(A) = \max_{x\neq 0}\frac{||Ax||}{||x||}\quad \text{ e } \quad minmag(A)=\frac{||Ax||}{||x||}$$

***Nota***: Ampliação máxima é outro nome para a norma induzida $||A||$.

### Propriedades

$$maxmag(A) = \frac{1}{minmag (A^{-1})}\quad \text{ e } maxmag(A^{-1}) = \frac{1}{minmag (A)}$$

---

<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Interpretação Geométrica do Condicionamento</h2>
</div>

### Prova
Sabendo que $\displaystyle {maxmag(A) = \max_{x\neq 0}\frac{||Ax||}{||x||}}$ e escrevendo $y=Ax$, obtemos

$$\begin{eqnarray}
\text{maxmag}(A) &=& \max_{A^{-1}y \neq 0} \frac{ \| y \| }{ \| A^{-1} y \| } = \min_{A^{-1}y \neq 0} \frac{ \| A^{-1} y \| }{ \| y \| } \\
&=& \min_{y \neq 0} \frac{ \| A^{-1} y \| }{ \| y \| } = \text{minmag}(A^{-1})
\end{eqnarray}
$$

---- 

<div style="position: fixed; top: 20px; width: 100%; background-color: white; z-index: 1000;">
<h2 style="text-align: left;">Interpretação Geométrica do Condicionamento</h2>
</div>


### Teorema 2.1.12

$$\kappa(A) = \frac{maxmag(A)}{minmag(A)}, \text{ para toda matriz $A$ n\~ao singular}.$$

***Nota***: 

1. Em matrizes mal condicionadas, a razão entre as amplificações máxima e mínima são muito grandes ($\kappa(A)\gg 1$). 
2. Portanto, alguns vetores serão muito ampliados, enquanto outros serão muito contraídos. 
3. Esta desproporção é que permite erros pequenos serem amplificados quando as matrizes são mal condicionadas.

---

### Condicionamento vs Determinante 
Ainda que o condicionamento envolva tanto $A$ quanto $A^{-1}$ e que $A^{-1}$ só exista se $det(A)\neq 0$, a verdade é que ***o determinante não é útil no cálculo do condicionamento***.

#### Exemplo
Considere a matriz 

$$A_\alpha =
\begin{bmatrix}
\alpha & 0 \\
0 & \alpha
\end{bmatrix}.$$

Temos $\det(A)=\alpha^2$, mas para qualquer norma induzida $\kappa(A)=1$. Portanto, $A_\alpha$ é bem condicionada mesmo quando temos $det(A)=\alpha^2$ muito pequeno.

---

## Mal Condicionamento e *Scaling*

Algumas vezes o problema do mal condicionamento é causado pela diferença entre as magnitudes das linhas (colunas) da matriz.

$$A =
\begin{bmatrix}
1 & 0 \\
0 & \epsilon
\end{bmatrix}
\begin{bmatrix}
x_1 \\
x_2
\end{bmatrix}=\begin{bmatrix}
1 \\
\epsilon
\end{bmatrix}.$$

Se fizermos uma perturbação $b+\delta b = \begin{bmatrix}
1 \\
2\epsilon
\end{bmatrix}$ encontraremos a solução perturabada $x+\delta x = \begin{bmatrix}
1 \\
2
\end{bmatrix}$, ou seja, $\frac{||\delta x||}{||x||} \gg \frac{||\delta b||}{||b||}$. 

De fato, $A$ é mal condicionada para $\epsilon\approx 0$, 
$$\kappa_1(A)=\kappa_2(A))=\kappa_\infty(A)=1/\epsilon$$

---

### Teorema 2.2.25  
Seja $A$ uma matriz não singular qualquer, e sejam $a_1, a_2, \dots, a_n$ suas colunas. Então, para qualquer $i$ e $j$,

$$\kappa_p(A) \geq \frac{\|a_i\|_p}{\|a_j\|_p}, \quad 1 \leq p \leq \infty.$$

**Prova**.  Claramente $a_i = A e_i$ ($e_i$ base canônica). Portanto,  

$$\text{maxmag}(A) = \max_{x \neq 0} \frac{\|Ax\|_p}{\|x\|_p} \geq \frac{\|Ae_i\|_p}{\|e_i\|_p} = \|a_i\|_p,$$

$$\text{minmag}(A) = \min_{x \neq 0} \frac{\|Ax\|_p}{\|x\|_p} \leq \frac{\|Ae_j\|_p}{\|e_j\|_p} = \|a_j\|_p,$$

$$\kappa_p(A) = \frac{\text{maxmag}(A)}{\text{minmag}(A)} \geq \frac{\|a_i\|_p}{\|a_j\|_p}.$$

---

## Estimando o Condicionamento

Uma vez que $\frac{\|A^{-1}w\|_1}{\|w\|_1} \leq \max_{y \neq 0} \frac{\|A^{-1}y\|_1}{\|y\|_1} = \|A^{-1}\|_1.$

Tomando $w = b$, temos $A^{-1}w = x$, então  

$$\frac{\|x\|_1}{\|b\|_1} \leq \|A^{-1}\|_1 \quad \text{e} \quad \kappa_1(A) \geq \frac{\|A\|_1 \|x\|_1}{\|b\|_1} = \frac{\|A\|_1 \|A^{-1}w\|_1}{\|w\|_1}.$$

Se tivermos uma decomposição $LU$ de $A$, podemos calcular $A^{-1}w$ resolvendo $Ac = w$. Além disso, se $w$ for escolhido em uma direção próxima da amplificação máxima por $A^{-1}$, a teremos

$$\kappa_1(A) \approx \frac{\|A\|_1 \|A^{-1}w\|_1}{\|w\|_1}$$

---

## Perturbação na Matriz $A$

### Teorema 2.3.1  
Se $A$ é não singular e  $\displaystyle \frac{\|\delta A\|}{\|A\|} < \frac{1}{\kappa(A)}$, então $A + \delta A$ é não singular.

### Teorema 2.3.3  
Seja $A$ não singular, seja $b \neq 0$, e sejam $x$ e $\hat{x} = x + \delta x$ soluções de $Ax = b$ e $(A + \delta A)\hat{x} = b$, respectivamente. Então,

$$\frac{\|\delta x\|}{\|x\|} \leq \kappa(A) \frac{\|\delta A\|}{\|A\|}$$

---

### Demonstração  
Reescrevendo a equação $(A + \delta A)\hat{x} = b$ como $Ax + A\delta x + \delta A\hat{x} = b$, utilizando a equação $Ax = b$, e reorganizando a equação resultante, obtemos $\delta x = -A^{-1}\delta A \hat{x}$. Assim,  

$$\|\delta x\| \leq \|A^{-1}\| \|\delta A\| \|\hat{x}\|.$$

Dividindo por $\|x\|$ e usando a definição $\kappa(A) = \|A\| \|A^{-1}\|$, obtemos o resultado desejado.

---

## Análise à *posteriori*, usando resíduo 

### Teorema 2.4.1  
Seja $A$ não singular, seja $b \neq 0$, e seja $\hat{x}$ uma aproximação para a solução de $Ax = b$ (em outras palavras, $\hat{x}$ é qualquer vetor). Seja $r = b - A\hat{x}$. Então,

$$\frac{\|x - \hat{x}\|}{\|x\|} \leq \kappa(A) \frac{\|r\|}{\|b\|}.$$

---

<!-- backgroundColor: orange -->

# PERGUNTAS?