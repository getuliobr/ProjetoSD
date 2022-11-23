# utPlace
Projeto da disciplina de Sistemas Distribuidos.

# Alunos

<center>
<table><tr>
<td align="center"><a href="https://github.com/getuliobr">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/51160837?v=4" width="100px;" alt=""/>
<br />
 <b>Getúlio Coimbra Regis</b></a>
 <a href="https://github.com/getuliobr" title="GitHub Getulio"></a>

<td align="center"><a href="https://github.com/nuisigor">
 <img style="border-radius: 50%;" src="https://avatars.githubusercontent.com/u/50688059?v=4" width="100px;" alt=""/>
<br />
 <b>Igor Lara de Oliveira</b>
 </a> <a href="https://github.com/nuisigor" title="GitHub Igor"></a>

</tr></table>
</center>

# Tecnologias utilizadas
<div style="display: inline_block"><br>
          
  <a href="https://www.python.org/"><img align="center" alt="python" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/python/python-original.svg"><a>
  <a href="https://developer.mozilla.org/pt-BR/docs/Web/HTML"><img align="center" alt="html" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/html5/html5-original.svg" /><a>
  <a href="https://developer.mozilla.org/pt-BR/docs/Web/JavaScript"><img align="center" alt="js" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/javascript/javascript-original.svg"><a>
  <a href="https://fastapi.tiangolo.com/"><img align="center" alt="fastapi" height="50" width="60"  src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/fastapi/fastapi-original-wordmark.svg" />
  <a href="https://tailwindcss.com/"><img align="center" alt="tailwind" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/tailwindcss/tailwindcss-plain.svg" /><a>
  <a href="https://www.docker.com/"><img align="center" alt="docker" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/docker/docker-original.svg" /><a>
  <a href="https://www.mongodb.com/"><img align="center" alt="mongodb" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/mongodb/mongodb-original-wordmark.svg"/><a>
  <a href="https://redis.io/"><img align="center" alt="redis" height="50" width="60" src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/redis/redis-original-wordmark.svg"/><a>

</div>

# Como rodar
Com o docker aberto digite o comando
	
	docker compose up

# Interfaces de serviço

Todas as mensagens cliente servidor são em formato JSON.

## Websocket
1. Receber uma modificação de pixel

	Toda vez que um usuário modificar um pixel, todos os usuários são notificados por uma mensagem no websocket, com a seguinte estrutura

	```py
	{
		"x": int,
		"y": int,
		"color": string
	}
	```

	Sendo *x* e *y* as coordenadas de cada pixel no quadro, e a color a cor desejada em hexadecimal.

## REST
1. Colocar/Modificar um pixel:
	### *Request*
	>É enviado uma requisição POST na rota */tile* com a seguinte estrutura:
	```py
	{
		"x": int,
		"y": int,
		"color": string
	}
	```
	Sendo *x* e *y* as coordenadas de cada pixel no quadro, e a *color* a cor desejada em hexadecimal.
	### *Response*
  	O formato de resposta generico é o seguinte
	
	```py
	{
		"success": boolean,
		"cooldown": float,
		"error": string
	}
	```
  	Caso o usuário consiga modificar um pixel o campo *__success__* vai ser *True*, caso constrario *False*, neste caso o campo error vai explicar o que esta de errado.
	
	Se o erro for devido ao usuário não ter esperado o tempo necessário para colocar o pixel o cooldown vai retornar o tempo restante, em caso de sucesso o campo cooldown também vai vir preenchido com o tempo de espera.

2. Pegar o estado atual do quadro
     ### *Request*
	>É enviado uma requisição GET na rota */place*.

    ### *Response*
    >É retornado uma imagem com o estado atual do quadro.

3. Pegar tempo de espera do usuário
    ### *Request*
	>É enviado uma requisição GET na rota */timeStampUser*.
	### *Responde*
	>É retornado o tempo de espera do usuário em segundos.

# Diagrama

<img src="util\utPlace.jpg"/>


# Dependências

## Python
	- FastAPI
	- websockets
	- uvicorn
	- numpy
	- pymongo
