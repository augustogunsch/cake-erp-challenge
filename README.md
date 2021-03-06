# Rodando
As dependências (Python) do projeto estão listadas em `requirements.txt`.

Vá para o diretório `api`:
```
cd api
```

Crie o banco de dados:
```
flask db init
flask db migrate
flask db upgrade
```

Inicie o servidor de desenvolvimento:
```
flask run
```

Por padrão o servidor tem sua interface em `http://localhost:5000`.

## Rodando Testes
No diretório **raíz**:
```
python3 -m api.tests
```

# Desenvolvimento
- Comecei a desenvolver o projeto em Rust, mas sofri muito com a linguagem, perdendo uma tarde inteira lutando com o *borrow checker* e o framework Rocket. Concluí que preciso aprender melhor as mecânicas de *ownership* do Rust, e decidi fazer em Python (framework Flask) ao invés.
- Pensei em fazer em C# ou C++, mas seria obrigado a usar um sistema de build como cmake, que demoraria bastante tempo pra organizar. Isso porque uso Linux, e não posso garantir a portabilidade das `Makefile`s pra outras plataformas.
- Comecei fazendo com SQL bruto, mas aprendi como funciona a biblioteca de ORM SQLAlchemy, e passei a usá-la.

# Endpoints
Os endpoints que já estão funcionando marcados:
- [X] GET /trainer
- [X] POST /trainer
- [X] POST /trainer/authenticate
- [X] GET /trainer/{trainerId}
- [X] GET /trainer/{trainerId}/pokemon
- [X] POST /trainer/{trainerId}/pokemon
- [X] GET /trainer/{trainerId}/pokemon/{pokemonId}
- [X] DELETE /trainer/{trainerId}/pokemon/{pokemonId}
