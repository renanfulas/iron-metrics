***The science of physique progress — simple, precise, and visual.***

**Iron Metrics é uma aplicação web desenvolvida para registrar avaliações físicas e visualizar a evolução corporal de forma clara e objetiva.**

Muitos profissionais de academia ainda dependem de planilhas desorganizadas ou aplicativos limitados.
Este projeto resolve esse problema criando um sistema simples e visual para acompanhar composição corporal ao longo do tempo.

🎯 Problema

**A maioria das ferramentas de acompanhamento físico foca apenas no peso corporal total, o que pode gerar interpretações equivocadas.**

Por exemplo:

-aumento de peso pode ser massa muscular

-ou retenção de líquido

-ou ganho de gordura

-Sem dados adequados, é difícil interpretar o progresso real.

💡 Solução

**O Iron Metrics utiliza o protocolo de 7 dobras cutâneas para estimar a composição corporal e apresentar os resultados de forma visual e muito prática.**

O sistema permite:

  -registrar avaliações físicas

  -acompanhar histórico corporal

  -visualizar gráficos de evolução

  -analisar mudanças reais na composição corporal

⚙️ Tecnologias utilizadas

O projeto foi desenvolvido com uma stack simples e eficiente:

  - **Backend**

  * *Python* *

  * *Flask* *

  * *SQLAlchemy* *

Visualização de dados:

  * *Plotly* (gráficos interativos)

  * **Frontend**

  * *Tailwind CSS* (interface moderna em Dark Mode)

✨ Funcionalidades
  -Gestão de alunos

  -cadastro de múltiplos perfis

  -organização das avaliações por aluno

Avaliação física:

  *cálculo de 7 dobras cutâneas (POLLOCK 7 DOBRAS)

  *registro de perimetria corporal (braço, tórax, coxa, etc.)

  -Histórico de avaliações

  *armazenamento das avaliações por data

  *fácil navegação entre registros anteriores

  -Dashboard de evolução

  *gráfico de linha mostrando evolução do BF%

  *gráfico de pizza mostrando composição atual

Interface interativa

seleção de avaliações antigas atualiza os gráficos automaticamente

📊 Exemplo de uso

-Fluxo típico dentro do sistema:

    cadastrar um aluno

-registrar uma avaliação física

    inserir medidas e dobras cutâneas

    visualizar automaticamente os gráficos de evolução

**Isso permite ao professor acompanhar se o aluno está realmente evoluindo.**

🚀 Como rodar o projeto localmente

Clone o repositório:

git clone https://github.com/seu-usuario/iron-metrics.git

Entre na pasta do projeto:

cd iron-metrics

Instale as dependências:

      -pip install flask flask_sqlalchemy plotly

Execute a aplicação:

python app.py

  Acesse no navegador:

          http://127.0.0.1:5000

Usuário padrão:

admin


🧠 Desafios de desenvolvimento

Durante o desenvolvimento, um dos principais desafios foi evitar o problema de Double Submit (quando o navegador envia duas requisições e gera registros duplicados).

  Para resolver isso, implementei:

   validação de tempo no backend

   estado disabled no botão de envio via JavaScript
  Isso garantiu que os registros fossem salvos apenas uma vez, tornando o fluxo mais confiável.

📚 Aprendizados

Este projeto foi importante para praticar:

-estruturação de aplicações web com Flask

-modelagem de dados com SQLAlchemy

-visualização de dados com Plotly

-integração entre backend e frontend

-prevenção de problemas comuns de formulário web

🔮 Possíveis melhorias futuras

-autenticação de múltiplos usuários

-exportação de relatórios em PDF

-comparação entre avaliações

-deploy online da aplicação

✅ Resultado:
Um sistema simples e funcional que demonstra como dados de avaliação física podem ser organizados e analisados de forma clara.
