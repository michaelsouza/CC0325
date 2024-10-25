# CC0325 - ÁLGEBRA LINEAR COMPUTACIONAL

### Ementa
Revisão de Álgebra Linear. Algoritmos para multiplicação matricial e sistemas triangulares. Métodos diretos para sistemas lineares. Decomposição LU, método de Gauss. Inversão de matrizes. Matrizes definidas positivas. Decomposição de Cholesky. Decomposição QR. Mínimos quadrados. Esparsidade. Condicionamento. Análise de erros. Métodos iterativos para sistemas lineares. Convergência. Determinação numérica de autovalores e autovetores. Implementações computacionais.

### Bibliografia Básica
1. WATKINS, David S. Fundamentals of matrix computations. 3rd ed. New Jersey: John Wiley & Sons, c2010. xiii, 644 p. ISBN 9780470528334 (enc.).
2. GOLUB, Gene H. Matrix computations. 3rd ed. Baltimore: Johns Hopkins University Press, 1996 xxvii, 694 p. ISBN 0-8018-5414-8 (broch.).
3. J. Demmel. Applied Numerical Linear Algebra. SIAM, 1997.

### Bibliografia Complementar
1. L. TREFETHEN, Lloyd N.; BAU, David. Numerical linear algebra. Philadelphia, PA: Society for Industrial and Applied Mathematics, c1997.
2. P. Gill, W. Murray e M. Wright. Numerical Linear Algebra and Optimization, Addison-Wesley Company, 1991.
3. ORTEGA, James M. Matrix theory: a second course. New York: Plenum, 1987.
4. SEARLE, Shayle R. Matrix algebra useful for statistics. New York: John Wiley, 1982.
5. NOBLE, Ben.; DANIEL, James W. Álgebra linear aplicada. 2. ed. Rio de Janeiro: Prentice Hall, c1986.

## Motivação
### Por que estudar Álgebra Linear Computacional?

A disciplina de Álgebra Linear Computacional é essencial para estudantes de Ciência de Dados e Matemática Aplicada, pois aborda ferramentas úteis para a resolução de problemas complexos em diversas áreas. Seja na análise de grandes volumes de dados, no desenvolvimento de algoritmos de machine learning ou na modelagem de sistemas físicos, sistemas lineares aparecem frequentemente como a base para a construção de soluções eficazes.

Esses modelos são especialmente relevantes porque, entre os muitos tipos de modelos matemáticos, os sistemas lineares são os únicos que realmente podem ser resolvidos de forma eficiente por computadores. 

Além do aspecto teórico, a disciplina foca na implementação de algoritmos eficientes para resolver problemas práticos, como decomposições de matrizes e métodos iterativos, essenciais para lidar com grandes volumes de dados e otimizar processos. Além disso, aprender a codificar essas soluções e medir sua performance em ambientes de computação de alto desempenho é uma habilidade importante para quem deseja atuar com matemática computacional, pois permite desenvolver soluções robustas e eficientes para problemas do mundo real.

## Materiais
A linguagem de programação recomendada para as implementações é C++, pois é uma linguagem de alto desempenho e é amplamente utilizada na computação científica.

## Organização do Curso

### Ambiente de Desenvolvimento
- **Conteúdo:**
  - Introdução ao C++ e ao ambiente de desenvolvimento (Google Colab).
  - Compilador GCC.
  - Ferramentas de compilação e depuração.
- **Atividades:**
  - Instalação e configuração do ambiente de desenvolvimento.
  - Escrita de programas simples em C++.

### Algoritmos para Multiplicação Matricial
- **Conteúdo:**
  - Algoritmos clássicos de multiplicação de matrizes.
  - Complexidade computacional.
  - Algoritmos otimizados para matrizes esparsas.
- **Atividades:**
  - Implementação básica de multiplicação matricial.
  - Discussão sobre otimizações.

### Sistemas Triangulares
- **Conteúdo:**
  - Resolução de sistemas triangulares superiores e inferiores.
  - Substituição direta e retroativa.
- **Atividades:**
  - Exercícios práticos de resolução de sistemas triangulares.
  - Implementação de métodos de substituição.

### Métodos para Sistemas Lineares
- **Conteúdo:**
  - Métodos diretos vs iterativos.  
  - Método de Gauss: eliminação gaussiana.
- **Atividades:**
  - Implementação do método de Gauss.
  - Análise de complexidade e estabilidade.

### Decomposição LU
- **Conteúdo:**
  - Fatoração LU de matrizes.
  - Pivoteamento parcial.
  - Aplicações da decomposição LU na resolução de sistemas.
- **Atividades:**
  - Implementação da decomposição LU com pivoteamento.
  - Exercícios aplicados.

### Inversão de Matrizes
- **Conteúdo:**
  - Métodos para calcular a inversa de uma matriz.
  - Relação entre decomposição LU e inversão.
- **Atividades:**
  - Implementação de algoritmos de inversão.
  - Análise de erros na inversão.

### Matrizes Definidas Positivas e Decomposição de Cholesky
- **Conteúdo:**
  - Propriedades de matrizes definidas positivas.
  - Decomposição de Cholesky.
  - Aplicações em sistemas lineares e mínimos quadrados.
- **Atividades:**
  - Implementação da decomposição de Cholesky.
  - Exercícios sobre aplicações práticas.

### Decomposição QR
- **Conteúdo:**
  - Fundamentos da decomposição QR.
  - Métodos de Gram-Schmidt e Householder.
  - Aplicações em mínimos quadrados e autovalores.
- **Atividades:**
  - Implementação de decomposição QR.
  - Comparação de métodos de obtenção da decomposição.

### Mínimos Quadrados
- **Conteúdo:**
  - Problema dos mínimos quadrados.
  - Solução via decomposição QR e LU.
  - Aplicações em ajuste de curvas e regressão.
- **Atividades:**
  - Implementação de métodos de mínimos quadrados.
  - Estudos de caso aplicados.

### Esparsidade e Armazenamento Eficiente
- **Conteúdo:**
  - Matrizes esparsas: definições e propriedades.
  - Técnicas de armazenamento eficiente.
  - Algoritmos otimizados para matrizes esparsas.
- **Atividades:**
  - Implementação de estruturas de dados para matrizes esparsas.
  - Exercícios sobre operações com matrizes esparsas.

### Condicionamento e Análise de Erros
- **Conteúdo:**
  - Condicionamento de matrizes e sistemas lineares.
  - Propagação de erros numéricos.
  - Estabilidade de algoritmos.
- **Atividades:**
  - Cálculo do número de condicionamento.
  - Análise de erros em implementações anteriores.

### Métodos Iterativos para Sistemas Lineares I
- **Conteúdo:**
  - Introdução aos métodos iterativos.
  - Método de Jacobi.
  - Método de Gauss-Seidel.
- **Atividades:**
  - Implementação dos métodos de Jacobi e Gauss-Seidel.
  - Análise de convergência.

### Métodos Iterativos para Sistemas Lineares II
- **Conteúdo:**
  - Métodos de Gradiente Conjugado.
  - Pré-condicionamento.
  - Comparação entre métodos diretos e iterativos.
- **Atividades:**
  - Implementação do método de gradiente conjugado.
  - Estudos comparativos de desempenho.

### Determinação Numérica de Autovalores e Autovetores
- **Conteúdo:**
  - Métodos de potência e potência inversa.
  - Decomposição espectral.
  - Aplicações na análise de sistemas.
- **Atividades:**
  - Implementação de métodos para autovalores.
  - Exercícios sobre aplicações práticas.

---

### **Avaliação do Curso:**
- **Avaliação 1:** 40%
- **Avaliação 2:** 40%
- **Trabalho de Codificação:** 20%
