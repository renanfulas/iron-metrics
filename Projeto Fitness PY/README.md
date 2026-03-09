🦾 Iron Metrics
A ciência do shape, sem burocracia.
O Iron Metrics nasceu da necessidade de visualizar a evolução física de forma bruta e precisa. Chega de planilhas de Excel bagunçadas ou apps cheios de anúncios. Aqui é código, peso e progresso. SIMPLES!

🎯 Por que este projeto existe?
Monitorar a composição corporal é um jogo de paciência. O problema é que a maioria das ferramentas foca apenas no peso total. O Iron Metrics separa o "joio do trigo": ele calcula sua massa magra e gordura real usando o protocolo de dobras cutâneas, entregando gráficos que mostram se você está realmente ganhando músculo ou apenas retendo líquido.

🛠 Eu escolhi um stack focado em performance e simplicidade:

Python + Flask: O coração da lógica e das rotas.

SQLAlchemy: Para garantir que os dados dos alunos estejam seguros e bem estruturados.

Plotly: Porque gráficos estáticos são chatos. Aqui a visualização é interativa.

Tailwind CSS: Para um visual Dark Mode moderno e agressivo, digno de uma central de comando.

✨ Funcionalidades Principais
Gestão de Alunos: Adicione e gerencie múltiplos perfis rapidamente.

Cálculo de Dobras (7 Dobras): Insira os milímetros e deixe a matemática comigo.

Histórico de Perimetria: Braço, tórax, coxa... tudo organizado por data.

Dashboard de Evolução: Gráficos de linha para o BF% e gráficos de pizza para a composição atual.

Interface Reativa: Clique em uma avaliação antiga na tabela e os gráficos se atualizam instantaneamente.

🚀 Como rodar na sua máquina
Se você quiser testar ou usar no seu consultório/academia, o processo é direto:

Clone o repositório:

Bash
git clone https://github.com/seu-usuario/iron-metrics.git
Instale as dependências:

Bash
pip install flask flask_sqlalchemy plotly
Inicie o motor:

Bash
python app.py
Acesse [http://127.0.0.1:5000](http://127.0.0.1:5000) e use a senha padrão admin.


🧠 Desafios de Desenvolvimento (O que eu aprendi)
Um dos maiores desafios foi lidar com o Double Submit do navegador (aquela dor de cabeça de salvar dois registros iguais). Resolvi isso implementando uma trava de segurança baseada em tempo no backend e um estado de disabled no botão de salvar via JavaScript. Ficou sólido.