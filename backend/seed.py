import json
from app.database import SessionLocal, init_db
from app.models import Document
from app.embeddings import gerar_embedding

# Documentos sobre o petshop
DOCS_PETSHOP = [
    {
        "titulo": "Horário de Funcionamento",
        "conteudo": """
        Nossa loja funciona de segunda a sexta das 9h às 19h, aos sábados das 9h às 17h.
        Aos domingos e feriados estamos fechados. O pet shop está localizado na Rua das Flores, 123.
        Para atendimento de emergência aos finais de semana, sugerimos contatar a Clínica Veterinária 24h
        que fica a duas quadras da nossa loja.
        """
    },
    {
        "titulo": "Serviços de Banho e Tosa",
        "conteudo": """
        Oferecemos serviços de banho e tosa para cães de todos os portes e gatos.
        O banho inclui shampoo especial, condicionador, secagem e escovação. A tosa pode ser higiênica
        ou completa, de acordo com a raça e preferência do tutor. Recomendamos agendar com antecedência.
        O tempo médio de serviço é de 2 horas para cães pequenos e até 4 horas para raças grandes.
        Preços variam de R$ 50 a R$ 150 dependendo do porte e tipo de serviço.
        """
    },
    {
        "titulo": "Vacinação e Consultas Veterinárias",
        "conteudo": """
        Temos veterinário disponível para consultas às terças e quintas das 14h às 18h.
        Aplicamos vacinas essenciais como V8, V10, antirrábica para cães e tríplice felina para gatos.
        É importante manter o cartão de vacinação em dia. Filhotes devem iniciar o protocolo vacinal
        com 45 dias de idade. Consultas custam R$ 120 e vacinas entre R$ 60 e R$ 100.
        Para emergências, indicamos a Clínica Veterinária 24h parceira.
        """
    },
    {
        "titulo": "Alimentação e Nutrição",
        "conteudo": """
        Trabalhamos com rações premium das marcas Royal Canin, Premier, Golden e Farmina.
        Oferecemos linha específica para filhotes, adultos, idosos e pets com necessidades especiais
        como controle de peso, problemas renais ou alergias. Também temos snacks naturais,
        ossinhos e petiscos funcionais. Nossa equipe pode ajudar a escolher a melhor alimentação
        para o seu pet. Fazemos entrega grátis para compras acima de R$ 200.
        """
    },
    {
        "titulo": "Produtos e Acessórios",
        "conteudo": """
        Vendemos coleiras, guias, camas, comedouros, bebedouros, brinquedos e arranhadores para gatos.
        Temos linha de produtos de higiene como shampoos, condicionadores, escovas e cortadores de unha.
        Também oferecemos roupinhas para pets, principalmente para raças pequenas e em épocas de frio.
        Todos os produtos possuem garantia do fabricante. Aceitamos cartões de crédito, débito e PIX.
        """
    },
    {
        "titulo": "Política de Devolução e Troca",
        "conteudo": """
        Aceitamos trocas de produtos em até 7 dias após a compra, desde que a embalagem esteja lacrada
        e com nota fiscal. Para rações, a troca só é possível se o pacote não foi aberto.
        Produtos em promoção não podem ser trocados. Em caso de defeito de fabricação,
        realizamos a troca imediata ou reembolso total. Serviços de banho e tosa não são reembolsáveis,
        mas refazemos gratuitamente caso o cliente não fique satisfeito.
        """
    },
    {
        "titulo": "Hospedagem e Hotel para Pets",
        "conteudo": """
        Oferecemos serviço de hospedagem para cães e gatos em ambiente seguro e climatizado.
        As baias são individuais e limpas diariamente. Incluímos alimentação (o tutor pode trazer
        a ração habitual), passeios para cães e monitoramento constante. O valor da diária é de
        R$ 80 para cães pequenos, R$ 100 para médios e R$ 120 para grandes. Gatos pagam R$ 70 a diária.
        Necessário apresentar carteira de vacinação atualizada.
        """
    },
    {
        "titulo": "Adestramento e Comportamento",
        "conteudo": """
        Oferecemos aulas de adestramento básico e avançado com profissional certificado.
        O treinamento pode ser individual ou em grupo. Trabalhamos comandos básicos como sentar,
        deitar, ficar e vir quando chamado. Também auxiliamos em problemas comportamentais como
        ansiedade de separação, latidos excessivos e agressividade. Pacotes de 4 aulas custam R$ 400
        para aulas individuais e R$ 250 por pet em turmas de grupo.
        """
    },
    {
        "titulo": "Planos e Programas de Fidelidade",
        "conteudo": """
        Temos um programa de fidelidade onde a cada R$ 100 em compras você acumula 10 pontos.
        Cada 100 pontos podem ser trocados por R$ 10 de desconto na próxima compra.
        Também oferecemos planos mensais de banho e tosa com desconto de 15% para pacotes
        de 4 sessões. Clientes cadastrados recebem ofertas exclusivas por email e SMS.
        Faça seu cadastro na loja ou pelo nosso site.
        """
    },
    {
        "titulo": "Cuidados com Animais Idosos",
        "conteudo": """
        Pets idosos precisam de atenção especial. Recomendamos consultas veterinárias regulares
        a cada 6 meses para check-up. A alimentação deve ser específica para a idade, com menor
        teor de gordura e proteínas de alta qualidade. Suplementos para articulações como
        condroitina e glucosamina podem ajudar na mobilidade. Mantemos rações Senior de diversas
        marcas e podemos indicar a melhor opção para seu pet. Banhos devem ser mais rápidos
        para evitar estresse.
        """
    }
]


def popular_banco():
    print("Iniciando seed do banco de dados...")
    
    init_db()
    db = SessionLocal()

    # bloco try-except-finally para garantir fechamento da sessão    
    try:
        # limpa docs antigos se existirem
        docs_existentes = db.query(Document).count()
        if docs_existentes > 0:
            print(f"Removendo {docs_existentes} documentos antigos...")
            db.query(Document).delete()
            db.commit()
        
        # insere cada documento com seu embedding
        for idx, doc_data in enumerate(DOCS_PETSHOP, 1):
            print(f"Processando documento {idx}/{len(DOCS_PETSHOP)}: {doc_data['titulo']}")
            
            # gera embedding do conteúdo completo
            # não usamos chunks aqui porque nossos docs já são pequenos (100-200 palavras).
            # Se tivéssemos docs grandes (>500 palavras), seria aqui que dividiríamos em chunks usando longchain.text_splitter
            texto = f"{doc_data['titulo']} {doc_data['conteudo']}"
            embedding = gerar_embedding(texto)
            
            # cria documento no banco
            doc = Document(
                titulo=doc_data["titulo"],
                conteudo=doc_data["conteudo"].strip(),
                embedding=json.dumps(embedding)  # salva como JSON string
            )
            
            db.add(doc)
        
        db.commit()
        print(f"\n Seed concluído! {len(DOCS_PETSHOP)} documentos inseridos com sucesso.")
        
    except Exception as e:
        print(f" Erro durante seed: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    popular_banco()

