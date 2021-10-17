# Rodando
As dependências (Python) do projeto estão listadas em `requirements.txt`.
Crie o banco de dados:
```python3 create_db.py```
Depois, no diretório `api`:
```flask run```
Por padrão o servidor tem sua interface em `http://localhost:5000`

# Desenvolvimento
- Comecei a desenvolver o projeto em Rust, mas sofri muito com a linguagem, perdendo uma tarde inteira lutando com o *borrow checker* e o framework Rocket. Concluí que preciso aprender melhor as mecânicas de *ownership* do Rust, e decidi fazer em Python (framework Flask) ao invés.
- Pensei em fazer em C# ou C++, mas seria obrigado a usar um sistema de build como cmake, que demoraria bastante tempo pra organizar. Isso porque uso Linux, e não posso garantir a portabilidade das `Makefile`s pra outras plataformas.
